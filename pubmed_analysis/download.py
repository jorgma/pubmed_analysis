import os
import numpy as np
import requests
import xmltodict
import pubmed_parser as pp
import time
from lxml import html

MAX_NUMBER_OF_ARTICLE = 100000


class EntrezSearch:
    """ main function: return pmid_list from entrez dataset

    input: term
    output: entrez database search result, including information below:
        pmid_list
    store path: 'entrez_search_result_' + store_file_name

    """

    def __init__(self, term, store_file_name='', mindate='', maxdate='', retmax=20, update=False, save=True):
        self.base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?\
        db=pubmed&mail=mail.yujun.liao@gmail.com&tool=tool_yujun\
        &apikey=721d1d88d973f59b3449e2e041f167de6308'
        # example
        # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=32272198
        self.save = save
        self.update = update
        self.store_file_name = store_file_name
        self.term = term
        self.mindate = str(mindate)
        self.maxdate = str(maxdate)
        self.retmax = str(retmax)
        self.pmid_list = self.get_result_from_entrez()['IdList']['Id']

    def get_result_from_entrez(self):
        print('------------------------------------------------------------')
        print('Get search result from entrez:')
        begin_time = time.time()
        entrez_file_name = self.store_file_name + 'entrez_search_result' + '.npy'
        if self.update == False and os.path.exists(entrez_file_name):
            # TODO(lyj): flat[0] 的用法是什么? 储存dictionary时load需要用，其他不用
            return np.load(entrez_file_name, allow_pickle=True).flat[0]

        # term= 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'
        url = self.base_url + '&term=' + self.term + '&retmax=' + self.retmax + '&datetype=pdat'
        if self.mindate is not None:
            url = url + '&mindate=' + self.mindate
        if self.maxdate is not None:
            url = url + '&maxdate=' + self.maxdate
        print('get', url)
        response = requests.get(url)
        print('Get result from entrez done, used time:', time.time() - begin_time)
        begin_time = time.time()
        search_result = xmltodict.parse(response.content)['eSearchResult']
        print('Parse result done, used time:', time.time() - begin_time)
        print('------------------------------------------------------------')
        if search_result['IdList'] is None:
            search_result['IdList'] = dict()
            search_result['IdList']['Id'] = list()
        if self.save == True:
            np.save(entrez_file_name, search_result)
        return search_result

def read_pmid_list_from_file(file):
    origin_pmid_list = list()
    lines = open(file)
    for line in lines:
        words = line.split(' ')
        if words[0] == 'AN':
            origin_pmid_list.append(words[3][:-1])
    print('origin pmid:', len(origin_pmid_list))
    return origin_pmid_list
    # np.save(store_file_name+'origin_pmid', origin_pmid_list, allow_pickle=True)

def get_citation_pmid_dict(origin_pmid_list, store_file_name='', update=False):
    """

    :param origin_pmid_list:
    store_path: 'citation_info_'+ store_file_name
    :return: a dictionary, whose key is pmid od original article, value is pmid list of cited article
    """
    print('------------------------------------------------------------')
    print('Get citation info:')
    begin_time = time.time()
    citation_info_file_name = store_file_name + 'citation_pmid' + '.npy'
    citation_pmid_dict = dict()
    if os.path.exists(citation_info_file_name):
        # TODO(lyj): flat[0] 的用法是什么? 储存dictionary时load需要用，其他不用
        citation_pmid_dict = np.load(citation_info_file_name, allow_pickle=True).flat[0]
        if update == False:
            return citation_pmid_dict
    delete_list = citation_pmid_dict.keys() - origin_pmid_list
    add_list = origin_pmid_list - citation_pmid_dict.keys()
    print("need to delete %d pmid" % len(delete_list))
    print("need to update %d pmid" % len(add_list))
    for pmid in delete_list:
        del citation_pmid_dict[pmid]
    i = 0
    for pmid in add_list:
        if i % 20 == 0:
            # 20 articles are saved
            np.save(citation_info_file_name, citation_pmid_dict)
            print(i, ' new pmid are added.', )
        print(i, end=' ')
        pmid_cited_info = pp.parse_outgoing_citation_web(pmid, id_type='PMID')
        if pmid_cited_info is None:
            citation_pmid_dict[pmid] = list()
            print(pmid, 'does not cite any article.')
            continue
        i += 1
        citation_pmid_dict[pmid] = pmid_cited_info['pmid_cited']
    np.save(citation_info_file_name, citation_pmid_dict)
    print(i, ' new pmid are added.', )
    print('Get article citation info done, used time:', time.time() - begin_time)
    print('------------------------------------------------------------')
    return citation_pmid_dict

# cited 被引用数量
# url example
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs&id=21876726&tool=my_tool&email=my_email@example.com
def get_cited_pmid_dict(origin_pmid_list, store_file_name='', update=False):
    print('------------------------------------------------------------')
    print('Get cited info:')
    begin_time = time.time()
    cited_info_file_name = store_file_name + 'cited_pmid' + '.npy'
    cited_pmid_dict = dict()
    if os.path.exists(cited_info_file_name):
        # TODO(lyj): flat[0] 的用法是什么? 储存dictionary时load需要用，其他不用
        cited_pmid_dict = np.load(cited_info_file_name, allow_pickle=True).flat[0]
        if update == False:
            return cited_pmid_dict
    delete_list = cited_pmid_dict.keys() - origin_pmid_list
    add_list = origin_pmid_list - cited_pmid_dict.keys()
    print("need to delete %d pmid" % len(delete_list))
    print("need to update %d pmid" % len(add_list))
    for pmid in delete_list:
        del cited_pmid_dict[pmid]
    i = 0
    for pmid in add_list:
        if i % 20 == 0:
            # 20 articles are saved
            np.save(cited_info_file_name, cited_pmid_dict)
            print(i, ' new pmid are added.', )
        print(i, end=' ')
        time.sleep(1)
        page = requests.get(
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&linkname=pubmed_pmc_refs\
            &id='+pmid+'&tool=tool_yujun&email=mail.yujun.liao@gmail.com'+\
                       '&apikey=721d1d88d973f59b3449e2e041f167de6308')
        tree = html.fromstring(page.content)
        ids = tree.xpath("//id")
        ids = [i.text for i in ids]
        if pmid in ids:
            ids.remove(pmid)

        # pmid_cited_info = pp.parse_citation_web(pmid, id_type='PMID')
        if len(ids)==0:
            cited_pmid_dict[pmid] = list()
            print('no article cite', pmid)
            continue
        i += 1
        cited_pmid_dict[pmid] = ids
    np.save(cited_info_file_name, cited_pmid_dict)
    print(i, ' new pmid are added.', )
    print('Get article cited info done, used time:', time.time() - begin_time)
    print('------------------------------------------------------------')
    return cited_pmid_dict


class ArticleInfo:
    def __init__(self, store_file_name, pmid_list, update=False):
        self.update = update
        self.store_file_name = store_file_name
        self.pmid_list = pmid_list
        self.article_info_dict = self.get_article_info_dict_from_pubmed()

    def get_article_info_dict_from_pubmed(self):
        """
        :param store_file_name:
        :param pmid_list:
        :return: a dictionary whose key is pmid, value is information of referred article,
            value is also a dictionary, including keys below:
            title : title
            abstract : abstract
            journal : journal
            affiliation : affiliation of first author
            authors : string of authors, separated by ;
            year : Publication year
            keywords : keywords or MESH terms of the article

        store path: 'articles_info_' + store_file_name
        """
        print('------------------------------------------------------------')
        print('Get article info:')

        def clean(s):
            s.replace("*", " ")
            s.replace("¶", " ")
            s.replace("†", " ")
            s.replace("§", " ")
            s.replace("-", " ")
            s = s.rstrip().lstrip()
            if s == '':
                return ''

            if s[0] == ',' or s[0] == '.':
                s = s[1:]
            if s == '':
                return ''
            if s[-1] == ')':
                s = s[:-1]
            return s

        begin_time = time.time()
        store_file_name = self.store_file_name + 'articles' + '.npy'
        article_info_dict = dict()
        if os.path.exists(store_file_name):
            # TODO(lyj): 为什么这里不用flat[0]
            article_info_dict = np.load(store_file_name, allow_pickle=True).flat[0]
            if self.update == False:
                return article_info_dict

        delete_list = article_info_dict.keys() - self.pmid_list
        add_list = self.pmid_list - article_info_dict.keys()
        print("need to delete %d articles" % len(delete_list))
        print("need to add %d articles" % len(add_list))
        for pmid in delete_list:
            del article_info_dict[pmid]
        i = 0
        for pmid in add_list:
            if i % 20 == 0:
                np.save(store_file_name, article_info_dict)
                print('\n%d new articles are saved' % i)
            try:
                article_info = pp.parse_xml_web(pmid, save_xml=False)
            except KeyboardInterrupt:
                # do the saving here
                exit(-1)  # exit the program with the return code -1
            except:
                print('\nerror in ', pmid)
            else:

                temp_list = []
                for item in article_info['authors'].split(';'):
                    item = clean(item)
                    if item == '':
                        continue
                    temp_list.append(item)
                article_info['authors'] = temp_list

                temp_list = []
                for item in article_info['affiliation'].split(';'):
                    item = clean(item)
                    if item == '':
                        continue
                    temp_list.append(item)
                article_info['affiliation'] = temp_list

                temp_list = []
                for item in article_info['keywords'].split(';'):
                    item = item.split(':')
                    item = item[1] if len(item) > 1 else item[0]
                    item = clean(item)
                    if item == '':
                        continue
                    temp_list.append(str.lower(item))
                    article_info['keywords'] = temp_list

                article_info_dict[pmid] = article_info
                i += 1
                print(i + 1, end=' ')

        np.save(store_file_name, article_info_dict)
        print('\n%d new articles are saved' % i)
        print('Get article info done, used time:', time.time() - begin_time)
        print('------------------------------------------------------------')
        return article_info_dict


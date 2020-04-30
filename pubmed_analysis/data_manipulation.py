import os
import time
from datetime import datetime
import numpy as np
import feather
import pandas as pd
from pubmed_analysis.download import EntrezSearch, MAX_NUMBER_OF_ARTICLE


class MyArticlesStatistics:
    def __init__(self, article_info_dict, store_file_name=''):
        print('------------------------------------------------------------')
        # self.term = term
        self.store_file_name = store_file_name
        self.article_info_dict = article_info_dict
        self.articles_by_years = self._category_articles_by_years()
        self.articles_by_journals = self._category_articles_by_journals()
        self.articles_by_Meshs = self._category_articles_by_Meshs()
        self.articles_by_authors = self._category_articles_by_authors()
        self.articles_by_affiliations = self._category_articles_by_affiliations()
        # self.normalizer_article_number_of_year = self.count_article_number_of_each_year(article_info_dict)

    def _category_articles_by_years(self):
        articles_of_year = dict()
        store_file_name = self.store_file_name + 'articles_of_year'
        if os.path.exists(store_file_name + '.npy'):
            articles_of_year = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
            return articles_of_year

        for pmid in self.article_info_dict.keys():
            year = self.article_info_dict[pmid]['year']
            if year not in articles_of_year.keys():
                articles_of_year[year] = list()
            articles_of_year[year].append(pmid)
        np.save(store_file_name, articles_of_year)
        return articles_of_year

    def _category_articles_by_journals(self):
        articles_of_journals = dict()
        store_file_name = self.store_file_name + 'articles_of_journals'
        if os.path.exists(store_file_name + '.npy'):
            articles_of_journals = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
            return articles_of_journals

        for pmid in self.article_info_dict.keys():
            journal = self.article_info_dict[pmid]['journal']
            if journal not in articles_of_journals.keys():
                articles_of_journals[journal] = list()
            articles_of_journals[journal].append(pmid)
        np.save(store_file_name, articles_of_journals)
        return articles_of_journals



        # total_article_number_of_each_indicator = dict()
        # total_article_number_of_each_indicator['year'] = dict()
        # if os.path.exists(self.store_file_name+'.npy'):
        #     total_article_number_of_each_indicator = np.load(self.store_file_name+'.npy',allow_pickle=True).flat[0]
        # # print(total_article_number_of_each_indicator['year'].keys())
        # for year in sorted(temp_dict.keys()):
        #     if year not in total_article_number_of_each_indicator['year'].keys():
        #         total_article_number_of_each_indicator['year'][year] = PubmedArticlesStatistics.get_total_article_number_of_year(year)
        #         np.save(self.store_file_name, total_article_number_of_each_indicator)
        #         print('save total article number of year: '+year)
        #         print('------------------------------------------------------------')
        #
        #
        # year_list =list()
        # normalized_article_number_of_each_year = list()
        # for year in sorted(temp_dict.keys()):
        #     total_article_number = total_article_number_of_each_indicator['year'][year]
        #     if total_article_number == 0:
        #         print('year %s did not publish article on this topic.'%year)
        #         continue
        #     year_list.append(year)
        #     normalized_article_number_of_each_year.append(
        #         temp_dict[year]
        #         # float(temp_dict[year])/float(total_article_number)
        #     )
        # print('------------------------------------------------------------')
        # print('number of year:', len(year_list), len(total_article_number_of_each_indicator['year'].keys()))
        # print('------------------------------------------------------------')
        # return year_list, normalized_article_number_of_each_year

    def _category_articles_by_Meshs(self):
        articles_of_Meshs = dict()
        store_file_name = self.store_file_name + 'articles_of_Meshs'
        if os.path.exists(store_file_name + '.npy'):
            articles_of_Meshs = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
            return articles_of_Meshs

        for pmid in self.article_info_dict.keys():
            for keyword in self.article_info_dict[pmid]['keywords']:
                keyword = keyword.split(':')[-1]
                if keyword not in articles_of_Meshs.keys():
                    articles_of_Meshs[keyword] = list()
                articles_of_Meshs[keyword].append(pmid)
        np.save(store_file_name, articles_of_Meshs)
        return articles_of_Meshs


        # total_article_number_of_each_indicator = dict()
        # total_article_number_of_each_indicator['year'] = dict()
        # if os.path.exists(self.store_file_name+'.npy'):
        #     total_article_number_of_each_indicator = np.load(self.store_file_name+'.npy',allow_pickle=True).flat[0]
        # # print(total_article_number_of_each_indicator['year'].keys())
        # for year in sorted(temp_dict.keys()):
        #     if year not in total_article_number_of_each_indicator['year'].keys():
        #         total_article_number_of_each_indicator['year'][year] = PubmedArticlesStatistics.get_total_article_number_of_year(year)
        #         np.save(self.store_file_name, total_article_number_of_each_indicator)
        #         print('save total article number of year: '+year)
        #         print('------------------------------------------------------------')
        #
        #
        # year_list =list()
        # normalized_article_number_of_each_year = list()
        # for year in sorted(temp_dict.keys()):
        #     total_article_number = total_article_number_of_each_indicator['year'][year]
        #     if total_article_number == 0:
        #         print('year %s did not publish article on this topic.'%year)
        #         continue
        #     year_list.append(year)
        #     normalized_article_number_of_each_year.append(
        #         temp_dict[year]
        #         # float(temp_dict[year])/float(total_article_number)
        #     )
        # print('------------------------------------------------------------')
        # print('number of year:', len(year_list), len(total_article_number_of_each_indicator['year'].keys()))
        # print('------------------------------------------------------------')
        # return year_list, normalized_article_number_of_each_year

    def _category_articles_by_authors(self):
        articles_of_authors = dict()
        store_file_name = self.store_file_name + 'articles_of_authors'
        if os.path.exists(store_file_name + '.npy'):
            articles_of_authors = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
            return articles_of_authors

        for pmid in self.article_info_dict.keys():
            for author in self.article_info_dict[pmid]['authors']:
                if author not in articles_of_authors.keys():
                    articles_of_authors[author] = list()
                articles_of_authors[author].append(pmid)
        np.save(store_file_name, articles_of_authors)
        return articles_of_authors

    def _category_articles_by_affiliations(self):
            articles_of_affiliations = dict()
            store_file_name = self.store_file_name + 'articles_of_affiliations'
            if os.path.exists(store_file_name + '.npy'):
                articles_of_affiliations = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
                return articles_of_affiliations

            for pmid in self.article_info_dict.keys():
                for affiliation in self.article_info_dict[pmid]['affiliation']:
                    if affiliation not in articles_of_affiliations.keys():
                        articles_of_affiliations[affiliation] = list()
                    articles_of_affiliations[affiliation].append(pmid)
            np.save(store_file_name, articles_of_affiliations)
            return articles_of_affiliations


        # total_article_number_of_each_indicator = dict()
        # total_article_number_of_each_indicator['year'] = dict()
        # if os.path.exists(self.store_file_name+'.npy'):
        #     total_article_number_of_each_indicator = np.load(self.store_file_name+'.npy',allow_pickle=True).flat[0]
        # # print(total_article_number_of_each_indicator['year'].keys())
        # for year in sorted(temp_dict.keys()):
        #     if year not in total_article_number_of_each_indicator['year'].keys():
        #         total_article_number_of_each_indicator['year'][year] = PubmedArticlesStatistics.get_total_article_number_of_year(year)
        #         np.save(self.store_file_name, total_article_number_of_each_indicator)
        #         print('save total article number of year: '+year)
        #         print('------------------------------------------------------------')
        #
        #
        # year_list =list()
        # normalized_article_number_of_each_year = list()
        # for year in sorted(temp_dict.keys()):
        #     total_article_number = total_article_number_of_each_indicator['year'][year]
        #     if total_article_number == 0:
        #         print('year %s did not publish article on this topic.'%year)
        #         continue
        #     year_list.append(year)
        #     normalized_article_number_of_each_year.append(
        #         temp_dict[year]
        #         # float(temp_dict[year])/float(total_article_number)
        #     )
        # print('------------------------------------------------------------')
        # print('number of year:', len(year_list), len(total_article_number_of_each_indicator['year'].keys()))
        # print('------------------------------------------------------------')
        # return year_list, normalized_article_number_of_each_year


class PubmedArticlesStatistics:
    def __init__(self):
        pass

    @staticmethod
    def get_total_article_number_of_topic_of_year(term='', year=''):
        entrez_result = EntrezSearch(
            term=term,
            mindate=year,
            maxdate=year,
            retmax=MAX_NUMBER_OF_ARTICLE,
            save=False
        )
        return len(entrez_result.pmid_list)

    @staticmethod
    def get_total_article_number_of_journal(term='', journal=''):
        entrez_result = EntrezSearch(
            term=term + ' ' + journal + '[TA]',
            retmax=MAX_NUMBER_OF_ARTICLE,
            save=False
        )
        return len(entrez_result.pmid_list)


class RDataFrame:
    def __init__(self, origin_pmids, date, store_file_name='', ):
        print('------------------------------------------------------------')
        print('data manipulation')
        self.date = date
        self.origin_pmids = origin_pmids
        self.store_file_name = store_file_name
        self.citation_pmid_dict = np.load(store_file_name + 'citation_pmid.npy', allow_pickle=True).flat[0]
        self.article_info_dict = np.load(store_file_name + 'articles.npy', allow_pickle=True).flat[0]
        # ['title', 'abstract', 'journal', 'affiliation', 'authors', 'keywords', 'doi', 'year', 'pmid']
        self.articles = np.load(store_file_name + 'articles.npy', allow_pickle=True).flat[0]
        self.articles_of_Meshs = np.load(store_file_name + 'articles_of_Meshs.npy', allow_pickle=True).flat[0]
        self.articles_of_journals = np.load(store_file_name + 'articles_of_journals.npy', allow_pickle=True).flat[0]
        self.articles_of_years = np.load(store_file_name + 'articles_of_year.npy', allow_pickle=True).flat[0]
        self.articles_of_authors = np.load(store_file_name + 'articles_of_authors.npy', allow_pickle=True).flat[0]
        self.articles_of_affiliations = np.load(store_file_name + 'articles_of_affiliations.npy', allow_pickle=True).flat[0]
        self.cited_pmid = np.load(store_file_name + 'cited_pmid.npy', allow_pickle=True).flat[0]
        if os.path.exists(store_file_name + 'rdata.npy'):
            self.rdata = np.load(store_file_name + 'rdata.npy', allow_pickle=True).flat[0]
        else:
            self.rdata = dict()

        self.nodes = {
            'pmid': list(),
            'title': list(),
            'journal': list(),
            'date': list(),
            'LitCovid': list(),
            # 'month': list(),
            # 'day': list(),
            'cited': list(),
            'language': list(),
            'country': list(),
        }
        self.nodems = {
            'pmid': list(),
            'type': list(),
            'value': list(),
        }
        self.cnet = {
            'source': list(),
            'target': list(),
        }
        self.sumSingle = {
            'type': list(),
            'value': list(),
            'N': list(),
        }
        self.sumMESH = {
            'MESH': list(),
            'type': list(),
            'value': list(),
            'N': list(),
        }
        self.rel = {
            'V1': list(),
            'V2': list(),
            'type': list(),
            'N': list(),
        }
        self.relPMID = {
                'PMID1': list(),
                'PMID2': list(),
                'type': list(),
                'N': list(),
            }
        # if 'nodes' in self.rdata.keys():
        #     self.nodes = self.rdata['nodes']
        # if 'nodems' in self.rdata.keys():
        #     self.nodems = self.rdata['nodems']
        # if 'cnet' in self.rdata.keys():
        #     self.cnet = self.rdata['cnet']
        # if 'sumSingle' in self.rdata.keys():
        #     self.sumSingle = self.rdata['sumSingle']
        # if 'sumMESH' in self.rdata.keys():
        #     self.sumMESH = self.rdata['sumMESH']
        # if 'rel' in self.rdata.keys():
        #     self.rel = self.rdata['rel']
        # if 'relPMID' in self.rdata.keys():
        #     self.relPMID  = self.rdata['relPMID']

        self.update()
        self.generate_r_dataframe()

        need_to_delete = ['articles_of_affiliations.npy',
                          'articles_of_authors.npy',
                          'articles_of_journals.npy',
                          'articles_of_year.npy',
                          'articles_of_Meshs.npy',
                          'rdata.npy', ]
        for file in need_to_delete:
            _ = f'{store_file_name}/{file}'
            if os.path.exists(_):
                os.remove(_)
                print(f'delete {_}')

    def update(self):
        print('------------------------------------------------------------')
        self.update_nodes()
        print('------------------------------------------------------------')
        self.update_nodems()
        print('------------------------------------------------------------')
        self.update_cnet()
        print('------------------------------------------------------------')
        # self.update_sum_single()
        # print('------------------------------------------------------------')
        # self.update_sum_Mesh()
        # print('------------------------------------------------------------')
        # self.update_rel()
        # print('------------------------------------------------------------')
        # self.update_relPMID()

    def update_nodes(self):
        print('Update nodes.')
        # nodes nodems
        for pmid in self.article_info_dict.keys():
            if self.article_info_dict[pmid]['title'] == '':
                continue
            self.nodes['pmid'].append(int(pmid))
            self.nodes['title'].append(self.article_info_dict[pmid]['title'])
            self.nodes['journal'].append(self.article_info_dict[pmid]['journal'])
            year = int(self.article_info_dict[pmid]['year'])
            month = int(self.article_info_dict[pmid]['month'])
            day = int(self.article_info_dict[pmid]['day'])
            self.nodes['date'].append(datetime(year,month=month,day=day))
            self.nodes['language'].append(self.article_info_dict[pmid]['language'])
            if pmid not in self.cited_pmid:
                self.nodes['cited'].append(0)
            else:
                self.nodes['cited'].append(len(self.cited_pmid[pmid]))
            in_litcovid = True if pmid in self.origin_pmids else False
            self.nodes['LitCovid'].append(in_litcovid)
            self.nodes['country'].append(self.article_info_dict[pmid]['country'])

        self.rdata['nodes'] = self.nodes
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update nodes successfully.')

    def update_nodems(self):
        print('Update_multinodes.')
        # nodems
        for pmid in self.article_info_dict.keys():
            # keywords authors affiliation journal year
            for keyword in self.article_info_dict[pmid]['keywords']:
                self.nodems['pmid'].append(int(pmid))
                self.nodems['type'].append('MESH')
                self.nodems['value'].append(keyword)
            for i in self.article_info_dict[pmid]['authors']:
                self.nodems['pmid'].append(int(pmid))
                self.nodems['type'].append('author')
                self.nodems['value'].append(i)
            for i in self.article_info_dict[pmid]['affiliation']:
                self.nodems['pmid'].append(int(pmid))
                self.nodems['type'].append('affiliation')
                self.nodems['value'].append(i)

            publication_type = self.article_info_dict[pmid]['publication_type']
            publication_type = publication_type.lstrip()
            if publication_type == '':
                continue
            self.nodems['pmid'].append(int(pmid))
            self.nodems['type'].append('PublicationType')
            self.nodems['value'].append(publication_type)

            # self.nodems['pmid'].append(int(pmid))
            # self.nodems['type'].append('journal')
            # self.nodems['value'].append(self.article_info_dict[pmid]['journal'])
            #
            # self.nodems['pmid'].append(int(pmid))
            # self.nodems['type'].append('year')
            # self.nodems['value'].append(self.article_info_dict[pmid]['year'])

        self.rdata['nodems'] = self.nodems
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update multinodes successfully.')

    def update_cnet(self):
        print('Update cnet.')
        # cnet
        for pmid in self.citation_pmid_dict.keys():
            for i in self.citation_pmid_dict[pmid]:
                self.cnet['source'].append(int(pmid))
                self.cnet['target'].append(int(i))

        self.rdata['cnet'] = self.cnet
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update cnet successfully.')

    def update_sum_single(self):
        print('Update sum_single.')
        # sumSingle
        for keyword in self.articles_of_Meshs.keys():
            self.sumSingle['type'].append('MESH')
            self.sumSingle['value'].append(keyword)
            self.sumSingle['N'].append(len(self.articles_of_Meshs[keyword]))

        for keyword in self.articles_of_journals.keys():
            self.sumSingle['type'].append('journal')
            self.sumSingle['value'].append(keyword)
            self.sumSingle['N'].append(len(self.articles_of_journals[keyword]))

        for keyword in self.articles_of_authors.keys():
            self.sumSingle['type'].append('author')
            self.sumSingle['value'].append(keyword)
            self.sumSingle['N'].append(len(self.articles_of_authors[keyword]))

        for keyword in self.articles_of_affiliations.keys():
            self.sumSingle['type'].append('affiliation')
            self.sumSingle['value'].append(keyword)
            self.sumSingle['N'].append(len(self.articles_of_affiliations[keyword]))

        for keyword in self.articles_of_years.keys():
                self.sumSingle['type'].append('year')
                self.sumSingle['value'].append(keyword)
                self.sumSingle['N'].append(len(self.articles_of_years[keyword]))

        self.rdata['sumSingle'] = self.sumSingle
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update sum_single successfully.')

    def update_sum_Mesh(self):
        print('Update sumMESH.')
        # sumMESH
        for keyword in self.articles_of_Meshs.keys():
            if keyword == '':
                continue
            temp_dict = dict()
            # get articles of this mesh
            for pmid in self.articles_of_Meshs[keyword]:
                # for each article, get journals
                journal = self.articles[pmid]['journal']
                if journal not in temp_dict.keys():
                    temp_dict[journal] = 0
                temp_dict[journal] += 1

            for journal in temp_dict.keys():
                self.sumMESH['MESH'].append(keyword)
                self.sumMESH['type'].append('journal')
                self.sumMESH['value'].append(journal)
                self.sumMESH['N'].append(temp_dict[journal])

        self.rdata['sumMESH'] = self.sumMESH
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update sumMESH successfully.')

    def update_rel(self):
        print('Update rel.')
        #rel
        temp_meshs = list(self.articles_of_Meshs.keys())
        print('mesh number: ', len(temp_meshs))
        for keyword in self.articles_of_Meshs.keys():
            if keyword == '':
                print('empty mesh in table of rel')
                continue
            pmid_list1 = self.articles_of_Meshs[keyword]
            temp_meshs.remove(keyword)
            for mesh in temp_meshs:
                pmid_list2 = self.articles_of_Meshs[mesh]
                N = len(set(pmid_list1).intersection(pmid_list2))
                if N == 0:
                    continue
                self.rel['V1'].append(mesh)
                self.rel['V2'].append(keyword)
                self.rel['type'].append('MESH')
                self.rel['N'].append(N)

                self.rel['V1'].append(keyword)
                self.rel['V2'].append(mesh)
                self.rel['type'].append('MESH')
                self.rel['N'].append(N)

        self.rdata['rel'] = self.rel
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update mesh part of rel successfully.')

        counter = 0
        temp_authors = list(self.articles_of_authors.keys())
        origin_length = len(temp_authors)
        print('authors number: ', origin_length)
        print('already exist: ', self.rel['type'].count('author'))
        for keyword in self.articles_of_authors.keys():
            if counter%2000==0:
                try:
                    self.rdata['rel'] = self.rel
                    np.save(self.store_file_name + 'rdata', self.rdata)
                    print("Finish ", 100*(1-len(temp_authors)/origin_length), 'percent', len(temp_authors))
                except :
                    np.save(self.store_file_name + 'rdata', self.rdata)
                    exit(-1)
            counter += 1

            if keyword == '':
                print('empty author in table of rel')
                continue
            pmid_list1 = self.articles_of_authors[keyword]
            temp_authors.remove(keyword)
            for author in temp_authors:
                pmid_list2 = self.articles_of_authors[author]
                N = len(set(pmid_list1).intersection(pmid_list2))
                if N == 0:
                    continue
                # print(keyword, author, 'add')
                self.rel['V1'].append(keyword)
                self.rel['V2'].append(author)
                self.rel['type'].append('author')
                self.rel['N'].append(N)

                self.rel['V1'].append(author)
                self.rel['V2'].append(keyword)
                self.rel['type'].append('author')
                self.rel['N'].append(N)

        self.rdata['rel'] = self.rel
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update author part of rel successfully.')

    def update_relPMID(self):
        print('Update relPMID.')

        origin_length = len(self.articles.keys())
        temp_pmids = list(self.articles.keys())
        for pmid1 in self.articles.keys():
            temp_pmids.remove(pmid1)
            if (origin_length-len(temp_pmids))%1000 == 0:
                print()
                print("Finish ", 100 * (1 - len(temp_pmids) / origin_length), 'percent', len(temp_pmids))
            for pmid2 in temp_pmids:
                if pmid1 in self.citation_pmid_dict and pmid2 in self.citation_pmid_dict:
                    pmid_list1 = self.citation_pmid_dict[pmid1]
                    pmid_list2 = self.citation_pmid_dict[pmid2]
                    N1 = len(set(pmid_list1).intersection(pmid_list2))
                    if N1 > 0:
                        self.relPMID['PMID1'].append(pmid1)
                        self.relPMID['PMID2'].append(pmid2)
                        self.relPMID['type'].append('shared citation')
                        self.relPMID['N'].append(N1)

                        self.relPMID['PMID1'].append(pmid2)
                        self.relPMID['PMID2'].append(pmid1)
                        self.relPMID['type'].append('shared citation')
                        self.relPMID['N'].append(N1)

                if pmid1 in self.cited_pmid and pmid2 in self.cited_pmid:
                    pmid_list3 = self.cited_pmid[pmid1]
                    pmid_list4 = self.cited_pmid[pmid2]
                    N2 = len(set(pmid_list3).intersection(pmid_list4))
                    if N2 > 0:
                        self.relPMID['PMID1'].append(pmid1)
                        self.relPMID['PMID2'].append(pmid2)
                        self.relPMID['type'].append('co-cited')
                        self.relPMID['N'].append(N2)

                        self.relPMID['PMID1'].append(pmid2)
                        self.relPMID['PMID2'].append(pmid1)
                        self.relPMID['type'].append('co-cited')
                        self.relPMID['N'].append(N2)

        self.rdata['relPMID'] = self.relPMID
        np.save(self.store_file_name + 'rdata', self.rdata)
        print('Update relPMID successfully.')

    def generate_r_dataframe(self):
        print('nodes: ', len(self.rdata['nodes']['pmid']))
        print('nodems: ', len(self.rdata['nodems']['pmid']))
        print('cnet: ', len(self.rdata['cnet']['source']))
        # print('sumSingle: ', len(self.rdata['sumSingle']['type']))
        # print('sumMESH: ', len(self.rdata['sumMESH']['type']))
        # print('rel: ', len(self.rdata['rel']['type']))
        # print('relPMID: ', len(self.rdata['relPMID']['type']))

        if not os.path.exists(self.store_file_name+'feather/'):
            os.mkdir(self.store_file_name+'feather/')
        df = pd.DataFrame(self.rdata['nodes'])
        feather.write_dataframe(df, self.store_file_name+'feather/nodes.feather')
        df = pd.DataFrame(self.rdata['nodems'])
        feather.write_dataframe(df, self.store_file_name+'feather/nodems.feather')
        df = pd.DataFrame(self.rdata['cnet'])
        feather.write_dataframe(df, self.store_file_name+'feather/cnet.feather')
        # df = pd.DataFrame(self.rdata['sumSingle'])
        # feather.write_dataframe(df, self.store_file_name+'feather/sumSingle.feather')
        # df = pd.DataFrame(self.rdata['sumMESH'])
        # feather.write_dataframe(df, self.store_file_name+'feather/sumMESH.feather')
        fdate = {
            # 'fdate':[datetime(2020, 4, 14)]
            'fdate': [self.date]
        }
        df = pd.DataFrame(fdate)
        feather.write_dataframe(df, self.store_file_name + 'feather/fdate.feather')
        # df = pd.DataFrame(self.rdata['rel'])
        # feather.write_dataframe(df, self.store_file_name+'feather/rel.feather')
        # df = pd.DataFrame(self.rdata['relPMID'])
        # feather.write_dataframe(df, self.store_file_name+'feather/relPMID.feather')








from datetime import datetime
import os
from pubmed_analysis import download as d
from pubmed_analysis.download import EntrezSearch, MAX_NUMBER_OF_ARTICLE
from pubmed_analysis import data_manipulation as dm


store_file_name = 'data/sars/'
if not os.path.exists(store_file_name):
    os.mkdir(store_file_name)


def get_articles():
    entrez_result = EntrezSearch(
        term='sars',
        mindate='2000',
        maxdate='2020',
        retmax=MAX_NUMBER_OF_ARTICLE,
        store_file_name=store_file_name,
        update=True
    )
    origin_pmid_list = entrez_result.pmid_list

    print('total origin pmid:', len(origin_pmid_list))
    citation_pmid_dict = d.get_citation_pmid_dict(
        origin_pmid_list,
        store_file_name=store_file_name,
        update=True
    )

    pmid_list = list(origin_pmid_list)
    for pmid in citation_pmid_dict.keys():
        pmid_list += citation_pmid_dict[pmid]
    print('total pmid:', len(pmid_list))
    print('total pmid without repetition:', len(list(set(pmid_list))))

    d.get_cited_pmid_dict(
        list(set(pmid_list)),
        store_file_name=store_file_name,
        update=True
    )

    article_info = d.ArticleInfo(
        store_file_name=store_file_name,
        pmid_list=list(set(pmid_list)),
        update=True
    )
    articles = article_info.article_info_dict
    print('total articles:', len(articles))
    return articles


def manipulate_data(articles):
    my_article_statistics = dm.MyArticlesStatistics(articles, store_file_name)
    print('year', len(my_article_statistics.articles_by_years.keys()))
    print('journals', len(my_article_statistics.articles_by_journals.keys()))
    print('Mesh:', len(my_article_statistics.articles_by_Meshs.keys()))
    print('authors:', len(my_article_statistics.articles_by_authors.keys()))
    print('affiliations:', len(my_article_statistics.articles_by_affiliations.keys()))

    origin_pmid_list = []
    dm.RDataFrame(origin_pmids=origin_pmid_list,
                  date=datetime.now(),
                  store_file_name=os.path.dirname(__file__) + '/' + store_file_name)

if __name__ =='__main__':
    articles = get_articles()
    manipulate_data(articles)










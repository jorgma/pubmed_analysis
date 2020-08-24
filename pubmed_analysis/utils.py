# import matplotlib.pyplot as plt
# import os
# import numpy as np
# from pyvis.network import Network
import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mail", default='mail.yujun.liao@gmail.com')
    parser.add_argument("--tool", default='tool_yujun')
    parser.add_argument("--apikey", default='721d1d88d973f59b3449e2e041f167de6308')
    parser.add_argument("--s", default=1, type=float)
    parser.add_argument("--plist", nargs='+', default=['32603479'])
    parser.add_argument("--search", default='sars')

    return parser.parse_args()


# class DataHelper:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def cmp(a, b):
#         if a > b:
#             return 1
#         elif a < b:
#             return -1
#         else:
#             return 0
#
#     @staticmethod
#     def yearly_trend(article_info_dict, store_file_name='', term='', min_year=2000, max_year=2020):
#         total_year_list = list()
#         for pmid in article_info_dict.keys():
#             if article_info_dict[pmid]['year'] not in total_year_list:
#                 total_year_list.append(article_info_dict[pmid]['year'])
#         total_year_list.sort()
#
#         total_article_number_of_each_indicator = dict()
#         store_file_name = store_file_name + '_PubmedStatistics'
#         if os.path.exists(store_file_name + '.npy'):
#             total_article_number_of_each_indicator = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
#         # print(total_article_number_of_each_indicator['year'].keys())
#         if 'year' not in total_article_number_of_each_indicator.keys():
#             total_article_number_of_each_indicator['year'] = dict()
#
#         for year in total_year_list:
#             if year not in total_article_number_of_each_indicator['year'].keys():
#                 total_article_number_of_each_indicator['year'][
#                     year] = PubmedArticlesStatistics.get_total_article_number_of_topic_of_year(
#                     term=term,
#                     year=year
#                 )
#                 np.save(store_file_name, total_article_number_of_each_indicator)
#                 print('save total article number of year: ' + year)
#                 print('------------------------------------------------------------')
#
#         year_list = [str(i) for i in range(min_year, max_year + 1)]
#         normalized_article_number_list = list()
#         for year in sorted(year_list):
#             total_article_number = total_article_number_of_each_indicator['year'][year]
#             if total_article_number == 0:
#                 print('year %s did not publish article on this topic.' % year)
#                 continue
#             my_article_number = MyArticlesStatistics.category_articles_by_years(article_info_dict, year)
#             normalized_article_number_list.append(
#                 float(my_article_number) / float(total_article_number)
#             )
#         print('------------------------------------------------------------')
#         print('available years from %s to %s, in total %d years' % (
#         total_year_list[0], total_year_list[-1], len(total_year_list)))
#         print('show from %d to %d, in total %d years' % (min_year, max_year, max_year - min_year + 1))
#         print(year_list)
#         print(normalized_article_number_list)
#         print('------------------------------------------------------------')
#         return year_list, normalized_article_number_list
#
#     @staticmethod
#     def journal_trend(article_info_dict, store_file_name='', term='', max_number=20):
#         total_journal_list = list()
#         for pmid in article_info_dict.keys():
#             if article_info_dict[pmid]['journal'] not in total_journal_list:
#                 total_journal_list.append(article_info_dict[pmid]['journal'])
#
#         sorted_journal_dict_store_file_name = store_file_name + '_sorted_journal_list'
#         if os.path.exists(sorted_journal_dict_store_file_name + '.npy'):
#             sorted_journal_list = np.load(sorted_journal_dict_store_file_name + '.npy', allow_pickle=True)
#         else:
#             temp_dict = dict()
#             for journal in total_journal_list:
#                 my_article_number = MyArticlesStatistics.category_articles_by_journals(article_info_dict, journal)
#                 temp_dict[journal] = my_article_number
#                 # print(journal, my_article_number)
#             sorted_journal_list = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
#             np.save(sorted_journal_dict_store_file_name, sorted_journal_list)
#
#         total_article_number_of_each_indicator = dict()
#         store_file_name = store_file_name + '_PubmedStatistics'
#         if os.path.exists(store_file_name + '.npy'):
#             total_article_number_of_each_indicator = np.load(store_file_name + '.npy', allow_pickle=True).flat[0]
#         # print(total_article_number_of_each_indicator['year'].keys())
#         if 'journal' not in total_article_number_of_each_indicator.keys():
#             total_article_number_of_each_indicator['journal'] = dict()
#
#         print(sorted_journal_list[:max_number])
#         for (journal, my_article_number) in sorted_journal_list[:max_number]:
#             if journal not in total_article_number_of_each_indicator['journal'].keys():
#                 total_article_number_of_each_indicator['journal'][
#                     journal] = PubmedArticlesStatistics.get_total_article_number_of_journal(
#                     term=term,
#                     journal=journal
#                 )
#                 np.save(store_file_name, total_article_number_of_each_indicator)
#                 print('save total article number of journal: ' + journal)
#                 print('------------------------------------------------------------')
#
#         journal_list = list()
#         normalized_article_number_list = list()
#         for (journal, my_article_number) in sorted_journal_list[:max_number]:
#             total_article_number = total_article_number_of_each_indicator['journal'][journal]
#             if total_article_number == 0:
#                 print('journal %s did not publish article on this topic.' % journal)
#                 continue
#             journal_list.append(journal)
#             normalized_article_number_list.append(
#                 float(my_article_number) / float(total_article_number)
#             )
#         print('------------------------------------------------------------')
#         print('available journals: %d' % (len(total_journal_list)))
#         print('show top %d journals' % max_number)
#         print(journal_list)
#         print(normalized_article_number_list)
#         print('------------------------------------------------------------')
#         return journal_list, normalized_article_number_list
#
#     # def journal_trend(self, articles_info_dict):
#     #     temp_dict = dict()
#     #     for pmid in articles_info_dict.keys():
#     #         journal = articles_info_dict[pmid]['journal']
#     #         if journal not in temp_dict.keys():
#     #             temp_dict[journal] = 0
#     #         temp_dict[journal] += 1
#     #
#     #     journal_list =list()
#     #     normalized_article_number_of_each_journal = list()
#     #     # TODO(lyj): sort dict. record
#     #     sorted_d = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)
#     #     for item in sorted_d:
#     #         journal_list.append(item[0])
#     #         normalized_article_number_of_each_journal.append(item[1])
#     #     return journal_list, normalized_article_number_of_each_journal
#
#     def count_normalized_article_number_of_each_author(self, articles_info_dict):
#         """
#
#         :param articles_info_dict: a dictionary whose key is pmid,
#         value is information of referred article
#         :return: two list, the first list contains information of author
#         the second list contains information of normalized article number of each author
#         """
#
#         temp_dict = dict()
#         for pmid in articles_info_dict.keys():
#             authors = articles_info_dict[pmid]['authors'].split(";")
#             for author in authors:
#                 if author not in temp_dict.keys():
#                     temp_dict[author] = 0
#                 temp_dict[author] += 1
#
#         author_list = list()
#         normalized_article_number_of_each_author = list()
#         # sort
#         sorted_d = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)
#         for item in sorted_d:
#             author_list.append(item[0])
#             normalized_article_number_of_each_author.append(item[1])
#         return author_list, normalized_article_number_of_each_author
#
#     def count_normalized_article_number_of_each_mesh_term(self, articles_info_dict):
#         """
#
#         :param articles_info_dict: a dictionary whose key is pmid,
#         value is information of referred article
#         :return: two list, the first list contains information of mesh_term
#         the second list contains information of normalized article number of each mesh_term
#         """
#
#         temp_dict = dict()
#         for pmid in articles_info_dict.keys():
#             mesh_terms = articles_info_dict[pmid]['keywords'].split(';')
#             for mesh_term in mesh_terms:
#                 mesh_term = mesh_term.split(':')
#                 if len(mesh_term) < 2:
#                     print("error mesh_term :", mesh_term)
#                     continue
#                 mesh_term = mesh_term[1]
#                 if mesh_term not in temp_dict.keys():
#                     temp_dict[mesh_term] = 0
#                 temp_dict[mesh_term] += 1
#
#         mesh_term_list = list()
#         normalized_article_number_of_each_mesh_term = list()
#         # sort
#         sorted_d = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)
#         for item in sorted_d:
#             mesh_term_list.append(item[0])
#             normalized_article_number_of_each_mesh_term.append(item[1])
#         return mesh_term_list, normalized_article_number_of_each_mesh_term
#
#     # def get_normalized_article_number_of_differnt_inicator(articles_info_dict):
#     #     """
#     #
#     #     :param articles_info_dict: a dictionary whose key is pmid,
#     #     value is information of referred article
#     #     :return: two list, the first list contains information of journal
#     #     the second list contains information of normalized article number of each journal
#     #     """
#     #     indicator_list = ['year', 'journal']
#     #     normalized_article_number_of_differnt_inicator = dict()
#     #     for indicator in indicator_list:
#     #         temp_dict = dict()
#     #         for pmid in articles_info_dict.keys():
#     #             value_of_indicator = articles_info_dict[pmid][indicator]
#     #             if value_of_indicator not in temp_dict.keys():
#     #                 temp_dict[value_of_indicator] = 0
#     #             temp_dict[value_of_indicator] += 1
#     #
#     #         temp_list =list()
#     #         normalized_article_number_of_indicator = list()
#     #         for value_of_indicator in sorted(temp_dict.keys()):
#     #             temp_list.append(value_of_indicator)
#     #             normalized_article_number_of_indicator.append(temp_dict[value_of_indicator])

class CitationMap:
    def __init__(self, store_file_name='covid19_1/covid19_1' + '_citation_pmid_info.npy'):
        self.store_file_name = store_file_name

    def cmp(a, b):
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0

    def show(self):
        store_file_name = self.store_file_name
        citation_pmid_dict = np.load(store_file_name, allow_pickle=True).flat[0]
        # TODO(lyj); sort dict
        sorted_citation_pmid_list = sorted(citation_pmid_dict.items(), key=lambda x: len(x[1]), reverse=True)

        g = Network()
        for item in sorted_citation_pmid_list[:20]:
            g.add_node(item[0])
            for citation in item[1][:20]:
                g.add_node(citation)
                g.add_edge(item[0], citation)

        g.show_buttons(filter_=['physics'])
        g.show("basic.html")


def draw_bar_plot(x_list=[], y_list=[], min=0, max=30, title='', x_label='', y_label=''):
    plt.bar(
        x_list[min:max],
        y_list[min:max]
    )
    plt.xticks(rotation=270)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def draw_3D_bar_plot(x_list, y_list, max_number=2):
    # setup the figure and axes
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111, projection='3d')

    # fake data
    # _x = np.arange(2)
    # _y = np.arange(3,5)
    _x = x_list[:max_number]
    _y = y_list[:max_number]
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()
    print(x)
    print(y)
    top = [0, 1, 1, 2]
    print(top)
    bottom = np.zeros_like(top)
    width = depth = 1

    ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
    ax1.set_title('journal-year')

    plt.show()


# t = DataHelper.yearly_trend(
#     article_info_dict,
#     store_file_name=store_file_name,
#     term=term,
#     min_year=2003,
#     max_year=2020
# )
# draw_bar_plot(
#     x_list=t[0],
#     y_list=t[1],
#     title='Yearly Trend',
#     x_label='Year',
#     y_label='Normalized Number'
# )
#
# t = DataHelper.journal_trend(
#     article_info_dict,
#     store_file_name= store_file_name,
#     term=term,
#     max_number=20
# )
# draw_bar_plot(
#     x_list=t[0],
#     y_list=t[1],
#     title='Journal Trend',
#     x_label='Journal',
#     y_label='Normalized Number'
# )
# citation_map = CitationMap()
# citation_map.show()
#
# t = get_normalized_article_number_of_each_journal(articles)
# print('journal:', len(t[0]), t[0])
# print(len(t[1]), t[1])
# draw_bar_plot(t[0], t[1])
#
#
# t = get_normalized_article_number_of_each_author(articles)
# print('author:', len(t[0]), t[0])
# print(len(t[1]), t[1])
# draw_bar_plot(t[0], t[1])
#
# t = get_normalized_article_number_of_each_mesh_term(articles)
# print('mesh_term:', len(t[0]), t[0])
# print(len(t[1]), t[1])
# draw_bar_plot(t[0], t[1])

# t = get_normalized_article_number_of_each_mesh_term(articles)
# print('mesh_term:', len(t[0]), t[0])
# print(len(t[1]), t[1])
#
# draw_3D_bar_plot(t[0], t[1])




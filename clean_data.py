from lxml import etree
from lxml import html

import feather
import numpy as np
import csv
import pandas as pd



# flag = 0
# articles = np.load('data/covid19/articles.npy', allow_pickle=True).flat[0]
# for k in list(articles.keys()):
#     tem_list = list()
#     for item in articles[k]['keywords']:
#         if "allee effect" in item:
#             print(k)
#         # if '<' in item or '#' in item or (len(item)>0 and item[0] == "\\" ):
#         # if "#" in item or "<" in item:
#         #     print(k)
#         #     temp_set.add(k)
#         # tem_list.append(item.rstrip().lstrip())
#     # articles[k]['keywords'] = tem_list
#     # print()
#
# #         if "6vsb" in item:
# # #         if item.isdigit():
# # #             templist.append(k)
# #             print(k)
# #             break
# # for k in temp_set:
# #     pass
# #     del articles[k]
# # np.save('data/covid19/articles.npy', articles)


# mesh = {
#     # 'fdate':[datetime(2020, 4, 14)]
#     'mesh': list(temp_set)
# }
# df = pd.DataFrame(mesh)
# feather.write_dataframe(df, 'mesh.feather')

## export mesh map info


import xml.etree.ElementTree as ET
for year in ['2018', '2019', '2020']:
    for type in ['desc', 'qual', 'supp']:
        print(type+year)
        name = 'data/covid19/mesh_db/'+type+year+'.xml'
        tree = ET.parse(name)
        root = tree.getroot()

        id_list = []
        mesh_list = []
        year_list  = []
        for i in root.getchildren():
            id = i[0].text
            mesh = i[1][0].text
            id_list.append(id)
            mesh_list.append(mesh)
            year_list.append(year)
        mesh_map_info = {
            # 'fdate':[datetime(2020, 4, 14)]
            'id' : id_list,
            'term': mesh_list,
            'year' : year_list
        }
        df = pd.DataFrame(mesh_map_info)
        feather.write_dataframe(df, './data/covid19/feather/'+type+year+'.feather')



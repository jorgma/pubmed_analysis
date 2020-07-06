import numpy as np



templist = []
flag = 0
articles = np.load('data/covid19/articles.npy', allow_pickle=True).flat[0]
for k in articles.keys():
    for item in articles[k]['keywords']:
        if "6vsb" in item:
#         if item.isdigit():
#             templist.append(k)
            print(k)
#             break
# for k in templist:
#     del articles[k]
np.save('data/covid19/articles.npy', articles)


# templist = []
# articles = np.load('data/covid19/articles.npy', allow_pickle=True).flat[0]
# t = articles['32603479']
# print()
# # np.save('data/covid19/articles.npy', articles)


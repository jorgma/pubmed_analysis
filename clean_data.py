import numpy as np




articles = np.load('data/covid19/articles.npy', allow_pickle=True).flat[0]
for k in articles.keys():
    for item in articles[k]['keywords']:
        if "(" in item:
            # articles[k]['keywords'].remove(item)
            # articles[k]['keywords'] += item.split(',')
            print(k)
            print(item)

# np.save('data/covid19/articles.npy', articles)
import re
from bs4 import BeautifulSoup
import lxml.html
import random
from collections import Counter
import math
from tqdm import tqdm
import pickle
import numpy as np
from sklearn.decomposition import TruncatedSVD
from scipy import sparse

with open("./enwiki-20150112-400-r100-10576.txt", mode="r")as f:
    corpus = [w2 for w2 in
              [re.sub("^[\.,!\?;:\(\)\[\]'\"]|[\.,!\?;:\(\)\[\]'\"]$", "",
                      w).replace("\n", "")for line in f.readlines()
               for w in line.split(" ")]
              if w2 != ""]
with open("./corpus.txt", mode="w")as f:
    f.write(" ".join(corpus))


with open("./country.html", mode="r")as f:
    countries = [i.text_content() for i in lxml.html.fromstring(f.read()).
                 xpath(
        "/html/body/div[2]/table/tr/td/table[2]/tr[*]/td[1]")][1:-1]
with open("./countries.pickle", mode="wb")as f:
    pickle.dump(countries[1:-1], f)

with open("./corpus.txt", mode="r")as f:
    corpus_txt = f.read()
for country in countries:
    corpus_txt = corpus_txt.replace(country, country.replace(" ", "_"))

corpus_list = corpus_txt.split(" ")

f_tc = []
f_t = []
f_c = []
N = len(corpus_list)

with open("./content.txt", mode="w")as f:
    for i, word in enumerate(corpus_list):
        d = random.randint(1, 5)
        context = " ".join([corpus_list[j]
                            for j in range(max(0, i - d),
                                           min(len(corpus_list),
                                               i + d + 1))if i != j])
        f_tc.append(word + "\t" + context)
        f_t.append(word)
        f_c.append(context)
        """
        print(" ".join([corpus_list[j]
                        for j in range(max(0, i - d),
                                       min(len(corpus_list),
                                           i + d + 1))if i != j]), file=f)
        """

count_f_tc = Counter(f_tc)
count_f_t = Counter(f_t)
count_f_c = Counter(f_c)

sorted_ts = sorted(count_f_t.keys())
t2index = {t: i for i, t in enumerate(sorted_ts)}
sorted_cs = sorted(count_f_c.keys())
c2index = {c: i for i, c in enumerate(sorted_cs)}

Y = sparse.lil_matrix((len(sorted_ts), len(sorted_cs)))
X = {}
for tc, count in tqdm(count_f_tc.items()):
    t, c = tc.split("\t")
    if t not in X:
        X[t] = {}
    if count < 10:
        X[t][c] = 0
    else:
        X[t][c] = max(math.log(N * count / (count_f_t[t] * count_f_c[c])), 0)
        Y[t2index[t], c2index[c]] = X[t][c]
with open("./X.pickle", mode="wb")as f:
    pickle.dump(X, f)

with open("./Y.pickle", mode="wb")as f:
    pickle.dump(Y, f)

with open("./t2index.pickle", mode="wb")as f:
    pickle.dump(t2index, f)


with open("./Y.pickle", mode="rb")as f:
    Y = pickle.load(f)

with open("./t2index.pickle", mode="rb")as f:
    t2index = pickle.load(f)


with open("./t2index.pickle", mode="rb")as f:
    t2index = pickle.load(f)

pca = TruncatedSVD(n_components=300)
pca_Y = pca.fit_transform(Y)

with open("./pca_Y.pickle", mode="wb")as f:
    pickle.dump(pca_Y, f)


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (1 + np.linalg.norm(v1) * np.linalg.norm(v2))


with open("./pca_Y.pickle", mode="rb")as f:
    pca_Y = pickle.load(f)
print(pca_Y[t2index["United_States"]])
print(cos_sim(pca_Y[t2index["United_States"]],
              pca_Y[t2index["U.S"]]))

index2t = {t2index[t]: t for t in sorted(t2index.keys())}
england_sim = np.array([cos_sim(pca_Y[t2index["England"]], pca_Y[t2index[t]])
                        for t in sorted(t2index.keys())])
print([(index2t[index], england_sim[index])
       for index in np.argsort(england_sim)[::-1][:10]])

country_vec = pca_Y[t2index["Spain"]] - \
    pca_Y[t2index["Madrid"]] + pca_Y[t2index["Athens"]]
print(country_vec)
country_sim = np.array([cos_sim(country_vec, pca_Y[t2index[t]])
                        for t in sorted(t2index.keys())])
print([(index2t[index], country_sim[index])
       for index in np.argsort(country_sim)[::-1][:10]])

from gensim.models import Word2Vec
import gensim
import pickle
import numpy as np
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, ward, leaves_list
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

model = Word2Vec(gensim.models.word2vec.Text8Corpus(
    "./../9/corpus_txt.txt"))
model.save("w2v.model")

model = Word2Vec.load("w2v.model")
print(model.wv["United_States"])
print(model.wv.distance("United_States", "U.S"))
print(model.most_similar([model.wv["England"]], [], 10))
print(model.most_similar(positive=['Spain', 'Athens'], negative=['Madrid']))

with open("./questions-words.txt", mode="r") as f:
    with open("./questions-words_family.txt", mode="w") as f2:
        write = False
        for line in f.readlines():
            if line == ": family\n":
                write = True
            elif write and line[0] == ":":
                break
            elif write:
                print(line, end="", file=f2)

with open("../9/t2index.pickle", mode="rb")as f:
    t2index = pickle.load(f)
with open("../9/pca_Y.pickle", mode="rb")as f:
    pca_Y = pickle.load(f)
index2t = {t2index[t]: t for t in sorted(t2index.keys())}


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (1 + np.linalg.norm(v1) * np.linalg.norm(v2))


score1 = []
score2 = []
with open("./questions-words_family.txt", mode="r") as f:
    for line in f.readlines():
        line_list = line.replace("\n", "").split(" ")
        if all([ll in t2index for ll in line_list]) and\
                all([ll in model.wv for ll in line_list]):
            pre1, _ = model.most_similar(positive=[
                model.wv[line_list[1]], model.wv[line_list[2]]],
                negative=[model.wv[line_list[0]]])[0]
            vec = pca_Y[t2index[line_list[1]]] - \
                pca_Y[t2index[line_list[0]]] + pca_Y[t2index[line_list[2]]]
            sim = np.array([cos_sim(vec, pca_Y[t2index[t]])
                            for t in sorted(t2index.keys())])
            pre2, _ = [(index2t[index], sim[index])
                       for index in np.argsort(sim)[::-1][:1]][0]
            score1.append(pre1 == line_list[3])
            score2.append(pre2 == line_list[3])
            print(pre1, pre2, line_list[3])
print(sum(score1) / len(score1), sum(score2) / len(score2))

sim1 = []
sim2 = []
sim_ans = []
score2 = []
with open("./wordsim353/combined.tab", mode="r") as f:
    for line in f.readlines()[1:]:
        line_list = line.replace("\n", "").split("\t")
        if all([ll in t2index for ll in line_list][:-1]) and\
                all([ll in model.wv for ll in line_list[:-1]]):
            pre1 = model.wv.distance(line_list[0], line_list[1])
            pre2 = cos_sim(pca_Y[t2index[line_list[0]]],
                           pca_Y[t2index[line_list[1]]])
            print(pre1, pre2, line_list[2])
            sim1.append(float(pre1))
            sim2.append(float(pre2))
            sim_ans.append(float(line_list[2]))
sort1 = np.argsort(sim1)
sort2 = np.argsort(sim2)
sort_ans = np.argsort(sim_ans)
N = len(sim1)
print("80", 1 -
      (6 * sum([(a - b)**2 for a, b in zip(sort1, sort_ans)]) / (N**3 - N)))
print("90", 1 -
      (6 * sum([(a - b)**2 for a, b in zip(sort2, sort_ans)]) / (N**3 - N)))

country_vec = []
country_names = []

with open("../9/countries.pickle", mode="rb")as f:
    countries = pickle.load(f)
for country in sorted(countries):
    country = country.replace(" ", "_")
    if country in model.wv:
        country_vec.append(model.wv[country])
        country_names.append(country)
country_vec = np.array(country_vec)

clf_kmeans = KMeans(n_clusters=5).fit(country_vec)
k_means = clf_kmeans.predict(country_vec)

print([(cluster, name)for cluster, name in zip(k_means, country_names)])


h_cls = ward(country_vec)
dendrogram(h_cls, labels=country_names)
plt.show()

fig, ax = plt.subplots()
X = TSNE(n_components=2, random_state=0).fit_transform(country_vec)
plt.scatter(X[:, 0], X[:, 1])
for i, X_i in enumerate(X):
    ax.annotate(country_names[i], X_i)
plt.show()

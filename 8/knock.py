import random
from nltk.stem import SnowballStemmer
import chardet
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt

with open("./rt-polaritydata/rt-polaritydata/rt-polarity.pos", mode="rb") as f:
    lines = ["+1 " + l.decode("Windows-1252") for l in f.readlines()]
    print(lines)
with open("./rt-polaritydata/rt-polaritydata/rt-polarity.neg", mode="rb") as f:
    lines.extend(["-1 " + l.decode("Windows-1252") for l in f.readlines()])
random.shuffle(lines)
with open("./segment.txt", mode="w") as f:
    f.write("\n".join(lines))

with open("./segment.txt", mode="r") as f:
    lines = f.readlines()

stop_words = ["a", "is", "the", "of", ".",
              ",", "?", "it", "this", "that", "", "\n", "and", "or"]


def in_stop_words(word): return word in stop_words  # これ関数にする意味ある？？？？？


assert in_stop_words("a") is True
assert in_stop_words("I") is False

stemmer = SnowballStemmer("english")
stem_counter = Counter([stemmer.stem(word)
                        for line in lines for word in line.split(" ")[1:]])
stem_dict = {word: i for i, word
             in enumerate([word for word, count in stem_counter.items()
                           if count < 0.5 * len(lines) and count > 2
                           and not(in_stop_words(word))])}

X = []
for line in lines:
    words = line.split(" ")
    X.append([1 if key in words else 0 for key in stem_dict])
X = np.array(X)
Y = np.array([1 if line.split(" ")[0] == "+1" else 0 for line in lines])


model = LogisticRegression()
model.fit(X, Y)
print(model.score(X, Y))
identity = list(zip(model.coef_[0], list(stem_dict)))
identity.sort(key=lambda x: x[0])

print(identity[:10])
print(identity[-10:])

for i, p in enumerate(model.predict_proba(X)):
    print("correct:{} ,predict:{} ,proba:{}".format(
        Y[i], np.argmax(p), np.max(p)))
pred_Y = model.predict(X)
print("適合率:{}, 再現率:{}, F1スコア{}".
      format(metrics.precision_score(Y, pred_Y),
             metrics.recall_score(Y, pred_Y), metrics.f1_score(Y, pred_Y)))

model2 = LogisticRegression()
scores = cross_validate(model2, X, Y, cv=KFold(
    n_splits=5), scoring=["f1", "precision", "recall"])
print(scores)

proba_Y = np.array(list(zip(*model.predict_proba(X)))[1])

threshold_list = [i * 0.05 for i in range(1, 20)]
plt.plot(threshold_list, [np.average(((proba_Y > th) == Y))
                          for th in threshold_list])
plt.show()

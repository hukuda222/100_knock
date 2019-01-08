import re
from nltk.stem.snowball import SnowballStemmer as SS
import xml.etree.ElementTree as ET
import pydot

nlp_txt = open("./nlp.txt", mode="r").read()
lines = re.split("(?<=[\.|;|\?|!]) (?=[A-Z])|\n+", nlp_txt)[:-1]

print(lines)

print([l.split(" ") for l in lines])

ss = SS("english")
print([[ss.stem(re.sub("\.|;|\?|!", "", w))
        for w in l.split(" ")] for l in lines])

tree = ET.ElementTree(file='nlp.txt.xml')
for ss in tree.getroot()[0][1]:
    for s in ss:
        for l in s:
            for w in s:
                print(w.find("word").text, end=" ")
                print(w.find("lemma").text, end=" ")
                print(w.find("POS").text)

for ss in tree.getroot()[0][1]:
    for s in ss:
        for l in s:
            for w in s:
                if w.find("POS").text == "NNP" or w.find("POS").text == "NNPS":
                    print(w.find("word").text)

for cs in tree.getroot()[0][2]:
    po = tree.getroot()[0][1][int(cs[0].find("sentence").text) -
                              1][0][int(cs[0].find("head").text) - 1].\
        find("word").text
    for c in cs:
        yo = tree.getroot()[0][1][int(c.find("sentence").text) -
                                  1][0][int(c.find("head").text) - 1].\
            find("word")
        yo.text = po + "(" + yo.text + ")"
        print(tree.getroot()[0][1][int(c.find("sentence").text) -
                                   1][0][int(c.find("head").text) - 1].
              find("word").text)

graph = pydot.Dot(graph_type='digraph')
sentence_root = tree.getroot()[0][1][0]  # 最後の0はindex

for d in sentence_root.find("./dependencies"):
    if not d.get("type") == "punct":
        graph.add_node(pydot.Node(
            str(d.find("./governor").get("idx")),
            label=d.find("./governor").text))
        graph.add_node(pydot.Node(
            str(d.find("./dependent").get("idx")),
            label=d.find("./dependent").text))
        graph.add_edge(pydot.Edge(
            str(d.find("./governor").get("idx")),
            str(d.find("./dependent").get("idx"))))
graph.write_png("po.png")


for sentence in tree.getroot()[0][1]:
    have_nsubj = {}
    have_dobj = {}
    for d in sentence.find("./dependencies"):
        if d.get("type") == "nsubj":
            have_nsubj[d.find("./governor").get("idx")
                       ] = (d.find("./dependent").text,
                            d.find("./governor").text)
        elif d.get("type") == "dobj":
            have_dobj[d.find("./governor").get("idx")
                      ] = (d.find("./dependent").text,
                           d.find("./governor").text)
    for ni in have_nsubj:
        for di in have_dobj:
            if ni == di:
                print(*have_nsubj[ni], have_dobj[di][0])
                break


sentence_parse = tree.getroot()[0][1][0].find("parse").text  # 3つ目の0はindex
np_blocks = []
np_lefts = []
kakko = 0
for c in re.split("(\)|\()", sentence_parse):
    for i in range(len(np_lefts)):
        np_lefts[i][1] += c
    if c == "(":
        kakko += 1
    elif c == ")":
        kakko -= 1
        for i in range(len(np_lefts)):
            if np_lefts[i][0] == kakko:
                np_blocks.append(np_lefts[i][1][:-1])
                np_lefts.pop(i)
                break
    elif c == "NP ":
        np_lefts.append([kakko - 1, ""])
        print("q")
print(np_blocks)

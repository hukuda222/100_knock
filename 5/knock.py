from collections import Counter
import CaboCha
import re
import pydot

c = CaboCha.Parser()

parse_txt = "".join([c.parse(l).toString(CaboCha.FORMAT_LATTICE)
                     for l in open("./neko.txt", mode="r").readlines()])
open("./neko.txt.cabocha", mode="w").write(parse_txt)
parse_txt = "\n".join(open("./neko.txt.cabocha", mode="r").readlines())


class Morph:
    def __init__(self, s, p, p1, b):
        self.surface = s
        self.base = b
        self.pos = p
        self.pos1 = p1

    def put(self):
        print(self.surface, self.base, self.pos, self.pos1)


class Chunk:
    def __init__(self, ms, d, s):
        self.morphs = ms
        self.dst = d
        self.srcs = s

    def put(self):
        print([(m.surface, m.base, m.pos, m.pos1)
               for m in self.morphs], self.dst, self.srcs)


all_morph = [[]]
all_chunk = [[]]
tmp_srcs = []
tmp_morphs = []
dst = 0
srcs = []

for line in parse_txt.split("\n"):
    if len(line) < 3:
        continue
    elif line == "EOS":
        if len(all_morph[-1]) > 0:
            all_chunk[-1].append(Chunk(tmp_morphs, dst, srcs))
            all_morph.append([])
            all_chunk.append([])
            tmp_srcs = []
            tmp_morphs = []
    elif line[0] == "*":
        if len(tmp_srcs) != 0:
            all_chunk[-1].append(Chunk(tmp_morphs, dst, srcs))
        infos = line.split(" ")
        index, dst = int(infos[1]), int(infos[2][:-1])
        tmp_srcs.append((index, dst))
        srcs = [ss[0] for ss in tmp_srcs if ss[1] == index]
        tmp_morphs = []
    else:
        wordinfo = re.split("[,|\t]", line)
        all_morph[-1].append(Morph(wordinfo[0], wordinfo[1],
                                   wordinfo[2], wordinfo[7]))
        tmp_morphs.append(Morph(wordinfo[0], wordinfo[1],
                                wordinfo[2], wordinfo[7]))

[w.put() for w in all_morph[2]]

[w.put() for w in all_chunk[7]]

[[print("".join([m.surface for m in c.morphs if m.pos != "記号"]),
        "".join([m.surface for m in cs[c.dst].morphs if m.pos != "記号"]))
  for c in cs] for cs in all_chunk]

[[print("".join([m.surface for m in c.morphs if m.pos != "記号"]),
        "".join([m.surface for m in cs[c.dst].morphs if m.pos != "記号"]))
  for c in cs if any([m.pos == "名詞" for m in c.morphs])and
  any([m.pos == "動詞" for m in cs[c.dst].morphs])] for cs in all_chunk]

graph = pydot.Dot(graph_type='digraph')
for i, p in enumerate(all_chunk[7]):
    graph.add_node(pydot.Node(str(i),
                              label="".join([m.surface for m in p.morphs
                                             if m.pos != "記号"])))
    if p.dst != -1:
        graph.add_edge(pydot.Edge(str(i), str(p.dst)))
graph.write_png("po.png")

for cs in all_chunk:
    for c in cs:
        if any([m.pos == "動詞" for m in c.morphs]) and \
                any([m.pos == "助詞" for src in c.srcs for m in cs[src].morphs]):
            for m in c.morphs:
                if m.pos == "動詞":
                    print(m.base, end=" ")
                    break
            for src in c.srcs:
                for m in cs[src].morphs:
                    if m.pos == "助詞":
                        print(m.base, end=" ")
            print()

for cs in all_chunk:
    for c in cs:
        if any([m.pos == "動詞" for m in c.morphs]) and \
                any([m.pos == "助詞" for src in c.srcs for m in cs[src].morphs]):
            for m in c.morphs:
                if m.pos == "動詞":
                    print(m.base, end=" ")
                    break
            for src in c.srcs:
                for m in cs[src].morphs:
                    if m.pos == "助詞":
                        print(m.base, end=" ")
            for src in c.srcs:
                print("".join([m.surface for m in cs[src].morphs]), end=" ")
            print()


for cs in all_chunk:
    for c in cs:
        if any([m.pos1 == "サ変接続" and c.morphs[i + 1].surface == "を"
                for i, m in enumerate(c.morphs[:-1])]) and \
                any([m.pos == "助詞"for src in c.srcs for m in cs[src].morphs])\
                and any([m.pos == "動詞" for m in cs[c.dst].morphs]):
            for m in c.morphs:
                if m.pos1 == "サ変接続":
                    print(m.base + "を", end="")
                    break
            for m in cs[c.dst].morphs:
                if m.pos == "動詞":
                    print(m.base, end=" ")
                    break
            josi_index = []
            for src in c.srcs:
                for m in cs[src].morphs:
                    if m.pos == "助詞":
                        print(m.base, end=" ")
                        josi_index.append(src)
                        break
            for src in c.srcs:
                if src in josi_index:
                    print(
                        "".join([m.surface for m in cs[src].morphs]), end=" ")
            print()

for cs in all_chunk:
    for i, c in enumerate(cs):
        if any([m.pos == "名詞" for m in c.morphs]) and c.dst != -1:
            print("".join([m.surface for m in c.morphs]), end="")
            new_c_i = i
            while(True):
                new_c_i = cs[new_c_i].dst
                if new_c_i == -1:
                    break
                print(
                    " -> " + "".join([m.surface for m in cs[new_c_i].morphs]),
                    end="")
            print()

for cs in all_chunk:
    for i, c in enumerate(cs[:-1]):
        if all([m.pos != "名詞" for m in c.morphs]) or c.dst == -1:
            continue
        new_c_i = i
        cx_list = [i]
        while(True):
            new_c_i = cs[new_c_i].dst
            if new_c_i == -1:
                break
            cx_list.append(new_c_i)
        for j, c2 in enumerate(cs):
            if i >= j:
                continue
            elif all([m.pos != "名詞" for m in c2.morphs]) or c2.dst == -1:
                continue
            new_c2_i = j
            cy_list = [j]
            if j not in cx_list:
                while(True):
                    new_c2_i = cs[new_c2_i].dst
                    cy_list.append(new_c2_i)
                    if new_c2_i in cx_list:
                        break
                print(
                    " -> ".join(["".join(["X" if ci == i and m.pos == "名詞"
                                          else m.surface
                                          for m in cs[ci].morphs])
                                 for ci in cx_list if ci < cy_list[-1]]),
                    end=" | ")
                print(
                    " -> ".join(["".join(["Y" if ci == j and m.pos == "名詞"
                                          else m.surface for m
                                          in cs[ci].morphs])for ci
                                 in cy_list[:-1]]),
                    end=" | ")
                print(
                    "".join([m.surface for m in cs[cy_list[-1]].morphs]))
            else:
                print(
                    " -> ".join(["".join(["X" if ci == i and m.pos == "名詞"
                                          else "Y" if ci == j and
                                          m.pos == "名詞" else m.surface for m
                                          in cs[ci].morphs])
                                 for ci in cx_list if ci <= j]))

import MeCab
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as mpl
font = {"family": "AppleGothic"}
mpl.rc('font', **font)


m = MeCab.Tagger()

parse_txt = m.parse("".join(open("./neko.txt", mode="r").readlines()))
open("./neko.txt.mecab", mode="w").write(parse_txt)

all_list = [[]]
[all_list[-1].append({"surface": l1, "base": l2[6], "pos":l2[0], "pos1":l2[1]})
 or (l1 == "。" and all_list.append([])) for l1, l2
 in [(l.split("\t")[0], l.split("\t")[-1].split(","))
     for l in parse_txt.split("\n") if len(l.split("\t")) > 1]]


print([l["surface"] for ls in all_list for l in ls if l["pos"] == "動詞"])

print([l["base"] for ls in all_list for l in ls if l["pos"] == "動詞"])

print([l for ls in all_list for l in ls if l["pos1"] == "サ変接続"])

print([(ls[i - 1], ls[i + 1])for ls in all_list for i, l in enumerate(ls)
       if l["surface"] == "の" and ls[i - 1]["pos"] == "名詞"
       and ls[i + 1]["pos"] == "名詞"])

longest = [[]]
[longest[-1].append(l) if l["pos"] == "名詞"
 else longest.append([]) if len(longest[-1]) > 0 else ""
 for ls in all_list for l in ls]
print(longest)

count = Counter([w["surface"] for l in all_list for w in l]).most_common()
print(count)

plt.bar(list(range(10)), [c for _, c in count[:10]],
        tick_label=[w for w, _ in count[:10]])
plt.show()

plt.hist([c for _, c in count], bins=30, range=(1, 40))
plt.show()

plt.loglog(list(range(len(count))), [c for _, c in count])
plt.show()

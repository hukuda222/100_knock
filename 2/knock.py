from collections import Counter

file = open("po.txt", mode="r").readlines()

print(len(file))

print([i.replace("\t", " ") for i in file])

open("col1.txt", mode="w").write(file[0])
open("col2.txt", mode="w").write(file[1])

print("\t".join([open("col" + str(i) + ".txt", mode="r").read()
                 for i in [1, 2]]))

print("".join((lambda n: file[:n])(3)))

print("".join((lambda n: file[-n:])(3)))

print((lambda n: ["".join(file[i::n]) for i in range(n)])(3))

print(set([l.split("\t")[0] for l in file]))

print(sorted(file, key=lambda l: -float(l.split("\t")[2])))

print([w for w, i in Counter([l.split("\t")[0] for l in file]).most_common()])

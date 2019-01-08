from collections import Counter
import random

print("stressed"[::-1])

print("".join([s for i, s in enumerate("パタトクカシーー") if i % 2]))

print("".join([s1 + s2 for s1, s2 in zip("パトカー", "タクシー")]))

pi = "Now I need a drink, alcoholic of course, after" +\
    " the heavy lectures involving quantum mechanics."

print([w for w, i in Counter([w[0] for w in pi.split(" ")]).most_common()])

ele = "Hi He Lied Because Boron Could Not Oxidize Fluorine." +\
    " New Nations Might Also Sign Peace Security Clause. Arthur King Can."
nums = [1, 5, 6, 7, 8, 9, 15, 16, 19]
print({w[0]if i in nums else w[0:2]: i for i, w in enumerate(ele.split(" "))})

gram = "I am an NLPer"


def ngram(n, s):
    return [s[i:i + 2]for i in range(len(s) - n)]


print(ngram(2, gram))
print(ngram(2, gram.split(" ")))


X = set(ngram(2, "paraparaparadise"))
Y = set(ngram(2, "paragraph"))

print(X | Y)
print(X & Y)
print(X - Y)

print((lambda x, y, z: x + "時の" + y + "は" + z)("12", "気温", "22.4"))

print("".join([(lambda x:chr(219 - ord(x)) if x >= "a" and x <=
                "z" else x)(c) for c in "i am pen."]))


poyo = "I couldn't believe that I could actually understand what " +\
    "I was reading : the phenomenal power of the human mind ."

print(" ".join([w if len(w) <= 4 else
                "".join([w[0]] + [w[i] for i in
                                  random.sample(list(range(1, len(w) - 1)),
                                                len(w) - 2)] + [w[-1]])
                for w in poyo.split(" ")]))

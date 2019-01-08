import json
import re
import urllib.parse
import urllib.request

f = open("./jawiki-country.json", mode="r")
data = [l2 for l2 in [json.loads(l)
                      for l in f] if l2["title"] == "イギリス"][0]
print(data["text"])

print("\n".join([l for l in data["text"].split(
    "\n") if l.find("Category") != -1]))

print([re.search("(?<=Category:)[^]]*", l).group(0)
       for l in data["text"].split("\n") if l.find("Category") != -1])

print({re.search("(?<==)[^=]+(?==)", l).group(0):
       len(re.search("=+", l).group(0)) - 1
       for l in data["text"].split("\n") if l.find("==") != -1})

print([re.search("(?<=File:)[^|]*", l).group(0)
       for l in data["text"].split("\n") if l.find("File") != -1])

print({re.search("(?<=|)[^|]+(?= = )", l).group(0):
       re.search("(?<= = ).+", l).group(0)
       for l in data["text"].split("\n") if l.find(" = ") != -1})


def all_sub(ps, ls, x):
    return all_sub(ps, ls, re.sub(ps.pop(0), ls.pop(0), x)
                   ) if len(ps) > 1 else re.sub(ps[0], ls[0], x)


print({re.search("(?<=|)[^|]+(?= = )", l).group(0):
       re.search("(?<= = ).+", l).group(0).replace("'", "")
       for l in data["text"].split("\n") if l.find(" = ") != -1})

print({re.search("(?<=|)[^|]+(?= = )", l).group(0):
       all_sub([re.compile("\[\[[^\|]*\|([^\|]*)\]\]"),
                re.compile("\[\[([^\]]*)\]\]")], ["\\1", "\\1"],
               re.search("(?<= = ).+", l).group(0).replace("'", ""))
       for l in data["text"].split("\n") if l.find(" = ") != -1})

dic = {re.search("(?<=|)[^|]+(?= = )", l).group(0):
       all_sub([re.compile("\[\[[^\|]*\|([^\|]*)\]\]"),
                re.compile("\[\[([^\]]*)\]\]"), re.compile("<.*>"),
                re.compile("['\[\]]")],
               ["\\1", "\\1", "", ""], re.search("(?<= = ).+", l).group(0))
       for l in data["text"].split("\n") if l.find(" = ") != -1}
print(dic)

url = "https://www.mediawiki.org/w/api.php?action=query&titles=File:"\
    + urllib.parse.quote(dic["国旗画像"])\
    + "&format=json&prop=imageinfo&iiprop=url"

connection = urllib.request.urlopen(urllib.request.Request(url))
print(json.loads(connection.read().decode())
      ["query"]["pages"]["-1"]["imageinfo"][0]["url"])

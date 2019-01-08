import pymongo
import redis
import json

r = redis.StrictRedis(host="localhost", port=6379, db=0)
r.flushdb()
with open("./artist.json", encoding="utf-8",)as f:
    for l in f.readlines():
        data = json.loads(l)
        if "area" in data:
            r.hset("area", data["name"], data["area"])
        if "tags" in data:
            r.hset("tags", data["name"],
                   json.dumps(data["tags"]))

print(r.hget("area", "Oasis").decode("utf-8"))

print(sum([1 for key in r.scan_iter() if r.get(key) == b"Japan"]))

print([(tag["value"], tag["count"])
       for tag in json.loads(r.hget("tags", "Oasis").decode("utf-8"))])

client = pymongo.MongoClient('localhost', 27017)
db = client["100_db"]
co = db.artist

db.artist.createIndex({"name": 1})
db.artist.createIndex({"aliases.name": 1})
db.artist.createIndex({"tags.value": 1})
db.artist.createIndex({"rating.value": 1})

[print(data) for data in co.find({"name": "Queen"})]

print(co.find({"area": "Japan"}).count())

[print(data) for data in co.find({"aliases.name": "Queen"})]

[print(data) for data in co.find({"tags.value": "dance"}).
 sort([("rating.count", -1)]).limit(10)]

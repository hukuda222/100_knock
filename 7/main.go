package main

import (
	"encoding/json"
	"github.com/julienschmidt/httprouter"
	mgo "gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"log"
	"net/http"
)

type tag struct {
	Count int
	Value string
}

type artist struct {
	ID   bson.ObjectId `bson:"_id,omitempty"`
	Name string        `bson:"name"`
	Area string        `bson:"area"`
	Tags []tag
}

func Index(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-Type", "application/json")
	session, _ := mgo.Dial("mongodb://localhost:27017")
	defer session.Close()
	db := session.DB("100_db")
	col := db.C("artist")
	var p []artist
	col.Find(bson.M{"name": r.URL.Query().Get("name")}).All(&p)
	json, _ := json.Marshal(p)
	w.Write(json)
}
func main() {
	router := httprouter.New()
	router.GET("/", Index)
	log.Fatal(http.ListenAndServe(":8080", router))
}

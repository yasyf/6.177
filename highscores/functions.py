#!/usr/bin/env python

import pymongo, os, datetime

client = pymongo.MongoClient(os.environ['db'])
db = client.highscores
highscores = db.highscores

def insert_high_score(values):
    if values.get('name') and values.get('score'):
        highscores.insert({"name": values.get('name'), "score": int(values.get('score')), "dt": datetime.datetime.now()})

def get_high_scores():
    return highscores.find().sort("score", -1)
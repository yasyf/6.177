#!/usr/bin/env python

import pymongo, os, datetime

client = pymongo.MongoClient(os.environ['db'])
db = client.highscores
highscores = db.highscores

#Gareth @ http://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

def insert_high_score(values):
    if values.get('name') and values.get('score'):
        highscores.update({"name": values.get('name')}, {"$set": {"score": int(values.get('score')), "dt": datetime.datetime.now()}}, True)
        return ordinal(highscores.find({"score": {"$gte": int(values.get('score'))}}).count())

def get_high_scores():
    return highscores.find().sort("score", -1)

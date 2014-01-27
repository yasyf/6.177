#!/usr/bin/env python

import pymongo, os

client = pymongo.MongoClient(os.environ['db'])
db = client.highscores
highscores = db.highscores
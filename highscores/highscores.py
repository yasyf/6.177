#!/usr/bin/env python

from flask import Flask, request, render_template
from functions import *

app = Flask(__name__)
app.secret_key = os.environ['sk']
    
@app.route('/')
def index():
	if request.values.get('name') and request.values.get('score'):
		return insert_high_score(request.values)
	return render_template('index.html',scores=get_high_scores())

@app.template_filter('ordinal')
def ordinal_filter(i):
    return ordinal(i)

if __name__ == '__main__':
	if os.environ.get('PORT'):
		app.run(host='0.0.0.0',port=int(os.environ.get('PORT')),debug=False)
	else:
		app.run(host='0.0.0.0',port=5000,debug=True)

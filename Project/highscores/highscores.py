#!/usr/bin/env python

from flask import Flask, Response, session, redirect, url_for, escape, request, render_template, g, flash, make_response
from functions import *
from bson.objectid import ObjectId
import time,urllib2,json

app = Flask(__name__)
app.secret_key = os.environ['sk']
    
@app.route('/')
def index():
	if g.userid:
		if g.need_to_gather:
			flash("Please complete your profile before continuing.")
			return redirect(url_for('user_settings'))
		else:
			now_appts = get_appointment_now(g.userid)
			if now_appts and g.type != "admin":
				return redirect(url_for('edit_appointment',appointmentid=str(now_appts[0]),now="true"))
			else:	
				return redirect(url_for('list_appointments'))
	else:
		return render_template('login.html')


if __name__ == '__main__':
	if os.environ.get('PORT'):
		app.run(host='0.0.0.0',port=int(os.environ.get('PORT')),debug=False)
	else:
		app.run(host='0.0.0.0',port=5000,debug=True)

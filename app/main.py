import time
import os.path
from os import path
from copy import deepcopy
import copy
import mysql.connector
from mysql.connector import Error
from datetime import date

from flask import Flask
from flask import Response
from flask import send_file
import json
import string

app = Flask(__name__)
config = {
	'user': 'root',
	'password': 'root',
	'host': 'db',
	'port': 3306,
	'database' : 'platform'
}

def call_proc(procName, parameters = None) :
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()

	if not parameters is None :
		cursor.callproc(procName, parameters)
	else :
		cursor.callproc(procName)

	for result in cursor.stored_results() :
		result = result.fetchall()
		cursor.close()
		connection.close()
		return result

@app.route('/get_user/<string:userName>/<string:password>', methods = ['GET'])
def get_user(userName, password) :
	result = call_proc('get_user', (userName, password))

	return json.dumps({'user' : result})

@app.route('/sign_up/<string:userName>/<string:email>/<string:password>', methods = ['POST'])
def sign_up(userName, email, password) :
	result = call_proc('insert_user', (userName, email, password))
	print(result)

	if len(result) == 1 :
		if result[0][0] == 1 :
			return "OK"

	return "NOT OK"

@app.route('/check', methods = ['GET'])
def check() :
	return "Asta merge"

if __name__ == "__main__" :
	app.run(host="0.0.0.0")
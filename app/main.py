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
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
config = {
	'user': 'root',
	'password': 'root',
	'host': 'db',
	'port': 3306,
	'database' : 'platform'
}

metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.3')

#docker service create --replicas 1 --network testapp_webnet --name metrics --mount type=bind,source=`pwd`/prometheus-testapp.yml,destination=/etc/prometheus/prometheus.yml --publish 9090:9090 prom/prometheus

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

@app.route('/genres', methods = ['GET'])
def init_genres() :
	paths = call_proc('get_genres')

	return json.dumps({'genres' : paths})

@app.route('/get_characters/<string:seriesId>', methods = ['GET'])
def get_characters(seriesId) :
	result = call_proc('get_characters', (seriesId, ))

	return json.dumps({'characters' : result})

@app.route('/get_comm_rate', methods = ['GET'])
def get_comments_rate() :
	result = call_proc('get_commentsRate')

	return json.dumps({'comms' : result})

@app.route('/get_most_stories', methods = ['GET'])
def init_most_stories() :
	result = call_proc('get_mostStories')

	return json.dumps({'series' : result})

@app.route('/get_most_stories_by_ch', methods = ['GET'])
def get_most_stories_by_chapters() :
	result = call_proc('get_mostStoriesByCh')

	return json.dumps({'stories' : result})

@app.route('/get_stories_nr_by_user', methods = ['GET'])
def get_stories_nr_by_users() :
	result = call_proc('get_StoriesNoByUser')

	return json.dumps({'users' : result})

@app.route('/get_comms_nr_by_user', methods = ['GET'])
def get_comments_nr_by_users() :
	result = call_proc('get_CommentsNoByUser')

	return json.dumps({'users' : result})

@app.route('/get_all_series', methods = ['GET'])
def all_series() :
	result = call_proc('get_allSeries')

	return json.dumps({'series' : result})

@app.route('/get_by_genre/<string:genreName>', methods = ['GET'])
def series_by_genre(genreName) :
	result = call_proc('get_seriesByGenre', (genreName, ))
	print(result)
	return json.dumps({'series' : result})

@app.route('/get_stories/<string:userName>/<string:seriesId>', methods = ['GET'])
def stories_of_series(userName, seriesId) :
	if seriesId == "No series" :
		seriesId = None
	if userName == "No user" :
		userName = None

	result = call_proc('get_storiesss', (seriesId, userName))

	return json.dumps({'stories' : result})

@app.route('/get_chapters/<string:storyId>', methods = ['GET'])
def chapters_of_story(storyId) :
	result = call_proc('get_chapters', (storyId, ))

	return json.dumps({'chapters' : result})

@app.route('/get_chapter/<string:chapterId>', methods = ['GET'])
def chapter(chapterId) :
	file_name = call_proc('get_chapter', (chapterId, ))
	file_name = file_name[0][0]

	return send_file(file_name)

@app.route('/get_comments/<string:storyId>', methods = ['GET'])
def comments_of_story(storyId) :
	result = call_proc('get_comments', (storyId, ))

	for i in range(len(result)) :
		date = result[i][2]
		new_result = (result[i][0], result[i][1], str(date), result[i][3])
		result[i] = new_result

	return json.dumps({'comments' : result})

@app.route('/get_user/<string:userName>/<string:password>', methods = ['GET'])
def get_user(userName, password) :
	result = call_proc('get_user', (userName, password))

	return json.dumps({'user' : result})

@app.route('/sign_up/<string:userName>/<string:email>/<string:password>', methods = ['POST'])
def sign_up(userName, email, password) :
	result = call_proc('insert_user', (userName, email, password))

	if len(result) == 1 :
		if result[0][0] == 1 :
			return "OK"

	return "NOT OK"

@app.route('/insert_genre/<string:gen_name>/<string:img_path>', methods = ['POST'])
def ins_gen(gen_name, img_path) :
	result = call_proc('insert_genre', (gen_name, "./poze/genresPictures/" + img_path))

	if len(result) == 1 :
		if result[0][0] == 1 :
			return "OK"

	return "NOT OK"

@app.route('/insert_series/<string:s_name>/<string:descr>/<string:img_path>/<string:gen_name>/<int:eps>', methods = ['POST'])
def ins_ser(s_name, descr, img_path, gen_name, eps) :
	result = call_proc('insert_series', (s_name, descr, "./poze/seriesPictures/" + img_path, gen_name, eps))

	if len(result) == 1 :
		if result[0][0] == 1 :
			return "OK"

	return "NOT OK"

@app.route('/insert_story/<string:title>/<string:description>/<int:series>/<string:user>/<string:characterName>', methods = ['POST'])
def insert_story(title, description, series, user, characterName) :
	if characterName == "-1" :
		characterName = None

	if description == "No description" :
		description = None

	result = call_proc('insert_story', (title, description, series, user, characterName))

	if len(result) == 1 :
		if result[0][0] != 0 :
			return str(result[0][0])

	return "NOT OK"

@app.route('/delete_story/<string:storyId>', methods = ['DELETE'])
def delete_story(storyId) :
	result = call_proc('delete_story', (storyId,))

	return "OK"

@app.route('/insert_chapter/<string:title>/<string:storyName>/<int:storyId>/<string:chapterContent>/<string:gen>', methods = ['POST'])
def insert_chapter(title, storyName, storyId, chapterContent, gen) :
	no_chapters = call_proc('get_number_of_chapters', (storyName,))
	no_chapters = no_chapters[0][0]
	no_chapters = no_chapters + 1

	file_name = '/chapters/' +  storyName.lower().replace(" ", "") + "_" + str(no_chapters) + ".txt"
	f = open(file_name, "a")
	f.write(chapterContent)
	f.close()

	if gen == "No genre" :
		genId = None

	result = call_proc('insert_chapter', (title, file_name, storyId, gen))

	return "OK"

@app.route('/add_comment/<string:comment>/<int:rating>/<string:userName>/<int:storyId>', methods = ['POST'])
def insert_comments(comment, rating, userName, storyId) :
	date_today = str(date.today())

	result = call_proc('insert_comments', (comment, rating, userName, storyId, date_today))

	return "OK"

if __name__ == "__main__" :
	#app.run(host="192.168.0.5")
	app.run(host="0.0.0.0")

import time
import os.path
from os import path
from copy import deepcopy
import copy
import tkinter as tk
from PIL import ImageTk, Image

import http.client
import json
import copy
from tkinter import ttk
from functools import partial
import urllib.parse
import urllib.request
import io
import requests
import base64
import time
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import subprocess

#connection = http.client.HTTPConnection('127.0.0.1', 5000)
#connection = http.client.HTTPConnection('192.168.0.5', 5000)
connection = http.client.HTTPConnection("0.0.0.0", 5000)

WIDTH = 1000
HEIGHT = 750
current_user = None
root = None

class StatsPage(tk.Frame) :
	canv = None

	def prop(self, n):
		return 360.0 * n

	def most_longer_stories(self, container) :
		if self.canv is not None :
			self.canv.destroy()

		colors = ["SkyBlue4", "cyan2", "DodgerBlue4"]

		query = "/get_most_stories_by_ch"
		connection.request("GET", urllib.parse.quote(query))
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		stories = json_response['stories']
		connection.close()

		self.canv = tk.Canvas(container, width=900, height=500)
		self.canv.pack(side = tk.TOP)
		self.canv.create_text(200, 50, anchor=tk.NW, text = "Most 3 longer stories by the number of chapters :", font = ("Verdana", 15, "italic"))
		k = 0

		len_stories = len(stories)
		count_sum = sum([stories[i][4] for i in range(len_stories)])

		for i in range(len_stories) :
			p = stories[i][4] / count_sum
			st_text = stories[i][2] + " - \" " + stories[i][1] + " \" BY : " + stories[i][3]
			self.canv.create_rectangle(150, 90 + i * 70, 600 + p * 250, 140 + i * 70, fill=colors[i], outline=colors[i])
			self.canv.create_text(170, 102 + i * 70, anchor=tk.NW, text = st_text, font = ("Verdana", 10, "bold"))
			self.canv.create_text(600 + p * 250 + 25, 96 + i * 70, anchor=tk.NW, text = stories[i][4], font = ("Verdana", 15, "bold"))

	def popular_series(self, container) :
		if self.canv is not None :
			self.canv.destroy()

		colors = ["SkyBlue4", "cyan2", "DodgerBlue4"]

		query = "/get_most_stories"
		connection.request("GET", urllib.parse.quote(query))
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		series = json_response['series']
		connection.close()

#(series_id, series_name, series_desc, series_img, st_count)
		self.canv = tk.Canvas(container, width=900, height=500)
		self.canv.pack(side = tk.TOP)
		self.canv.create_text(15, 15, anchor=tk.NW, text = "Most 3 popular series by the number of related stories :", font = ("Verdana", 15, "italic"))
		k = 0

		len_series = len(series)
		count_sum = sum([series[i][4] for i in range(len_series)])

		for i in range(len_series) :
			p = series[i][4] / count_sum
			self.canv.create_arc((65,65,485,485), fill=colors[i], outline=colors[i], start=self.prop(k), extent = self.prop(p))
			k += p
			self.canv.create_rectangle(600, 55 + i * 30, 850, 75 + i * 30, fill=colors[i], outline=colors[i])
			self.canv.create_text(620, 57 + i * 30, anchor=tk.NW, text = series[i][1], font = ("Verdana", 10, "bold"))

	def get_comm_nr(self, user_name, users_c, l) :
		for i in range(l) :
			if users_c[i][0] == user_name :
				return users_c[i][1]
		return 0

	def users_activity(self, container) :
		if self.canv is not None :
			self.canv.destroy()

		colors = ["DeepSkyBlue3", "bisque3", "thistle"]

		query = "/get_stories_nr_by_user"
		connection.request("GET", urllib.parse.quote(query))
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		users_s = json_response['users']
		connection.close()

		query = "/get_comms_nr_by_user"
		connection.request("GET", urllib.parse.quote(query))
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		users_c = json_response['users']
		connection.close()

		self.canv = tk.Canvas(container, width=900, height=500)
		self.canv.pack(side = tk.TOP)
		self.canv.create_text(150, 50, anchor=tk.NW, text = "Number of written stories and comments of each user :", font = ("Verdana", 15, "italic"))
		len_users = len(users_s)

		for i in range(len_users) :
			self.canv.create_rectangle(200 + i * 135, 450 - users_s[i][1] * 83, 245 + i * 135, 465, fill=colors[0], outline=colors[0])
			self.canv.create_rectangle(255 + i * 135, 450 - self.get_comm_nr(users_s[i][0], users_c, len_users) * 83, 300 + i * 130, 465, fill=colors[1], outline=colors[1])

			self.canv.create_text(200 + i * 135, 425 - users_s[i][1] * 83, anchor=tk.NW, text = users_s[i][1], font = ("Verdana", 15, "bold"))
			self.canv.create_text(255 + i * 135, 425 - self.get_comm_nr(users_s[i][0], users_c, len_users) * 83, anchor=tk.NW, text = self.get_comm_nr(users_s[i][0], users_c, len_users), font = ("Verdana", 15, "bold"))
			self.canv.create_text(195 + i * 135, 475, anchor=tk.NW, text = users_s[i][0], font = ("Verdana", 10, "bold"))

		self.canv.create_rectangle(700, 150, 850, 170, fill=colors[0], outline=colors[0])
		self.canv.create_rectangle(700, 175, 850, 195, fill=colors[1], outline=colors[1])
		self.canv.create_text(710, 152, anchor=tk.NW, text = "stories", font = ("Verdana", 11))
		self.canv.create_text(710, 177, anchor=tk.NW, text = "comments", font = ("Verdana", 11))

	def __init__(self, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		back = tk.Button(self, text = "BACK", command = self.destroy)
		back.pack()
		buttonframe = tk.Frame(self, height = 5, width =WIDTH)
		buttonframe.pack(side = tk.TOP, fill="both", expand=False)
		graphsframe = tk.Frame(self, height = 700, width = WIDTH)
		graphsframe.pack(fill="both", expand=False)

		button1 = tk.Button(buttonframe, text = "MOST LONGER STORIES", command = partial(self.most_longer_stories, graphsframe), font = ("Verdana", 15, "bold"), fg = 'pink4', height=2, width=22, anchor = tk.CENTER)
		button1.configure(activebackground = "#33B5E5", relief = tk.FLAT)
		button1.grid(row=0, column=0)

		button2 = tk.Button(buttonframe, text = "POPULAR SERIES", command = partial(self.popular_series, graphsframe), font = ("Verdana", 15, "bold"), fg = 'pink4', height=2, width=22, anchor = tk.CENTER)
		button2.configure(activebackground = "#33B5E5", relief = tk.FLAT)
		button2.grid(row=0, column=1)

		button3 = tk.Button(buttonframe, text = "USERS ACTIVITY", command = partial(self.users_activity, graphsframe), font = ("Verdana", 15, "bold"), fg = 'pink4', height=2, width=22, anchor = tk.CENTER)
		button3.configure(activebackground = "#33B5E5", relief = tk.FLAT)
		button3.grid(row=0, column=2)

		self.most_longer_stories(graphsframe)

class AddGenrePage(tk.Frame) :
	error_message = None

	def add_genre(self, entries) :
		if self.error_message is not None :
			self.error_message.destroy()
		name = entries[0].get()
		i_path = entries[1].get()

		if name != "" and i_path != "" :
			query = "/insert_genre/" + name + "/" + i_path
			connection.request("POST", urllib.parse.quote(query))
			response = connection.getresponse().read().decode()

			connection.close()

			if response == "OK" :
				self.error_message = tk.Label(self, text = "New genre succesfully added!", anchor = tk.NW)
				self.error_message.pack()
			else :
				self.error_message = tk.Label(self, text = "Genre with given name already exists!", anchor = tk.NW)
				self.error_message.pack()

	def __init__(self, genres, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		back = tk.Button(self, text = "BACK", command = self.destroy)
		back.pack()

		name_f = tk.Frame(self)
		name_f.pack()
		path_f = tk.Frame(self)
		path_f.pack()

		frames = [name_f, path_f]
		texts = ["GENRE", "IMAGE"]
		verify_string = [tk.StringVar() for i in range(2)]

		labels = []
		entries = []
		for i in range(2) :
			labels.append(tk.Label(frames[i], text = texts[i]))
			entries.append(tk.Entry(frames[i], textvariable = verify_string[i]))
			labels[i].pack(side = tk.LEFT, fill = "both")
			entries[i].pack(side = tk.RIGHT, fill = "both")

		login = tk.Button(self, text = "ADD GENRE", anchor = tk.NW, command = partial(self.add_genre, entries))
		login.pack()

class AddSeriesPage(tk.Frame) :
	error_message = None

	def add_series(self, entries) :
		if self.error_message is not None :
			self.error_message.destroy()
		name = entries[0].get()
		descr = entries[1].get()
		i_path = entries[2].get()
		gen = entries[3].get()
		eps = entries[4].get()

		if name != "" and i_path != "" and descr != "" and gen != "" and eps != "" :
			query = "/insert_series/" + name + "/" + descr + "/" + i_path + "/" + gen + "/" + eps
			connection.request("POST", urllib.parse.quote(query))
			response = connection.getresponse().read().decode()

			connection.close()

			if response == "OK" :
				self.error_message = tk.Label(self, text = "New series succesfully added!", anchor = tk.NW)
				self.error_message.pack()
			else :
				self.error_message = tk.Label(self, text = "Series with given name already exists or given genre doesn't exists!", anchor = tk.NW)
				self.error_message.pack()

	def __init__(self, genres, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		back = tk.Button(self, text = "BACK", command = self.destroy)
		back.pack()

		name_f = tk.Frame(self)
		name_f.pack()
		descr_f = tk.Frame(self)
		descr_f.pack()
		path_f = tk.Frame(self)
		path_f.pack()
		gen_f = tk.Frame(self)
		gen_f.pack()
		eps_f = tk.Frame(self)
		eps_f.pack()

		frames = [name_f, descr_f, path_f, gen_f, eps_f]
		texts = ["NAME", "DESCRIPTION", "IMAGE", "GENRE", "EPISODES"]
		verify_string = [tk.StringVar() for i in range(5)]

		labels = []
		entries = []
		for i in range(5) :
			labels.append(tk.Label(frames[i], text = texts[i]))
			entries.append(tk.Entry(frames[i], textvariable = verify_string[i]))
			labels[i].pack(side = tk.LEFT, fill = "both")
			entries[i].pack(side = tk.RIGHT, fill = "both")

		login = tk.Button(self, text = "ADD GENRE", anchor = tk.NW, command = partial(self.add_series, entries))
		login.pack()

class InsertOptPage(tk.Frame) :
	def go_to_gen_page(self, container, parent) :
		page = AddGenrePage(parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def go_to_ser_options(self, container, parent) :
		page = AddSeriesPage(parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def __init__(self, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		back = tk.Button(self, text = "BACK", command = self.destroy)
		back.pack()
		buttons = tk.Frame(self)
		#buttons.pack()
		buttons.place(x=0, y=200, width=1000, height=700)
		gen_frame = tk.Frame(buttons)
		gen_frame.pack()
		ser_frame = tk.Frame(buttons)
		ser_frame.pack()

		gen_but = tk.Button(gen_frame, anchor=tk.CENTER, text="ADD NEW MOVIE GENRE", command = partial(self.go_to_gen_page, self, self), font = ("Verdana", 20, "bold"), fg = 'pink4', bg = 'bisque', height=4, width=25)
		gen_but.pack()
		ser_but = tk.Button(gen_frame, anchor=tk.CENTER, text="ADD NEW SERIES", command = partial(self.go_to_ser_options, self, self), font = ("Verdana", 20, "bold"), fg = 'pink4', bg = 'bisque', height=4, width=25)
		ser_but.pack()

class MainPage(tk.Frame) :
	def go_to_stats_page(self, container, parent) :
		page = StatsPage(parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def go_to_insert_options(self, container, parent) :
		page = InsertOptPage(parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def __init__(self, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		stats_frame = tk.Frame(self)
		stats_frame.pack(side = tk.LEFT)
		new_in_frame = tk.Frame(self)
		new_in_frame.pack(side = tk.RIGHT)

		stats_but = tk.Button(stats_frame, text="VIEW APP STATISTICS", command = partial(self.go_to_stats_page, self, self), font = ("Verdana", 25, "bold"), fg = 'pink4', height=5, width=20)
		stats_but.pack()
		new_in_but = tk.Button(new_in_frame, text="INSERT NEW OPTIONS", command = partial(self.go_to_insert_options, self, self), font = ("Verdana", 25, "bold"), fg = 'pink4', height=5, width=20)
		new_in_but.pack()

class MainView(tk.Frame) :
	error_message = None

	def init_page(self, user_e, pass_e, parent, container) :
		global current_user
		if self.error_message is not None :
			self.error_message.destroy()
		user_name = user_e.get()
		password = pass_e.get()

		if user_name != "" and password != "" :
			query = "/get_user/" + user_name + "/" + password
			connection.request("GET", urllib.parse.quote(query))
			response = connection.getresponse()
			json_response = json.loads(response.read().decode())
			user = json_response['user']
			connection.close()

			if len(user) > 0 :
				current_user = (user_name, user[0][0], user[0][1])
				if user[0][1] == 'ADMIN' :
					page = MainPage(parent)
					page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
					page.lift
				else :
					self.error_message = tk.Label(self, text = "You are not ADMIN!", anchor = tk.NW)
					self.error_message.pack()
			else :
				self.error_message = tk.Label(self, text = "Username or password incorrect!", anchor = tk.NW)
				self.error_message.pack()

	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		admin_req = tk.Label(self, text = "Please enter your credentials if you have ADMIN privilegies")
		admin_req.pack()

		usef_f = tk.Frame(self)
		usef_f.pack()
		pass_f = tk.Frame(self)
		pass_f.pack()

		username_verify = tk.StringVar()
		password_verify = tk.StringVar()

		user_l = tk.Label(usef_f, text = "USERNAME")
		user_e = tk.Entry(usef_f, textvariable=username_verify)
		user_l.pack(side = tk.LEFT, fill = "both")
		user_e.pack(side = tk.RIGHT, fill = "both")
		pass_l = tk.Label(pass_f, text = "PASSWORD")
		pass_e = tk.Entry(pass_f, textvariable=password_verify, show= '*')
		pass_l.pack(side = tk.LEFT, fill = "both")
		pass_e.pack(side = tk.RIGHT, fill = "both")

		login = tk.Button(self, text = "LOGIN", anchor = tk.CENTER, command = partial(self.init_page, user_e, pass_e, self, self))
		login.pack()

def init() :
	global root
	time.sleep(20)
	root = tk.Tk()
	root.geometry(str(WIDTH) + 'x' + str(HEIGHT) + "+0+0")
	main = MainView(root)
	main.pack(side="top", fill="both", expand=True)
	root.mainloop()

if __name__ == "__main__" :
	init()
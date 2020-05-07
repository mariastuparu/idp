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

root = None

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

#connection = http.client.HTTPConnection('192.168.0.5', 5000)
#connection = http.client.HTTPConnection('127.0.0.1', 5000)
connection = http.client.HTTPConnection("0.0.0.0", 5000)

WIDTH = 1000
HEIGHT = 1000
p_all = None
p_genres = []
current_user = None
current_pass = None

def mockup_f() :
	print("ceva")

def get_resize_path(img_path, min_size) :
	splitPath = img_path.split(".")
	copy_file = splitPath[0] + "_copy_" + str(min_size) + "." + splitPath[1]
	size = min_size, min_size

	if not path.exists(copy_file) :
		img = Image.open(img_path)
		img = img.resize(size, Image.ANTIALIAS)
		img.save(copy_file)

	return copy_file

class CommentsPage(tk.Frame):
	storyId = None
	add_comment = None

	def add(self, rate_e, comment) :
		global connection

		comm_text = comment.get("1.0", 'end-1c')
		rating = rate_e.get()

		if comm_text != "" and rating != "" and rating.isdigit() :
			if int(rating) >= 1 and int(rating) <= 100 :
				query = "/add_comment/" + comm_text + "/" + rating + "/" + current_user[0] + "/" + str(self.storyId)
				connection.request("POST", urllib.parse.quote(query))
				connection.close()
				page = CommentsPage(self.storyId, self)
				page.place(in_= self, x=0, y=0, relwidth=1, relheight=1)
				page.lift
				self.destroy()

	def add_new_comment(self, container) :
		self.add_comment.destroy()
		rate = tk.Frame(container)
		rate.pack(fill = "both")
		rate_text = tk.Label(rate, text = "Rating : (1 - 100)")
		rate_text.pack(side = tk.LEFT, fill = "both", expand = True)
		rate_e = tk.Entry(rate)
		rate_e.pack(side = tk.RIGHT, fill = "both", expand = True)
		comment = tk.Text(container, height = 4)
		comment.pack()

		add_comm = tk.Button(container, text = "ADD COMMENT", command = partial(self.add, rate_e, comment))
		add_comm.pack()

	def __init__(self, storyId, *args, **kwargs):
		global connection
		self.storyId = storyId
		query = "/get_comments/" + str(storyId)
		connection.request("GET", urllib.parse.quote(query))

		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		comments = json_response['comments']
		connection.close()
		
		tk.Frame.__init__(self, *args, **kwargs)
		back_frame = tk.Frame(self)
		back_frame.pack(fill = "both")
		add_frame = tk.Frame(self)
		add_frame.pack(fill = "both")

		back_button = tk.Button(back_frame, text = "Back to story", command = self.destroy)
		back_button.pack(side = tk.LEFT)
		if current_user is not None :
			self.add_comment = tk.Button(back_frame, text = "Add new comment", command = partial(self.add_new_comment, add_frame))
			self.add_comment.pack(side = tk.RIGHT)

		commsFrame = ScrollableFrame(self)
		commsFrame.pack(fill = "both", expand = True)

		comm_height = 0
		if len(comments) > 0 :
			comm_height = int(500 / len(comments))

		for comm in comments :
			(commentText, rating, postDate, userName) = comm

			canvas = tk.Canvas(commsFrame.scrollable_frame, height = comm_height)
			canvas.pack(fill = "both")

			head_frame = tk.Frame(canvas)
			comm_frame = tk.Frame(canvas)

			head_frame.pack(side = "top", fill = "both", expand = True)
			comm_frame.pack(side = "bottom", fill = "both", expand = True)

			user = tk.Label(head_frame, text = userName, anchor = tk.NW, font = ("Verdana", 10, "bold"))
			date = tk.Label(head_frame, text = postDate, anchor = tk.NW, font = ("Verdana", 10, "italic"))
			rate = tk.Label(head_frame, text = rating, anchor = tk.NW, font = ("Verdana", 10, ), fg = "orange3")

			user.grid(row = 0, column = 0)
			date.grid(row = 0, column = 1)
			rate.grid(row = 0, column = 2)

			comment = tk.Text(comm_frame, height = 4)
			comment.insert(tk.END, commentText)
			comment.pack(fill = "both", expand = "True")

class OneStoryPage(tk.Frame) :
	ch = None
	current_ch = 0
	buttons = []
	chapters = []
	prev_no = "1"
	star = None

	def add_chapter(self, parent, container, storyId, storyTitle) :
		page = AddChapterPage(storyTitle, storyId, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def comm_page(self, parent, container, storyId) :
		page = CommentsPage(storyId, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def change_state(self, n, state) :
		for i in range(2) :
			self.buttons[i + n].configure(state = state)

	def to_first(self, chapterframe) :
		self.current_ch = 0
		self.change_state(0, tk.DISABLED)
		self.change_state(2, tk.NORMAL)

		self.show_chapter(chapterframe)

	def move_back(self, chapterframe) :
		self.current_ch -= 1

		if self.current_ch == 0 :
			self.change_state(0, tk.DISABLED)
		self.change_state(2, tk.NORMAL)

		self.show_chapter(chapterframe)

	def move_fwd(self, chapterframe) :
		self.current_ch += 1

		if self.current_ch == len(self.chapters) - 1 :
			self.change_state(2, tk.DISABLED)
		self.change_state(0, tk.NORMAL)

		self.show_chapter(chapterframe)

	def to_last(self, chapterframe) :
		self.current_ch = len(self.chapters) - 1
		self.change_state(2, tk.DISABLED)
		self.change_state(0, tk.NORMAL)

		self.show_chapter(chapterframe)

	def check_chapter(self, entry_chapter, chapterframe) :
		chapters_len = len(self.chapters)
		chapter_no = entry_chapter.get()

		if chapter_no.isdigit() :
			chapter_no = int(chapter_no)
		else :
			chapter_no = 0

		if chapter_no > 0 and chapter_no <= chapters_len :
			self.prev_no = str(chapter_no)
			self.current_ch = chapter_no - 1

			if self.current_ch > 0 :
				self.change_state(0, tk.NORMAL)
			else :
				self.change_state(0, tk.DISABLED)

			if self.current_ch < len(self.chapters) - 1 :
				self.change_state(2, tk.NORMAL)
			else :
				self.change_state(2, tk.DISABLED)

			self.show_chapter(chapterframe)

		else :
			entry_chapter.delete(0, 20)
			entry_chapter.insert(0, self.prev_no)

	def __init__(self, storyId, storyTitle, grade, story_user_name, *args, **kwargs):
		global connection
		query = "/get_chapters/" + str(storyId)
		connection.request("GET", urllib.parse.quote(query))

		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		self.chapters = json_response['chapters']
		chapters_len = len(self.chapters)

		self.current_ch = 0
		
		tk.Frame.__init__(self, *args, **kwargs)
		
		up_canvas_h = 150
		main_canvas = tk.Canvas(self)
		main_canvas.pack(side = "right", fill = "both", expand = True)
		up_canvas = tk.Canvas(main_canvas, height = up_canvas_h)
		down_canvas = tk.Canvas(main_canvas, height = HEIGHT - up_canvas_h - 50)
		chapterframe = ScrollableFrame(down_canvas, height = HEIGHT - up_canvas_h - 50)
		up_canvas.pack(side = tk.TOP, fill = "both", expand = True)
		down_canvas.pack(side = tk.BOTTOM, fill = "both", expand = True)

		chapterframe.pack(side = tk.TOP, fill = "both", expand = True)

		# Buttons for chapters :
		
		back_and_add = tk.Frame(up_canvas)
		back_and_add.pack()
		back_button = tk.Button(back_and_add, text = "BACK", command = self.destroy)

		if current_user is not None and current_user[0] == story_user_name :
			add_chapter_button = tk.Button(back_and_add, text = "ADD NEW CHAPTER", command = partial(self.add_chapter, self, self, storyId, storyTitle))
			add_chapter_button.pack(side = tk.RIGHT)

		print_story = tk.Button(up_canvas, text = "Print", anchor = tk.NW)
		print_story.pack()
		choose_ch_canvas = tk.Canvas(up_canvas, height = 40)
		buttons_canvas = tk.Canvas(up_canvas, height = up_canvas_h - 40 - 30)
		story_title = tk.Label(up_canvas, text = "Story : " + storyTitle, font = ("Verdana", 13, "italic"), fg = "LightSkyBlue3")
		rating_canvas = tk.Canvas(up_canvas, height = 50)
		from_user = tk.Label(up_canvas, text = "From : " + story_user_name, font = ("Verdana", 10, "italic"), fg = "LightSkyBlue4")

		back_button.pack(side = tk.LEFT)
		choose_ch_canvas.pack(fill = "both", expand = True)
		buttons_canvas.pack(fill = "both")
		story_title.pack(fill = "both")

		star_path = 'D:\\Facultate\\Anul4I\\BD2\\Proiect'
		#rating_star = get_resize_path(star_path + '\\ratingStar.png', 50)
		rating_star = star_path
		self.star = tk.PhotoImage(rating_star)

		stars_buttons = []
		if chapters_len > 0 :
			for i in range(grade) :
				stars_buttons.append(tk.Button(rating_canvas, image = self.star, state = tk.DISABLED, anchor = tk.NW, relief = tk.FLAT))

		rating_canvas.pack(expand = True)
		from_user.pack(fill = "both")

		for i in range(grade) :
			stars_buttons[i].grid(row = 0, column = i)

		insert_label = tk.Label(choose_ch_canvas, text = "Chapter :")
		insert_label.grid(row = 0, column = 0)

		self.prev_no = "1"
		entry_chapter = tk.Entry(choose_ch_canvas)
		entry_chapter.insert(0, "1")
		entry_chapter.grid(row = 0, column = 1)

		find_button = tk.Button(choose_ch_canvas, text = "FIND", command = partial(self.check_chapter, entry_chapter, chapterframe))
		find_button.grid(row = 0, column = 2)
		self.buttons = []
		texts = ["FIRST CHAPTER", "<-", "->", "CHAPTER " + str(chapters_len)]
		commands = [self.to_first, self.move_back, self.move_fwd, self.to_last]

		for i in range(4) :
			button = tk.Button(buttons_canvas, text=texts[i], anchor = tk.NW, command = partial(commands[i], chapterframe), relief = tk.FLAT)
			self.buttons.append(button)

		n = 2
		if chapters_len < 2 :
			n += 2

		for i in range(n) :
			self.buttons[i].configure(state = tk.DISABLED)

		for i in range(4) :
			self.buttons[i].place(relx = 0.45 + i * 0.094, rely = 0.5, anchor = tk.CENTER)

		# Content :
		self.show_chapter(chapterframe)

		# Comments :
		view_comments = tk.Button(down_canvas, text = "View comments", anchor = tk.NW, command = partial(self.comm_page, down_canvas, down_canvas, storyId), height = 50)
		view_comments.pack(side = tk.BOTTOM, fill = "both", expand = True)

	def show_chapter(self, chapterframe) :
		global connection
		
		if len(self.chapters) > 0 :		
			query = "/get_chapter/" + str(self.chapters[self.current_ch][0])
			connection.request("GET", urllib.parse.quote(query))

			ch_response = connection.getresponse()
			chapter_text = ch_response.read().decode()

			if self.ch is not None :
				self.ch.pack_forget()

			self.ch = tk.Text(chapterframe.scrollable_frame)
			self.ch.configure(font = ("Verdana", 11))
			self.ch.pack(fill = "both", expand = True)
			chapter_title = "~~~  " + self.chapters[self.current_ch][1] + "  ~~~"
			self.ch.insert(tk.END, chapter_title + "\n\n")
			self.ch.insert(tk.END, chapter_text)

			self.ch.tag_configure("title_tag", font = ("Verdana", 13, "bold"), foreground = 'SlateBlue4')
			self.ch.tag_add("title_tag", "1.0", "1." + str(len(chapter_title)))

class StoriesPage(tk.Frame) :
	story_p = []
	sId = None
	uName = None

	def add_chapter(self, container, parent, storyName, storyId) :
		page = AddChapterPage(storyName, storyId, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def delete_no(self, popup) :
		popup.destroy()

	def delete_yes(self, popup, storyId, container, parent) :
		global connection

		query = "/delete_story/" + str(storyId)
		connection.request("DELETE", urllib.parse.quote(query))
		response = connection.getresponse()
		connection.close()

		delete_ok = tk.Label(popup, text = "Story succesfully deleted!")
		time.sleep(2)
		popup.destroy()
		page = StoriesPage(self.sId, self.uName, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift
		self.destroy()

	def delete_st(self, parent, container, storyId) :
		popup = tk.Tk()
		popup.geometry('300x300')
		check = tk.Label(popup, text = "\n\n\nAre you sure you want to delete this story?", fg = "red")
		check.pack(fill = "both", expand = True)

		buttons = tk.Frame(popup)
		buttons.pack()
		yes = tk.Button(buttons, text = "YES", anchor = tk.NW, command = partial(self.delete_yes, popup, storyId, container, parent))
		yes.pack(side = tk.LEFT, fill = "both")
		no = tk.Button(buttons, text = "NO", anchor = tk.NW, command = partial(self.delete_no, popup))
		no.pack(side = tk.RIGHT, fill = "both")
		popup.mainloop()

	def init_page(self, parent, container, storyId, storyTitle, grade, story_user_name) :
		page = OneStoryPage(storyId, storyTitle, grade, story_user_name, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def __init__(self, seriesId, userName, *args, **kwargs):
		global connection

		self.sId = seriesId
		self.uName = userName

		query = "/get_stories/"
		if seriesId is not None :
			query = query + "No user" + "/" + str(seriesId)
		else :
			query = query + userName + "/" + "No series"
		connection.request("GET", urllib.parse.quote(query))
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		series = json_response['stories']
		connection.close()
		
		tk.Frame.__init__(self, *args, **kwargs)
		back_button = tk.Button(self, text = "BACK", command = self.destroy)
		back_button.pack()

		buttonsframe = ScrollableFrame(self)
		buttonsframe.place(x = 150, y = 150, height = 550, width = 550)

		i = 1
		labels = []
		self.story_p = []

		for line in series :
			(storyId, storyTitle, storyDescription, grade, no_comments, seriesName, characterId, story_user_name) = line
			if grade is None :
				grade = 0

			canvas = tk.Canvas(buttonsframe.scrollable_frame, height = 200, width = 550)
			canvas.pack(fill = "both")

			button = tk.Button(canvas, text=storyTitle, anchor = tk.NW, command = partial(self.init_page, self, self, storyId, storyTitle, grade, story_user_name), relief = tk.FLAT)
			button.configure(font = ("Verdana", 14, "bold"))
			button.pack()

			info_frame = tk.Frame(canvas)
			info_frame.pack()
			grade_l = tk.Label(info_frame, text = "Rating " + str(grade))
			no_comm_l = tk.Label(info_frame, text = str(no_comments) + " comments")
			grade_l.pack(side = tk.LEFT, fill = "both")
			no_comm_l.pack(side = tk.RIGHT, fill = "both")
			
			descFrame = ScrollableFrame(canvas)

			desc = tk.Text(descFrame.scrollable_frame, height = 5, width = 30)
			descFrame.pack()
			
			if storyDescription is not None :
				desc.insert(tk.END, storyDescription)
			desc.pack()

			if userName is not None :
				buttns = tk.Frame(canvas)
				buttns.pack()
				add_chapter_b = tk.Button(buttns, text = "Add next chapter", anchor = tk.NW, command = partial(self.add_chapter, self, self, storyTitle, storyId))
				add_chapter_b.pack(side = tk.LEFT, fill = "both")
				delete_story = tk.Button(buttns, text = "Delete this story", anchor = tk.NW, command = partial(self.delete_st, self, self, storyId))
				delete_story.pack(side = tk.RIGHT, fill = "both")
			
			i += 1

class AddChapterPage(tk.Frame):
	genres = None
	selected_genre = None
	content = None
	title_e = None
	add = None

	def get_genre(self, selection) :
		self.selected_genre = selection

	def get_genres(self) :
		global connection

		connection.request("GET", "/genres")
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		self.genres = json_response['genres']
		connection.close()

	def add_chapter(self, container, parent, storyId, storyName) :
		title = self.title_e.get()
		new_content = self.content.get("1.0", 'end-1c')

		if title != "" and new_content != "" :
			global connection

			if self.selected_genre is None :
				self.selected_genre = "No genre"

			query = "/insert_chapter/" + title + "/" + storyName + "/" + str(storyId) + "/" + new_content + "/" + self.selected_genre
			connection.request("POST", urllib.parse.quote(query))
			connection.close()
			self.add.destroy()
			ok = tk.Label(self, text = "New chapter succesfully added!", fg = 'green', font = ("Verdana", 13, "bold"))
			ok.pack()

	def __init__(self, storyName, storyId, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.get_genres()

		back_frame = tk.Frame(self)
		back_frame.pack(fill = "both")
		back_button = tk.Button(back_frame, text = "BACK", command = self.destroy)
		back_button.pack(side = tk.LEFT)

		head = tk.Label(self, text = "New chapter for " + storyName)
		head.configure(font = ("Verdana", 16, "bold"), fg = 'azure3')
		head.pack()
		title = tk.Frame(self)
		title.pack()
		genre = tk.Frame(self)
		genre.pack()

		title_l = tk.Label(title, text = "Chapter title")
		self.title_e = tk.Entry(title)
		title_l.pack(side = tk.LEFT, fill = "both")
		self.title_e.pack(side = tk.RIGHT, fill = "both")

		genvar = tk.StringVar(genre)
		genre_names = {self.genres[i][1] for i in range(len(self.genres))}
		genre_names.add("")
		genvar.set("")

		genre_l = tk.Label(genre, text = "Primary genre of this chapter")
		genre_e = tk.OptionMenu(genre, genvar, *genre_names, command = self.get_genre)
		genre_l.pack(side = tk.LEFT, fill = "both")
		genre_e.pack(side = tk.RIGHT, fill = "both")

		self.content = tk.Text(self)
		self.content.pack(fill = "both", expand = True)

		self.add = tk.Button(self, text = "ADD CHAPTER", anchor = tk.NW, command = partial(self.add_chapter, self, self, storyId, storyName))
		self.add.pack()

class AddStoryPage(tk.Frame):
	characters = []
	title_e = None
	description_e = None
	character_e = None
	characterName = None
	add = None

	def getCharacter(self, selection):
		print(selection)
		self.characterName = selection

	def add_new_chapter(self, container, parent, storyName, storyId) :
		page = AddChapterPage(storyName, storyId, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def add_story(self, container, parent, seriesId) :
		global connection
		title = self.title_e.get()
		description = self.description_e.get() if self.description_e.get() != "" else "No description"
		character = self.characterName if self.characterName != "" and self.characterName is not None else "-1"

		if title != "" :
			query = "/insert_story/" + title + "/" + description + "/" + str(seriesId) + "/" + current_user[0] + "/" + character
			connection.request("POST", urllib.parse.quote(query))
			response = connection.getresponse()
			connection.close()
			response = response.read().decode()

			if response != "NOT OK" :
				self.add.destroy()
				insert_ok = tk.Label(self, text = "Story succesfully inserted!")
				insert_ok.pack(fill = "both")
				add_chapter = tk.Button(self, text = "Add first chapter of the story", anchor = tk.NW, command = partial(self.add_new_chapter, self, self, title, str(response)))
				add_chapter.pack()
			else :
				self.error_message = tk.Label(self, text = "Inserted title already exists!", anchor = tk.NW)
				self.error_message.pack()


	def __init__(self, seriesName, seriesId, *args, **kwargs):
		global connection

		connection.request("GET", "/get_characters/" + str(seriesId))
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		self.characters = json_response['characters']
		connection.close()

		tk.Frame.__init__(self, *args, **kwargs)
		back_frame = tk.Frame(self)
		back_frame.pack(fill = "both")
		back_button = tk.Button(back_frame, text = "BACK", command = self.destroy)
		back_button.pack(side = tk.LEFT)

		head = tk.Label(self, text = "Story for " + seriesName)
		head.configure(font = ("Verdana", 16, "bold"), fg = 'azure3')
		head.pack()
		title = tk.Frame(self)
		title.pack()
		description = tk.Frame(self)
		description.pack()
		character = tk.Frame(self)
		character.pack()

		title_l = tk.Label(title, text = "Story title")
		self.title_e = tk.Entry(title)
		title_l.pack(side = tk.LEFT, fill = "both")
		self.title_e.pack(side = tk.RIGHT, fill = "both")
		description_l = tk.Label(description, text = "Story description")
		self.description_e = tk.Entry(description)
		description_l.pack(side = tk.LEFT, fill = "both")
		self.description_e.pack(side = tk.RIGHT, fill = "both")

		chvar = tk.StringVar(character)
		char_names = {self.characters[i][1] for i in range(len(self.characters))}
		char_names.add("")
		choose_character = tk.Frame(character)
		choose_character.pack()

		character_l = tk.Label(choose_character, text = "About character")
		self.character_e = tk.OptionMenu(choose_character, chvar, *char_names, command = self.getCharacter)
		chvar.set("")
		character_l.pack(side = tk.LEFT, fill = "both")
		self.character_e.pack(side = tk.RIGHT, fill = "both")

		self.add = tk.Button(self, text = "ADD STORY", anchor = tk.NW, command = partial(self.add_story, self, self, seriesId))
		self.add.pack()

class SeriesPage(tk.Frame):
	imggg = []

	def init_page(self, parent, container, seriesId) :
		page = StoriesPage(seriesId, None, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def add_new_story(self, parent, container, seriesName, seriesId) :
		page = AddStoryPage(seriesName, seriesId, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def __init__(self, genre, *args, **kwargs):
		self.imggg = []
		global connection

		if genre == "all" :
			connection.request("GET", "/get_all_series")
		elif genre == "most" :
			connection.request("GET", "/get_most_stories")
		else :
			query = "/get_by_genre/" + genre
			connection.request("GET", urllib.parse.quote(query))

		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		series = json_response['series']
		
		tk.Frame.__init__(self, *args, **kwargs)
		buttonsframe = ScrollableFrame(self)
		buttonsframe.place(x = 150, y = 150, height = 550, width = 550)

		buttons = []
		text_frames = []
			
		i = 1
		for line in series :
			(seriesId, seriesName, seriesDescription, seriesPicture, storiesCount) = line

			img = Image.open(seriesPicture)
			self.imggg.append(ImageTk.PhotoImage(img))

			canvas = tk.Canvas(buttonsframe.scrollable_frame, height = 200, width = 550)
			canvas.pack(fill = "both")

			button = tk.Button(canvas, image = self.imggg[i - 1], anchor = tk.NW, command = partial(self.init_page, self, self, seriesId))
			button.configure(width = 200, height = 200, activebackground = "#33B5E5", relief = tk.FLAT)
			buttons.append(button)

			text_frame = tk.Frame(canvas)
			name_label = tk.Label(text_frame, text=seriesName, anchor = tk.NW, font = ("Verdana", 14, "bold"), fg = 'ivory3')
			name_label.pack()

			desc_label = tk.Text(text_frame, font = ("Verdana", 10, 'italic'), fg = "SlateGray3", height = 5)
			desc_label.insert(tk.END, seriesDescription)
			desc_label.pack()
			if storiesCount is None :
				storiesCount = 0
			stories_no_text = str(storiesCount) + " stories" if storiesCount != 1 else str(storiesCount) + " story"
			stories_no = tk.Label(text_frame, text=stories_no_text, anchor = tk.NW)
			stories_no.pack(fill = "both", expand = True)
			if current_user is not None :
				add_story = tk.Button(text_frame, text = "Add a new story", anchor = tk.NW, command = partial(self.add_new_story, self, self, seriesName, seriesId))
				add_story.pack()
			text_frames.append(text_frame)
			i += 1

		for i in range(len(buttons)) :
			buttons[i].place(x = 0, y = 0, width = 200, height = 200)
			text_frames[i].place(x = 300, y = 0, width = 200, height = 200)

		buttonsframe.lift()

	def show(self):
		self.lift()

class LoginPage(tk.Frame) :
	error_message = None

	def go_to_signup(self, container, parent, genres) :
		page = SignUpPage(genres, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def init_page(self, user_e, pass_e, parent, container, genres) :
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
				page = MainView(genres, parent)
				page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
				page.lift
			else :
				self.error_message = tk.Label(self, text = "Username or password incorrect!", anchor = tk.NW)
				self.error_message.pack()

	def __init__(self, genres, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		to_signup = tk.Label(self, text = "Don't have an account?")
		to_signup.pack()
		signup = tk.Button(self, text = "SIGN UP", anchor = tk.NW, command = partial(self.go_to_signup, self, self, genres))
		signup.pack()

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

		login = tk.Button(self, text = "LOGIN", anchor = tk.NW, command = partial(self.init_page, user_e, pass_e, self, self, genres))
		login.pack()

		back = tk.Button(self, text = "BACK", command = self.destroy)
		back.pack()

class SignUpPage(tk.Frame) :
	error_message = None
	USER = 0
	EMAIL = 1
	PASSWORD = 2
	CONFIRM_PASSWORD = 3

	def init_page(self, entries, parent, container, genres) :
		global current_user
		if self.error_message is not None :
			self.error_message.destroy()
		user_name = entries[self.USER].get()
		email = entries[self.EMAIL].get()
		password = entries[self.PASSWORD].get()
		confirm_password = entries[self.CONFIRM_PASSWORD].get()

		if user_name != "" and email != "" and password != "" and confirm_password != "" :
			if password != confirm_password :
				self.error_message = tk.Label(self, text = "Inserted passwords don\'t match!", anchor = tk.NW)
				self.error_message.pack()
			else :	
				query = "/sign_up/" + user_name + "/" + email + "/" + password
				connection.request("POST", urllib.parse.quote(query))
				response = connection.getresponse().read().decode()
				print(response)

				connection.close()

				if response == "OK" :
					current_user = (user_name, email, "", "")
					page = MainView(genres, parent)
					page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
					page.lift
				else :
					self.error_message = tk.Label(self, text = "Username or email already used!", anchor = tk.NW)
					self.error_message.pack()

	def go_to_login(self, parent, container, genres) :
		page = LoginPage(genres, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def __init__(self, genres, *args, **kwargs) :
		tk.Frame.__init__(self, *args, **kwargs)
		back = tk.Button(self, text = "BACK", command = self.destroy)
		back.pack()
		to_login = tk.Label(self, text = "Already have an account?")
		to_login.pack()
		login = tk.Button(self, text = "LOGIN", anchor = tk.NW, command = partial(self.go_to_login, self, self, genres))
		login.pack()

		user_f = tk.Frame(self)
		user_f.pack()
		email_f = tk.Frame(self)
		email_f.pack()
		pass_f = tk.Frame(self)
		pass_f.pack()
		confirm_pass_f = tk.Frame(self)
		confirm_pass_f.pack()

		verify_string = [tk.StringVar() for i in range(4)]
		frames = [user_f, email_f, pass_f, confirm_pass_f]
		texts = ["USERNAME", "EMAIL", "PASSWORD", "CONFIRM PASSWORD"]
		
		labels = []
		entries = []
		for i in range(4) :
			labels.append(tk.Label(frames[i], text = texts[i]))
			entries.append(tk.Entry(frames[i], textvariable = verify_string[i]))
			if i == self.PASSWORD or i == self.CONFIRM_PASSWORD :
				entries[i].configure(show = "*")
			labels[i].pack(side = tk.LEFT, fill = "both")
			entries[i].pack(side = tk.RIGHT, fill = "both")

		login = tk.Button(self, text = "SIGN UP AND LOGIN", anchor = tk.NW, command = partial(self.init_page, entries, self, self, genres))
		login.pack()

class MainView(tk.Frame) :
	all_img = None
	imgg = []
	genres = None
	buttons = []
	user = None
	logout = None

	def get_genres(self) :
		global connection

		connection.request("GET", "/genres")
		response = connection.getresponse()
		json_response = json.loads(response.read().decode())
		self.genres = json_response['genres']
		connection.close()

	def init_page(self, parent, container, genre) :
		page = SeriesPage(genre, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def log_out(self, container, parent) :
		global current_user
		current_user = None
		page = MainView(self.genres, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def view_stories(self, parent, container) :
		page = StoriesPage(None, current_user[0], parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def go_to_login(self, parent, container, genres) :
		page = LoginPage(genres, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def go_to_signup(self, container, parent, genres) :
		page = SignUpPage(genres, parent)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def go_to_main(self, container) :
		page = MainView(root)
		page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		page.lift

	def __init__(self, genres, *args, **kwargs):
		global p_all
		global p_genres
		self.imgg = []

		self.get_genres()
		tk.Frame.__init__(self, *args, **kwargs)
		nsteps = len(self.genres)
		step_x = int(WIDTH / (nsteps + 1))
		step_y = int(HEIGHT / (nsteps + 1))
		min_size = min(step_x, step_y)
		size = min_size, min_size

		buttonframe = tk.Frame(self, height = HEIGHT, width = min_size)
		main_page = tk.Frame(self)
		login_frame = tk.Frame(main_page, height = 50)
		container = tk.Frame(main_page)
		buttonframe.pack(side = tk.LEFT, fill="both", expand=False)
		main_page.pack(side = tk.RIGHT, fill="both", expand=True)
		login_frame.pack(side = tk.TOP, fill = "both")
		container.pack(side = tk.BOTTOM, fill = "both", expand = True)

		if current_user is None :
			# Login / Sign up :
			login = tk.Button(login_frame, text = "Login", anchor = tk.NW, command = partial(self.go_to_login, self, self, genres))
			login.pack(side = tk.LEFT)
			sign_up = tk.Button(login_frame, text = "Sign Up", anchor = tk.NW, command = partial(self.go_to_signup, self, self, genres))
			sign_up.pack(side = tk.RIGHT)

		else :
			self.user = tk.Button(login_frame, text = current_user[0], anchor = tk.NW, relief = tk.FLAT, command = partial(self.view_stories, self, container))
			self.user.configure(font = ("Verdana", 13, "italic"), fg = 'dark turquoise')
			self.user.pack(side = tk.LEFT, fill = "both", expand = True)
			self.logout = tk.Button(login_frame, text = "LOGOUT", anchor = tk.NW, command = partial(self.log_out, self, self))
			self.logout.pack(side = tk.RIGHT, fill = "both")

		refr = tk.Button(login_frame, text = "RELOAD", command = partial(self.go_to_main, self))
		refr.pack()

		p_init = SeriesPage("most", self)
		
		p_init.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		copy_file = "./poze/genresPictures/all_copy_62.jpg"
		self.all_img = ImageTk.PhotoImage(Image.open(copy_file))
		button1 = tk.Button(buttonframe, image = self.all_img, anchor = tk.NW, command = partial(self.init_page, self, container, "all"))
		button1.configure(width = min_size, height = min_size, activebackground = "#33B5E5", relief = tk.FLAT)
		button1.pack(side = tk.TOP, fill = "y")

		i = 1
		self.buttons = []

		for line in self.genres :
			(idd, name, imagePath) = line
			
			img = Image.open(imagePath)
			self.imgg.append(ImageTk.PhotoImage(img))
			button = tk.Button(buttonframe, image = self.imgg[i - 1], anchor = tk.NW, command = partial(self.init_page, self, container, self.genres[i - 1][1]))
			button.configure(width = min_size, height = min_size, activebackground = "#33B5E5", relief = tk.FLAT)
			self.buttons.append(button)

			i += 1

		for i in range(nsteps) :
			self.buttons[i].pack(side = tk.TOP, fill = "y")
		
		p_init.show()

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

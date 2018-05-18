#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.13
# In conjunction with Tcl version 8.6
#    May 04, 2018 10:05:14 AM

import sys
import SmartTable_GUI_support
import SmartTable_p2_3
import pymysql.cursors

try:
	from Tkinter import *
except ImportError:
	from tkinter import *
	from tkinter import messagebox
	# import tkinter.ttk as ttk

try:
	import ttk
	py3 = False
except ImportError:
	import tkinter.ttk as ttk
	py3 = True

def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root
	root = Tk()
	top = Smart_Table (root)
	SmartTable_GUI_support.init(root, top)
	root.resizable(0,0)
	# root.after(100, SmartTable_p2_3.loopTest)
	root.mainloop()

w = None
def create_Smart_Table(root, *args, **kwargs):
	'''Starting point when module is imported by another program.'''
	global w, w_win, rt
	rt = root
	w = Toplevel (root)
	top = Smart_Table (w)
	SmartTable_GUI_support.init(w, top, *args, **kwargs)
	return (w, top)

def destroy_Smart_Table():
	global w
	w.destroy()
	w = None


def initDatabase():
	connection = pymysql.connect(host='localhost',
								user='root',
								password='password',
								charset='utf8mb4',
								cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			cursor.execute("create database if not exists nmc")
			cursor.execute("use nmc")
			cursor.execute("""
			create table if not exists PolyTop (
				Style varchar(100) not null,
				Size varchar(10) not null,
				BodyHeight float(4,1) not null,
				BodyHeightTol float(2,1) not null,
				BodyWidth float(4,1) not null,
				BodyWidthTol float(2,1) not null,
				BodySweap float(4,1) not null,
				BodySweapTol float(2,1) not null,
				BackNeckWidth float(4,1) not null,
				BackNeckWidthTol float(2,1) not null,
				primary key(Style, Size)
			);
			""")
			# print("Database initialized")
		connection.commit()
	finally:
		connection.close()


class Smart_Table:

	def onEnter(self, event):
		# print (event.char)
		widget = event.widget
		# print ("search " + widget.get())
		if widget == self.txtStyleNo:
			self.txtSize.focus()
		elif widget == self.txtSize:
			self.txtBodyHeight.focus()
			self.loadData(event)
		elif widget == self.txtBodyHeight:
			self.txtBodyHeightTol.focus()
		elif widget == self.txtBodyHeightTol:
			self.txtBodyWidth.focus()
		elif widget == self.txtBodyWidth:
			self.txtBodyWidthTol.focus()
		elif widget == self.txtBodyWidthTol:
			self.txtBodySweap.focus()
		elif widget == self.txtBodySweap:
			self.txtBodySweapTol.focus()
		elif widget == self.txtBodySweapTol:
			self.txtBackNeckWidth.focus()
		elif widget == self.txtBackNeckWidth:
			self.txtBackNeckWidthTol.focus()
		elif widget == self.txtBackNeckWidthTol:
			self.btnRun.focus()


	def loadData(self, event):
		widget = event.widget
		styleNo = self.txtStyleNo.get()
		size = self.txtSize.get()
		connection = pymysql.connect(host='localhost',
									user='root',
									password='password',
									charset='utf8mb4',
									cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				cursor.execute("use nmc")
				sql = "SELECT * FROM PolyTop where Style=%s and Size=%s"
				cursor.execute(sql, (styleNo, size))
				result = cursor.fetchall()
				# print (result)
				if len(result) > 0:
					self.txtBodyHeight.delete(0,len(self.txtBodyHeight.get()))
					self.txtBodyHeight.insert(0,result[0]['BodyHeight'])
					self.txtBodyHeightTol.delete(0,len(self.txtBodyHeightTol.get()))
					self.txtBodyHeightTol.insert(0,result[0]['BodyHeightTol'])
					self.txtBodyWidth.delete(0,len(self.txtBodyWidth.get()))
					self.txtBodyWidth.insert(0,result[0]['BodyWidth'])
					self.txtBodyWidthTol.delete(0,len(self.txtBodyWidthTol.get()))
					self.txtBodyWidthTol.insert(0,result[0]['BodyWidthTol'])
					self.txtBodySweap.delete(0,len(self.txtBodySweap.get()))
					self.txtBodySweap.insert(0,result[0]['BodySweap'])
					self.txtBodySweapTol.delete(0,len(self.txtBodySweapTol.get()))
					self.txtBodySweapTol.insert(0,result[0]['BodySweapTol'])
					self.txtBackNeckWidth.delete(0,len(self.txtBackNeckWidth.get()))
					self.txtBackNeckWidth.insert(0,result[0]['BackNeckWidth'])
					self.txtBackNeckWidthTol.delete(0,len(self.txtBackNeckWidthTol.get()))
					self.txtBackNeckWidthTol.insert(0,result[0]['BackNeckWidthTol'])
				# elif widget == self.txtBodyHeight or widget == self.txtSize:
				elif widget == self.txtSize:
					self.txtBodyHeight.delete(0,len(self.txtBodyHeight.get()))
					self.txtBodyHeightTol.delete(0,len(self.txtBodyHeightTol.get()))
					self.txtBodyWidth.delete(0,len(self.txtBodyWidth.get()))
					self.txtBodyWidthTol.delete(0,len(self.txtBodyWidthTol.get()))
					self.txtBodySweap.delete(0,len(self.txtBodySweap.get()))
					self.txtBodySweapTol.delete(0,len(self.txtBodySweapTol.get()))
					self.txtBackNeckWidth.delete(0,len(self.txtBackNeckWidth.get()))
					self.txtBackNeckWidthTol.delete(0,len(self.txtBackNeckWidthTol.get()))
			connection.commit()

		finally:
			connection.close()


	def runMeasuring(self):
		sN = self.txtStyleNo.get()
		sz = self.txtSize.get()
		bH = self.txtBodyHeight.get()
		bHT = self.txtBodyHeightTol.get()
		bW = self.txtBodyWidth.get()
		bWT = self.txtBodyWidthTol.get()
		bS = self.txtBodySweap.get()
		bST = self.txtBodySweapTol.get()
		bNW = self.txtBackNeckWidth.get()
		bNWT = self.txtBackNeckWidthTol.get()

		if not sN:
			self.txtStyleNo.focus()
			messagebox.showerror("Input Error", "Please enter valid Style Number")
		elif not sz:
			self.txtSize.focus()
			messagebox.showerror("Input Error", "Please enter valid Size")
		elif not bH:
			self.txtBodyHeight.focus()
			messagebox.showerror("Input Error", "Please enter valid Body Length Value")
		elif not bHT:
			self.txtBodyHeightTol.focus()
			messagebox.showerror("Input Error", "Please enter valid Body Length Tolerance")
		elif not bW:
			self.txtBodyWidth.focus()
			messagebox.showerror("Input Error", "Please enter valid Body Width Value")
		elif not bWT:
			self.txtBodyWidthTol.focus()
			messagebox.showerror("Input Error", "Please enter valid Body Length Tolerance")
		elif not bS:
			self.txtBodySweap.focus()
			messagebox.showerror("Input Error", "Please enter valid Body Sweep Value")
		elif not bST:
			self.txtBodySweapTol.focus()
			messagebox.showerror("Input Error", "Please enter valid Body Sweep Tolerance")
		elif not bNW:
			self.txtBackNeckWidth.focus()
			messagebox.showerror("Input Error", "Please enter valid Back Neck Width Value")
		elif not bNWT:
			self.txtBackNeckWidthTol.focus()
			messagebox.showerror("Input Error", "Please enter valid Back Neck Width Tolerance")
		# elif not bH or not bHT or not bW or not bWT or not bS or not bST or not bNW or not bNWT:
		# 	messagebox.showerror("Input Error", "Please enter valid Measurement Values for all fields")
		else:
			self.btnRun.configure(state = "disabled")
			self.btnRun.pack_forget()
			SmartTable_p2_3.getMeasurements(sN, sz, bH, bHT, bW, bWT, bS, bST, bNW, bNWT)
			self.btnRun.configure(state = "normal")

			connection = pymysql.connect(host='localhost',
										user='root',
										password='password',
										charset='utf8mb4',
										cursorclass=pymysql.cursors.DictCursor)
			try:
				with connection.cursor() as cursor:
					cursor.execute("use nmc")
					# print(float(self.txtBodyHeight.get()))
					sql = "INSERT INTO PolyTop VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					cursor.execute(sql, (sN, sz, float(bH), float(bHT), float(bW), float(bWT),
										float(bS), float(bST), float(bNW), float(bNWT)))
				connection.commit()

			finally:
				connection.close()


	def validateFloat(self, value, preValue, action):
		try:
			if '0' == action:
				# print("YYY")
				return True
			elif '.' == value:
				finalValue = preValue + value
				# print("YY")
				float(finalValue)
				return True
			else:
				# print("Y")
				float(value)
				return True
		except ValueError:
			# print("N")
			return False

	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85' 
		_ana2color = '#d9d9d9' # X11 color: 'gray85'

		# self.theme = ttk.Style()
		# print(self.theme.theme_names())
		# # self.theme.theme_use('clam')
		# print(self.theme.theme_use())


		# top.geometry("377x379+417+148")
		top.geometry("377x500+417+148")
		top.title("Smart Table")
		# top.iconbitmap("MAS-KREEDA-NMC.ico")
		top.configure(background="#d9d9d9")
		top.configure(highlightbackground="#d9d9d9")
		top.configure(highlightcolor="black")


		self.frameData = Frame(top)
		self.frameData.place(relx=0.03, rely=0.025, relheight=0.75, relwidth=0.94)
		self.frameData.configure(relief=GROOVE)
		self.frameData.configure(borderwidth="2")
		self.frameData.configure(relief=GROOVE)
		self.frameData.configure(background="#d9d9d9")
		self.frameData.configure(highlightbackground="#d9d9d9")
		self.frameData.configure(highlightcolor="black")
		self.frameData.configure(width=355)

		self.lblStyleNo = Label(self.frameData)
		self.lblStyleNo.place(relx=0.06, rely=0.07, height=21, width=53)
		self.lblStyleNo.configure(activebackground="#f9f9f9")
		self.lblStyleNo.configure(activeforeground="black")
		self.lblStyleNo.configure(background="#d9d9d9")
		self.lblStyleNo.configure(disabledforeground="#a3a3a3")
		self.lblStyleNo.configure(foreground="#000000")
		self.lblStyleNo.configure(highlightbackground="#d9d9d9")
		self.lblStyleNo.configure(highlightcolor="black")
		self.lblStyleNo.configure(text='''Style No.''')

		self.lblSize = Label(self.frameData)
		self.lblSize.place(relx=0.06, rely=0.21, height=21, width=26)
		self.lblSize.configure(activebackground="#f9f9f9")
		self.lblSize.configure(activeforeground="black")
		self.lblSize.configure(background="#d9d9d9")
		self.lblSize.configure(disabledforeground="#a3a3a3")
		self.lblSize.configure(foreground="#000000")
		self.lblSize.configure(highlightbackground="#d9d9d9")
		self.lblSize.configure(highlightcolor="black")
		self.lblSize.configure(text='''Size''')

		self.lblTol = Label(self.frameData)
		self.lblTol.place(relx=0.71, rely=0.37, height=21, width=84)
		self.lblTol.configure(activebackground="#f9f9f9")
		self.lblTol.configure(activeforeground="black")
		self.lblTol.configure(background="#d9d9d9")
		self.lblTol.configure(disabledforeground="#a3a3a3")
		self.lblTol.configure(foreground="#000000")
		self.lblTol.configure(highlightbackground="#d9d9d9")
		self.lblTol.configure(highlightcolor="black")
		self.lblTol.configure(text='''Tolerance (cm)''')

		self.lblBodyHeight = Label(self.frameData)
		self.lblBodyHeight.place(relx=0.055, rely=0.46, height=21, width=94)
		self.lblBodyHeight.configure(activebackground="#f9f9f9")
		self.lblBodyHeight.configure(activeforeground="black")
		self.lblBodyHeight.configure(background="#d9d9d9")
		self.lblBodyHeight.configure(disabledforeground="#a3a3a3")
		self.lblBodyHeight.configure(foreground="#000000")
		self.lblBodyHeight.configure(highlightbackground="#d9d9d9")
		self.lblBodyHeight.configure(highlightcolor="black")
		self.lblBodyHeight.configure(text='''Body Length (cm)''')

		self.lblBodyWidth = Label(self.frameData)
		self.lblBodyWidth.place(relx=0.06, rely=0.60, height=21, width=88)
		self.lblBodyWidth.configure(activebackground="#f9f9f9")
		self.lblBodyWidth.configure(activeforeground="black")
		self.lblBodyWidth.configure(background="#d9d9d9")
		self.lblBodyWidth.configure(disabledforeground="#a3a3a3")
		self.lblBodyWidth.configure(foreground="#000000")
		self.lblBodyWidth.configure(highlightbackground="#d9d9d9")
		self.lblBodyWidth.configure(highlightcolor="black")
		self.lblBodyWidth.configure(text='''Body Width (cm)''')

		self.lblBodySweap = Label(self.frameData)
		self.lblBodySweap.place(relx=0.06, rely=0.74, height=21, width=90)
		self.lblBodySweap.configure(activebackground="#f9f9f9")
		self.lblBodySweap.configure(activeforeground="black")
		self.lblBodySweap.configure(background="#d9d9d9")
		self.lblBodySweap.configure(disabledforeground="#a3a3a3")
		self.lblBodySweap.configure(foreground="#000000")
		self.lblBodySweap.configure(highlightbackground="#d9d9d9")
		self.lblBodySweap.configure(highlightcolor="black")
		self.lblBodySweap.configure(text='''Body Sweep (cm)''')

		self.lblBackNeckWidth = Label(self.frameData)
		self.lblBackNeckWidth.place(relx=0.06, rely=0.88, height=21, width=116)
		self.lblBackNeckWidth.configure(activebackground="#f9f9f9")
		self.lblBackNeckWidth.configure(activeforeground="black")
		self.lblBackNeckWidth.configure(background="#d9d9d9")
		self.lblBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.lblBackNeckWidth.configure(foreground="#000000")
		self.lblBackNeckWidth.configure(highlightbackground="#d9d9d9")
		self.lblBackNeckWidth.configure(highlightcolor="black")
		self.lblBackNeckWidth.configure(text='''Back Neck Width (cm)''')

		self.txtStyleNo = Entry(self.frameData)
		self.txtStyleNo.place(relx=0.48, rely=0.07,height=20, relwidth=0.46)
		self.txtStyleNo.configure(background="white")
		self.txtStyleNo.configure(disabledforeground="#a3a3a3")
		self.txtStyleNo.configure(font="TkFixedFont")
		self.txtStyleNo.configure(foreground="#000000")
		self.txtStyleNo.configure(highlightbackground="#d9d9d9")
		self.txtStyleNo.configure(highlightcolor="black")
		self.txtStyleNo.configure(insertbackground="black")
		self.txtStyleNo.configure(selectbackground="#c4c4c4")
		self.txtStyleNo.configure(selectforeground="black")

		self.txtStyleNo.focus()
		# self.txtStyleNo.bind("<Key>", click)
		self.txtStyleNo.bind("<Return>", self.onEnter)
		# self.txtStyleNo.bind("<Return>", lambda event: self.txtSize.focus())

		self.txtSize = Entry(self.frameData)
		self.txtSize.place(relx=0.48, rely=0.21,height=20, relwidth=0.46)
		self.txtSize.configure(background="white")
		self.txtSize.configure(disabledforeground="#a3a3a3")
		self.txtSize.configure(font="TkFixedFont")
		self.txtSize.configure(foreground="#000000")
		self.txtSize.configure(highlightbackground="#d9d9d9")
		self.txtSize.configure(highlightcolor="black")
		self.txtSize.configure(insertbackground="black")
		self.txtSize.configure(selectbackground="#c4c4c4")
		self.txtSize.configure(selectforeground="black")

		self.txtSize.bind("<Return>", self.onEnter)
		# self.txtSize.bind("<Return>", self.loadData)
		self.txtSize.bind("<Tab>", self.loadData)

		self.txtBodyHeight = Entry(self.frameData)
		self.txtBodyHeight.place(relx=0.48, rely=0.46,height=20, relwidth=0.2)
		self.txtBodyHeight.configure(background="white")
		self.txtBodyHeight.configure(disabledforeground="#a3a3a3")
		self.txtBodyHeight.configure(font="TkFixedFont")
		self.txtBodyHeight.configure(foreground="#000000")
		self.txtBodyHeight.configure(highlightbackground="#d9d9d9")
		self.txtBodyHeight.configure(highlightcolor="black")
		self.txtBodyHeight.configure(insertbackground="black")
		self.txtBodyHeight.configure(selectbackground="#c4c4c4")
		self.txtBodyHeight.configure(selectforeground="black")
		validateSupport = self.txtBodyHeight.register(self.validateFloat)
		self.txtBodyHeight.configure(validate="key")
		self.txtBodyHeight.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyHeight.bind("<Return>", self.onEnter)
		self.txtBodyHeight.bind("<Button-1>", self.loadData)

		self.txtBodyHeightTol = Entry(self.frameData)
		self.txtBodyHeightTol.place(relx=0.73, rely=0.46,height=20, relwidth=0.2)
		self.txtBodyHeightTol.configure(background="white")
		self.txtBodyHeightTol.configure(disabledforeground="#a3a3a3")
		self.txtBodyHeightTol.configure(font="TkFixedFont")
		self.txtBodyHeightTol.configure(foreground="#000000")
		self.txtBodyHeightTol.configure(highlightbackground="#d9d9d9")
		self.txtBodyHeightTol.configure(highlightcolor="black")
		self.txtBodyHeightTol.configure(insertbackground="black")
		self.txtBodyHeightTol.configure(selectbackground="#c4c4c4")
		self.txtBodyHeightTol.configure(selectforeground="black")
		validateSupport = self.txtBodyHeightTol.register(self.validateFloat)
		self.txtBodyHeightTol.configure(validate="key")
		self.txtBodyHeightTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyHeightTol.bind("<Return>", self.onEnter)
		self.txtBodyHeightTol.bind("<Button-1>", self.loadData)

		self.txtBodyWidth = Entry(self.frameData)
		self.txtBodyWidth.place(relx=0.48, rely=0.60,height=20, relwidth=0.2)
		self.txtBodyWidth.configure(background="white")
		self.txtBodyWidth.configure(disabledforeground="#a3a3a3")
		self.txtBodyWidth.configure(font="TkFixedFont")
		self.txtBodyWidth.configure(foreground="#000000")
		self.txtBodyWidth.configure(highlightbackground="#d9d9d9")
		self.txtBodyWidth.configure(highlightcolor="black")
		self.txtBodyWidth.configure(insertbackground="black")
		self.txtBodyWidth.configure(selectbackground="#c4c4c4")
		self.txtBodyWidth.configure(selectforeground="black")
		validateSupport = self.txtBodyWidth.register(self.validateFloat)
		self.txtBodyWidth.configure(validate="key")
		self.txtBodyWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyWidth.bind("<Return>", self.onEnter)
		self.txtBodyWidth.bind("<Button-1>", self.loadData)

		self.txtBodyWidthTol = Entry(self.frameData)
		self.txtBodyWidthTol.place(relx=0.73, rely=0.60,height=20, relwidth=0.2)
		self.txtBodyWidthTol.configure(background="white")
		self.txtBodyWidthTol.configure(disabledforeground="#a3a3a3")
		self.txtBodyWidthTol.configure(font="TkFixedFont")
		self.txtBodyWidthTol.configure(foreground="#000000")
		self.txtBodyWidthTol.configure(highlightbackground="#d9d9d9")
		self.txtBodyWidthTol.configure(highlightcolor="black")
		self.txtBodyWidthTol.configure(insertbackground="black")
		self.txtBodyWidthTol.configure(selectbackground="#c4c4c4")
		self.txtBodyWidthTol.configure(selectforeground="black")
		validateSupport = self.txtBodyWidthTol.register(self.validateFloat)
		self.txtBodyWidthTol.configure(validate="key")
		self.txtBodyWidthTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyWidthTol.bind("<Return>", self.onEnter)
		self.txtBodyWidthTol.bind("<Button-1>", self.loadData)

		self.txtBodySweap = Entry(self.frameData)
		self.txtBodySweap.place(relx=0.48, rely=0.74,height=20, relwidth=0.2)
		self.txtBodySweap.configure(background="white")
		self.txtBodySweap.configure(disabledforeground="#a3a3a3")
		self.txtBodySweap.configure(font="TkFixedFont")
		self.txtBodySweap.configure(foreground="#000000")
		self.txtBodySweap.configure(highlightbackground="#d9d9d9")
		self.txtBodySweap.configure(highlightcolor="black")
		self.txtBodySweap.configure(insertbackground="black")
		self.txtBodySweap.configure(selectbackground="#c4c4c4")
		self.txtBodySweap.configure(selectforeground="black")
		validateSupport = self.txtBodySweap.register(self.validateFloat)
		self.txtBodySweap.configure(validate="key")
		self.txtBodySweap.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodySweap.bind("<Return>", self.onEnter)
		self.txtBodySweap.bind("<Button-1>", self.loadData)

		self.txtBodySweapTol = Entry(self.frameData)
		self.txtBodySweapTol.place(relx=0.73, rely=0.74,height=20, relwidth=0.2)
		self.txtBodySweapTol.configure(background="white")
		self.txtBodySweapTol.configure(disabledforeground="#a3a3a3")
		self.txtBodySweapTol.configure(font="TkFixedFont")
		self.txtBodySweapTol.configure(foreground="#000000")
		self.txtBodySweapTol.configure(highlightbackground="#d9d9d9")
		self.txtBodySweapTol.configure(highlightcolor="black")
		self.txtBodySweapTol.configure(insertbackground="black")
		self.txtBodySweapTol.configure(selectbackground="#c4c4c4")
		self.txtBodySweapTol.configure(selectforeground="black")
		validateSupport = self.txtBodySweapTol.register(self.validateFloat)
		self.txtBodySweapTol.configure(validate="key")
		self.txtBodySweapTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodySweapTol.bind("<Return>", self.onEnter)
		self.txtBodySweapTol.bind("<Button-1>", self.loadData)

		self.txtBackNeckWidth = Entry(self.frameData)
		self.txtBackNeckWidth.place(relx=0.48, rely=0.88, height=20
		        , relwidth=0.2)
		self.txtBackNeckWidth.configure(background="white")
		self.txtBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.txtBackNeckWidth.configure(font="TkFixedFont")
		self.txtBackNeckWidth.configure(foreground="#000000")
		self.txtBackNeckWidth.configure(highlightbackground="#d9d9d9")
		self.txtBackNeckWidth.configure(highlightcolor="black")
		self.txtBackNeckWidth.configure(insertbackground="black")
		self.txtBackNeckWidth.configure(selectbackground="#c4c4c4")
		self.txtBackNeckWidth.configure(selectforeground="black")
		validateSupport = self.txtBackNeckWidth.register(self.validateFloat)
		self.txtBackNeckWidth.configure(validate="key")
		self.txtBackNeckWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBackNeckWidth.bind("<Return>", self.onEnter)
		self.txtBackNeckWidth.bind("<Button-1>", self.loadData)

		self.txtBackNeckWidthTol = Entry(self.frameData)
		self.txtBackNeckWidthTol.place(relx=0.73, rely=0.88, height=20
		        , relwidth=0.2)
		self.txtBackNeckWidthTol.configure(background="white")
		self.txtBackNeckWidthTol.configure(disabledforeground="#a3a3a3")
		self.txtBackNeckWidthTol.configure(font="TkFixedFont")
		self.txtBackNeckWidthTol.configure(foreground="#000000")
		self.txtBackNeckWidthTol.configure(highlightbackground="#d9d9d9")
		self.txtBackNeckWidthTol.configure(highlightcolor="black")
		self.txtBackNeckWidthTol.configure(insertbackground="black")
		self.txtBackNeckWidthTol.configure(selectbackground="#c4c4c4")
		self.txtBackNeckWidthTol.configure(selectforeground="black")
		validateSupport = self.txtBackNeckWidthTol.register(self.validateFloat)
		self.txtBackNeckWidthTol.configure(validate="key")
		self.txtBackNeckWidthTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBackNeckWidthTol.bind("<Return>", self.onEnter)
		self.txtBackNeckWidthTol.bind("<Button-1>", self.loadData)

		self.frameRun = Frame(top)
		self.frameRun.place(relx=0.03, rely=0.8, relheight=0.18, relwidth=0.94)
		self.frameRun.configure(relief=GROOVE)
		self.frameRun.configure(borderwidth="2")
		self.frameRun.configure(relief=GROOVE)
		self.frameRun.configure(background="#d9d9d9")
		self.frameRun.configure(highlightbackground="#d9d9d9")
		self.frameRun.configure(highlightcolor="black")
		self.frameRun.configure(width=355)

		self.btnRun = Button(self.frameRun)
		# self.btnRun.place(relx=0.2, rely=0.13, height=54, width=64)
		self.btnRun.place(relx=0.07, rely=0.2, height=54, width=300)
		self.btnRun.configure(activebackground="#008000")
		self.btnRun.configure(activeforeground="#000000")
		self.btnRun.configure(background="#00FF00")
		# self.btnRun.configure(background="#d9d9d9")
		self.btnRun.configure(cursor="hand2")
		self.btnRun.configure(disabledforeground="#000000")
		self.btnRun.configure(foreground="#000000")
		self.btnRun.configure(highlightbackground="#000000")
		self.btnRun.configure(highlightcolor="#000000")
		self.btnRun.configure(pady="0")
		self.btnRun.configure(state="normal")
		self.btnRun.configure(font=('Courier', 30, 'bold'))
		self.btnRun.configure(text='''Run''')
		# self.btnRun.configure(command=SmartTable_p2_3.getMeasurements)
		self.btnRun.configure(command=self.runMeasuring)

		# self.btnStop = Button(self.frameRun)
		# self.btnStop.place(relx=0.59, rely=0.13, height=54, width=64)
		# self.btnStop.configure(activebackground="red")
		# self.btnStop.configure(activeforeground="#000000")
		# self.btnStop.configure(background="#FF4040")
		# self.btnStop.configure(cursor="hand2")
		# self.btnStop.configure(disabledforeground="#a3a3a3")
		# self.btnStop.configure(foreground="#000000")
		# self.btnStop.configure(highlightbackground="#d9d9d9")
		# self.btnStop.configure(highlightcolor="black")
		# self.btnStop.configure(pady="0")
		# self.btnStop.configure(state=NORMAL)
		# self.btnStop.configure(text='''Stop''')
		# self.btnStop.configure(command=SmartTable_p2_3.testing)


# ~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~

initDatabase()


if __name__ == '__main__':
	vp_start_gui()

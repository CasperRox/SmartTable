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
	root.after(100, SmartTable_p2_3.loopTest)
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
				BodyWidth float(4,1) not null, 
				BodySweap float(4,1) not null, 
				BackNeckWidth float(4,1) not null, 
				primary key(Style, Size)
			);
			""")
			print("Database initialized")
		connection.commit()
	finally:
		connection.close()


class Smart_Table:

	def on_enter(self, event):
		# print (event.char)
		widget = event.widget
		# print ("search " + widget.get())
		if widget == self.txtStyleNo:
			self.txtSize.focus()
		elif widget == self.txtSize:
			self.txtBodyHeight.focus()
			self.loadData(event)
		elif widget == self.txtBodyHeight:
			self.txtBodyWidth.focus()
		elif widget == self.txtBodyWidth:
			self.txtBodySweap.focus()
		elif widget == self.txtBodySweap:
			self.txtBackNeckWidth.focus()
		elif widget == self.txtBackNeckWidth:
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
					self.txtBodyWidth.delete(0,len(self.txtBodyWidth.get()))
					self.txtBodyWidth.insert(0,result[0]['BodyWidth'])
					self.txtBodySweap.delete(0,len(self.txtBodySweap.get()))
					self.txtBodySweap.insert(0,result[0]['BodySweap'])
					self.txtBackNeckWidth.delete(0,len(self.txtBackNeckWidth.get()))
					self.txtBackNeckWidth.insert(0,result[0]['BackNeckWidth'])
				elif widget == self.txtBodyHeight or self.txtSize:
					self.txtBodyHeight.delete(0,len(self.txtBodyHeight.get()))
					self.txtBodyWidth.delete(0,len(self.txtBodyWidth.get()))
					self.txtBodySweap.delete(0,len(self.txtBodySweap.get()))
					self.txtBackNeckWidth.delete(0,len(self.txtBackNeckWidth.get()))
			connection.commit()

		finally:
			connection.close()


	def runMeasuring(self):
		sN = self.txtStyleNo.get()
		sz = self.txtSize.get()
		bH = self.txtBodyHeight.get()
		bW = self.txtBodyWidth.get()
		bS = self.txtBodySweap.get()
		bNW = self.txtBackNeckWidth.get()

		SmartTable_p2_3.getMeasurements(sN, sz, bH, bW, bS, bNW)

		connection = pymysql.connect(host='localhost',
									user='root',
									password='password',
									charset='utf8mb4',
									cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				cursor.execute("use nmc")
				# print(float(self.txtBodyHeight.get()))
				sql = "INSERT INTO PolyTop VALUES (%s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (sN, sz, float(bH), float(bW), float(bS), float(bNW)))
			connection.commit()

		finally:
			connection.close()


	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85' 
		_ana2color = '#d9d9d9' # X11 color: 'gray85' 

		top.geometry("377x379+417+148")
		top.title("Smart Table")
		top.configure(background="#d9d9d9")
		top.configure(highlightbackground="#d9d9d9")
		top.configure(highlightcolor="black")


		self.frameData = Frame(top)
		self.frameData.place(relx=0.03, rely=0.03, relheight=0.7, relwidth=0.94)
		self.frameData.configure(relief=GROOVE)
		self.frameData.configure(borderwidth="2")
		self.frameData.configure(relief=GROOVE)
		self.frameData.configure(background="#d9d9d9")
		self.frameData.configure(highlightbackground="#d9d9d9")
		self.frameData.configure(highlightcolor="black")
		self.frameData.configure(width=355)

		self.lblStyleNo = Label(self.frameData)
		self.lblStyleNo.place(relx=0.06, rely=0.08, height=21, width=53)
		self.lblStyleNo.configure(activebackground="#f9f9f9")
		self.lblStyleNo.configure(activeforeground="black")
		self.lblStyleNo.configure(background="#d9d9d9")
		self.lblStyleNo.configure(disabledforeground="#a3a3a3")
		self.lblStyleNo.configure(foreground="#000000")
		self.lblStyleNo.configure(highlightbackground="#d9d9d9")
		self.lblStyleNo.configure(highlightcolor="black")
		self.lblStyleNo.configure(text='''Style No.''')

		self.lblSize = Label(self.frameData)
		self.lblSize.place(relx=0.06, rely=0.23, height=21, width=26)
		self.lblSize.configure(activebackground="#f9f9f9")
		self.lblSize.configure(activeforeground="black")
		self.lblSize.configure(background="#d9d9d9")
		self.lblSize.configure(disabledforeground="#a3a3a3")
		self.lblSize.configure(foreground="#000000")
		self.lblSize.configure(highlightbackground="#d9d9d9")
		self.lblSize.configure(highlightcolor="black")
		self.lblSize.configure(text='''Size''')

		self.lblBodyHeight = Label(self.frameData)
		self.lblBodyHeight.place(relx=0.06, rely=0.38, height=21, width=84)
		self.lblBodyHeight.configure(activebackground="#f9f9f9")
		self.lblBodyHeight.configure(activeforeground="black")
		self.lblBodyHeight.configure(background="#d9d9d9")
		self.lblBodyHeight.configure(disabledforeground="#a3a3a3")
		self.lblBodyHeight.configure(foreground="#000000")
		self.lblBodyHeight.configure(highlightbackground="#d9d9d9")
		self.lblBodyHeight.configure(highlightcolor="black")
		self.lblBodyHeight.configure(text='''Body Height''')

		self.lblBodyWidth = Label(self.frameData)
		self.lblBodyWidth.place(relx=0.06, rely=0.53, height=21, width=68)
		self.lblBodyWidth.configure(activebackground="#f9f9f9")
		self.lblBodyWidth.configure(activeforeground="black")
		self.lblBodyWidth.configure(background="#d9d9d9")
		self.lblBodyWidth.configure(disabledforeground="#a3a3a3")
		self.lblBodyWidth.configure(foreground="#000000")
		self.lblBodyWidth.configure(highlightbackground="#d9d9d9")
		self.lblBodyWidth.configure(highlightcolor="black")
		self.lblBodyWidth.configure(text='''Body Width''')

		self.lblBodySweap = Label(self.frameData)
		self.lblBodySweap.place(relx=0.06, rely=0.68, height=21, width=70)
		self.lblBodySweap.configure(activebackground="#f9f9f9")
		self.lblBodySweap.configure(activeforeground="black")
		self.lblBodySweap.configure(background="#d9d9d9")
		self.lblBodySweap.configure(disabledforeground="#a3a3a3")
		self.lblBodySweap.configure(foreground="#000000")
		self.lblBodySweap.configure(highlightbackground="#d9d9d9")
		self.lblBodySweap.configure(highlightcolor="black")
		self.lblBodySweap.configure(text='''Body Sweap''')

		self.lblBackNeckWidth = Label(self.frameData)
		self.lblBackNeckWidth.place(relx=0.06, rely=0.83, height=21, width=96)
		self.lblBackNeckWidth.configure(activebackground="#f9f9f9")
		self.lblBackNeckWidth.configure(activeforeground="black")
		self.lblBackNeckWidth.configure(background="#d9d9d9")
		self.lblBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.lblBackNeckWidth.configure(foreground="#000000")
		self.lblBackNeckWidth.configure(highlightbackground="#d9d9d9")
		self.lblBackNeckWidth.configure(highlightcolor="black")
		self.lblBackNeckWidth.configure(text='''Back Neck Width''')

		self.txtStyleNo = Entry(self.frameData)
		self.txtStyleNo.place(relx=0.48, rely=0.08,height=20, relwidth=0.46)
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
		self.txtStyleNo.bind("<Return>", self.on_enter)
		# self.txtStyleNo.bind("<Return>", lambda event: self.txtSize.focus())

		self.txtSize = Entry(self.frameData)
		self.txtSize.place(relx=0.48, rely=0.23,height=20, relwidth=0.46)
		self.txtSize.configure(background="white")
		self.txtSize.configure(disabledforeground="#a3a3a3")
		self.txtSize.configure(font="TkFixedFont")
		self.txtSize.configure(foreground="#000000")
		self.txtSize.configure(highlightbackground="#d9d9d9")
		self.txtSize.configure(highlightcolor="black")
		self.txtSize.configure(insertbackground="black")
		self.txtSize.configure(selectbackground="#c4c4c4")
		self.txtSize.configure(selectforeground="black")

		self.txtSize.bind("<Return>", self.on_enter)
		# self.txtSize.bind("<Return>", self.loadData)
		self.txtSize.bind("<Tab>", self.loadData)

		self.txtBodyHeight = Entry(self.frameData)
		self.txtBodyHeight.place(relx=0.48, rely=0.38,height=20, relwidth=0.46)
		self.txtBodyHeight.configure(background="white")
		self.txtBodyHeight.configure(disabledforeground="#a3a3a3")
		self.txtBodyHeight.configure(font="TkFixedFont")
		self.txtBodyHeight.configure(foreground="#000000")
		self.txtBodyHeight.configure(highlightbackground="#d9d9d9")
		self.txtBodyHeight.configure(highlightcolor="black")
		self.txtBodyHeight.configure(insertbackground="black")
		self.txtBodyHeight.configure(selectbackground="#c4c4c4")
		self.txtBodyHeight.configure(selectforeground="black")

		self.txtBodyHeight.bind("<Return>", self.on_enter)
		self.txtBodyHeight.bind("<Button-1>", self.loadData)

		self.txtBodyWidth = Entry(self.frameData)
		self.txtBodyWidth.place(relx=0.48, rely=0.53,height=20, relwidth=0.46)
		self.txtBodyWidth.configure(background="white")
		self.txtBodyWidth.configure(disabledforeground="#a3a3a3")
		self.txtBodyWidth.configure(font="TkFixedFont")
		self.txtBodyWidth.configure(foreground="#000000")
		self.txtBodyWidth.configure(highlightbackground="#d9d9d9")
		self.txtBodyWidth.configure(highlightcolor="black")
		self.txtBodyWidth.configure(insertbackground="black")
		self.txtBodyWidth.configure(selectbackground="#c4c4c4")
		self.txtBodyWidth.configure(selectforeground="black")

		self.txtBodyWidth.bind("<Return>", self.on_enter)
		self.txtBodyWidth.bind("<Button-1>", self.loadData)

		self.txtBodySweap = Entry(self.frameData)
		self.txtBodySweap.place(relx=0.48, rely=0.68,height=20, relwidth=0.46)
		self.txtBodySweap.configure(background="white")
		self.txtBodySweap.configure(disabledforeground="#a3a3a3")
		self.txtBodySweap.configure(font="TkFixedFont")
		self.txtBodySweap.configure(foreground="#000000")
		self.txtBodySweap.configure(highlightbackground="#d9d9d9")
		self.txtBodySweap.configure(highlightcolor="black")
		self.txtBodySweap.configure(insertbackground="black")
		self.txtBodySweap.configure(selectbackground="#c4c4c4")
		self.txtBodySweap.configure(selectforeground="black")

		self.txtBodySweap.bind("<Return>", self.on_enter)
		self.txtBodySweap.bind("<Button-1>", self.loadData)

		self.txtBackNeckWidth = Entry(self.frameData)
		self.txtBackNeckWidth.place(relx=0.48, rely=0.83, height=20
		        , relwidth=0.46)
		self.txtBackNeckWidth.configure(background="white")
		self.txtBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.txtBackNeckWidth.configure(font="TkFixedFont")
		self.txtBackNeckWidth.configure(foreground="#000000")
		self.txtBackNeckWidth.configure(highlightbackground="#d9d9d9")
		self.txtBackNeckWidth.configure(highlightcolor="black")
		self.txtBackNeckWidth.configure(insertbackground="black")
		self.txtBackNeckWidth.configure(selectbackground="#c4c4c4")
		self.txtBackNeckWidth.configure(selectforeground="black")

		self.txtBackNeckWidth.bind("<Return>", self.on_enter)
		self.txtBackNeckWidth.bind("<Button-1>", self.loadData)

		self.frameRun = Frame(top)
		self.frameRun.place(relx=0.03, rely=0.77, relheight=0.2, relwidth=0.94)
		self.frameRun.configure(relief=GROOVE)
		self.frameRun.configure(borderwidth="2")
		self.frameRun.configure(relief=GROOVE)
		self.frameRun.configure(background="#d9d9d9")
		self.frameRun.configure(highlightbackground="#d9d9d9")
		self.frameRun.configure(highlightcolor="black")
		self.frameRun.configure(width=355)

		self.btnRun = Button(self.frameRun)
		self.btnRun.place(relx=0.2, rely=0.13, height=54, width=64)
		self.btnRun.configure(activebackground="#008000")
		self.btnRun.configure(activeforeground="#000000")
		self.btnRun.configure(background="#00FF00")
		self.btnRun.configure(cursor="hand2")
		self.btnRun.configure(disabledforeground="#a3a3a3")
		self.btnRun.configure(foreground="#000000")
		self.btnRun.configure(highlightbackground="#000000")
		self.btnRun.configure(highlightcolor="#000000")
		self.btnRun.configure(pady="0")
		self.btnRun.configure(state=NORMAL)
		self.btnRun.configure(text='''Run''')
		# self.btnRun.configure(command=SmartTable_p2_3.getMeasurements)
		self.btnRun.configure(command=self.runMeasuring)

		self.btnStop = Button(self.frameRun)
		self.btnStop.place(relx=0.59, rely=0.13, height=54, width=64)
		self.btnStop.configure(activebackground="red")
		self.btnStop.configure(activeforeground="#000000")
		self.btnStop.configure(background="#FF4040")
		self.btnStop.configure(cursor="hand2")
		self.btnStop.configure(disabledforeground="#a3a3a3")
		self.btnStop.configure(foreground="#000000")
		self.btnStop.configure(highlightbackground="#d9d9d9")
		self.btnStop.configure(highlightcolor="black")
		self.btnStop.configure(pady="0")
		self.btnStop.configure(state=NORMAL)
		self.btnStop.configure(text='''Stop''')
		self.btnStop.configure(command=SmartTable_p2_3.testing)


# ~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~

initDatabase()


if __name__ == '__main__':
	vp_start_gui()

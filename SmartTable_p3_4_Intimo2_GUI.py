import sys
import SmartTable_p3_4_Intimo2_GUI_support
import SmartTable_p3_4_Intimo2
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
	SmartTable_p3_4_Intimo2_GUI_support.init(root, top)
	root.resizable(0,0)
	# root.after(100, SmartTable_p3_4_Intimo2.loopTest)
	root.mainloop()

w = None
def create_Smart_Table(root, *args, **kwargs):
	'''Starting point when module is imported by another program.'''
	global w, w_win, rt
	rt = root
	w = Toplevel (root)
	top = Smart_Table (w)
	SmartTable_p3_4_Intimo2_GUI_support.init(w, top, *args, **kwargs)
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
			cursor.execute("""
			create table if not exists PolyTop_Records (
				DateTime varchar(30) not null,
				TableIndex varchar(10) not null,
				Plant varchar(100) not null,
				Style varchar(100) not null,
				Size varchar(10) not null,
				BodyHeight float(4,1) not null,
				BodyHeightDif float(3,1) not null,
				BodyWidth float(4,1) not null,
				BodyWidthDif float(3,1) not null,
				BodySweap float(4,1) not null,
				BodySweapDif float(3,1) not null,
				BackNeckWidth float(4,1) not null,
				BackNeckWidthDif float(3,1) not null,
				primary key(DateTime, TableIndex, Plant, Style, Size)
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
		whiteMode = self.onoff.get()

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
			SmartTable_p3_4_Intimo2.getMeasurements(sN, sz, bH, bHT, bW, bWT, bS, bST, bNW, bNWT, whiteMode)
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
					sql = (
						"INSERT INTO PolyTop VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
						"ON DUPLICATE KEY UPDATE "
						"BodyHeight = %s, BodyHeightTol = %s, BodyWidth = %s, BodyWidthTol = %s, "
						"BodySweap = %s, BodySweapTol = %s, BackNeckWidth = %s, BackNeckWidthTol = %s"
					)
					cursor.execute(sql, (sN, sz, float(bH), float(bHT), float(bW), float(bWT),
										float(bS), float(bST), float(bNW), float(bNWT),
										float(bH), float(bHT), float(bW), float(bWT),
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


	def whiteGarmentModeOnOff(self):
		# status = self.lblWhiteGarmentStatus.cget("textvariable")
		status = self.onoff.get()
		# print(status)
		if "ON" == status:
			self.onoff.set("OFF")
		elif "OFF" == status:
			self.onoff.set("ON")


	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_bgcolor = '#27408B'  # X11 color: 'gray85'
		# _fgcolor = '#8470FF'  # X11 color: 'black'
		_fgcolor = 'white'  # X11 color: 'black'
		_highlightbgcolor = '#4169E1'
		_compcolor = '#27408B' # X11 color: 'gray85'
		_ana1color = '#27408B' # X11 color: 'gray85' 
		_ana2color = '#27408B' # X11 color: 'gray85'

		# self.theme = ttk.Style()
		# print(self.theme.theme_names())
		# # self.theme.theme_use('clam')
		# print(self.theme.theme_use())


		# top.geometry("377x379+417+148")
		# top.geometry("377x550+417+100")
		top.geometry("377x550+150+200")
		top.title("Smart Table")
		top.iconbitmap("MASKreedaNMC.ico")
		# top.configure(background="#d9d9d9")
		top.configure(background=_bgcolor)
		# top.configure(image="MASKreedaNMC_Set.jpg")
		top.configure(highlightbackground=_bgcolor)
		top.configure(highlightcolor=_fgcolor)


		# photo = PhotoImage(file="MASKreedaNMC_Set.gif")
		# self.lblBG = Label(top)
		# self.lblBG.place(relx=0, rely=0, height=500, width=377)
		# self.lblBG.configure(image=photo)

		# self.frameData = Frame(top)
		# self.frameData.place(relx=0.03, rely=0.025, relheight=0.75, relwidth=0.94)
		# # self.frameData.configure(relief=GROOVE)
		# self.frameData.configure(relief=FLAT)
		# self.frameData.configure(borderwidth="1")
		# self.frameData.configure(background=_bgcolor)
		# self.frameData.configure(highlightbackground=_bgcolor)
		# self.frameData.configure(highlightcolor=_fgcolor)
		# self.frameData.configure(width=355)

		# self.lblBG = Label(self.frameData)
		# self.lblBG.place(relx=0, rely=0, height=300, width=300)
		# self.lblBG.configure(image=photo)

		self.cnvsData = Canvas(top)
		self.cnvsData.place(relx=0.03, rely=0.023, relheight=0.825, relwidth=0.94)
		self.cnvsData.configure(relief=FLAT)
		self.cnvsData.configure(borderwidth="0")
		self.cnvsData.configure(background=_bgcolor)
		self.cnvsData.configure(highlightbackground=_bgcolor)
		self.cnvsData.configure(highlightcolor=_bgcolor)
		self.cnvsData.configure(width=355)
		# self.cnvsData.create_line(170,46,335,46, fill=_fgcolor, width="3", dash=(4,2))
		self.cnvsData.create_line(170,46,335,46, fill=_fgcolor, width="1")
		self.cnvsData.create_line(170,100,335,100, fill=_fgcolor, width="1")
		self.cnvsData.create_line(170,194,242,194, fill=_fgcolor, width="1")
		self.cnvsData.create_line(259,194,335,194, fill=_fgcolor, width="1")
		self.cnvsData.create_line(170,246,242,246, fill=_fgcolor, width="1")
		self.cnvsData.create_line(259,246,335,246, fill=_fgcolor, width="1")
		self.cnvsData.create_line(170,299,242,299, fill=_fgcolor, width="1")
		self.cnvsData.create_line(259,299,335,299, fill=_fgcolor, width="1")
		self.cnvsData.create_line(170,351,242,351, fill=_fgcolor, width="1")
		self.cnvsData.create_line(259,351,335,351, fill=_fgcolor, width="1")

		self.lblStyleNo = Label(self.cnvsData)
		self.lblStyleNo.place(relx=0.06, rely=0.055, height=21, width=53)
		self.lblStyleNo.configure(activebackground="#f9f9f9")
		self.lblStyleNo.configure(activeforeground=_fgcolor)
		self.lblStyleNo.configure(background=_bgcolor)
		self.lblStyleNo.configure(disabledforeground="#a3a3a3")
		self.lblStyleNo.configure(foreground=_fgcolor)
		self.lblStyleNo.configure(highlightbackground=_bgcolor)
		self.lblStyleNo.configure(highlightcolor=_fgcolor)
		self.lblStyleNo.configure(font=('Helvetica', 8, 'bold'))
		self.lblStyleNo.configure(text='''Style No.''')

		self.lblSize = Label(self.cnvsData)
		self.lblSize.place(relx=0.06, rely=0.175, height=21, width=26)
		self.lblSize.configure(activebackground="#f9f9f9")
		self.lblSize.configure(activeforeground=_fgcolor)
		self.lblSize.configure(background=_bgcolor)
		self.lblSize.configure(disabledforeground="#a3a3a3")
		self.lblSize.configure(foreground=_fgcolor)
		self.lblSize.configure(highlightbackground=_bgcolor)
		self.lblSize.configure(highlightcolor=_fgcolor)
		self.lblSize.configure(font=('Helvetica', 8, 'bold'))
		self.lblSize.configure(text='''Size''')

		self.lblTol = Label(self.cnvsData)
		self.lblTol.place(relx=0.69, rely=0.3, height=21, width=104)
		self.lblTol.configure(activebackground="#f9f9f9")
		self.lblTol.configure(activeforeground=_fgcolor)
		self.lblTol.configure(background=_bgcolor)
		self.lblTol.configure(disabledforeground="#a3a3a3")
		self.lblTol.configure(foreground=_fgcolor)
		self.lblTol.configure(highlightbackground=_bgcolor)
		self.lblTol.configure(highlightcolor=_fgcolor)
		self.lblTol.configure(font=('Helvetica', 8, 'bold'))
		self.lblTol.configure(text='''Tolerance (cm)''')

		self.lblBodyHeight = Label(self.cnvsData)
		self.lblBodyHeight.place(relx=0.055, rely=0.38, height=21, width=114)
		self.lblBodyHeight.configure(activebackground="#f9f9f9")
		self.lblBodyHeight.configure(activeforeground=_fgcolor)
		self.lblBodyHeight.configure(background=_bgcolor)
		self.lblBodyHeight.configure(disabledforeground="#a3a3a3")
		self.lblBodyHeight.configure(foreground=_fgcolor)
		self.lblBodyHeight.configure(highlightbackground=_bgcolor)
		self.lblBodyHeight.configure(highlightcolor=_fgcolor)
		self.lblBodyHeight.configure(font=('Helvetica', 8, 'bold'))
		self.lblBodyHeight.configure(text='''Body Length (cm)''')

		self.lblBodyWidth = Label(self.cnvsData)
		self.lblBodyWidth.place(relx=0.06, rely=0.495, height=21, width=108)
		self.lblBodyWidth.configure(activebackground="#f9f9f9")
		self.lblBodyWidth.configure(activeforeground=_fgcolor)
		self.lblBodyWidth.configure(background=_bgcolor)
		self.lblBodyWidth.configure(disabledforeground="#a3a3a3")
		self.lblBodyWidth.configure(foreground=_fgcolor)
		self.lblBodyWidth.configure(highlightbackground=_bgcolor)
		self.lblBodyWidth.configure(highlightcolor=_fgcolor)
		self.lblBodyWidth.configure(font=('Helvetica', 8, 'bold'))
		self.lblBodyWidth.configure(text='''Body Width (cm)''')

		self.lblBodySweap = Label(self.cnvsData)
		self.lblBodySweap.place(relx=0.06, rely=0.61, height=21, width=110)
		self.lblBodySweap.configure(activebackground="#f9f9f9")
		self.lblBodySweap.configure(activeforeground=_fgcolor)
		self.lblBodySweap.configure(background=_bgcolor)
		self.lblBodySweap.configure(disabledforeground="#a3a3a3")
		self.lblBodySweap.configure(foreground=_fgcolor)
		self.lblBodySweap.configure(highlightbackground=_bgcolor)
		self.lblBodySweap.configure(highlightcolor=_fgcolor)
		self.lblBodySweap.configure(font=('Helvetica', 8, 'bold'))
		self.lblBodySweap.configure(text='''Body Sweep (cm)''')

		self.lblBackNeckWidth = Label(self.cnvsData)
		self.lblBackNeckWidth.place(relx=0.06, rely=0.725, height=21, width=136)
		self.lblBackNeckWidth.configure(activebackground="#f9f9f9")
		self.lblBackNeckWidth.configure(activeforeground=_fgcolor)
		self.lblBackNeckWidth.configure(background=_bgcolor)
		self.lblBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.lblBackNeckWidth.configure(foreground=_fgcolor)
		self.lblBackNeckWidth.configure(highlightbackground=_bgcolor)
		self.lblBackNeckWidth.configure(highlightcolor=_fgcolor)
		self.lblBackNeckWidth.configure(font=('Helvetica', 8, 'bold'))
		self.lblBackNeckWidth.configure(text='''Back Neck Width (cm)''')

		self.lblWhiteGarmentMode = Label(self.cnvsData)
		self.lblWhiteGarmentMode.place(relx=0.06, rely=0.87, height=21, width=136)
		self.lblWhiteGarmentMode.configure(activebackground="#f9f9f9")
		self.lblWhiteGarmentMode.configure(activeforeground=_fgcolor)
		self.lblWhiteGarmentMode.configure(background=_bgcolor)
		self.lblWhiteGarmentMode.configure(disabledforeground="#a3a3a3")
		self.lblWhiteGarmentMode.configure(foreground=_fgcolor)
		self.lblWhiteGarmentMode.configure(highlightbackground=_bgcolor)
		self.lblWhiteGarmentMode.configure(highlightcolor=_fgcolor)
		self.lblWhiteGarmentMode.configure(font=('Helvetica', 8, 'bold'))
		self.lblWhiteGarmentMode.configure(text='''White Garment Mode''')

		self.onoff = StringVar()
		self.onoff.set("OFF")

		self.lblWhiteGarmentStatus = Label(self.cnvsData)
		self.lblWhiteGarmentStatus.place(relx=0.45, rely=0.87, height=21, width=90)
		self.lblWhiteGarmentStatus.configure(activebackground="#f9f9f9")
		self.lblWhiteGarmentStatus.configure(activeforeground=_fgcolor)
		self.lblWhiteGarmentStatus.configure(background=_bgcolor)
		self.lblWhiteGarmentStatus.configure(disabledforeground="#a3a3a3")
		self.lblWhiteGarmentStatus.configure(foreground=_fgcolor)
		self.lblWhiteGarmentStatus.configure(highlightbackground=_bgcolor)
		self.lblWhiteGarmentStatus.configure(highlightcolor=_fgcolor)
		self.lblWhiteGarmentStatus.configure(font=('TkFixedFont', 12, 'bold'))
		self.lblWhiteGarmentStatus.configure(textvariable=self.onoff)

		self.btnOnOff = Button(self.cnvsData)
		self.btnOnOff.place(relx=0.74, rely=0.87, height=20, width=70)
		self.btnOnOff.configure(activebackground="#008000")
		self.btnOnOff.configure(activeforeground=_fgcolor)
		self.btnOnOff.configure(background="#3A5FCD")
		self.btnOnOff.configure(cursor="hand2")
		self.btnOnOff.configure(relief=FLAT)
		self.btnOnOff.configure(disabledforeground=_fgcolor)
		self.btnOnOff.configure(foreground=_fgcolor)
		self.btnOnOff.configure(highlightbackground=_fgcolor)
		self.btnOnOff.configure(highlightcolor=_fgcolor)
		self.btnOnOff.configure(pady="0")
		self.btnOnOff.configure(state="normal")
		self.btnOnOff.configure(font=('Helvetica', 8, 'bold'))
		self.btnOnOff.configure(text='''ON / OFF''')
		self.btnOnOff.configure(command=self.whiteGarmentModeOnOff)

		self.txtStyleNo = Entry(self.cnvsData)
		self.txtStyleNo.place(relx=0.48, rely=0.056,height=20, relwidth=0.46)
		self.txtStyleNo.configure(background=_bgcolor)
		self.txtStyleNo.configure(disabledforeground="#a3a3a3")
		self.txtStyleNo.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtStyleNo.configure(foreground=_fgcolor)
		self.txtStyleNo.configure(highlightbackground=_bgcolor)
		self.txtStyleNo.configure(highlightcolor=_fgcolor)
		self.txtStyleNo.configure(insertbackground=_fgcolor)
		self.txtStyleNo.configure(selectbackground=_highlightbgcolor)
		self.txtStyleNo.configure(selectforeground=_fgcolor)
		self.txtStyleNo.configure(relief=FLAT)

		self.txtStyleNo.focus()
		# self.txtStyleNo.bind("<Key>", click)
		self.txtStyleNo.bind("<Return>", self.onEnter)
		# self.txtStyleNo.bind("<Return>", lambda event: self.txtSize.focus())

		self.txtSize = Entry(self.cnvsData)
		self.txtSize.place(relx=0.48, rely=0.175,height=20, relwidth=0.46)
		self.txtSize.configure(background=_bgcolor)
		self.txtSize.configure(disabledforeground="#a3a3a3")
		self.txtSize.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtSize.configure(foreground=_fgcolor)
		self.txtSize.configure(highlightbackground=_bgcolor)
		self.txtSize.configure(highlightcolor=_fgcolor)
		self.txtSize.configure(insertbackground=_fgcolor)
		self.txtSize.configure(selectbackground=_highlightbgcolor)
		self.txtSize.configure(selectforeground=_fgcolor)
		self.txtSize.configure(relief=FLAT)

		self.txtSize.bind("<Return>", self.onEnter)
		# self.txtSize.bind("<Return>", self.loadData)
		self.txtSize.bind("<Tab>", self.loadData)

		self.txtBodyHeight = Entry(self.cnvsData)
		self.txtBodyHeight.place(relx=0.48, rely=0.38,height=20, relwidth=0.2)
		self.txtBodyHeight.configure(background=_bgcolor)
		self.txtBodyHeight.configure(disabledforeground="#a3a3a3")
		self.txtBodyHeight.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodyHeight.configure(foreground=_fgcolor)
		self.txtBodyHeight.configure(highlightbackground=_bgcolor)
		self.txtBodyHeight.configure(highlightcolor=_fgcolor)
		self.txtBodyHeight.configure(insertbackground=_fgcolor)
		self.txtBodyHeight.configure(selectbackground=_highlightbgcolor)
		self.txtBodyHeight.configure(selectforeground=_fgcolor)
		self.txtBodyHeight.configure(relief=FLAT)
		validateSupport = self.txtBodyHeight.register(self.validateFloat)
		self.txtBodyHeight.configure(validate="key")
		self.txtBodyHeight.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyHeight.bind("<Return>", self.onEnter)
		self.txtBodyHeight.bind("<Button-1>", self.loadData)

		self.txtBodyHeightTol = Entry(self.cnvsData)
		self.txtBodyHeightTol.place(relx=0.73, rely=0.38,height=20, relwidth=0.2)
		self.txtBodyHeightTol.configure(background=_bgcolor)
		self.txtBodyHeightTol.configure(disabledforeground="#a3a3a3")
		self.txtBodyHeightTol.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodyHeightTol.configure(foreground=_fgcolor)
		self.txtBodyHeightTol.configure(highlightbackground=_bgcolor)
		self.txtBodyHeightTol.configure(highlightcolor=_fgcolor)
		self.txtBodyHeightTol.configure(insertbackground=_fgcolor)
		self.txtBodyHeightTol.configure(selectbackground=_highlightbgcolor)
		self.txtBodyHeightTol.configure(selectforeground=_fgcolor)
		self.txtBodyHeightTol.configure(relief=FLAT)
		validateSupport = self.txtBodyHeightTol.register(self.validateFloat)
		self.txtBodyHeightTol.configure(validate="key")
		self.txtBodyHeightTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyHeightTol.bind("<Return>", self.onEnter)
		self.txtBodyHeightTol.bind("<Button-1>", self.loadData)

		self.txtBodyWidth = Entry(self.cnvsData)
		self.txtBodyWidth.place(relx=0.48, rely=0.495,height=20, relwidth=0.2)
		self.txtBodyWidth.configure(background=_bgcolor)
		self.txtBodyWidth.configure(disabledforeground="#a3a3a3")
		self.txtBodyWidth.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodyWidth.configure(foreground=_fgcolor)
		self.txtBodyWidth.configure(highlightbackground=_bgcolor)
		self.txtBodyWidth.configure(highlightcolor=_fgcolor)
		self.txtBodyWidth.configure(insertbackground=_fgcolor)
		self.txtBodyWidth.configure(selectbackground=_highlightbgcolor)
		self.txtBodyWidth.configure(selectforeground=_fgcolor)
		self.txtBodyWidth.configure(relief=FLAT)
		validateSupport = self.txtBodyWidth.register(self.validateFloat)
		self.txtBodyWidth.configure(validate="key")
		self.txtBodyWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyWidth.bind("<Return>", self.onEnter)
		self.txtBodyWidth.bind("<Button-1>", self.loadData)

		self.txtBodyWidthTol = Entry(self.cnvsData)
		self.txtBodyWidthTol.place(relx=0.73, rely=0.495,height=20, relwidth=0.2)
		self.txtBodyWidthTol.configure(background=_bgcolor)
		self.txtBodyWidthTol.configure(disabledforeground="#a3a3a3")
		self.txtBodyWidthTol.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodyWidthTol.configure(foreground=_fgcolor)
		self.txtBodyWidthTol.configure(highlightbackground=_bgcolor)
		self.txtBodyWidthTol.configure(highlightcolor=_fgcolor)
		self.txtBodyWidthTol.configure(insertbackground=_fgcolor)
		self.txtBodyWidthTol.configure(selectbackground=_highlightbgcolor)
		self.txtBodyWidthTol.configure(selectforeground=_fgcolor)
		self.txtBodyWidthTol.configure(relief=FLAT)
		validateSupport = self.txtBodyWidthTol.register(self.validateFloat)
		self.txtBodyWidthTol.configure(validate="key")
		self.txtBodyWidthTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyWidthTol.bind("<Return>", self.onEnter)
		self.txtBodyWidthTol.bind("<Button-1>", self.loadData)

		self.txtBodySweap = Entry(self.cnvsData)
		self.txtBodySweap.place(relx=0.48, rely=0.61,height=20, relwidth=0.2)
		self.txtBodySweap.configure(background=_bgcolor)
		self.txtBodySweap.configure(disabledforeground="#a3a3a3")
		self.txtBodySweap.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodySweap.configure(foreground=_fgcolor)
		self.txtBodySweap.configure(highlightbackground=_bgcolor)
		self.txtBodySweap.configure(highlightcolor=_fgcolor)
		self.txtBodySweap.configure(insertbackground=_fgcolor)
		self.txtBodySweap.configure(selectbackground=_highlightbgcolor)
		self.txtBodySweap.configure(selectforeground=_fgcolor)
		self.txtBodySweap.configure(relief=FLAT)
		validateSupport = self.txtBodySweap.register(self.validateFloat)
		self.txtBodySweap.configure(validate="key")
		self.txtBodySweap.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodySweap.bind("<Return>", self.onEnter)
		self.txtBodySweap.bind("<Button-1>", self.loadData)

		self.txtBodySweapTol = Entry(self.cnvsData)
		self.txtBodySweapTol.place(relx=0.73, rely=0.61,height=20, relwidth=0.2)
		self.txtBodySweapTol.configure(background=_bgcolor)
		self.txtBodySweapTol.configure(disabledforeground="#a3a3a3")
		self.txtBodySweapTol.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodySweapTol.configure(foreground=_fgcolor)
		self.txtBodySweapTol.configure(highlightbackground=_bgcolor)
		self.txtBodySweapTol.configure(highlightcolor=_fgcolor)
		self.txtBodySweapTol.configure(insertbackground=_fgcolor)
		self.txtBodySweapTol.configure(selectbackground=_highlightbgcolor)
		self.txtBodySweapTol.configure(selectforeground=_fgcolor)
		self.txtBodySweapTol.configure(relief=FLAT)
		validateSupport = self.txtBodySweapTol.register(self.validateFloat)
		self.txtBodySweapTol.configure(validate="key")
		self.txtBodySweapTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodySweapTol.bind("<Return>", self.onEnter)
		self.txtBodySweapTol.bind("<Button-1>", self.loadData)

		self.txtBackNeckWidth = Entry(self.cnvsData)
		self.txtBackNeckWidth.place(relx=0.48, rely=0.725, height=20, relwidth=0.2)
		self.txtBackNeckWidth.configure(background=_bgcolor)
		self.txtBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.txtBackNeckWidth.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBackNeckWidth.configure(foreground=_fgcolor)
		self.txtBackNeckWidth.configure(highlightbackground=_bgcolor)
		self.txtBackNeckWidth.configure(highlightcolor=_fgcolor)
		self.txtBackNeckWidth.configure(insertbackground=_fgcolor)
		self.txtBackNeckWidth.configure(selectbackground=_highlightbgcolor)
		self.txtBackNeckWidth.configure(selectforeground=_fgcolor)
		self.txtBackNeckWidth.configure(relief=FLAT)
		validateSupport = self.txtBackNeckWidth.register(self.validateFloat)
		self.txtBackNeckWidth.configure(validate="key")
		self.txtBackNeckWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBackNeckWidth.bind("<Return>", self.onEnter)
		self.txtBackNeckWidth.bind("<Button-1>", self.loadData)

		self.txtBackNeckWidthTol = Entry(self.cnvsData)
		self.txtBackNeckWidthTol.place(relx=0.73, rely=0.725, height=20, relwidth=0.2)
		self.txtBackNeckWidthTol.configure(background=_bgcolor)
		self.txtBackNeckWidthTol.configure(disabledforeground="#a3a3a3")
		self.txtBackNeckWidthTol.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBackNeckWidthTol.configure(foreground=_fgcolor)
		self.txtBackNeckWidthTol.configure(highlightbackground=_bgcolor)
		self.txtBackNeckWidthTol.configure(highlightcolor=_fgcolor)
		self.txtBackNeckWidthTol.configure(insertbackground=_fgcolor)
		self.txtBackNeckWidthTol.configure(selectbackground=_highlightbgcolor)
		self.txtBackNeckWidthTol.configure(selectforeground=_fgcolor)
		self.txtBackNeckWidthTol.configure(relief=FLAT)
		validateSupport = self.txtBackNeckWidthTol.register(self.validateFloat)
		self.txtBackNeckWidthTol.configure(validate="key")
		self.txtBackNeckWidthTol.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBackNeckWidthTol.bind("<Return>", self.onEnter)
		self.txtBackNeckWidthTol.bind("<Button-1>", self.loadData)

		self.frameRun = Frame(top)
		self.frameRun.place(relx=0.03, rely=0.82, relheight=0.18, relwidth=0.94)
		self.frameRun.configure(relief=FLAT)
		self.frameRun.configure(borderwidth="0.5")
		self.frameRun.configure(background=_bgcolor)
		self.frameRun.configure(highlightbackground=_bgcolor)
		self.frameRun.configure(highlightcolor=_fgcolor)
		self.frameRun.configure(width=355)

		self.btnRun = Button(self.frameRun)
		# self.btnRun.place(relx=0.2, rely=0.13, height=54, width=64)
		self.btnRun.place(relx=0.07, rely=0.2, height=54, width=300)
		self.btnRun.configure(activebackground="#008000")
		self.btnRun.configure(activeforeground=_fgcolor)
		self.btnRun.configure(background="#3A5FCD")
		# self.btnRun.configure(background=_bgcolor)
		self.btnRun.configure(cursor="hand2")
		self.btnRun.configure(relief=FLAT)
		self.btnRun.configure(disabledforeground=_fgcolor)
		self.btnRun.configure(foreground=_fgcolor)
		self.btnRun.configure(highlightbackground=_fgcolor)
		self.btnRun.configure(highlightcolor=_fgcolor)
		self.btnRun.configure(pady="0")
		self.btnRun.configure(state="normal")
		self.btnRun.configure(font=('Helvetica', 20, 'bold'))
		self.btnRun.configure(text='''Run''')
		# self.btnRun.configure(command=SmartTable_p3_4_Intimo2.getMeasurements)
		self.btnRun.configure(command=self.runMeasuring)

		# self.btnStop = Button(self.frameRun)
		# self.btnStop.place(relx=0.59, rely=0.13, height=54, width=64)
		# self.btnStop.configure(activebackground="red")
		# self.btnStop.configure(activeforeground=_fgcolor)
		# self.btnStop.configure(background="#FF4040")
		# self.btnStop.configure(cursor="hand2")
		# self.btnStop.configure(disabledforeground="#a3a3a3")
		# self.btnStop.configure(foreground=_fgcolor)
		# self.btnStop.configure(highlightbackground=_bgcolor)
		# self.btnStop.configure(highlightcolor=_fgcolor)
		# self.btnStop.configure(pady="0")
		# self.btnStop.configure(state=NORMAL)
		# self.btnStop.configure(text='''Stop''')
		# self.btnStop.configure(command=SmartTable_p3_4_Intimo2.testing)


# ~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~

initDatabase()


if __name__ == '__main__':
	vp_start_gui()

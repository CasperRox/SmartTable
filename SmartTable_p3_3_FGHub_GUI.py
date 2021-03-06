import sys
import SmartTable_p3_3_FGHub_GUI_support
import SmartTable_p3_3_FGHub
import SmartTable_p3_3_FGHub_GUI_2
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
	SmartTable_p3_3_FGHub_GUI_support.init(root, top)
	root.resizable(0,0)
	# root.after(100, SmartTable_p3_3_FGHub.loopTest)
	root.mainloop()

w = None
def create_Smart_Table(root, *args, **kwargs):
	'''Starting point when module is imported by another program.'''
	global w, w_win, rt
	rt = root
	w = Toplevel (root)
	top = Smart_Table (w)
	SmartTable_p3_3_FGHub_GUI_support.init(w, top, *args, **kwargs)
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
			create table if not exists TShirts (
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
			# cursor.execute("""
			# create table if not exists PolyTop_Records (
			# 	DateTime varchar(30) not null,
			# 	TableIndex varchar(10) not null,
			# 	Plant varchar(100) not null,
			# 	Style varchar(100) not null,
			# 	Size varchar(10) not null,
			# 	BodyHeight float(4,1) not null,
			# 	BodyHeightDif float(3,1) not null,
			# 	BodyWidth float(4,1) not null,
			# 	BodyWidthDif float(3,1) not null,
			# 	BodySweap float(4,1) not null,
			# 	BodySweapDif float(3,1) not null,
			# 	BackNeckWidth float(4,1) not null,
			# 	BackNeckWidthDif float(3,1) not null,
			# 	primary key(DateTime, TableIndex, Plant, Style, Size)
			# );
			# """)
			cursor.execute("""
			create table if not exists TShirt_Measurement_Records (
				DateTime varchar(30) not null,
				TableIndex varchar(10) not null,
				PONumber varchar(100) not null,
				LINumber varchar(100) not null,
				Plant varchar(100) not null,
				StyleNumber varchar(100) not null,
				Size varchar(10) not null,
				BodyLength float(4,1) not null,
				BodyWidth float(4,1) not null,
				BodySweep float(4,1) not null,
				BackNeckWidth float(4,1) not null,
				CollarHeight float(4,1) not null,
				BackNeckDrop float(4,1) not null,
				XDistance float(4,1) not null,
				WaistWidth float(4,1) not null,
				LSSleeveLength float(4,1) not null,
				SleeveWidth float(4,1) not null,
				ElbowWidth float(4,1) not null,
				ForeArmWidth float(4,1) not null,
				SleeveOpening float(4,1) not null,
				FrontNeckDrop float(4,1) not null,
				NeckOpening float(4,1) not null,
				CollarPoints float(4,1) not null,
				CollarLength float(4,1) not null,
				ZipperLength float(4,1) not null,
				DropTailLength float(4,1) not null,
				PocketHeight float(4,1) not null,
				primary key(DateTime, TableIndex, Plant, PONumber, LINumber, StyleNumber, Size)
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
				sql = "SELECT * FROM TShirts where Style=%s and Size=%s"
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
		po = self.txtPONumber.get()
		li = self.txtLINumber.get()
		pl = self.txtPlant.get()
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

		if not po:
			self.txtPONumber.focus()
			messagebox.showerror("Input Error", "Please enter valid PO Number")
		elif not li:
			self.txtLINumber.focus()
			messagebox.showerror("Input Error", "Please enter valid LI Number")
		elif not pl:
			self.txtPlant.focus()
			messagebox.showerror("Input Error", "Please enter valid Plant Name")
		elif not sN:
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
			# self.btnRun.configure(state = "disabled")
			self.btnRun.pack_forget()

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
						"INSERT INTO TShirts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
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

			try:
				# SmartTable_p3_3_FGHub.getMeasurements(sN, sz, bH, bHT, bW, bWT, bS, bST, bNW, bNWT, whiteMode)
				SmartTable_p3_3_FGHub_GUI_2.startGUI(po, li, pl, sN, sz, float(bH), float(bHT), float(bW), float(bWT), 
													float(bS), float(bST), float(bNW), float(bNWT), whiteMode)
			except Exception as e:
				print("[INFO] Caught a Runtime Error GUI 1")
				print("[INFO] Error type : " + str(e))
			# finally:
			# 	self.btnRun.configure(state = "normal")


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


		# top.geometry("377x550+150+200")
		UIWidth = 400
		UIHeight = 700
		top.geometry("{0}x{1}+150+0".format(UIWidth, UIHeight))
		# top.geometry("400x700+150+0")
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
		self.cnvsData.place(relx=0.03, rely=0.02, relheight=0.82, relwidth=0.94)
		self.cnvsData.configure(relief=FLAT)
		self.cnvsData.configure(borderwidth="0")
		self.cnvsData.configure(background=_bgcolor)
		# self.cnvsData.configure(background=_fgcolor)
		self.cnvsData.configure(highlightbackground=_bgcolor)
		self.cnvsData.configure(highlightcolor=_bgcolor)
		# self.cnvsData.configure(highlightbackground=_fgcolor)
		# self.cnvsData.configure(highlightcolor=_fgcolor)
		self.cnvsData.configure(width=355)
		# self.cnvsData.create_line(170,46,335,46, fill=_fgcolor, width="3", dash=(4,2))
		cnvDataWidth = UIWidth * 0.94
		cnvDataHeight = UIHeight * 0.82
		# self.cnvsData.create_line(170,46,335,46, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.085, cnvDataWidth*0.96, cnvDataHeight*0.085, fill=_fgcolor, width="1")		# (x1,y1,x2,y2)
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.165, cnvDataWidth*0.96, cnvDataHeight*0.165, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.245, cnvDataWidth*0.96, cnvDataHeight*0.245, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.325, cnvDataWidth*0.96, cnvDataHeight*0.325, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.405, cnvDataWidth*0.96, cnvDataHeight*0.405, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.585, cnvDataWidth*0.73, cnvDataHeight*0.585, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.77, cnvDataHeight*0.585, cnvDataWidth*0.96, cnvDataHeight*0.585, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.665, cnvDataWidth*0.73, cnvDataHeight*0.665, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.77, cnvDataHeight*0.665, cnvDataWidth*0.96, cnvDataHeight*0.665, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.745, cnvDataWidth*0.73, cnvDataHeight*0.745, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.77, cnvDataHeight*0.745, cnvDataWidth*0.96, cnvDataHeight*0.745, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.54, cnvDataHeight*0.825, cnvDataWidth*0.73, cnvDataHeight*0.825, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.77, cnvDataHeight*0.825, cnvDataWidth*0.96, cnvDataHeight*0.825, fill=_fgcolor, width="1")

		self.lblPONumber = Label(self.cnvsData)
		self.lblPONumber.place(relx=0.04, rely=0.04, relheight=0.04, relwidth=0.42)
		self.lblPONumber.configure(activebackground="#f9f9f9")
		self.lblPONumber.configure(activeforeground=_fgcolor)
		self.lblPONumber.configure(background=_bgcolor)
		self.lblPONumber.configure(disabledforeground="#a3a3a3")
		self.lblPONumber.configure(foreground=_fgcolor)
		self.lblPONumber.configure(highlightbackground=_bgcolor)
		self.lblPONumber.configure(highlightcolor=_fgcolor)
		self.lblPONumber.configure(font=('Helvetica', 9, 'bold'))
		self.lblPONumber.configure(text='''PO Number''')
		self.lblPONumber.configure(anchor='w')

		self.lblLINumber = Label(self.cnvsData)
		self.lblLINumber.place(relx=0.04, rely=0.12, relheight=0.04, relwidth=0.42)
		self.lblLINumber.configure(activebackground="#f9f9f9")
		self.lblLINumber.configure(activeforeground=_fgcolor)
		self.lblLINumber.configure(background=_bgcolor)
		self.lblLINumber.configure(disabledforeground="#a3a3a3")
		self.lblLINumber.configure(foreground=_fgcolor)
		self.lblLINumber.configure(highlightbackground=_bgcolor)
		self.lblLINumber.configure(highlightcolor=_fgcolor)
		self.lblLINumber.configure(font=('Helvetica', 9, 'bold'))
		self.lblLINumber.configure(text='''LI Number''')
		self.lblLINumber.configure(anchor='w')

		self.lblPlant = Label(self.cnvsData)
		self.lblPlant.place(relx=0.04, rely=0.20, relheight=0.04, relwidth=0.42)
		self.lblPlant.configure(activebackground="#f9f9f9")
		self.lblPlant.configure(activeforeground=_fgcolor)
		self.lblPlant.configure(background=_bgcolor)
		self.lblPlant.configure(disabledforeground="#a3a3a3")
		self.lblPlant.configure(foreground=_fgcolor)
		self.lblPlant.configure(highlightbackground=_bgcolor)
		self.lblPlant.configure(highlightcolor=_fgcolor)
		self.lblPlant.configure(font=('Helvetica', 9, 'bold'))
		self.lblPlant.configure(text='''Plant''')
		self.lblPlant.configure(anchor='w')

		self.lblStyleNo = Label(self.cnvsData)
		self.lblStyleNo.place(relx=0.04, rely=0.28, relheight=0.04, relwidth=0.42)
		self.lblStyleNo.configure(activebackground="#f9f9f9")
		self.lblStyleNo.configure(activeforeground=_fgcolor)
		self.lblStyleNo.configure(background=_bgcolor)
		self.lblStyleNo.configure(disabledforeground="#a3a3a3")
		self.lblStyleNo.configure(foreground=_fgcolor)
		self.lblStyleNo.configure(highlightbackground=_bgcolor)
		self.lblStyleNo.configure(highlightcolor=_fgcolor)
		self.lblStyleNo.configure(font=('Helvetica', 9, 'bold'))
		self.lblStyleNo.configure(text='''Style No.''')
		self.lblStyleNo.configure(anchor='w')

		self.lblSize = Label(self.cnvsData)
		self.lblSize.place(relx=0.04, rely=0.36, relheight=0.04, relwidth=0.42)
		self.lblSize.configure(activebackground="#f9f9f9")
		self.lblSize.configure(activeforeground=_fgcolor)
		self.lblSize.configure(background=_bgcolor)
		self.lblSize.configure(disabledforeground="#a3a3a3")
		self.lblSize.configure(foreground=_fgcolor)
		self.lblSize.configure(highlightbackground=_bgcolor)
		self.lblSize.configure(highlightcolor=_fgcolor)
		self.lblSize.configure(font=('Helvetica', 9, 'bold'))
		self.lblSize.configure(text='''Size''')
		self.lblSize.configure(anchor='w')

		self.lblTol = Label(self.cnvsData)
		self.lblTol.place(relx=0.70, rely=0.50, relheight=0.04, relwidth=0.26)
		self.lblTol.configure(activebackground="#f9f9f9")
		self.lblTol.configure(activeforeground=_fgcolor)
		self.lblTol.configure(background=_bgcolor)
		self.lblTol.configure(disabledforeground="#a3a3a3")
		self.lblTol.configure(foreground=_fgcolor)
		self.lblTol.configure(highlightbackground=_bgcolor)
		self.lblTol.configure(highlightcolor=_fgcolor)
		self.lblTol.configure(font=('Helvetica', 9, 'bold'))
		self.lblTol.configure(text='''Tolerance (cm)''')

		self.lblBodyHeight = Label(self.cnvsData)
		self.lblBodyHeight.place(relx=0.04, rely=0.54, relheight=0.04, relwidth=0.42)
		self.lblBodyHeight.configure(activebackground="#f9f9f9")
		self.lblBodyHeight.configure(activeforeground=_fgcolor)
		self.lblBodyHeight.configure(background=_bgcolor)
		self.lblBodyHeight.configure(disabledforeground="#a3a3a3")
		self.lblBodyHeight.configure(foreground=_fgcolor)
		self.lblBodyHeight.configure(highlightbackground=_bgcolor)
		self.lblBodyHeight.configure(highlightcolor=_fgcolor)
		self.lblBodyHeight.configure(font=('Helvetica', 9, 'bold'))
		self.lblBodyHeight.configure(text='''Body Length (cm)''')
		self.lblBodyHeight.configure(anchor='w')

		self.lblBodyWidth = Label(self.cnvsData)
		self.lblBodyWidth.place(relx=0.04, rely=0.62, relheight=0.04, relwidth=0.42)
		self.lblBodyWidth.configure(activebackground="#f9f9f9")
		self.lblBodyWidth.configure(activeforeground=_fgcolor)
		self.lblBodyWidth.configure(background=_bgcolor)
		self.lblBodyWidth.configure(disabledforeground="#a3a3a3")
		self.lblBodyWidth.configure(foreground=_fgcolor)
		self.lblBodyWidth.configure(highlightbackground=_bgcolor)
		self.lblBodyWidth.configure(highlightcolor=_fgcolor)
		self.lblBodyWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblBodyWidth.configure(text='''Body Width (cm)''')
		self.lblBodyWidth.configure(anchor='w')

		self.lblBodySweap = Label(self.cnvsData)
		self.lblBodySweap.place(relx=0.04, rely=0.70, relheight=0.04, relwidth=0.42)
		self.lblBodySweap.configure(activebackground="#f9f9f9")
		self.lblBodySweap.configure(activeforeground=_fgcolor)
		self.lblBodySweap.configure(background=_bgcolor)
		self.lblBodySweap.configure(disabledforeground="#a3a3a3")
		self.lblBodySweap.configure(foreground=_fgcolor)
		self.lblBodySweap.configure(highlightbackground=_bgcolor)
		self.lblBodySweap.configure(highlightcolor=_fgcolor)
		self.lblBodySweap.configure(font=('Helvetica', 9, 'bold'))
		self.lblBodySweap.configure(text='''Body Sweep (cm)''')
		self.lblBodySweap.configure(anchor='w')

		self.lblBackNeckWidth = Label(self.cnvsData)
		self.lblBackNeckWidth.place(relx=0.04, rely=0.78, relheight=0.04, relwidth=0.42)
		self.lblBackNeckWidth.configure(activebackground="#f9f9f9")
		self.lblBackNeckWidth.configure(activeforeground=_fgcolor)
		self.lblBackNeckWidth.configure(background=_bgcolor)
		self.lblBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.lblBackNeckWidth.configure(foreground=_fgcolor)
		self.lblBackNeckWidth.configure(highlightbackground=_bgcolor)
		self.lblBackNeckWidth.configure(highlightcolor=_fgcolor)
		self.lblBackNeckWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblBackNeckWidth.configure(text='''Back Neck Width (cm)''')
		self.lblBackNeckWidth.configure(anchor='w')

		self.lblWhiteGarmentMode = Label(self.cnvsData)
		self.lblWhiteGarmentMode.place(relx=0.04, rely=0.92, relheight=0.04, relwidth=0.42)
		self.lblWhiteGarmentMode.configure(activebackground="#f9f9f9")
		self.lblWhiteGarmentMode.configure(activeforeground=_fgcolor)
		self.lblWhiteGarmentMode.configure(background=_bgcolor)
		self.lblWhiteGarmentMode.configure(disabledforeground="#a3a3a3")
		self.lblWhiteGarmentMode.configure(foreground=_fgcolor)
		self.lblWhiteGarmentMode.configure(highlightbackground=_bgcolor)
		self.lblWhiteGarmentMode.configure(highlightcolor=_fgcolor)
		self.lblWhiteGarmentMode.configure(font=('Helvetica', 9, 'bold'))
		self.lblWhiteGarmentMode.configure(text='''White Garment Mode''')
		self.lblWhiteGarmentMode.configure(anchor='w')

		self.onoff = StringVar()
		self.onoff.set("OFF")

		self.lblWhiteGarmentStatus = Label(self.cnvsData)
		self.lblWhiteGarmentStatus.place(relx=0.54, rely=0.92, relheight=0.04, relwidth=0.19)
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
		self.btnOnOff.place(relx=0.77, rely=0.92, relheight=0.04, relwidth=0.19)
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
		self.btnOnOff.configure(font=('Helvetica', 9, 'bold'))
		self.btnOnOff.configure(text='''ON / OFF''')
		self.btnOnOff.configure(command=self.whiteGarmentModeOnOff)

		self.txtPONumber = Entry(self.cnvsData)
		self.txtPONumber.place(relx=0.54, rely=0.04, relheight=0.04, relwidth=0.42)
		self.txtPONumber.configure(background=_bgcolor)
		self.txtPONumber.configure(disabledforeground="#a3a3a3")
		self.txtPONumber.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtPONumber.configure(foreground=_fgcolor)
		self.txtPONumber.configure(highlightbackground=_bgcolor)
		self.txtPONumber.configure(highlightcolor=_fgcolor)
		self.txtPONumber.configure(insertbackground=_fgcolor)
		self.txtPONumber.configure(selectbackground=_highlightbgcolor)
		self.txtPONumber.configure(selectforeground=_fgcolor)
		self.txtPONumber.configure(relief=FLAT)

		self.txtPONumber.focus()
		# self.txtPONumber.bind("<Key>", click)
		self.txtPONumber.bind("<Return>", self.onEnter)
		# self.txtPONumber.bind("<Return>", lambda event: self.txtLINumber.focus())

		self.txtLINumber = Entry(self.cnvsData)
		self.txtLINumber.place(relx=0.54, rely=0.12, relheight=0.04, relwidth=0.42)
		self.txtLINumber.configure(background=_bgcolor)
		self.txtLINumber.configure(disabledforeground="#a3a3a3")
		self.txtLINumber.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtLINumber.configure(foreground=_fgcolor)
		self.txtLINumber.configure(highlightbackground=_bgcolor)
		self.txtLINumber.configure(highlightcolor=_fgcolor)
		self.txtLINumber.configure(insertbackground=_fgcolor)
		self.txtLINumber.configure(selectbackground=_highlightbgcolor)
		self.txtLINumber.configure(selectforeground=_fgcolor)
		self.txtLINumber.configure(relief=FLAT)

		self.txtLINumber.bind("<Return>", self.onEnter)

		self.txtPlant = Entry(self.cnvsData)
		self.txtPlant.place(relx=0.54, rely=0.20, relheight=0.04, relwidth=0.42)
		self.txtPlant.configure(background=_bgcolor)
		self.txtPlant.configure(disabledforeground="#a3a3a3")
		self.txtPlant.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtPlant.configure(foreground=_fgcolor)
		self.txtPlant.configure(highlightbackground=_bgcolor)
		self.txtPlant.configure(highlightcolor=_fgcolor)
		self.txtPlant.configure(insertbackground=_fgcolor)
		self.txtPlant.configure(selectbackground=_highlightbgcolor)
		self.txtPlant.configure(selectforeground=_fgcolor)
		self.txtPlant.configure(relief=FLAT)

		self.txtPlant.bind("<Return>", self.onEnter)

		self.txtStyleNo = Entry(self.cnvsData)
		self.txtStyleNo.place(relx=0.54, rely=0.28, relheight=0.04, relwidth=0.42)
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

		# self.txtStyleNo.focus()
		self.txtStyleNo.bind("<Return>", self.onEnter)

		self.txtSize = Entry(self.cnvsData)
		self.txtSize.place(relx=0.54, rely=0.36, relheight=0.04, relwidth=0.42)
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
		self.txtBodyHeight.place(relx=0.54, rely=0.54, relheight=0.04, relwidth=0.19)
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
		self.txtBodyHeightTol.place(relx=0.77, rely=0.54, relheight=0.04, relwidth=0.19)
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
		self.txtBodyWidth.place(relx=0.54, rely=0.62, relheight=0.04, relwidth=0.19)
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
		self.txtBodyWidthTol.place(relx=0.77, rely=0.62, relheight=0.04, relwidth=0.19)
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
		self.txtBodySweap.place(relx=0.54, rely=0.70, relheight=0.04, relwidth=0.19)
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
		self.txtBodySweapTol.place(relx=0.77, rely=0.70, relheight=0.04, relwidth=0.19)
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
		self.txtBackNeckWidth.place(relx=0.54, rely=0.78, relheight=0.04, relwidth=0.19)
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
		self.txtBackNeckWidthTol.place(relx=0.77, rely=0.78, relheight=0.04, relwidth=0.19)
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
		self.frameRun.place(relx=0.03, rely=0.86, relheight=0.12, relwidth=0.94)
		self.frameRun.configure(relief=FLAT)
		self.frameRun.configure(borderwidth="0.5")
		self.frameRun.configure(background=_bgcolor)
		# self.frameRun.configure(background=_fgcolor)
		self.frameRun.configure(highlightbackground=_bgcolor)
		self.frameRun.configure(highlightcolor=_fgcolor)
		self.frameRun.configure(width=355)

		self.btnRun = Button(self.frameRun)
		# self.btnRun.place(relx=0.2, rely=0.13, height=54, width=64)
		self.btnRun.place(relx=0.10, rely=0.15, relheight=0.70, relwidth=0.80)
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
		self.btnRun.configure(font=('Helvetica', 30, 'bold'))
		self.btnRun.configure(text='''Run''')
		# self.btnRun.configure(command=SmartTable_p3_3_FGHub.getMeasurements)
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
		# self.btnStop.configure(command=SmartTable_p3_3_FGHub.testing)


# ~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~

initDatabase()


if __name__ == '__main__':
	vp_start_gui()

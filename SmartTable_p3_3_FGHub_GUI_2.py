import sys
import SmartTable_p3_3_FGHub_GUI_2_support
import SmartTable_p3_3_FGHub
import pymysql.cursors
import numpy as np
import cv2
import math
import threading
from PIL import Image as PILImage
from PIL import ImageTk
import time
import datetime

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
	global val, w2, root

	root = Tk()
	top = Smart_Table (root)
	SmartTable_p3_3_FGHub_GUI_2_support.init(root, top)
	root.resizable(0,0)
	root.mainloop()


def startGUI(po, li, pl, sN, sz, bH, bHT, bW, bWT, bS, bST, bNW, bNWT, wM):
	global root
	global poNumber, liNumber, plant, styleNumber, size, targetBodyHeight, bodyHeightTol, targetBodyWidth
	global bodyWidthTol, targetBodySweep, bodySweepTol, targetBackNeckWidth, backNeckWidthTol, whiteMode

	poNumber = po
	liNumber = li
	plant = pl
	styleNumber = sN
	size = sz
	targetBodyHeight = bH
	bodyHeightTol = bHT
	targetBodyWidth = bW
	bodyWidthTol = bWT
	targetBodySweep = bS
	bodySweepTol = bST
	targetBackNeckWidth = bNW
	backNeckWidthTol = bNWT
	whiteMode = wM

	vp_start_gui()
	create_Smart_Table(root)
	# create_Smart_Table()


w2 = None
def create_Smart_Table(root, *args, **kwargs):
	'''Starting point when module is imported by another program.'''
	global w2, w_win, rt
	rt = root
	w2 = Toplevel (root)
	top = Smart_Table (w2)
	SmartTable_p3_3_FGHub_GUI_2_support.init(w2, top, *args, **kwargs)
	return (w2, top)

def destroy_Smart_Table():
	global w2, thread

	print("[INFO] Closing...")
	stopEvent.set()
	thread.join()

	w2.destroy()
	w2 = None


def initSerialRead():
	global ser

	try:
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if " CH340 " in p.description:
				des = p.description				# "USB-SERIAL CH340 (COM15)" supposed to be come, since Arduino Nano uses CH340 chip for serial communication
		serialPort = 'COM' + des[(des.rfind("COM")+3):(des.rfind(")"))]
		# ser = serial.Serial(serialPort, 9600, timeout=1)			# comport, baud-rate, timeout=the max time between two button press events to capture them within one buffer
		ser = serial.Serial(serialPort, 9600, timeout=0)			# comport, baud-rate, timeout=the max time between two button press events to capture them within one buffer
	except NameError:
		print("\n***** Error: Serial communication port is not connected properly\n")


class Smart_Table:

	def onEnter(self, event):
		# print (event.char)
		widget = event.widget
		# print ("search " + widget.get())
		if widget == self.txtBodyLength:
			self.txtBodyWidth.focus()
		elif widget == self.txtBodyWidth:
			self.txtBodySweep.focus()
			# self.loadData(event)
		elif widget == self.txtBodySweep:
			self.txtBackNeckWidth.focus()
		elif widget == self.txtBackNeckWidth:
			self.txtCollarHeight.focus()
		elif widget == self.txtCollarHeight:
			self.txtBackNeckDrop.focus()
		elif widget == self.txtBackNeckDrop:
			self.txtXDistance.focus()
		elif widget == self.txtXDistance:
			self.txtBodyWaistWidth.focus()
		elif widget == self.txtBodyWaistWidth:
			self.txtLSSleeveLength.focus()
		elif widget == self.txtLSSleeveLength:
			self.txtSleeveWidth.focus()
		elif widget == self.txtSleeveWidth:
			self.txtElbowWidth.focus()
		elif widget == self.txtElbowWidth:
			self.txtForeArmWidth.focus()
		elif widget == self.txtForeArmWidth:
			self.txtSleeveOpening.focus()
		elif widget == self.txtSleeveOpening:
			self.txtFrontNeckDrop.focus()
		elif widget == self.txtFrontNeckDrop:
			self.txtNeckOpening.focus()
		elif widget == self.txtNeckOpening:
			self.txtCollarPoints.focus()
		elif widget == self.txtCollarPoints:
			self.txtCollarLength.focus()
		elif widget == self.txtCollarLength:
			self.txtZipperLength.focus()
		elif widget == self.txtZipperLength:
			self.txtDropTailLength.focus()
		elif widget == self.txtDropTailLength:
			self.txtPocketHeight.focus()
		elif widget == self.txtPocketHeight:
			self.btnSave.focus()


	def liveMeasuring(self):
		global ser, buttonPressed
		global poNumber, liNumber, plant, styleNumber, size, targetBodyHeight, bodyHeightTol, targetBodyWidth
		global bodyWidthTol, targetBodySweep, bodySweepTol, targetBackNeckWidth, backNeckWidthTol, whiteMode
		global thread, stopEvent

		SmartTable_p3_3_FGHub.loadCalibrationData()

		cap = cv2.VideoCapture(0)
		# cap = cv2.VideoCapture("E:\SmartTable_Test\WIN_20181220_12_37_36_Pro.mp4")

		UIWidth = root.winfo_screenwidth()
		UIHeight = root.winfo_screenheight()-60

		try:
			# while(True):
			while not stopEvent.is_set():
				buttonPressed = False
				# Capture frame-by-frame
				ret, frame = cap.read()
				if ret:
					(height, width) = frame.shape[:2]
					# print("height ", height, "width ", width)
					frame = frame[0:height, int(60/640*width):int(620/640*width)]			# 480, 560 # This is correct crop for SmartTable in Vaanavil
					# frame = cv2.resize(frame, (int(width*0.17),int(height*0.17)))
					frame, bodyLength, bodyWidth, bodySweep, backNeckWidth = SmartTable_p3_3_FGHub.tshirtMeasuring(frame, 
											poNumber, liNumber, plant, styleNumber, size, targetBodyHeight, bodyHeightTol, targetBodyWidth,
											bodyWidthTol, targetBodySweep, bodySweepTol, targetBackNeckWidth, backNeckWidthTol, whiteMode)						# Process live video
					# frame = cv2.resize(frame, (int(UIWidth*0.69*0.98),int(UIHeight*0.96*0.98)))
					frame = cv2.resize(frame, (int(UIWidth*0.69),int(UIHeight*0.96)))
					# cv2.namedWindow("Smart Table", cv2.WINDOW_NORMAL)
					# cv2.imshow("Smart Table", frame)
					# cv2.waitKey(1)
					frame = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
					frame = PILImage.fromarray(frame)
					frame = ImageTk.PhotoImage(frame, master=root)
					self.lblImage.configure(image=frame)
					self.lblImage.image = frame
					if bodyLength > 0:
						self.txtBodyLength.delete(0,len(self.txtBodyLength.get()))
						self.txtBodyLength.insert(0, bodyLength)
					if bodyWidth > 0:
						self.txtBodyWidth.delete(0,len(self.txtBodyWidth.get()))
						self.txtBodyWidth.insert(0, bodyWidth)
					if bodySweep > 0:
						self.txtBodySweep.delete(0,len(self.txtBodySweep.get()))
						self.txtBodySweep.insert(0, bodySweep)
					if backNeckWidth > 0:
						self.txtBackNeckWidth.delete(0,len(self.txtBackNeckWidth.get()))
						self.txtBackNeckWidth.insert(0, backNeckWidth)
					if buttonPressed:
						time.sleep(2)

				# if cv2.waitKey(1) & 0xFF == ord('q'):					# "q" key to quit
				# 	print("q")
				# 	break
				# if cv2.waitKey(1) & 0xFF == ord('Q'):					# "Q" key to quit
				# 	print("Q")
				# 	break
				# self.stopEvent.set()

			# When everything done, release the capture
			cap.release()
			cv2.destroyAllWindows()

		except Exception as e:
			print("[INFO] Caught a Runtime Error GUI 2")
			print("[INFO] Error type : " + str(e))

	# def liveTest(self):
	# 	cap = cv2.VideoCapture(0)
	# 	# cap = cv2.VideoCapture("E:\SmartTable_Test\WIN_20181220_12_37_36_Pro.mp4")

	# 	UIWidth = root.winfo_screenwidth()
	# 	UIHeight = root.winfo_screenheight()

	# 	while(True):
	# 		# Capture frame-by-frame
	# 		ret, frame = cap.read()
	# 		if ret:
	# 			(height, width) = frame.shape[:2]
	# 			# print("height ", height, "width ", width)
	# 			frame = frame[0:height, int(60/640*width):int(620/640*width)]			# 480, 560 # This is correct crop for SmartTable in Vaanavil
	# 			# frame = cv2.resize(frame, (int(width*0.17),int(height*0.17)))
	# 			# frame = cv2.resize(frame, (int(UIWidth*0.69*0.98),int(UIHeight*0.96*0.98)))
	# 			frame = cv2.resize(frame, (int(UIWidth*0.69),int(UIHeight*0.96)))
	# 			# cv2.namedWindow("Smart Table", cv2.WINDOW_NORMAL)
	# 			# cv2.imshow("Smart Table", frame)
	# 			frame = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
	# 			frame = PILImage.fromarray(frame)
	# 			frame = ImageTk.PhotoImage(frame)
	# 			self.lblImage.configure(image=frame)
	# 			self.lblImage.image = frame
	# 			cv2.waitKey(1)

	# 		if cv2.waitKey(1) & 0xFF == ord('q'):					# "q" key to quit
	# 			print("q")
	# 			break
	# 		if cv2.waitKey(1) & 0xFF == ord('Q'):					# "Q" key to quit
	# 			print("Q")
	# 			break

	# 	# When everything done, release the capture
	# 	cap.release()
	# 	cv2.destroyAllWindows()


	def saveMeasurements(self):
		global tableIndex, poNumber, liNumber, plant, styleNumber, size

		# if len(self.txtBodyLength.get()) == 0:
		# 	bodyLength = 0.0
		# else:
		# 	bodyLength = round(float(self.txtBodyLength.get()),1)

		bodyLength = 0.0 if len(self.txtBodyLength.get()) == 0 else round(float(self.txtBodyLength.get()),1)
		bodyWidth = 0.0 if len(self.txtBodyWidth.get()) == 0 else round(float(self.txtBodyWidth.get()),1)
		bodySweep = 0.0 if len(self.txtBodySweep.get()) == 0 else round(float(self.txtBodySweep.get()),1)
		backNeckWidth = 0.0 if len(self.txtBackNeckWidth.get()) == 0 else round(float(self.txtBackNeckWidth.get()),1)
		collarHeight = 0.0 if len(self.txtCollarHeight.get()) == 0 else round(float(self.txtCollarHeight.get()),1)
		backNeckDrop = 0.0 if len(self.txtBackNeckDrop.get()) == 0 else round(float(self.txtBackNeckDrop.get()),1)
		xDistance = 0.0 if len(self.txtXDistance.get()) == 0 else round(float(self.txtXDistance.get()),1)
		waistWidth = 0.0 if len(self.txtBodyWaistWidth.get()) == 0 else round(float(self.txtBodyWaistWidth.get()),1)
		lSSleeveLength = 0.0 if len(self.txtLSSleeveLength.get()) == 0 else round(float(self.txtLSSleeveLength.get()),1)
		sleeveWidth = 0.0 if len(self.txtSleeveWidth.get()) == 0 else round(float(self.txtSleeveWidth.get()),1)
		elbowWidth = 0.0 if len(self.txtElbowWidth.get()) == 0 else round(float(self.txtElbowWidth.get()),1)
		foreArmWidth = 0.0 if len(self.txtForeArmWidth.get()) == 0 else round(float(self.txtForeArmWidth.get()),1)
		sleeveOpening = 0.0 if len(self.txtSleeveOpening.get()) == 0 else round(float(self.txtSleeveOpening.get()),1)
		frontNeckDrop = 0.0 if len(self.txtFrontNeckDrop.get()) == 0 else round(float(self.txtFrontNeckDrop.get()),1)
		neckOpening = 0.0 if len(self.txtNeckOpening.get()) == 0 else round(float(self.txtNeckOpening.get()),1)
		collarPoints = 0.0 if len(self.txtCollarPoints.get()) == 0 else round(float(self.txtCollarPoints.get()),1)
		collarLength = 0.0 if len(self.txtCollarLength.get()) == 0 else round(float(self.txtCollarLength.get()),1)
		zipperLength = 0.0 if len(self.txtZipperLength.get()) == 0 else round(float(self.txtZipperLength.get()),1)
		dropTailLength = 0.0 if len(self.txtDropTailLength.get()) == 0 else round(float(self.txtDropTailLength.get()),1)
		pocketHeight = 0.0 if len(self.txtPocketHeight.get()) == 0 else round(float(self.txtPocketHeight.get()),1)

		connection = pymysql.connect(host='localhost',
									user='root',
									password='password',
									charset='utf8mb4',
									cursorclass=pymysql.cursors.DictCursor)

		try:
			with connection.cursor() as cursor:
				cursor.execute("use nmc")
				sql = (
					"INSERT INTO TShirt_Measurement_Records VALUES "
					"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
					"ON DUPLICATE KEY UPDATE "
					# "DateTime = %s, TableIndex = %s, PONumber = %s, LINumber = %s, Plant = %s, StyleNumber = %s, Size = %s, "
					"BodyLength = %s, BodyWidth = %s, BodySweep = %s, BackNeckWidth = %s, CollarHeight = %s, BackNeckDrop = %s, "
					"XDistance = %s, WaistWidth = %s, LSSleeveLength = %s, SleeveWidth = %s, ElbowWidth = %s, ForeArmWidth = %s, "
					"SleeveOpening = %s, FrontNeckDrop = %s, NeckOpening = %s, CollarPoints = %s, CollarLength = %s, "
					"ZipperLength = %s, DropTailLength = %s, PocketHeight = %s"
				)
				cursor.execute(sql, (datetime.datetime.now(), tableIndex, poNumber, liNumber, plant, styleNumber, size, bodyLength, 
									bodyWidth, bodySweep, backNeckWidth, collarHeight, backNeckDrop, xDistance, waistWidth,
									lSSleeveLength, sleeveWidth, elbowWidth, foreArmWidth, sleeveOpening, frontNeckDrop, 
									neckOpening, collarPoints, collarLength, zipperLength, dropTailLength, pocketHeight,
									# datetime.datetime.now(), tableIndex, poNumber, liNumber, plant, styleNumber, size, 
									bodyLength, bodyWidth, bodySweep, backNeckWidth, collarHeight, backNeckDrop, xDistance, waistWidth,
									lSSleeveLength, sleeveWidth, elbowWidth, foreArmWidth, sleeveOpening, frontNeckDrop, 
									neckOpening, collarPoints, collarLength, zipperLength, dropTailLength, pocketHeight))
			connection.commit()
		finally:
			connection.close()


		# messagebox.showwarning("Saved", "Measurement Values Saved")
		time.sleep(2)

		print("saved @ ", datetime.datetime.now())

		self.txtBodyLength.delete(0,len(self.txtBodyLength.get()))
		self.txtBodyLength.insert(0,"")
		self.txtBodyWidth.delete(0,len(self.txtBodyWidth.get()))
		self.txtBodyWidth.insert(0,"")
		self.txtBodySweep.delete(0,len(self.txtBodySweep.get()))
		self.txtBodySweep.insert(0,"")
		self.txtBackNeckWidth.delete(0,len(self.txtBackNeckWidth.get()))
		self.txtBackNeckWidth.insert(0,"")
		self.txtCollarHeight.delete(0,len(self.txtCollarHeight.get()))
		self.txtCollarHeight.insert(0,"")
		self.txtBackNeckDrop.delete(0,len(self.txtBackNeckDrop.get()))
		self.txtBackNeckDrop.insert(0,"")
		self.txtXDistance.delete(0,len(self.txtXDistance.get()))
		self.txtXDistance.insert(0,"")
		self.txtBodyWaistWidth.delete(0,len(self.txtBodyWaistWidth.get()))
		self.txtBodyWaistWidth.insert(0,"")
		self.txtLSSleeveLength.delete(0,len(self.txtLSSleeveLength.get()))
		self.txtLSSleeveLength.insert(0,"")
		self.txtSleeveWidth.delete(0,len(self.txtSleeveWidth.get()))
		self.txtSleeveWidth.insert(0,"")
		self.txtElbowWidth.delete(0,len(self.txtElbowWidth.get()))
		self.txtElbowWidth.insert(0,"")
		self.txtForeArmWidth.delete(0,len(self.txtForeArmWidth.get()))
		self.txtForeArmWidth.insert(0,"")
		self.txtSleeveOpening.delete(0,len(self.txtSleeveOpening.get()))
		self.txtSleeveOpening.insert(0,"")
		self.txtFrontNeckDrop.delete(0,len(self.txtFrontNeckDrop.get()))
		self.txtFrontNeckDrop.insert(0,"")
		self.txtNeckOpening.delete(0,len(self.txtNeckOpening.get()))
		self.txtNeckOpening.insert(0,"")
		self.txtCollarPoints.delete(0,len(self.txtCollarPoints.get()))
		self.txtCollarPoints.insert(0,"")
		self.txtCollarLength.delete(0,len(self.txtCollarLength.get()))
		self.txtCollarLength.insert(0,"")
		self.txtZipperLength.delete(0,len(self.txtZipperLength.get()))
		self.txtZipperLength.insert(0,"")
		self.txtDropTailLength.delete(0,len(self.txtDropTailLength.get()))
		self.txtDropTailLength.insert(0,"")
		self.txtPocketHeight.delete(0,len(self.txtPocketHeight.get()))
		self.txtPocketHeight.insert(0,"")


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

		global thread, stopEvent

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
		UIWidth = root.winfo_screenwidth()
		UIHeight = root.winfo_screenheight()-60
		top.geometry("{0}x{1}+-8+0".format(UIWidth, UIHeight))
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
		self.cnvsData.place(relx=0.01, rely=0.02, relheight=0.88, relwidth=0.28)
		self.cnvsData.configure(relief=FLAT)
		self.cnvsData.configure(borderwidth="0")
		self.cnvsData.configure(background=_bgcolor)
		self.cnvsData.configure(highlightbackground=_bgcolor)
		self.cnvsData.configure(highlightcolor=_bgcolor)
		# self.cnvsData.configure(background=_fgcolor)
		# self.cnvsData.configure(highlightbackground=_fgcolor)
		# self.cnvsData.configure(highlightcolor=_fgcolor)
		# self.cnvsData.configure(width=355)
		# self.cnvsData.create_line(170,46,335,46, fill=_fgcolor, width="3", dash=(4,2))
		cnvDataWidth = UIWidth * 0.28
		cnvDataHeight = UIHeight * 0.88
		# self.cnvsData.create_line(170,100,335,100, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.045, cnvDataWidth*0.98, cnvDataHeight*0.045, fill=_fgcolor, width="1")		# (x1,y1,x2,y2)
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.095, cnvDataWidth*0.98, cnvDataHeight*0.095, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.145, cnvDataWidth*0.98, cnvDataHeight*0.145, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.195, cnvDataWidth*0.98, cnvDataHeight*0.195, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.245, cnvDataWidth*0.98, cnvDataHeight*0.245, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.295, cnvDataWidth*0.98, cnvDataHeight*0.295, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.345, cnvDataWidth*0.98, cnvDataHeight*0.345, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.395, cnvDataWidth*0.98, cnvDataHeight*0.395, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.445, cnvDataWidth*0.98, cnvDataHeight*0.445, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.495, cnvDataWidth*0.98, cnvDataHeight*0.495, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.545, cnvDataWidth*0.98, cnvDataHeight*0.545, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.595, cnvDataWidth*0.98, cnvDataHeight*0.595, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.645, cnvDataWidth*0.98, cnvDataHeight*0.645, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.695, cnvDataWidth*0.98, cnvDataHeight*0.695, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.745, cnvDataWidth*0.98, cnvDataHeight*0.745, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.795, cnvDataWidth*0.98, cnvDataHeight*0.795, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.845, cnvDataWidth*0.98, cnvDataHeight*0.845, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.895, cnvDataWidth*0.98, cnvDataHeight*0.895, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.945, cnvDataWidth*0.98, cnvDataHeight*0.945, fill=_fgcolor, width="1")
		self.cnvsData.create_line(cnvDataWidth*0.51, cnvDataHeight*0.995, cnvDataWidth*0.98, cnvDataHeight*0.995, fill=_fgcolor, width="1")

		self.lblInfo_1 = Label(self.cnvsData)
		self.lblInfo_1.place(relx=0.51, rely=0.00, relheight=0.01, relwidth=0.47)
		self.lblInfo_1.configure(activebackground="#f9f9f9")
		self.lblInfo_1.configure(activeforeground=_fgcolor)
		self.lblInfo_1.configure(background=_bgcolor)
		self.lblInfo_1.configure(disabledforeground="#a3a3a3")
		self.lblInfo_1.configure(foreground=_fgcolor)
		self.lblInfo_1.configure(highlightbackground=_bgcolor)
		self.lblInfo_1.configure(highlightcolor=_fgcolor)
		self.lblInfo_1.configure(font=('Helvetica', 6, 'bold'))
		self.lblInfo_1.configure(text='''*** All values are in Centimetre (cm)''')
		self.lblInfo_1.configure(anchor='w')

		self.lblBodyLength = Label(self.cnvsData)
		# self.lblBodyLength.place(relx=0.06, rely=0.055, height=21, width=53)
		self.lblBodyLength.place(relx=0.02, rely=0.01, relheight=0.03, relwidth=0.47)
		self.lblBodyLength.configure(activebackground="#f9f9f9")
		self.lblBodyLength.configure(activeforeground=_fgcolor)
		self.lblBodyLength.configure(background=_bgcolor)
		self.lblBodyLength.configure(disabledforeground="#a3a3a3")
		self.lblBodyLength.configure(foreground=_fgcolor)
		self.lblBodyLength.configure(highlightbackground=_bgcolor)
		self.lblBodyLength.configure(highlightcolor=_fgcolor)
		self.lblBodyLength.configure(font=('Helvetica', 9, 'bold'))
		self.lblBodyLength.configure(text='''Body Length''')
		self.lblBodyLength.configure(anchor='w')

		self.lblBodyWidth = Label(self.cnvsData)
		self.lblBodyWidth.place(relx=0.02, rely=0.06, relheight=0.03, relwidth=0.47)
		self.lblBodyWidth.configure(activebackground="#f9f9f9")
		self.lblBodyWidth.configure(activeforeground=_fgcolor)
		self.lblBodyWidth.configure(background=_bgcolor)
		self.lblBodyWidth.configure(disabledforeground="#a3a3a3")
		self.lblBodyWidth.configure(foreground=_fgcolor)
		self.lblBodyWidth.configure(highlightbackground=_bgcolor)
		self.lblBodyWidth.configure(highlightcolor=_fgcolor)
		self.lblBodyWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblBodyWidth.configure(text='''Body Width''')
		self.lblBodyWidth.configure(anchor='w')

		self.lblBodySweep = Label(self.cnvsData)
		self.lblBodySweep.place(relx=0.02, rely=0.11, relheight=0.03, relwidth=0.47)
		self.lblBodySweep.configure(activebackground="#f9f9f9")
		self.lblBodySweep.configure(activeforeground=_fgcolor)
		self.lblBodySweep.configure(background=_bgcolor)
		self.lblBodySweep.configure(disabledforeground="#a3a3a3")
		self.lblBodySweep.configure(foreground=_fgcolor)
		self.lblBodySweep.configure(highlightbackground=_bgcolor)
		self.lblBodySweep.configure(highlightcolor=_fgcolor)
		self.lblBodySweep.configure(font=('Helvetica', 9, 'bold'))
		self.lblBodySweep.configure(text='''Body Sweep''')
		self.lblBodySweep.configure(anchor='w')

		self.lblBackNeckWidth = Label(self.cnvsData)
		self.lblBackNeckWidth.place(relx=0.02, rely=0.16, relheight=0.03, relwidth=0.47)
		self.lblBackNeckWidth.configure(activebackground="#f9f9f9")
		self.lblBackNeckWidth.configure(activeforeground=_fgcolor)
		self.lblBackNeckWidth.configure(background=_bgcolor)
		self.lblBackNeckWidth.configure(disabledforeground="#a3a3a3")
		self.lblBackNeckWidth.configure(foreground=_fgcolor)
		self.lblBackNeckWidth.configure(highlightbackground=_bgcolor)
		self.lblBackNeckWidth.configure(highlightcolor=_fgcolor)
		self.lblBackNeckWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblBackNeckWidth.configure(text='''Back Neck Width''')
		self.lblBackNeckWidth.configure(anchor='w')

		self.lblCollarHeight = Label(self.cnvsData)
		self.lblCollarHeight.place(relx=0.02, rely=0.21, relheight=0.03, relwidth=0.47)
		self.lblCollarHeight.configure(activebackground="#f9f9f9")
		self.lblCollarHeight.configure(activeforeground=_fgcolor)
		self.lblCollarHeight.configure(background=_bgcolor)
		self.lblCollarHeight.configure(disabledforeground="#a3a3a3")
		self.lblCollarHeight.configure(foreground=_fgcolor)
		self.lblCollarHeight.configure(highlightbackground=_bgcolor)
		self.lblCollarHeight.configure(highlightcolor=_fgcolor)
		self.lblCollarHeight.configure(font=('Helvetica', 9, 'bold'))
		self.lblCollarHeight.configure(text='''Collar Height''')
		self.lblCollarHeight.configure(anchor='w')

		self.lblBackNeckDrop = Label(self.cnvsData)
		self.lblBackNeckDrop.place(relx=0.02, rely=0.26, relheight=0.03, relwidth=0.47)
		self.lblBackNeckDrop.configure(activebackground="#f9f9f9")
		self.lblBackNeckDrop.configure(activeforeground=_fgcolor)
		self.lblBackNeckDrop.configure(background=_bgcolor)
		self.lblBackNeckDrop.configure(disabledforeground="#a3a3a3")
		self.lblBackNeckDrop.configure(foreground=_fgcolor)
		self.lblBackNeckDrop.configure(highlightbackground=_bgcolor)
		self.lblBackNeckDrop.configure(highlightcolor=_fgcolor)
		self.lblBackNeckDrop.configure(font=('Helvetica', 9, 'bold'))
		self.lblBackNeckDrop.configure(text='''Back Neck Drop''')
		self.lblBackNeckDrop.configure(anchor='w')

		self.lblXDistance = Label(self.cnvsData)
		self.lblXDistance.place(relx=0.02, rely=0.31, relheight=0.03, relwidth=0.47)
		self.lblXDistance.configure(activebackground="#f9f9f9")
		self.lblXDistance.configure(activeforeground=_fgcolor)
		self.lblXDistance.configure(background=_bgcolor)
		self.lblXDistance.configure(disabledforeground="#a3a3a3")
		self.lblXDistance.configure(foreground=_fgcolor)
		self.lblXDistance.configure(highlightbackground=_bgcolor)
		self.lblXDistance.configure(highlightcolor=_fgcolor)
		self.lblXDistance.configure(font=('Helvetica', 9, 'bold'))
		self.lblXDistance.configure(text='''X Distance''')
		self.lblXDistance.configure(anchor='w')

		self.lblWaistWidth = Label(self.cnvsData)
		self.lblWaistWidth.place(relx=0.02, rely=0.36, relheight=0.03, relwidth=0.47)
		self.lblWaistWidth.configure(activebackground="#f9f9f9")
		self.lblWaistWidth.configure(activeforeground=_fgcolor)
		self.lblWaistWidth.configure(background=_bgcolor)
		self.lblWaistWidth.configure(disabledforeground="#a3a3a3")
		self.lblWaistWidth.configure(foreground=_fgcolor)
		self.lblWaistWidth.configure(highlightbackground=_bgcolor)
		self.lblWaistWidth.configure(highlightcolor=_fgcolor)
		self.lblWaistWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblWaistWidth.configure(text='''Waist Width''')
		self.lblWaistWidth.configure(anchor='w')

		self.lblLSSleeveLength = Label(self.cnvsData)
		self.lblLSSleeveLength.place(relx=0.02, rely=0.41, relheight=0.03, relwidth=0.47)
		self.lblLSSleeveLength.configure(activebackground="#f9f9f9")
		self.lblLSSleeveLength.configure(activeforeground=_fgcolor)
		self.lblLSSleeveLength.configure(background=_bgcolor)
		self.lblLSSleeveLength.configure(disabledforeground="#a3a3a3")
		self.lblLSSleeveLength.configure(foreground=_fgcolor)
		self.lblLSSleeveLength.configure(highlightbackground=_bgcolor)
		self.lblLSSleeveLength.configure(highlightcolor=_fgcolor)
		self.lblLSSleeveLength.configure(font=('Helvetica', 9, 'bold'))
		self.lblLSSleeveLength.configure(text='''LS Sleeve Length''')
		self.lblLSSleeveLength.configure(anchor='w')

		self.lblSleeveWidth = Label(self.cnvsData)
		self.lblSleeveWidth.place(relx=0.02, rely=0.46, relheight=0.03, relwidth=0.47)
		self.lblSleeveWidth.configure(activebackground="#f9f9f9")
		self.lblSleeveWidth.configure(activeforeground=_fgcolor)
		self.lblSleeveWidth.configure(background=_bgcolor)
		self.lblSleeveWidth.configure(disabledforeground="#a3a3a3")
		self.lblSleeveWidth.configure(foreground=_fgcolor)
		self.lblSleeveWidth.configure(highlightbackground=_bgcolor)
		self.lblSleeveWidth.configure(highlightcolor=_fgcolor)
		self.lblSleeveWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblSleeveWidth.configure(text='''Sleeve Width''')
		self.lblSleeveWidth.configure(anchor='w')

		self.lblElbowWidth = Label(self.cnvsData)
		self.lblElbowWidth.place(relx=0.02, rely=0.51, relheight=0.03, relwidth=0.47)
		self.lblElbowWidth.configure(activebackground="#f9f9f9")
		self.lblElbowWidth.configure(activeforeground=_fgcolor)
		self.lblElbowWidth.configure(background=_bgcolor)
		self.lblElbowWidth.configure(disabledforeground="#a3a3a3")
		self.lblElbowWidth.configure(foreground=_fgcolor)
		self.lblElbowWidth.configure(highlightbackground=_bgcolor)
		self.lblElbowWidth.configure(highlightcolor=_fgcolor)
		self.lblElbowWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblElbowWidth.configure(text='''Elbow Width''')
		self.lblElbowWidth.configure(anchor='w')

		self.lblForeArmWidth = Label(self.cnvsData)
		self.lblForeArmWidth.place(relx=0.02, rely=0.56, relheight=0.03, relwidth=0.47)
		self.lblForeArmWidth.configure(activebackground="#f9f9f9")
		self.lblForeArmWidth.configure(activeforeground=_fgcolor)
		self.lblForeArmWidth.configure(background=_bgcolor)
		self.lblForeArmWidth.configure(disabledforeground="#a3a3a3")
		self.lblForeArmWidth.configure(foreground=_fgcolor)
		self.lblForeArmWidth.configure(highlightbackground=_bgcolor)
		self.lblForeArmWidth.configure(highlightcolor=_fgcolor)
		self.lblForeArmWidth.configure(font=('Helvetica', 9, 'bold'))
		self.lblForeArmWidth.configure(text='''ForeArm Width''')
		self.lblForeArmWidth.configure(anchor='w')

		self.lblSleeveOpening = Label(self.cnvsData)
		self.lblSleeveOpening.place(relx=0.02, rely=0.61, relheight=0.03, relwidth=0.47)
		self.lblSleeveOpening.configure(activebackground="#f9f9f9")
		self.lblSleeveOpening.configure(activeforeground=_fgcolor)
		self.lblSleeveOpening.configure(background=_bgcolor)
		self.lblSleeveOpening.configure(disabledforeground="#a3a3a3")
		self.lblSleeveOpening.configure(foreground=_fgcolor)
		self.lblSleeveOpening.configure(highlightbackground=_bgcolor)
		self.lblSleeveOpening.configure(highlightcolor=_fgcolor)
		self.lblSleeveOpening.configure(font=('Helvetica', 9, 'bold'))
		self.lblSleeveOpening.configure(text='''Sleeve Opening''')
		self.lblSleeveOpening.configure(anchor='w')

		self.lblFrontNeckDrop = Label(self.cnvsData)
		self.lblFrontNeckDrop.place(relx=0.02, rely=0.66, relheight=0.03, relwidth=0.47)
		self.lblFrontNeckDrop.configure(activebackground="#f9f9f9")
		self.lblFrontNeckDrop.configure(activeforeground=_fgcolor)
		self.lblFrontNeckDrop.configure(background=_bgcolor)
		self.lblFrontNeckDrop.configure(disabledforeground="#a3a3a3")
		self.lblFrontNeckDrop.configure(foreground=_fgcolor)
		self.lblFrontNeckDrop.configure(highlightbackground=_bgcolor)
		self.lblFrontNeckDrop.configure(highlightcolor=_fgcolor)
		self.lblFrontNeckDrop.configure(font=('Helvetica', 9, 'bold'))
		self.lblFrontNeckDrop.configure(text='''Front Neck Drop''')
		self.lblFrontNeckDrop.configure(anchor='w')

		self.lblNeckOpening = Label(self.cnvsData)
		self.lblNeckOpening.place(relx=0.02, rely=0.71, relheight=0.03, relwidth=0.47)
		self.lblNeckOpening.configure(activebackground="#f9f9f9")
		self.lblNeckOpening.configure(activeforeground=_fgcolor)
		self.lblNeckOpening.configure(background=_bgcolor)
		self.lblNeckOpening.configure(disabledforeground="#a3a3a3")
		self.lblNeckOpening.configure(foreground=_fgcolor)
		self.lblNeckOpening.configure(highlightbackground=_bgcolor)
		self.lblNeckOpening.configure(highlightcolor=_fgcolor)
		self.lblNeckOpening.configure(font=('Helvetica', 9, 'bold'))
		self.lblNeckOpening.configure(text='''Neck Opening''')
		self.lblNeckOpening.configure(anchor='w')

		self.lblCollarPoints = Label(self.cnvsData)
		self.lblCollarPoints.place(relx=0.02, rely=0.76, relheight=0.03, relwidth=0.47)
		self.lblCollarPoints.configure(activebackground="#f9f9f9")
		self.lblCollarPoints.configure(activeforeground=_fgcolor)
		self.lblCollarPoints.configure(background=_bgcolor)
		self.lblCollarPoints.configure(disabledforeground="#a3a3a3")
		self.lblCollarPoints.configure(foreground=_fgcolor)
		self.lblCollarPoints.configure(highlightbackground=_bgcolor)
		self.lblCollarPoints.configure(highlightcolor=_fgcolor)
		self.lblCollarPoints.configure(font=('Helvetica', 9, 'bold'))
		self.lblCollarPoints.configure(text='''Collar Points''')
		self.lblCollarPoints.configure(anchor='w')

		self.lblCollarLength = Label(self.cnvsData)
		self.lblCollarLength.place(relx=0.02, rely=0.81, relheight=0.03, relwidth=0.47)
		self.lblCollarLength.configure(activebackground="#f9f9f9")
		self.lblCollarLength.configure(activeforeground=_fgcolor)
		self.lblCollarLength.configure(background=_bgcolor)
		self.lblCollarLength.configure(disabledforeground="#a3a3a3")
		self.lblCollarLength.configure(foreground=_fgcolor)
		self.lblCollarLength.configure(highlightbackground=_bgcolor)
		self.lblCollarLength.configure(highlightcolor=_fgcolor)
		self.lblCollarLength.configure(font=('Helvetica', 9, 'bold'))
		self.lblCollarLength.configure(text='''Collar Length''')
		self.lblCollarLength.configure(anchor='w')

		self.lblZipperLength = Label(self.cnvsData)
		self.lblZipperLength.place(relx=0.02, rely=0.86, relheight=0.03, relwidth=0.47)
		self.lblZipperLength.configure(activebackground="#f9f9f9")
		self.lblZipperLength.configure(activeforeground=_fgcolor)
		self.lblZipperLength.configure(background=_bgcolor)
		self.lblZipperLength.configure(disabledforeground="#a3a3a3")
		self.lblZipperLength.configure(foreground=_fgcolor)
		self.lblZipperLength.configure(highlightbackground=_bgcolor)
		self.lblZipperLength.configure(highlightcolor=_fgcolor)
		self.lblZipperLength.configure(font=('Helvetica', 9, 'bold'))
		self.lblZipperLength.configure(text='''Zipper Length''')
		self.lblZipperLength.configure(anchor='w')

		self.lblDropTailLength = Label(self.cnvsData)
		self.lblDropTailLength.place(relx=0.02, rely=0.91, relheight=0.03, relwidth=0.47)
		self.lblDropTailLength.configure(activebackground="#f9f9f9")
		self.lblDropTailLength.configure(activeforeground=_fgcolor)
		self.lblDropTailLength.configure(background=_bgcolor)
		self.lblDropTailLength.configure(disabledforeground="#a3a3a3")
		self.lblDropTailLength.configure(foreground=_fgcolor)
		self.lblDropTailLength.configure(highlightbackground=_bgcolor)
		self.lblDropTailLength.configure(highlightcolor=_fgcolor)
		self.lblDropTailLength.configure(font=('Helvetica', 9, 'bold'))
		self.lblDropTailLength.configure(text='''Drop Tail Length''')
		self.lblDropTailLength.configure(anchor='w')

		self.lblPocketHeight = Label(self.cnvsData)
		self.lblPocketHeight.place(relx=0.02, rely=0.96, relheight=0.03, relwidth=0.47)
		self.lblPocketHeight.configure(activebackground="#f9f9f9")
		self.lblPocketHeight.configure(activeforeground=_fgcolor)
		self.lblPocketHeight.configure(background=_bgcolor)
		self.lblPocketHeight.configure(disabledforeground="#a3a3a3")
		self.lblPocketHeight.configure(foreground=_fgcolor)
		self.lblPocketHeight.configure(highlightbackground=_bgcolor)
		self.lblPocketHeight.configure(highlightcolor=_fgcolor)
		self.lblPocketHeight.configure(font=('Helvetica', 9, 'bold'))
		self.lblPocketHeight.configure(text='''Pocket Height''')
		self.lblPocketHeight.configure(anchor='w')

		# self.onoff = StringVar()
		# self.onoff.set("OFF")

		# self.lblWhiteGarmentStatus = Label(self.cnvsData)
		# self.lblWhiteGarmentStatus.place(relx=0.45, rely=0.87, height=21, width=90)
		# self.lblWhiteGarmentStatus.configure(activebackground="#f9f9f9")
		# self.lblWhiteGarmentStatus.configure(activeforeground=_fgcolor)
		# self.lblWhiteGarmentStatus.configure(background=_bgcolor)
		# self.lblWhiteGarmentStatus.configure(disabledforeground="#a3a3a3")
		# self.lblWhiteGarmentStatus.configure(foreground=_fgcolor)
		# self.lblWhiteGarmentStatus.configure(highlightbackground=_bgcolor)
		# self.lblWhiteGarmentStatus.configure(highlightcolor=_fgcolor)
		# self.lblWhiteGarmentStatus.configure(font=('TkFixedFont', 12, 'bold'))
		# self.lblWhiteGarmentStatus.configure(textvariable=self.onoff)

		# self.btnOnOff = Button(self.cnvsData)
		# self.btnOnOff.place(relx=0.74, rely=0.87, height=20, width=70)
		# self.btnOnOff.configure(activebackground="#008000")
		# self.btnOnOff.configure(activeforeground=_fgcolor)
		# self.btnOnOff.configure(background="#3A5FCD")
		# self.btnOnOff.configure(cursor="hand2")
		# self.btnOnOff.configure(relief=FLAT)
		# self.btnOnOff.configure(disabledforeground=_fgcolor)
		# self.btnOnOff.configure(foreground=_fgcolor)
		# self.btnOnOff.configure(highlightbackground=_fgcolor)
		# self.btnOnOff.configure(highlightcolor=_fgcolor)
		# self.btnOnOff.configure(pady="0")
		# self.btnOnOff.configure(state="normal")
		# self.btnOnOff.configure(font=('Helvetica', 8, 'bold'))
		# self.btnOnOff.configure(text='''ON / OFF''')
		# self.btnOnOff.configure(command=self.whiteGarmentModeOnOff)

		self.txtBodyLength = Entry(self.cnvsData)
		# self.txtBodyLength.place(relx=0.48, rely=0.056,height=20, relwidth=0.46)
		self.txtBodyLength.place(relx=0.51, rely=0.01, relheight=0.03, relwidth=0.47)
		self.txtBodyLength.configure(background=_bgcolor)
		self.txtBodyLength.configure(disabledforeground="#a3a3a3")
		self.txtBodyLength.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodyLength.configure(foreground=_fgcolor)
		self.txtBodyLength.configure(highlightbackground=_bgcolor)
		self.txtBodyLength.configure(highlightcolor=_fgcolor)
		self.txtBodyLength.configure(insertbackground=_fgcolor)
		self.txtBodyLength.configure(selectbackground=_highlightbgcolor)
		self.txtBodyLength.configure(selectforeground=_fgcolor)
		self.txtBodyLength.configure(relief=FLAT)
		validateSupport = self.txtBodyLength.register(self.validateFloat)
		self.txtBodyLength.configure(validate="key")
		self.txtBodyLength.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyLength.focus()
		# self.txtBodyLength.bind("<Key>", click)
		self.txtBodyLength.bind("<Return>", self.onEnter)
		# self.txtBodyLength.bind("<Return>", lambda event: self.txtSize.focus())

		self.txtBodyWidth = Entry(self.cnvsData)
		self.txtBodyWidth.place(relx=0.51, rely=0.06, relheight=0.03, relwidth=0.47)
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
		# self.txtBodyWidth.bind("<Return>", self.loadData)
		# self.txtBodyWidth.bind("<Tab>", self.loadData)

		self.txtBodySweep = Entry(self.cnvsData)
		self.txtBodySweep.place(relx=0.51, rely=0.11, relheight=0.03, relwidth=0.47)
		self.txtBodySweep.configure(background=_bgcolor)
		self.txtBodySweep.configure(disabledforeground="#a3a3a3")
		self.txtBodySweep.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodySweep.configure(foreground=_fgcolor)
		self.txtBodySweep.configure(highlightbackground=_bgcolor)
		self.txtBodySweep.configure(highlightcolor=_fgcolor)
		self.txtBodySweep.configure(insertbackground=_fgcolor)
		self.txtBodySweep.configure(selectbackground=_highlightbgcolor)
		self.txtBodySweep.configure(selectforeground=_fgcolor)
		self.txtBodySweep.configure(relief=FLAT)
		validateSupport = self.txtBodySweep.register(self.validateFloat)
		self.txtBodySweep.configure(validate="key")
		self.txtBodySweep.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodySweep.bind("<Return>", self.onEnter)
		# self.txtBodySweep.bind("<Button-1>", self.loadData)

		self.txtBackNeckWidth = Entry(self.cnvsData)
		self.txtBackNeckWidth.place(relx=0.51, rely=0.16, relheight=0.03, relwidth=0.47)
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
		# self.txtBackNeckWidth.bind("<Button-1>", self.loadData)

		self.txtCollarHeight = Entry(self.cnvsData)
		self.txtCollarHeight.place(relx=0.51, rely=0.21, relheight=0.03, relwidth=0.47)
		self.txtCollarHeight.configure(background=_bgcolor)
		self.txtCollarHeight.configure(disabledforeground="#a3a3a3")
		self.txtCollarHeight.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtCollarHeight.configure(foreground=_fgcolor)
		self.txtCollarHeight.configure(highlightbackground=_bgcolor)
		self.txtCollarHeight.configure(highlightcolor=_fgcolor)
		self.txtCollarHeight.configure(insertbackground=_fgcolor)
		self.txtCollarHeight.configure(selectbackground=_highlightbgcolor)
		self.txtCollarHeight.configure(selectforeground=_fgcolor)
		self.txtCollarHeight.configure(relief=FLAT)
		validateSupport = self.txtCollarHeight.register(self.validateFloat)
		self.txtCollarHeight.configure(validate="key")
		self.txtCollarHeight.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtCollarHeight.bind("<Return>", self.onEnter)
		# self.txtCollarHeight.bind("<Button-1>", self.loadData)

		self.txtBackNeckDrop = Entry(self.cnvsData)
		self.txtBackNeckDrop.place(relx=0.51, rely=0.26, relheight=0.03, relwidth=0.47)
		self.txtBackNeckDrop.configure(background=_bgcolor)
		self.txtBackNeckDrop.configure(disabledforeground="#a3a3a3")
		self.txtBackNeckDrop.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBackNeckDrop.configure(foreground=_fgcolor)
		self.txtBackNeckDrop.configure(highlightbackground=_bgcolor)
		self.txtBackNeckDrop.configure(highlightcolor=_fgcolor)
		self.txtBackNeckDrop.configure(insertbackground=_fgcolor)
		self.txtBackNeckDrop.configure(selectbackground=_highlightbgcolor)
		self.txtBackNeckDrop.configure(selectforeground=_fgcolor)
		self.txtBackNeckDrop.configure(relief=FLAT)
		validateSupport = self.txtBackNeckDrop.register(self.validateFloat)
		self.txtBackNeckDrop.configure(validate="key")
		self.txtBackNeckDrop.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBackNeckDrop.bind("<Return>", self.onEnter)
		# self.txtBackNeckDrop.bind("<Button-1>", self.loadData)

		self.txtXDistance = Entry(self.cnvsData)
		self.txtXDistance.place(relx=0.51, rely=0.31, relheight=0.03, relwidth=0.47)
		self.txtXDistance.configure(background=_bgcolor)
		self.txtXDistance.configure(disabledforeground="#a3a3a3")
		self.txtXDistance.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtXDistance.configure(foreground=_fgcolor)
		self.txtXDistance.configure(highlightbackground=_bgcolor)
		self.txtXDistance.configure(highlightcolor=_fgcolor)
		self.txtXDistance.configure(insertbackground=_fgcolor)
		self.txtXDistance.configure(selectbackground=_highlightbgcolor)
		self.txtXDistance.configure(selectforeground=_fgcolor)
		self.txtXDistance.configure(relief=FLAT)
		validateSupport = self.txtXDistance.register(self.validateFloat)
		self.txtXDistance.configure(validate="key")
		self.txtXDistance.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtXDistance.bind("<Return>", self.onEnter)
		# self.txtXDistance.bind("<Button-1>", self.loadData)

		self.txtBodyWaistWidth = Entry(self.cnvsData)
		self.txtBodyWaistWidth.place(relx=0.51, rely=0.36, relheight=0.03, relwidth=0.47)
		self.txtBodyWaistWidth.configure(background=_bgcolor)
		self.txtBodyWaistWidth.configure(disabledforeground="#a3a3a3")
		self.txtBodyWaistWidth.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtBodyWaistWidth.configure(foreground=_fgcolor)
		self.txtBodyWaistWidth.configure(highlightbackground=_bgcolor)
		self.txtBodyWaistWidth.configure(highlightcolor=_fgcolor)
		self.txtBodyWaistWidth.configure(insertbackground=_fgcolor)
		self.txtBodyWaistWidth.configure(selectbackground=_highlightbgcolor)
		self.txtBodyWaistWidth.configure(selectforeground=_fgcolor)
		self.txtBodyWaistWidth.configure(relief=FLAT)
		validateSupport = self.txtBodyWaistWidth.register(self.validateFloat)
		self.txtBodyWaistWidth.configure(validate="key")
		self.txtBodyWaistWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtBodyWaistWidth.bind("<Return>", self.onEnter)
		# self.txtBodyWaistWidth.bind("<Button-1>", self.loadData)

		self.txtLSSleeveLength = Entry(self.cnvsData)
		self.txtLSSleeveLength.place(relx=0.51, rely=0.41, relheight=0.03, relwidth=0.47)
		self.txtLSSleeveLength.configure(background=_bgcolor)
		self.txtLSSleeveLength.configure(disabledforeground="#a3a3a3")
		self.txtLSSleeveLength.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtLSSleeveLength.configure(foreground=_fgcolor)
		self.txtLSSleeveLength.configure(highlightbackground=_bgcolor)
		self.txtLSSleeveLength.configure(highlightcolor=_fgcolor)
		self.txtLSSleeveLength.configure(insertbackground=_fgcolor)
		self.txtLSSleeveLength.configure(selectbackground=_highlightbgcolor)
		self.txtLSSleeveLength.configure(selectforeground=_fgcolor)
		self.txtLSSleeveLength.configure(relief=FLAT)
		validateSupport = self.txtLSSleeveLength.register(self.validateFloat)
		self.txtLSSleeveLength.configure(validate="key")
		self.txtLSSleeveLength.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtLSSleeveLength.bind("<Return>", self.onEnter)
		# self.txtLSSleeveLength.bind("<Button-1>", self.loadData)

		self.txtSleeveWidth = Entry(self.cnvsData)
		self.txtSleeveWidth.place(relx=0.51, rely=0.46, relheight=0.03, relwidth=0.47)
		self.txtSleeveWidth.configure(background=_bgcolor)
		self.txtSleeveWidth.configure(disabledforeground="#a3a3a3")
		self.txtSleeveWidth.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtSleeveWidth.configure(foreground=_fgcolor)
		self.txtSleeveWidth.configure(highlightbackground=_bgcolor)
		self.txtSleeveWidth.configure(highlightcolor=_fgcolor)
		self.txtSleeveWidth.configure(insertbackground=_fgcolor)
		self.txtSleeveWidth.configure(selectbackground=_highlightbgcolor)
		self.txtSleeveWidth.configure(selectforeground=_fgcolor)
		self.txtSleeveWidth.configure(relief=FLAT)
		validateSupport = self.txtSleeveWidth.register(self.validateFloat)
		self.txtSleeveWidth.configure(validate="key")
		self.txtSleeveWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtSleeveWidth.bind("<Return>", self.onEnter)
		# self.txtSleeveWidth.bind("<Button-1>", self.loadData)

		self.txtElbowWidth = Entry(self.cnvsData)
		self.txtElbowWidth.place(relx=0.51, rely=0.51, relheight=0.03, relwidth=0.47)
		self.txtElbowWidth.configure(background=_bgcolor)
		self.txtElbowWidth.configure(disabledforeground="#a3a3a3")
		self.txtElbowWidth.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtElbowWidth.configure(foreground=_fgcolor)
		self.txtElbowWidth.configure(highlightbackground=_bgcolor)
		self.txtElbowWidth.configure(highlightcolor=_fgcolor)
		self.txtElbowWidth.configure(insertbackground=_fgcolor)
		self.txtElbowWidth.configure(selectbackground=_highlightbgcolor)
		self.txtElbowWidth.configure(selectforeground=_fgcolor)
		self.txtElbowWidth.configure(relief=FLAT)
		validateSupport = self.txtElbowWidth.register(self.validateFloat)
		self.txtElbowWidth.configure(validate="key")
		self.txtElbowWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtElbowWidth.bind("<Return>", self.onEnter)
		# self.txtElbowWidth.bind("<Button-1>", self.loadData)

		self.txtForeArmWidth = Entry(self.cnvsData)
		self.txtForeArmWidth.place(relx=0.51, rely=0.56, relheight=0.03, relwidth=0.47)
		self.txtForeArmWidth.configure(background=_bgcolor)
		self.txtForeArmWidth.configure(disabledforeground="#a3a3a3")
		self.txtForeArmWidth.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtForeArmWidth.configure(foreground=_fgcolor)
		self.txtForeArmWidth.configure(highlightbackground=_bgcolor)
		self.txtForeArmWidth.configure(highlightcolor=_fgcolor)
		self.txtForeArmWidth.configure(insertbackground=_fgcolor)
		self.txtForeArmWidth.configure(selectbackground=_highlightbgcolor)
		self.txtForeArmWidth.configure(selectforeground=_fgcolor)
		self.txtForeArmWidth.configure(relief=FLAT)
		validateSupport = self.txtForeArmWidth.register(self.validateFloat)
		self.txtForeArmWidth.configure(validate="key")
		self.txtForeArmWidth.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtForeArmWidth.bind("<Return>", self.onEnter)
		# self.txtForeArmWidth.bind("<Button-1>", self.loadData)

		self.txtSleeveOpening = Entry(self.cnvsData)
		self.txtSleeveOpening.place(relx=0.51, rely=0.61, relheight=0.03, relwidth=0.47)
		self.txtSleeveOpening.configure(background=_bgcolor)
		self.txtSleeveOpening.configure(disabledforeground="#a3a3a3")
		self.txtSleeveOpening.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtSleeveOpening.configure(foreground=_fgcolor)
		self.txtSleeveOpening.configure(highlightbackground=_bgcolor)
		self.txtSleeveOpening.configure(highlightcolor=_fgcolor)
		self.txtSleeveOpening.configure(insertbackground=_fgcolor)
		self.txtSleeveOpening.configure(selectbackground=_highlightbgcolor)
		self.txtSleeveOpening.configure(selectforeground=_fgcolor)
		self.txtSleeveOpening.configure(relief=FLAT)
		validateSupport = self.txtSleeveOpening.register(self.validateFloat)
		self.txtSleeveOpening.configure(validate="key")
		self.txtSleeveOpening.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtSleeveOpening.bind("<Return>", self.onEnter)
		# self.txtSleeveOpening.bind("<Button-1>", self.loadData)

		self.txtFrontNeckDrop = Entry(self.cnvsData)
		self.txtFrontNeckDrop.place(relx=0.51, rely=0.66, relheight=0.03, relwidth=0.47)
		self.txtFrontNeckDrop.configure(background=_bgcolor)
		self.txtFrontNeckDrop.configure(disabledforeground="#a3a3a3")
		self.txtFrontNeckDrop.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtFrontNeckDrop.configure(foreground=_fgcolor)
		self.txtFrontNeckDrop.configure(highlightbackground=_bgcolor)
		self.txtFrontNeckDrop.configure(highlightcolor=_fgcolor)
		self.txtFrontNeckDrop.configure(insertbackground=_fgcolor)
		self.txtFrontNeckDrop.configure(selectbackground=_highlightbgcolor)
		self.txtFrontNeckDrop.configure(selectforeground=_fgcolor)
		self.txtFrontNeckDrop.configure(relief=FLAT)
		validateSupport = self.txtFrontNeckDrop.register(self.validateFloat)
		self.txtFrontNeckDrop.configure(validate="key")
		self.txtFrontNeckDrop.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtFrontNeckDrop.bind("<Return>", self.onEnter)
		# self.txtFrontNeckDrop.bind("<Button-1>", self.loadData)

		self.txtNeckOpening = Entry(self.cnvsData)
		self.txtNeckOpening.place(relx=0.51, rely=0.71, relheight=0.03, relwidth=0.47)
		self.txtNeckOpening.configure(background=_bgcolor)
		self.txtNeckOpening.configure(disabledforeground="#a3a3a3")
		self.txtNeckOpening.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtNeckOpening.configure(foreground=_fgcolor)
		self.txtNeckOpening.configure(highlightbackground=_bgcolor)
		self.txtNeckOpening.configure(highlightcolor=_fgcolor)
		self.txtNeckOpening.configure(insertbackground=_fgcolor)
		self.txtNeckOpening.configure(selectbackground=_highlightbgcolor)
		self.txtNeckOpening.configure(selectforeground=_fgcolor)
		self.txtNeckOpening.configure(relief=FLAT)
		validateSupport = self.txtNeckOpening.register(self.validateFloat)
		self.txtNeckOpening.configure(validate="key")
		self.txtNeckOpening.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtNeckOpening.bind("<Return>", self.onEnter)
		# self.txtNeckOpening.bind("<Button-1>", self.loadData)

		self.txtCollarPoints = Entry(self.cnvsData)
		self.txtCollarPoints.place(relx=0.51, rely=0.76, relheight=0.03, relwidth=0.47)
		self.txtCollarPoints.configure(background=_bgcolor)
		self.txtCollarPoints.configure(disabledforeground="#a3a3a3")
		self.txtCollarPoints.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtCollarPoints.configure(foreground=_fgcolor)
		self.txtCollarPoints.configure(highlightbackground=_bgcolor)
		self.txtCollarPoints.configure(highlightcolor=_fgcolor)
		self.txtCollarPoints.configure(insertbackground=_fgcolor)
		self.txtCollarPoints.configure(selectbackground=_highlightbgcolor)
		self.txtCollarPoints.configure(selectforeground=_fgcolor)
		self.txtCollarPoints.configure(relief=FLAT)
		validateSupport = self.txtCollarPoints.register(self.validateFloat)
		self.txtCollarPoints.configure(validate="key")
		self.txtCollarPoints.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtCollarPoints.bind("<Return>", self.onEnter)
		# self.txtCollarPoints.bind("<Button-1>", self.loadData)

		self.txtCollarLength = Entry(self.cnvsData)
		self.txtCollarLength.place(relx=0.51, rely=0.81, relheight=0.03, relwidth=0.47)
		self.txtCollarLength.configure(background=_bgcolor)
		self.txtCollarLength.configure(disabledforeground="#a3a3a3")
		self.txtCollarLength.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtCollarLength.configure(foreground=_fgcolor)
		self.txtCollarLength.configure(highlightbackground=_bgcolor)
		self.txtCollarLength.configure(highlightcolor=_fgcolor)
		self.txtCollarLength.configure(insertbackground=_fgcolor)
		self.txtCollarLength.configure(selectbackground=_highlightbgcolor)
		self.txtCollarLength.configure(selectforeground=_fgcolor)
		self.txtCollarLength.configure(relief=FLAT)
		validateSupport = self.txtCollarLength.register(self.validateFloat)
		self.txtCollarLength.configure(validate="key")
		self.txtCollarLength.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtCollarLength.bind("<Return>", self.onEnter)
		# self.txtCollarLength.bind("<Button-1>", self.loadData)

		self.txtZipperLength = Entry(self.cnvsData)
		self.txtZipperLength.place(relx=0.51, rely=0.86, relheight=0.03, relwidth=0.47)
		self.txtZipperLength.configure(background=_bgcolor)
		self.txtZipperLength.configure(disabledforeground="#a3a3a3")
		self.txtZipperLength.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtZipperLength.configure(foreground=_fgcolor)
		self.txtZipperLength.configure(highlightbackground=_bgcolor)
		self.txtZipperLength.configure(highlightcolor=_fgcolor)
		self.txtZipperLength.configure(insertbackground=_fgcolor)
		self.txtZipperLength.configure(selectbackground=_highlightbgcolor)
		self.txtZipperLength.configure(selectforeground=_fgcolor)
		self.txtZipperLength.configure(relief=FLAT)
		validateSupport = self.txtZipperLength.register(self.validateFloat)
		self.txtZipperLength.configure(validate="key")
		self.txtZipperLength.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtZipperLength.bind("<Return>", self.onEnter)
		# self.txtZipperLength.bind("<Button-1>", self.loadData)

		self.txtDropTailLength = Entry(self.cnvsData)
		self.txtDropTailLength.place(relx=0.51, rely=0.91, relheight=0.03, relwidth=0.47)
		self.txtDropTailLength.configure(background=_bgcolor)
		self.txtDropTailLength.configure(disabledforeground="#a3a3a3")
		self.txtDropTailLength.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtDropTailLength.configure(foreground=_fgcolor)
		self.txtDropTailLength.configure(highlightbackground=_bgcolor)
		self.txtDropTailLength.configure(highlightcolor=_fgcolor)
		self.txtDropTailLength.configure(insertbackground=_fgcolor)
		self.txtDropTailLength.configure(selectbackground=_highlightbgcolor)
		self.txtDropTailLength.configure(selectforeground=_fgcolor)
		self.txtDropTailLength.configure(relief=FLAT)
		validateSupport = self.txtDropTailLength.register(self.validateFloat)
		self.txtDropTailLength.configure(validate="key")
		self.txtDropTailLength.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtDropTailLength.bind("<Return>", self.onEnter)
		# self.txtDropTailLength.bind("<Button-1>", self.loadData)

		self.txtPocketHeight = Entry(self.cnvsData)
		self.txtPocketHeight.place(relx=0.51, rely=0.96, relheight=0.03, relwidth=0.47)
		self.txtPocketHeight.configure(background=_bgcolor)
		self.txtPocketHeight.configure(disabledforeground="#a3a3a3")
		self.txtPocketHeight.configure(font=("TkFixedFont", 12, 'bold'))
		self.txtPocketHeight.configure(foreground=_fgcolor)
		self.txtPocketHeight.configure(highlightbackground=_bgcolor)
		self.txtPocketHeight.configure(highlightcolor=_fgcolor)
		self.txtPocketHeight.configure(insertbackground=_fgcolor)
		self.txtPocketHeight.configure(selectbackground=_highlightbgcolor)
		self.txtPocketHeight.configure(selectforeground=_fgcolor)
		self.txtPocketHeight.configure(relief=FLAT)
		validateSupport = self.txtPocketHeight.register(self.validateFloat)
		self.txtPocketHeight.configure(validate="key")
		self.txtPocketHeight.configure(validatecommand=(validateSupport, '%S', '%s', '%d'))

		self.txtPocketHeight.bind("<Return>", self.onEnter)
		# self.txtPocketHeight.bind("<Button-1>", self.loadData)


		self.cnvsLive = Canvas(top)
		self.cnvsLive.place(relx=0.30, rely=0.02, relheight=0.96, relwidth=0.69)
		self.cnvsLive.configure(relief=FLAT)
		self.cnvsLive.configure(borderwidth="0")
		self.cnvsLive.configure(background=_bgcolor)
		self.cnvsLive.configure(highlightbackground=_bgcolor)
		self.cnvsLive.configure(highlightcolor=_bgcolor)
		# self.cnvsLive.configure(background=_fgcolor)
		# self.cnvsLive.configure(highlightbackground=_fgcolor)
		# self.cnvsLive.configure(highlightcolor=_fgcolor)
		# self.cnvsLive.configure(width=355)

		self.lblImage = Label(self.cnvsLive)
		# self.lblImage.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)
		self.lblImage.place(relx=0.00, rely=0.00, relheight=1.00, relwidth=1.00)
		# self.lblImage.place(relx=0.01, rely=0.01)
		self.lblImage.configure(activebackground="#f9f9f9")
		self.lblImage.configure(activeforeground=_fgcolor)
		self.lblImage.configure(background=_bgcolor)
		self.lblImage.configure(disabledforeground="#a3a3a3")
		self.lblImage.configure(foreground=_fgcolor)
		self.lblImage.configure(highlightbackground=_bgcolor)
		self.lblImage.configure(highlightcolor=_fgcolor)
		self.lblImage.configure(font=('Helvetica', 28, 'bold'))
		self.lblImage.configure(text='''Live''')


		self.frameSave = Frame(top)
		self.frameSave.place(relx=0.01, rely=0.92, relheight=0.06, relwidth=0.28)
		self.frameSave.configure(relief=FLAT)
		self.frameSave.configure(borderwidth="0.5")
		self.frameSave.configure(background=_bgcolor)
		self.frameSave.configure(highlightbackground=_bgcolor)
		self.frameSave.configure(highlightcolor=_fgcolor)
		# self.frameSave.configure(background=_fgcolor)
		# self.frameSave.configure(highlightbackground=_fgcolor)
		# self.frameSave.configure(highlightcolor=_fgcolor)
		# self.frameSave.configure(width=355)

		self.btnSave = Button(self.frameSave)
		# self.btnSave.place(relx=0.07, rely=0.2, height=54, width=300)
		self.btnSave.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
		self.btnSave.configure(activebackground="#008000")
		self.btnSave.configure(activeforeground=_fgcolor)
		self.btnSave.configure(background="#3A5FCD")
		# self.btnSave.configure(background=_bgcolor)
		self.btnSave.configure(cursor="hand2")
		self.btnSave.configure(relief=FLAT)
		self.btnSave.configure(disabledforeground=_fgcolor)
		self.btnSave.configure(foreground=_fgcolor)
		self.btnSave.configure(highlightbackground=_fgcolor)
		self.btnSave.configure(highlightcolor=_fgcolor)
		self.btnSave.configure(pady="0")
		self.btnSave.configure(state="normal")
		self.btnSave.configure(font=('Helvetica', 20, 'bold'))
		self.btnSave.configure(text='''Save''')
		# self.btnSave.configure(command=SmartTable_p3_3_FGHub.getMeasurements)
		self.btnSave.configure(command=self.saveMeasurements)


		# self.thread = None
		# self.stopEvent = None

		# self.stopEvent = threading.Event()
		# self.thread = threading.Thread(target=self.liveMeasuring)
		stopEvent = threading.Event()
		thread = threading.Thread(target=self.liveMeasuring)
		# self.thread = threading.Thread(target=self.liveMeasuring, daemon=True)
		# self.thread = threading.Thread(target=self.liveTest)

		# self.thread.start()
		thread.start()

		# root.protocol("WM_DELETE_WINDOW", self.on_closing)



	# def on_closing(self):
	# 	self.thread.stop()
	# 	print("Done")



# ~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~

serRead = None
ser = None
buttonPressed = False

tableIndex = "st0001"
poNumber = None
liNumber = None
plant = None
styleNumber = None
size = None
targetBodyHeight = 0
bodyHeightTol = 0
targetBodyWidth = 0
bodyWidthTol = 0
targetBodySweep = 0
bodySweepTol = 0
targetBackNeckWidth = 0
backNeckWidthTol = 0
whiteMode = None

thread = None
stopEvent = None

initSerialRead()


if __name__ == '__main__':
	vp_start_gui()

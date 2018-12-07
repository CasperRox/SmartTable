import serial
import serial.tools.list_ports
import time
import pymysql.cursors
import datetime
import sys


status = None
ser = None

connection = pymysql.connect(host='localhost',
							user='root',
							password='password',
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)

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
# ser = serial.Serial('COM15', 9600, timeout=1)			# comport, baud-rate, timeout=the max time between two button press events to capture them within one buffer

# ser = serial.Serial('/dev/tty.usbserial', 9600)
# ser = serial.Serial('/dev/ttyUSB0')
# time.sleep(2)

try:
	with connection.cursor() as cursor:
		cursor.execute("create database if not exists nmc")
		cursor.execute("use nmc")
		cursor.execute("""
		create table if not exists PolyTop_Records (
			Date_Time varchar(30) not null,
			Style varchar(100) not null,
			Size varchar(10) not null,
			BodyHeight float(4,1) not null,
			BodyWidth float(4,1) not null,
			BodySweap float(4,1) not null,
			BackNeckWidth float(4,1) not null,
			primary key(Date_Time, Style, Size)
		);
		""")
	connection.commit()
finally:
	connection.close()

a=0
while True:
	if ser is not None:
		a=a+1
		print(a)
		# print(ser)
		# status = ser.readline()
		status = ser.readlines()
		# print(status)
		# print(ser.readlines())
		# ser.readlines()

		# if status == 1:
		if len(status)>0 and status[0] == b'1\r\n' and a%10==0:
			print ("Button pressed")

			connection = pymysql.connect(host='localhost',
										user='root',
										password='password',
										charset='utf8mb4',
										cursorclass=pymysql.cursors.DictCursor)

			try:
				with connection.cursor() as cursor:
					cursor.execute("use nmc")
					sql = (
						"INSERT INTO PolyTop_Records VALUES (%s, %s, %s, %s, %s, %s, %s) "
						"ON DUPLICATE KEY UPDATE "
						"Date_Time = %s, Style = %s, Size = %s, "
						"BodyHeight = %s, BodyWidth = %s, BodySweap = %s, BackNeckWidth = %s"
					)
					cursor.execute(sql, (datetime.datetime.now(), '123', 'm', float(25), float(11), float(19), float(91),
										datetime.datetime.now(), '123', 'm', float(25), float(11), float(19), float(91)))
				connection.commit()
			finally:
				connection.close()

		# time.sleep(1)

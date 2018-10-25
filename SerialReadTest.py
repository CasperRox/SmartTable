import serial
import time
import pymysql.cursors
import datetime

# ser = serial.Serial('/dev/tty.usbserial', 9600)
# ser = serial.Serial('/dev/ttyUSB0')
ser = serial.Serial('COM15', 9600)
# time.sleep(2)

status = 0

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



while True:
	status = ser.readline()
	print(status)

	# if status == 1:
	if status == b'1\r\n':
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

	time.sleep(2)

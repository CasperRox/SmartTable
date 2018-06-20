import csv

with open('CalibrationDataFile.csv', newline='') as csvfile:
	data = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))
	print("sssssssss", float(data[1][0].split(',')[1]))
	# data = csv.reader(csvfile, delimiter=' ', quotechar='|')
	# for row in data:
	# 	# print(', '.join(row))
	# 	print(row[0])
	# 	# a,b,c,d = row[0].split(',')
	# 	if len(row[0].split(',')) == 2:
	# 		a,b = row[0].split(',')
	# 		print(a)
	# 		print(b)
	# 	print('test')
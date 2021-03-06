import numpy as np
import cv2
import math
# import pymysql.cursors
import csv


def getmmDistance(pixel):														# Calibration to get mm from pixel
	global calibrationSlope, calibrationIntersect
	# mm = ((pixel - 2.7463) / 0.559)
	mm = ((pixel - calibrationIntersect) / calibrationSlope)
	if mm > 0:
		return mm
	else:
		return 0


def getPixelDistance(mm):														# Calibration to get pixel from mm
	global calibrationSlope, calibrationIntersect
	# pixel = (0.559 * mm) + 2.7463
	pixel = (calibrationSlope * mm) + calibrationIntersect
	if pixel > 0:
		return pixel
	else:
		return 0


def addTextOnFrame(imgSrc):														# Add default text on frame and resize it
	global styleNo, size
	(height, width) = imgSrc.shape[:2]
	# frame_diagonal = int(math.sqrt(math.pow(height,2) + math.pow(width,2)))
	# rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), 180, 1)	# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# rotation_matrix[0,2] += int((height/2)-width/2)
	# rotation_matrix[1,2] += int((width/2)-height/2)
	# imgSrc = cv2.warpAffine(imgSrc, rotation_matrix, (width,height))			# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)
	imgTemp = imgSrc.copy()
	cv2.rectangle(imgTemp,(0,0),(width,25),(0,0,0),-1)
	cv2.addWeighted(imgTemp,0.5,imgSrc,0.5,0,imgSrc)							# Adding transparent layer
	cv2.putText(imgSrc, "Style No: %s     Size: %s" %(styleNo, size), (20,15), cv2.FONT_HERSHEY_TRIPLEX, 0.40, (255,255,255), 1, cv2.LINE_AA)
	cv2.putText(imgSrc, "Press 'q' to Exit", (width-150,15), cv2.FONT_HERSHEY_TRIPLEX, 0.40, (255,255,255), 1, cv2.LINE_AA)
	imgSrc = cv2.resize(imgSrc, (int(width*1.2),int(height*1.2)))
	# imgSrc = cv2.resize(imgSrc, (int(width*1.45),int(height*1.45)))
	# imgSrc = cv2.resize(imgSrc, (int(width*2.1),int(height*2.1)))
	# imgSrc = cv2.resize(imgSrc, (int(width*2.5),int(height*2.2)))
	# imgSrc = cv2.resize(imgSrc, (int(width*0.7),int(height*0.7)))
	# imgSrc = cv2.resize(imgSrc, (int(width*0.3),int(height*0.3)))
	return imgSrc


def valueColor(value, comparator, tolerance):
	color = (0,0,0)
	if abs(comparator - value) <= tolerance - 0.3:
		color = (0,255,0)
	elif abs(comparator - value) <= tolerance + 0.3:
		color = (0,255,255)
	else:
		color = (0,0,255)
	return color


def tshirtMeasuring(imgSrc):
	# print("New")
	global preRotatedFrame, preRotatedMask, preAreaTshirt
	global preHeight, preSweap, preWidth, preBackNeck
	global targetBodyHeight, targetBodyHeightTol, targetBodyWidth, targetBodyWidthTol
	global targetBodySweap, targetBodySweapTol, targetBackNeckWidth, targetBackNeckWidthTol
	global whiteMode
	frame = imgSrc.copy()														# Backup original image
	# cv2.imshow("Original", imgSrc)

	# (height, width) = frame.shape[:2]
	# rotation_matrix_temp = cv2.getRotationMatrix2D((width/2, height/2), 180, 1)	# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# frame = cv2.warpAffine(frame, rotation_matrix_temp, (width,height))			# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)

	# (height, width) = frame.shape[:2]
	# rotation_matrix1 = cv2.getRotationMatrix2D((width/2, height/2), 270, 1)		# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# # rotation_matrix1 = cv2.getRotationMatrix2D((width/2, height/2), 90, 1)		# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# rotation_matrix1[0,2] += int((height/2)-width/2)
	# rotation_matrix1[1,2] += int((width/2)-height/2)
	# frame = cv2.warpAffine(frame, rotation_matrix1, (height,width))				# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)
	(height, width) = frame.shape[:2]
	# print("height ", height, "width ", width)
	# frame = frame[int(150/640*height):int(590/640*height), 0:width]
	# frame = frame[150:590, 0:480]
	gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)						# Convert image into grayscale
	# median = cv2.medianBlur(gray, 11)											# Median filtering(second parameter can only be an odd number)
	median = cv2.medianBlur(gray, 7)											# Median filtering(second parameter can only be an odd number)
	# cv2.imshow("Test1", median)
	# thresh = 200
	thresh = 180
	binary = cv2.threshold(median, thresh, 255, cv2.THRESH_BINARY_INV)[1]		# Convert image into black & white
	if "ON" == whiteMode:
		thresh = 75
		binary = cv2.threshold(median, thresh, 255, cv2.THRESH_BINARY)[1]		# Convert image into black & white
	# binary = cv2.Canny(median, 30, 150)			# Edge detection(2nd & 3rd parameters are minVal & maxVal, 
													# below min -> not edge, above max -> sure edge, between -> only is connected with sure edge)
	# kernel = np.ones((5,5),np.uint8)											# for Morphology
	# binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)				# dilation then erosion

	binary = cv2.dilate(binary, None, iterations=2)								# Dilation - make bigger white area
	binary = cv2.erode(binary, None, iterations=2)								# Erosion - make smaller white area
	# cv2.imshow("Test2", binary)

	cnts = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]	# Contour tracking(), function will modify source image
	if len(cnts) == 0:			# If no contours detected skip further process
		return addTextOnFrame(frame)


	# test_img = cv2.imread("E:\MachineLearning\Images\TShirt\img2890.jpg")
	# # rotation_matrix2 = cv2.getRotationMatrix2D((width/2, height/2), 10, 1)		# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# # binary2 = cv2.warpAffine(binary.copy(), rotation_matrix2, (width,height))
	# gray2 = cv2.cvtColor(test_img.copy(), cv2.COLOR_BGR2GRAY)						# Convert image into grayscale
	# median2 = cv2.medianBlur(gray2, 11)											# Median filtering(second parameter can only be an odd number)
	# thresh2 = 200
	# binary2 = cv2.threshold(median2, thresh2, 255, cv2.THRESH_BINARY_INV)[1]		# Convert image into black & white
	# binary2 = cv2.dilate(binary2, None, iterations=2)								# Dilation - make bigger white area
	# binary2 = cv2.erode(binary2, None, iterations=2)								# Erosion - make smaller white area
	# cnts2 = cv2.findContours(binary2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]	# Contour tracking(), function will modify source image
	# cnts2 = sorted(cnts2, key = cv2.contourArea, reverse = True)[:1]				# Sort contours area wise from bigger to smaller
	# cv2.drawContours(test_img, cnts2, 0, (0,255,0), 3)								# Draw boundary for contour(-1 for third -> draw all contours, 3 -> width of boundary)
	# cv2.imshow("Test5", test_img)


	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]				# Sort contours area wise from bigger to smaller

	# print(cv2.matchShapes(cnts[0],cnts2[0],1,0.0))


	areaTshirt = cv2.contourArea(cnts[0])
	# print("area %.2f" %areaTshirt)
	if (areaTshirt<(height*width*.20)) or ((height*width*.75)<areaTshirt):		# If contour is too small or too big, ignore it
		return addTextOnFrame(frame)

	cv2.drawContours(frame, cnts, 0, (0,255,0), 2)								# Draw boundary for contour(-1 for third -> draw all contours, 3 -> width of boundary)
	mask = np.zeros(gray.shape,np.uint8)										# Create a black colored empty frame
	cv2.drawContours(mask, cnts, 0, 255, -1)				# Draw T.shirt on it (0 -> contourIndex, 255 -> color(white), -1 -> filledContour)
															# Color can be represented using one integer since "mask" is black & white (or grayscale)
	cv2.imshow("Test3", mask)

	ellipse = cv2.fitEllipse(cnts[0])						# [ellipse] = [(center), (MajorAxisLength, MinorAxisLength), clockwiseAngleFromXAxisToMajorOrMinorAxis]
	print(ellipse)		#!!!!!!!!!!!!!!!!!!!
	if len(ellipse) < 1:														# If ellipse detection false, all other calculations are useless
		return addTextOnFrame(frame)

	cv2.ellipse(frame, ellipse, (0,0,255), 3)		#!!!!!!!!!!!!!!!!!!!!!!!!
	# print(int(ellipse[0][0]), int(ellipse[0][1]))
	box = cv2.boxPoints(ellipse)		#!!!!!!!!!!!!!!!!!!!!												# Take 4 cordinates of enclosing rectangle for the ellipse
	box = np.int0(box)		#!!!!!!!!!!!!!!!!!!!
	cv2.drawContours(frame,[box],0,(0,0,255),3)		#!!!!!!!!!!!!!!!!!!!!!!!
	# print(box)

	# frame_diagonal = int(math.sqrt(math.pow(height,2) + math.pow(width,2)))
	rotation_angle = 0
	if ellipse[2] <= 90:
		rotation_angle = ellipse[2]
	else:
		rotation_angle = ellipse[2] + 180
	print(rotation_angle)		#!!!!!!!!!!!!!!!!!!!!!!!
	rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], rotation_angle, 1)	# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# rotation_matrix = cv2.getRotationMatrix2D((int(ellipse[0][0]),int(ellipse[0][1])), (int(ellipse[2])-90), 1)
	# rotation_matrix[0,2] += int((frame_diagonal/2)-ellipse[0][0])
	# rotation_matrix[1,2] += int((frame_diagonal/2)-ellipse[0][1])

	rotated_mask = cv2.warpAffine(mask, rotation_matrix, (width,height))		# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)		#!!!!!!!!!!!!!!!!!!!!!!
	# rotated_mask = mask.copy()		!!!!!!!!!!!!!!!!!!!!!!!!!!!
	# rotated_frame = cv2.warpAffine(frame, rotation_matrix, (frame_diagonal,frame_diagonal))		# Rotate actual image
	rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width,height))		#!!!!!!!!!!!!!!!!!!!!
	# rotated_frame = frame.copy()		!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	cv2.imshow("Test4", rotated_mask)
	cv2.imshow("Test5", rotated_frame)

	dummy = np.full(frame.shape, 255, np.uint8)									# Dummy white image to get missing parts of rotated frame
	rotated_dummy = cv2.warpAffine(dummy, rotation_matrix, (width,height))		# Rotate dummy to get exact position

	# if abs(areaTshirt - preAreaTshirt) < (height*width*.01):
	# 	rotated_frame = preRotatedFrame.copy()
	# 	rotated_mask = preRotatedMask.copy()
	# 	return addTextOnFrame(preRotatedFrame.copy())
	# else:
	# 	preRotatedFrame = rotated_frame.copy()
	# 	preRotatedMask = rotated_mask.copy()
	# 	preAreaTshirt = areaTshirt
	# print("areaPre %.2f" %preAreaTshirt)

	# cv2.drawContours(frame, cnts, 0, (0,255,0), 3)								# Draw boundary for contour(-1 for third -> draw all contours, 3 -> width of boundary)

	# *************************************************************
	# ***********************Body Height***************************
	# *************************************************************
	transpose_rotated_mask = np.transpose(rotated_mask)							# Easy to consider row wise
	height_array_x = int(ellipse[0][0])
	# print(transpose_rotated_mask[height_array_x])
	white = False
	body_height_first = 0
	body_height_last = 0
	if height_array_x<=0 or width<=height_array_x:								# If center of ellipse is at out of frame, further calculations are useless
		return addTextOnFrame(frame)

	for i in range(0,len(transpose_rotated_mask[height_array_x])):				# Calculate pixel height by checking pixel value
		if white == False and transpose_rotated_mask[height_array_x][i] != 0:
			body_height_first = i 												# first white pixel
			white = True
		elif white == True and transpose_rotated_mask[height_array_x][i] == 0:
			body_height_last = i-1												# last white pixel
			white = False
	pixel_height = body_height_last - body_height_first - 12
	# print("pixelHeight = %d" %pixel_height)
	if pixel_height <= getPixelDistance(250):									# If height is less than 25cm, most probably it is a garbage value
		return addTextOnFrame(frame)
	cv2.line(rotated_frame, (height_array_x,body_height_first+12), (height_array_x,body_height_last), (255,0,0), 2)	# Draw height calculating line on image
	cv2.circle(rotated_frame,(height_array_x,body_height_first+12), 3, (0,0,255), -1)
	cv2.circle(rotated_frame,(height_array_x,body_height_last), 3, (0,0,255), -1)
	font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
	valueHeight = getmmDistance(pixel_height)/10
	if abs(preHeight - valueHeight) < 1:
		valueHeight = preHeight
	else:
		preHeight = valueHeight
	cv2.putText(rotated_frame, '%.1f cm / %.1f cm' %(valueHeight, targetBodyHeight), (height_array_x+10,body_height_first+100), 
				font, 0.5, valueColor(valueHeight, targetBodyHeight, targetBodyHeightTol), 1, cv2.LINE_AA)	# Display height value on image


	# *************************************************************
	# *************************************************************
	# *************************************************************
	mid_width_array_y = int(ellipse[0][1])										# To calculate body sweap & body width
	sleeve_check_length = int(pixel_height * 27 /100)							# Guessing the general distance from middle to sleeve level
	# cv2.line(rotated_frame, (0,mid_width_array_y), (640,mid_width_array_y), (255,0,0), 3)													# Middle line
	# cv2.line(rotated_frame, (0,mid_width_array_y-sleeve_check_length), (640,mid_width_array_y-sleeve_check_length), (255,255,0), 3)		# Sleeve check line
	# cv2.line(rotated_frame, (0,mid_width_array_y+sleeve_check_length), (640,mid_width_array_y+sleeve_check_length), (255,255,0), 3)		# Sleeve check line
	if mid_width_array_y<=sleeve_check_length or (height-sleeve_check_length)<=mid_width_array_y or sleeve_check_length<=0:		# If this false width calculation is useless

		# !!!!!!!!!!!!!!!!!
		rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], (360-rotation_angle), 1)		# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
		rotated_frame = cv2.warpAffine(rotated_frame, rotation_matrix, (width,height))		# Rotate actual image
		rotated_dummy = cv2.warpAffine(rotated_dummy, rotation_matrix, (width,height))		# Rotate actual image
		rotated_frame = cv2.add(rotated_frame, cv2.subtract(frame, rotated_dummy))			# Fill missing parts of final output
		# !!!!!!!!!!!!!!!!!

		# cv2.addWeighted(frame,0.5,rotated_frame,0.5,0,rotated_frame)						# Adding missing parts
		return addTextOnFrame(rotated_frame)

	sleeve_check_temp1_count = np.count_nonzero(rotated_mask[mid_width_array_y-sleeve_check_length])	# Get number of white pixels
	sleeve_check_temp2_count = np.count_nonzero(rotated_mask[mid_width_array_y+sleeve_check_length])	# Get number of white pixels
	sleeve_side = 0
	non_sleeve_side = 0
	rotated = False																# To capture rotated or not
	if sleeve_check_temp1_count > sleeve_check_temp2_count:						# Sleeves are at starting side
		sleeve_side = mid_width_array_y-sleeve_check_length
		non_sleeve_side = mid_width_array_y+sleeve_check_length
		rotated = False
	else:																		# Sleeves are at ending side
		sleeve_side = mid_width_array_y+sleeve_check_length
		non_sleeve_side = mid_width_array_y-sleeve_check_length
		rotated = True


	# *************************************************************
	# ***********************Body Sweap****************************
	# *************************************************************
	body_sweap_y = 0
	temp_width_pre = np.count_nonzero(rotated_mask[non_sleeve_side])			# Storing previous white pixel count to check with next
	step = 1																	# White pixel count checking step size
	while True:																	# Loop to get the body sweap pixel line
		if rotated == False:
			non_sleeve_side += step 											# Checking ending side
			if non_sleeve_side >= body_height_last-step:
				break
			temp_count = np.count_nonzero(rotated_mask[non_sleeve_side])
			if temp_count < temp_width_pre-5:										# Compare pixel counts
				temp_count2 = np.count_nonzero(rotated_mask[non_sleeve_side+step])
				if temp_count2 < temp_count-5:									# Compare next line also to verify
					body_sweap_y = non_sleeve_side-step
					break
			else:
				temp_width_pre = temp_count 									# Update previous pixel count
		else:
			non_sleeve_side -= step 											# Checking starting side
			if non_sleeve_side <= body_height_first+step:
				break
			temp_count = np.count_nonzero(rotated_mask[non_sleeve_side])
			if temp_count < temp_width_pre-5: 									# Compare pixel counts
				temp_count2 = np.count_nonzero(rotated_mask[non_sleeve_side-step])
				if temp_count2 < temp_count-5:									# Compare next line also to verify
					body_sweap_y = non_sleeve_side+step
					break
			else:
				temp_width_pre = temp_count 									# Update previous pixel count

	if 0 < body_sweap_y and body_sweap_y < height:
		white = False
		first = 0
		last = 0
		for i in range(0,len(rotated_mask[body_sweap_y])):						# Calculate pixel body sweap by checking pixel value
			if white == False and rotated_mask[body_sweap_y][i] != 0:
				first = i 														# First white pixel
				white = True
			elif white == True and rotated_mask[body_sweap_y][i] == 0:
				last = i-1 														# Last white pixel
				white = False
		pixel_body_sweap = last - first
		# print("pixelBodySweap = %d" %pixel_body_sweap)
		cv2.line(rotated_frame, (first,body_sweap_y), (last,body_sweap_y), (255,0,0), 2)	# Draw body sweap calculating line on image
		cv2.circle(rotated_frame,(first,body_sweap_y), 3, (0,0,255), -1)
		cv2.circle(rotated_frame,(last,body_sweap_y), 3, (0,0,255), -1)
		font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
		valueSweap = (getmmDistance(pixel_body_sweap)/10)
		if abs(preSweap - valueSweap) < 1:
			valueSweap = preSweap
		else:
			preSweap = valueSweap
		cv2.putText(rotated_frame, '%.1f cm / %.1f cm' %(valueSweap, targetBodySweap), (first,body_sweap_y-10),
					font, 0.5, valueColor(valueSweap, targetBodySweap, targetBodySweapTol), 1, cv2.LINE_AA)	# Display body sweap value on image


	# *************************************************************
	# *************************Body Width**************************
	# *************************************************************
	body_width_y = 0
	temp_width_pre = np.count_nonzero(rotated_mask[mid_width_array_y])			# To compare with
	sleeve_check = mid_width_array_y 											# Sleeve checking pixel line
	step = 2 																	# Sleeve checking step size
	# body_width_y_dif = int(getPixelDistance(25)/step)							# Pixel distance from sleeve joint to body width
	body_width_y_dif = int(getPixelDistance(35)/step)							# Pixel distance from sleeve joint to body width
	body_width_first = [] 														# To store white area starting points
	body_width_last = [] 														# To store white area ending points
	count_for_dif = 0
	dif = 5																		# Target pixel difference at sleeve starting
	continuous_white_counts = []												# Number of white pixels in each white region
	max_index = 0																# Index of region which have max no. of white pixels
	first = []																	# Starting points of each white ragion
	last = []																	# Ending points of each white region
	pixel_body_width_actual = 0
	while True:
		count_for_dif += 1														# No. of cycles in the loop
		if rotated == False:
			sleeve_check -= step												# Pixel value checking frequency
			if sleeve_check <= sleeve_side:
				break
			white = False
			continuous_white = 0
			continuous_white_counts = []
			for i in range(0,len(rotated_mask[sleeve_check])):					# Calculate continuous white by checking pixel value
				if white == False and rotated_mask[sleeve_check][i] != 0:		# Black to white
					first.append(i)
					continuous_white = 1
					white = True
				elif white == True and rotated_mask[sleeve_check][i] != 0:		# White to white
					continuous_white += 1
					white = True
				elif white == True and rotated_mask[sleeve_check][i] == 0:		# White to white
					continuous_white_counts.append(continuous_white)
					last.append(i)
					white = False
			if len(continuous_white_counts) > 0:								# If white areas found
				max_index = np.argmax(continuous_white_counts)
				if count_for_dif - body_width_y_dif > 0:
					body_width_first.append(first[max_index])					# Storing first & last values of several pixel lines before
					body_width_last.append(last[max_index])
				temp_count = continuous_white_counts[max_index]
				if temp_count > temp_width_pre+dif:								# Sleeve detected
					body_width_y = sleeve_check+step
					break
				else:
					temp_width_pre = temp_count
		else:																	# Same as previous, but changing the scaning direction
			sleeve_check += step
			if sleeve_check >= sleeve_side:
				break
			white = False
			continuous_white = 0
			continuous_white_counts = []
			for i in range(0,len(rotated_mask[sleeve_check])):					# Calculate continuous white by checking pixel value
				if white == False and rotated_mask[sleeve_check][i] != 0:
					first.append(i)
					continuous_white = 1
					white = True
				elif white == True and rotated_mask[sleeve_check][i] != 0:
					continuous_white += 1
					white = True
				elif white == True and rotated_mask[sleeve_check][i] == 0:
					continuous_white_counts.append(continuous_white)
					last.append(i)
					white = False
			if len(continuous_white_counts) > 0:
				max_index = np.argmax(continuous_white_counts)
				if count_for_dif - body_width_y_dif > 0:
					body_width_first.append(first[max_index])
					body_width_last.append(last[max_index])
				temp_count = continuous_white_counts[max_index]
				if temp_count > temp_width_pre+dif:
					body_width_y = sleeve_check-step
					break
				else:
					temp_width_pre = temp_count
	
	if len(continuous_white_counts) > 0:
		pixel_body_width = continuous_white_counts[max_index]					# Body width in pixels
		# pixel_body_width2 = last[max_index] - first[max_index]				# Body width in pixels

		if len(body_width_first)>0 and len(body_width_last)>0:
			pixel_body_width_actual = body_width_last[len(body_width_last)-1] - body_width_first[len(body_width_first)-1]
			# pixel_body_width_actual = body_width_last[len(body_width_last)-1-body_width_y_dif] - body_width_first[len(body_width_first)-1-body_width_y_dif]
			# print("pixelBodyWidthActual = %d" %pixel_body_width_actual)
			if rotated == False:
				cv2.line(rotated_frame, (body_width_first[len(body_width_first)-1],(body_width_y+body_width_y_dif*step)),
					(body_width_last[len(body_width_last)-1],(body_width_y+body_width_y_dif*step)), (255,0,0), 2)	# Draw body width calculating line on image
				# cv2.line(rotated_frame, (body_width_first[len(body_width_first)-1-body_width_y_dif],(body_width_y+body_width_y_dif)),
				# 	(body_width_last[len(body_width_last)-1-body_width_y_dif],(body_width_y+body_width_y_dif)), (255,0,0), 3)	# Draw body width calculating line on image
				cv2.circle(rotated_frame,(body_width_first[len(body_width_first)-1],(body_width_y+body_width_y_dif*step)), 3, (0,0,255), -1)
				cv2.circle(rotated_frame,(body_width_last[len(body_width_last)-1],(body_width_y+body_width_y_dif*step)), 3, (0,0,255), -1)
			else:
				cv2.line(rotated_frame, (body_width_first[len(body_width_first)-1],(body_width_y-body_width_y_dif*step)),
					(body_width_last[len(body_width_last)-1],(body_width_y-body_width_y_dif*step)), (255,0,0), 2)	# Draw body width calculating line on image
				# cv2.line(rotated_frame, (body_width_first[len(body_width_first)-1-body_width_y_dif],(body_width_y-body_width_y_dif)),
				# 	(body_width_last[len(body_width_last)-1-body_width_y_dif],(body_width_y-body_width_y_dif)), (255,0,0), 3)	# Draw body width calculating line on image
				cv2.circle(rotated_frame,(body_width_first[len(body_width_first)-1],(body_width_y-body_width_y_dif*step)), 3, (0,0,255), -1)
				cv2.circle(rotated_frame,(body_width_last[len(body_width_last)-1],(body_width_y-body_width_y_dif*step)), 3, (0,0,255), -1)
			font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
			valueWidth = (getmmDistance(pixel_body_width_actual)/10)
			if abs(preWidth - valueWidth) < 1:
				valueWidth = preWidth
			else:
				preWidth = valueWidth
			cv2.putText(rotated_frame, '%.1f cm / %.1f cm' %(valueWidth, targetBodyWidth), (body_width_first[len(body_width_first)-1],body_width_y-10),
						font, 0.5, valueColor(valueWidth, targetBodyWidth, targetBodyWidthTol), 1, cv2.LINE_AA)		# Display body width value on image


	# rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], (360-rotation_angle), 1)	# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# rotated_frame = cv2.warpAffine(rotated_frame, rotation_matrix, (width,height))	# Rotate actual image
	# rotated_dummy = cv2.warpAffine(rotated_dummy, rotation_matrix, (width,height))	# Rotate actual image
	# rotated_frame = cv2.add(rotated_frame, cv2.subtract(frame, rotated_dummy))		# Fill missing parts of final output
	# cv2.addWeighted(frame,0.5,rotated_frame,0.5,0,rotated_frame)					# Adding missing parts
	# return addTextOnFrame(rotated_frame)


	# *************************************************************
	# **********************Back Neck Width************************
	# *************************************************************
	############################################## First identify x positions and then y position

	# print("height_array_x ", height_array_x)
	back_neck_x1 = height_array_x 												# Initializing to the center of neck
	back_neck_x2 = height_array_x
	back_neck_y1 = 0 															# Initializing to zero
	back_neck_y2 = 0
	step = int(width*0.005)														# Neck checking step size changes according to camera frame size
	temp_count_pre_1 = np.count_nonzero(transpose_rotated_mask[height_array_x])	# To store previous value to compare with white pixel count
	temp_count_pre_2 = temp_count_pre_1
	# print("pixel_body_width_actual ", pixel_body_width_actual)

	for i in range(int(pixel_body_width_actual*0.02),int(pixel_body_width_actual*0.5)):		# Pre guessing a range for neck width with respect to body width
		temp_count_1 = np.count_nonzero(transpose_rotated_mask[height_array_x+(i*step)])	# White pixel count to compare
		# print("test 1 ", temp_count_1)
		if temp_count_1 < temp_count_pre_1:
			temp_count_1_1 = np.count_nonzero(transpose_rotated_mask[height_array_x+(i*step)+step])
			if temp_count_1_1 < temp_count_1:
				back_neck_x1 = height_array_x + (i*step)
				break
		else:
			temp_count_pre_1 = temp_count_1

	for i in range(int(pixel_body_width_actual*0.02),int(pixel_body_width_actual*0.5)):
		temp_count_2 = np.count_nonzero(transpose_rotated_mask[height_array_x-(i*step)])
		# print("test 2 ", temp_count_2)
		if temp_count_2 < temp_count_pre_2:
			temp_count_2_1 = np.count_nonzero(transpose_rotated_mask[height_array_x-(i*step)-step])
			if (temp_count_2_1<temp_count_2): # and abs(temp_count_2-temp_count_1)<100:
				back_neck_x2 = height_array_x - (i*step)
				break
		else:
			temp_count_pre_2 = temp_count_2

	if rotated == False:
		# print("body_height_first ", body_height_first)
		# cv2.line(rotated_frame, (back_neck_x1,body_height_first), (back_neck_x2,body_height_first), (255,0,0), 3)
		# for i in range(0,body_height_first):
		for i in range(0,int(width*0.5)):
			# if transpose_rotated_mask[back_neck_x1,i] != 0:
			if rotated_mask[i,back_neck_x1] != 0:
				back_neck_y1 = i
				break
		# for i in range(0,body_height_first):
		for i in range(0,int(width*0.5)):
			# if transpose_rotated_mask[back_neck_x2,i] != 0:
			if rotated_mask[i,back_neck_x2] != 0:
				back_neck_y2 = i
				break

	else:
		for i in range(body_height_last,height):
			# if rotated_mask[back_neck_x1,i] == 0:
			if rotated_mask[i,back_neck_x1] == 0:
				back_neck_y1 = i-1
				break
		for i in range(body_height_last,height):
			# if rotated_mask[back_neck_x2,i] == 0:
			if rotated_mask[i,back_neck_x2] == 0:
				back_neck_y2 = i-1
				break

	# temp_img = cv2.resize(rotated_mask, (int(width*0.2),int(height*0.2)))
	# cv2.imshow("test6", temp_img)
	# print("neckWidth_x ", abs(back_neck_x2 - back_neck_x1))
	# print("neckWidth_y ", abs(back_neck_y2 - back_neck_y1))
	if width*0.05 < abs(back_neck_x2 - back_neck_x1) and abs(back_neck_x2 - back_neck_x1) < width*0.9 and abs(back_neck_y2 - back_neck_y1) < height*0.01:
		# print("******x1 ", back_neck_x1)
		# print("******x2 ", back_neck_x2)
		# print("******y1 ", back_neck_y1)
		# print("******y2 ", back_neck_y2)
		# cv2.line(rotated_frame, (back_neck_x1,body_height_last), (back_neck_x2,body_height_last), (255,0,0), 3)
		# cv2.line(rotated_frame, (back_neck_x1,body_height_first), (back_neck_x2,body_height_first), (255,0,0), 3)
		cv2.line(rotated_frame, (back_neck_x1,back_neck_y1), (back_neck_x2,back_neck_y2), (255,0,0), 2)
		cv2.circle(rotated_frame,(back_neck_x1,back_neck_y1), 3, (0,0,255), -1)
		cv2.circle(rotated_frame,(back_neck_x2,back_neck_y2), 3, (0,0,255), -1)
		font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
		pixel_back_neck = abs(back_neck_x2-back_neck_x1)
		valueBackNeck = getmmDistance(pixel_back_neck)/10
		if abs(preBackNeck - valueBackNeck) < 1:
			valueBackNeck = preBackNeck
		else:
			preBackNeck = valueBackNeck
		cv2.putText(rotated_frame, '%.1f cm / %.1f cm' %(valueBackNeck, targetBackNeckWidth), (back_neck_x1,back_neck_y1+20),
					font, 0.5, valueColor(valueBackNeck, targetBackNeckWidth, targetBackNeckWidthTol), 1, cv2.LINE_AA)		# Display body width value on image


	# if 
	# step = 5
	# if rotated:
	# 	neck_check_y = body_height_last
	# 	temp_count_pre = np.count_nonzero(rotated_mask[neck_check_y])
	# 	for i in range(body_height_last,height):
	# 		neck_check_y += step
	# 		temp_count = np.count_nonzero(rotated_mask[neck_check_y])
	# 		if temp_count == 0:
	# 			temp_count2 = np.count_nonzero(rotated_mask[neck_check_y+step])
	# 			if temp_count2 == 0:
	# 				back_neck_y = neck_check_y-step
	# 				break
	# 		else:
	# 			temp_count_pre = temp_count

	# 	print(body_height_last)
	# else:
	# 	print(body_height_first)

	# !!!!!!!!!!!!!!!!!!!!!!
	rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], (360-rotation_angle), 1)	# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	rotated_frame = cv2.warpAffine(rotated_frame, rotation_matrix, (width,height))	# Rotate actual image
	rotated_dummy = cv2.warpAffine(rotated_dummy, rotation_matrix, (width,height))	# Rotate actual image
	rotated_frame = cv2.add(rotated_frame, cv2.subtract(frame, rotated_dummy))		# Fill missing parts of final output
	# !!!!!!!!!!!!!!!!!!!!

	# preRotatedFrame = rotated_frame.copy()												# Save a copy to avoid value variation
	return addTextOnFrame(rotated_frame)


def getMeasurements():
# def getMeasurements(sN, sz, bH, bHT, bW, bWT, bS, bST, bNW, bNWT, wM):
# 	global styleNo, size, targetBodyHeight, targetBodyHeightTol, targetBodyWidth, targetBodyWidthTol
# 	global targetBodySweap, targetBodySweapTol, targetBackNeckWidth, targetBackNeckWidthTol
# 	global whiteMode
# 	styleNo = sN
# 	size = sz
# 	targetBodyHeight = float(bH)
# 	targetBodyHeightTol = float(bHT)
# 	targetBodyWidth = float(bW)
# 	targetBodyWidthTol = float(bWT)
# 	targetBodySweap = float(bS)
# 	targetBodySweapTol = float(bST)
# 	targetBackNeckWidth = float(bNW)
# 	targetBackNeckWidthTol = float(bNWT)

# 	whiteMode = wM

	loadCalibrationData()

	cap = cv2.VideoCapture(0)
	# cap = cv2.VideoCapture("E:\SmartTable_Test\WIN_20180907_14_59_07_Pro.mp4")
	# cap = cv2.VideoCapture("test\WIN_20180403_081531.MP4")
	# cap.set(cv2.CAP_PROP_SETTINGS, 0)
	# original = cv2.imread("test\WIN_20180126_152758.JPG")
	# count_temp = 0

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		if ret:
			# count_temp += 1
			# if count_temp%50 != 0:
			# 	# print(count_temp)
			# 	continue
			# print("New frame")
			(height, width) = frame.shape[:2]
			# print("height ", height, "width ", width)
			frame = frame[0:height, int(60/640*width):int(620/640*width)]
			# frame = frame[0:height, int(150/640*width):int(615/640*width)]
			# frame = frame[150:590, 0:480]
			output = tshirtMeasuring(frame)						# Process live video
			# output = tshirtMeasuring(original.copy())			# Process a saved image instead of live video
			cv2.imshow("Smart Table", output)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if cv2.waitKey(1) & 0xFF == ord('Q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()


def loadCalibrationData():
	global calibrationSlope, calibrationIntersect
	with open('CalibrationDataFile.csv', newline='') as csvfile:
		dataList = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))
		calibrationSlope = float(dataList[0][0].split(',')[1])
		calibrationIntersect = float(dataList[1][0].split(',')[1])


# ~~~~~~~~~~~~~~~~~ Main Program ~~~~~~~~~~~~~~~~~

preRotatedFrame = None
preRotatedMask = None
preAreaTshirt = 0
preHeight = 0
preSweap = 0
preWidth = 0
preBackNeck = 0

styleNo = None
size = None
targetBodyHeight = 0
targetBodyHeightTol = 0
targetBodyWidth = 0
targetBodyWidthTol = 0
targetBodySweap = 0
targetBodySweapTol = 0
targetBackNeckWidth = 0
targetBackNeckWidthTol = 0

calibrationSlope = 1
calibrationIntersect = 0

whiteMode = None

# initDatabase()
# getDatabaseValues()
# getMeasurements()

if __name__ == "__main__":
	getMeasurements()
	# testing()


# def testing():
# 	print("Testing")
# 	# cap.release()
# 	cv2.destroyAllWindows()

# def loopTest():
# 	print("Loop Test")
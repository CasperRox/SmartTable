import numpy as np
import cv2
import math


def getmmDistance(pixel):														# Calibration to get mm from pixel
    mm = ((pixel - 15.694) / 0.7056)
    if mm > 0:
        return mm
    else:
        return 0


def getPixelDistance(mm):														# Calibration to get pixel from mm
    pixel = (0.7056 * mm) + 15.694
    if pixel > 0:
        return pixel
    else:
        return 0


def addTextOnFrame(imgSrc):														# Add default text on frame and resize it
	(height, width) = imgSrc.shape[:2]
	# frame_diagonal = int(math.sqrt(math.pow(height,2) + math.pow(width,2)))
	# rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), 180, 1)			# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# rotation_matrix[0,2] += int((height/2)-width/2)
	# rotation_matrix[1,2] += int((width/2)-height/2)
	# imgSrc = cv2.warpAffine(imgSrc, rotation_matrix, (width,height))				# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)
	imgTemp = imgSrc.copy()
	cv2.rectangle(imgTemp,(0,0),(width,30),(0,0,0),-1)
	cv2.addWeighted(imgTemp,0.5,imgSrc,0.5,0,imgSrc)							# Adding transparent layer
	cv2.putText(imgSrc, "Press 'q' to Exit", (width-150,20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
	# imgSrc = cv2.resize(imgSrc, (int(width*1.5),int(height*1.5)))
	return imgSrc


def tshirtMeasuring(imgSrc):
	frame = imgSrc.copy()														# Backup original image
	# cv2.imshow("Original", imgSrc)

	(height, width) = frame.shape[:2]
	rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), 90, 1)			# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	rotation_matrix[0,2] += int((height/2)-width/2)
	rotation_matrix[1,2] += int((width/2)-height/2)
	frame = cv2.warpAffine(frame, rotation_matrix, (height,width))				# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)
	gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)						# Convert image into grayscale
	median = cv2.medianBlur(gray, 11)											# Median filtering(second parameter can only be an odd number)
	# cv2.imshow("Test1", median)
	thresh = 200
	binary = cv2.threshold(median, thresh, 255, cv2.THRESH_BINARY_INV)[1]		# Convert image into black & white
	# binary = cv2.Canny(median, 30, 150)			# Edge detection(2nd & 3rd parameters are minVal & maxVal, 
													# below min -> not edge, above max -> sure edge, between -> only is connected with sure edge)
	# kernel = np.ones((5,5),np.uint8)
	# binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)	# dilation then erosion
	binary = cv2.dilate(binary, None, iterations=2)								# Dilation - make bigger white area
	binary = cv2.erode(binary, None, iterations=2)								# Erosion - make smaller white area
	# cv2.imshow("Test2", binary)

	cnts = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]	# Contour tracking(), function will modify source image
	if len(cnts) == 0:			# If no contours detected skip further process
		return addTextOnFrame(frame)

	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]				# Sort contours area wise from bigger to smaller
	areaTshirt = cv2.contourArea(cnts[0])
	# print("area %.2f" %areaTshirt)
	if ((height*width*.25)>areaTshirt) or ((height*width*.7)<areaTshirt):		# If contour is too small or too big, ignore it
		return addTextOnFrame(frame)

	cv2.drawContours(frame, cnts, 0, (0,255,0), 3)								# Draw boundary for contour(-1 for third -> draw all contours, 3 -> width of boundary)
	mask = np.zeros(gray.shape,np.uint8)										# Create a black colored empty frame
	cv2.drawContours(mask, cnts, 0, 255, -1)				# Draw T.shirt on it (0 -> contourIndex, 255 -> color(white), -1 -> filledContour)
															# Color can be represented using one integer since "mask" is black & white (or grayscale)
	# cv2.imshow("Test3", mask)

	ellipse = cv2.fitEllipse(cnts[0])						# [ellipse] = [(center), (MajorAxisLength, MinorAxisLength), clockwiseAngleFromXAxisToMajorOrMinorAxis]
	if len(ellipse) < 1:																# If ellipse detection false, all other calculations are useless
		return addTextOnFrame(frame)

	# cv2.ellipse(frame, ellipse, (0,0,255), 3)
	# print(int(ellipse[0][0]), int(ellipse[0][1]))
	# box = cv2.boxPoints(ellipse)														# Take 4 cordinates of enclosing rectangle for the ellipse
	# box = np.int0(box)
	# cv2.drawContours(frame,[box],0,(0,0,255),3)
	# print(box)

	frame_diagonal = int(math.sqrt(math.pow(height,2) + math.pow(width,2)))
	rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], (ellipse[2]-90), 1)			# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	# rotation_matrix = cv2.getRotationMatrix2D((int(ellipse[0][0]),int(ellipse[0][1])), (int(ellipse[2])-90), 1)
	# rotation_matrix[0,2] += int((frame_diagonal/2)-ellipse[0][0])
	# rotation_matrix[1,2] += int((frame_diagonal/2)-ellipse[0][1])
	rotated_mask = cv2.warpAffine(mask, rotation_matrix, (width,height))				# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)
	# rotated_frame = cv2.warpAffine(frame, rotation_matrix, (frame_diagonal,frame_diagonal))		# Rotate actual image
	rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width,height))
	# cv2.imshow("Test4", rotated_mask)
	dummy = np.full(rotated_frame.shape, 255, np.uint8)									# Dummy white image to get missing parts of rotated frame
	rotated_dummy = cv2.warpAffine(dummy, rotation_matrix, (width,height))				# Rotate dummy to get exact position


	# *************************************************************
	# ***********************Body Height***************************
	# *************************************************************
	height_array_y = int(ellipse[0][1])
	# print(rotated_mask[height_array_y])
	white = False
	first = 0
	last = 0
	if height_array_y<=0 or height<=height_array_y:										# If center of ellipse is at out of frame, further calculations are useless
		return addTextOnFrame(frame)

	for i in range(0,len(rotated_mask[height_array_y])):								# Calculate pixel height by checking pixel value
		if white == False and rotated_mask[height_array_y][i] != 0:
			first = i 			# first white pixel
			white = True
		elif white == True and rotated_mask[height_array_y][i] == 0:
			last = i-1			# last white pixel
			white = False
	pixel_height = last - first
	# print("pixelHeight = %d" %pixel_height)
	cv2.line(rotated_frame, (first,height_array_y), (last,height_array_y), (255,0,0), 3)	# Draw height calculating line on image
	font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
	cv2.putText(rotated_frame, '%.1f cm' %(getmmDistance(pixel_height)/10), (first,height_array_y-10), font, 1, (255,0,0), 2, cv2.LINE_AA)	# Display height value on image


	# *************************************************************
	# *************************************************************
	# *************************************************************
	mid_width_array_x = int(ellipse[0][0])												# To calculate body sweap & body width
	sleeve_check_length = int(pixel_height * 27 /100)									# Guessing the general distance from middle to sleeve level
	# cv2.line(rotated_frame, (mid_width_array_x,0), (mid_width_array_x,480), (255,0,0), 3)													# Middle line
	# cv2.line(rotated_frame, (mid_width_array_x-sleeve_check_length,0), (mid_width_array_x-sleeve_check_length,480), (255,255,0), 3)		# Sleeve check line
	# cv2.line(rotated_frame, (mid_width_array_x+sleeve_check_length,0), (mid_width_array_x+sleeve_check_length,480), (255,255,0), 3)		# Sleeve check line
	if mid_width_array_x<sleeve_check_length or (width-sleeve_check_length)<mid_width_array_x or sleeve_check_length<0:		# If this false width calculation is useless
		rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], (360-(ellipse[2]-90)), 1)						# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
		rotated_frame = cv2.warpAffine(rotated_frame, rotation_matrix, (frame.shape[1],frame.shape[0]))		# Rotate actual image
		cv2.addWeighted(frame,0.5,rotated_frame,0.5,0,rotated_frame)										# Adding missing parts
		rotated_frame = cv2.add(rotated_frame, cv2.subtract(frame, rotated_dummy))									# Fill missing parts of final output
		return addTextOnFrame(rotated_frame)

	transpose_rotated_mask = np.transpose(rotated_mask)		# Easy to consider row wise
	sleeve_check_temp1_count = np.count_nonzero(transpose_rotated_mask[mid_width_array_x-sleeve_check_length])		# Get number of white pixels
	sleeve_check_temp2_count = np.count_nonzero(transpose_rotated_mask[mid_width_array_x+sleeve_check_length])		# Get number of white pixels
	sleeve_side = 0
	non_sleeve_side = 0
	rotated = False																		# To capture rotated or not
	if sleeve_check_temp1_count > sleeve_check_temp2_count:								# Sleeves are at starting side
		sleeve_side = mid_width_array_x-sleeve_check_length
		non_sleeve_side = mid_width_array_x+sleeve_check_length
		rotated = False
	else:																				# Sleeves are at ending side
		sleeve_side = mid_width_array_x+sleeve_check_length
		non_sleeve_side = mid_width_array_x-sleeve_check_length
		rotated = True


	# *************************************************************
	# ***********************Body Sweap****************************
	# *************************************************************
	body_sweap_x = 0
	temp_width_pre = np.count_nonzero(transpose_rotated_mask[non_sleeve_side])			# Storing previous white pixel count to check with next
	step = 5			# White pixel count checking step size
	while True:			# Loop to get the body sweap pixel line
		if rotated == False:
			non_sleeve_side += step 													# Checking ending side
			if non_sleeve_side > last:
				break
			temp_count = np.count_nonzero(transpose_rotated_mask[non_sleeve_side])
			if temp_count < temp_width_pre:												# Compare pixel counts
				temp_count2 = np.count_nonzero(transpose_rotated_mask[non_sleeve_side+step])
				if temp_count2 < temp_count:											# Compare next line also to verify
					body_sweap_x = non_sleeve_side-step
					break
			else:
				temp_width_pre = temp_count 											# Update previous pixel count
		else:
			non_sleeve_side -= step 													# Checking starting side
			if non_sleeve_side < first:
				break
			temp_count = np.count_nonzero(transpose_rotated_mask[non_sleeve_side])
			if temp_count < temp_width_pre: 											# Compare pixel counts
				temp_count2 = np.count_nonzero(transpose_rotated_mask[non_sleeve_side-step])
				if temp_count2 < temp_count:											# Compare next line also to verify
					body_sweap_x = non_sleeve_side+step
					break
			else:
				temp_width_pre = temp_count 											# Update previous pixel count
	if body_sweap_x > 0:
		white = False
		first = 0
		last = 0
		for i in range(0,len(transpose_rotated_mask[body_sweap_x])):					# Calculate pixel body sweap by checking pixel value
			if white == False and transpose_rotated_mask[body_sweap_x][i] != 0:
				first = i 				# First white pixel
				white = True
			elif white == True and transpose_rotated_mask[body_sweap_x][i] == 0:
				last = i-1 				# Last white pixel
				white = False
		pixel_body_sweap = last - first
		# print("pixelBodySweap = %d" %pixel_body_sweap)
		cv2.line(rotated_frame, (body_sweap_x,first), (body_sweap_x,last), (255,0,0), 3)	# Draw body sweap calculating line on image
		font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
		cv2.putText(rotated_frame, '%.1f cm' %(getmmDistance(pixel_body_sweap)/10), (body_sweap_x-50,first-10), font, 1, (255,0,0), 2, cv2.LINE_AA)		# Display body sweap value on image


	# *************************************************************
	# *************************Body Width**************************
	# *************************************************************
	body_width_x = 0
	temp_width_pre = np.count_nonzero(transpose_rotated_mask[mid_width_array_x])		# To compare with
	sleeve_check = mid_width_array_x 													# Sleeve checking pixel line
	step = 5 																			# Sleeve checking step size
	body_width_x_dif = int(getPixelDistance(25)/step)									# Pixel distance from sleeve joint to body width
	# body_width_x_dif = int(33/step)													# Pixel distance from sleeve joint to body width
	body_width_first = [] 																# To store white area starting points
	body_width_last = [] 																# To store white area ending points
	count_for_dif = 0
	dif = 5																				# Target pixel difference at sleeve starting
	continuous_white_counts = []														# Number of white pixels in each white region
	max_index = 0																		# Index of region which have max no. of white pixels
	first = []																			# Starting points of each white ragion
	last = []																			# Ending points of each white region
	while True:
		count_for_dif += 1																# No. of cycles in the loop
		if rotated == False:
			sleeve_check -= step														# Pixel value checking frequency
			if sleeve_check <= sleeve_side:
				break
			white = False
			continuous_white = 0
			continuous_white_counts = []
			for i in range(0,len(transpose_rotated_mask[sleeve_check])):				# Calculate continuous white by checking pixel value
				if white == False and transpose_rotated_mask[sleeve_check][i] != 0:		# Black to white
					first.append(i)
					continuous_white = 1
					white = True
				elif white == True and transpose_rotated_mask[sleeve_check][i] != 0:	# White to white
					continuous_white += 1
					white = True
				elif white == True and transpose_rotated_mask[sleeve_check][i] == 0:	# White to white
					continuous_white_counts.append(continuous_white)
					last.append(i)
					white = False
			if len(continuous_white_counts) > 0:										# If white areas found
				max_index = np.argmax(continuous_white_counts)
				if count_for_dif - body_width_x_dif > 0:
					body_width_first.append(first[max_index])							# Storing first & last values of several pixel lines before
					body_width_last.append(last[max_index])
				temp_count = continuous_white_counts[max_index]
				if temp_count > temp_width_pre+dif:										# Sleeve detected
					body_width_x = sleeve_check+step
					break
				else:
					temp_width_pre = temp_count
		else:																			# Same as previous, but changing the scaning direction
			sleeve_check += step
			if sleeve_check >= sleeve_side:
				break
			white = False
			continuous_white = 0
			continuous_white_counts = []
			for i in range(0,len(transpose_rotated_mask[sleeve_check])):				# Calculate continuous white by checking pixel value
				if white == False and transpose_rotated_mask[sleeve_check][i] != 0:
					first.append(i)
					continuous_white = 1
					white = True
				elif white == True and transpose_rotated_mask[sleeve_check][i] != 0:
					continuous_white += 1
					white = True
				elif white == True and transpose_rotated_mask[sleeve_check][i] == 0:
					continuous_white_counts.append(continuous_white)
					last.append(i)
					white = False
			if len(continuous_white_counts) > 0:
				max_index = np.argmax(continuous_white_counts)
				if count_for_dif - body_width_x_dif > 0:
					body_width_first.append(first[max_index])
					body_width_last.append(last[max_index])
				temp_count = continuous_white_counts[max_index]
				if temp_count > temp_width_pre+dif:
					body_width_x = sleeve_check-step
					break
				else:
					temp_width_pre = temp_count
	if len(continuous_white_counts) > 0:
		pixel_body_width = continuous_white_counts[max_index]							# Body width in pixels
		# pixel_body_width2 = last[max_index] - first[max_index]							# Body width in pixels

		# print("pixelBodyWidth = %d" %pixel_body_width)
		# cv2.line(rotated_frame, (body_width_x,first[max_index]), (body_width_x,last[max_index]), (255,0,0), 3)			# Draw body width calculating line on image
		# font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
		# cv2.putText(rotated_frame, '%.1f pixel' %pixel_body_width, (body_width_x-100,first[max_index]-10), font, 1, (255,0,0), 2, cv2.LINE_AA)			# Display body width value on image

		if len(body_width_first)>0 and len(body_width_last)>0:
			pixel_body_width_actual = body_width_last[len(body_width_last)-1] - body_width_first[len(body_width_first)-1]
			# print("pixelBodyWidthActual = %d" %pixel_body_width_actual)
			if rotated == False:
				cv2.line(rotated_frame, ((body_width_x + body_width_x_dif),body_width_first[len(body_width_first)-1]), ((body_width_x + body_width_x_dif),body_width_last[len(body_width_last)-1]), (255,0,0), 3)	# Draw body width calculating line on image
			else:
				cv2.line(rotated_frame, ((body_width_x - body_width_x_dif),body_width_first[len(body_width_first)-1]), ((body_width_x - body_width_x_dif),body_width_last[len(body_width_last)-1]), (255,0,0), 3)	# Draw body width calculating line on image
			font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
			cv2.putText(rotated_frame, '%.1f cm' %(getmmDistance(pixel_body_width_actual)/10), (body_width_x-50,body_width_first[len(body_width_first)-1]-10), font, 1, (255,0,0), 2, cv2.LINE_AA)			# Display body width value on image


	rotation_matrix = cv2.getRotationMatrix2D(ellipse[0], (360-(ellipse[2]-90)), 1)			# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
	rotated_frame = cv2.warpAffine(rotated_frame, rotation_matrix, (frame.shape[1],frame.shape[0]))				# Rotate actual image
	rotated_dummy = cv2.warpAffine(rotated_dummy, rotation_matrix, (frame.shape[1],frame.shape[0]))				# Rotate actual image
	rotated_frame = cv2.add(rotated_frame, cv2.subtract(frame, rotated_dummy))									# Fill missing parts of final output
	# cv2.addWeighted(frame,0.5,rotated_frame,0.5,0,rotated_frame)												# Adding missing parts
	return addTextOnFrame(rotated_frame)


def getMeasurements():
	cap = cv2.VideoCapture(1)
	# cap.set(cv2.CAP_PROP_SETTINGS, 1)
	original = cv2.imread("E:\MachineLearning\Images\TShirt\img2890.jpg")

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		if ret:
			# print("New frame")
			output = tshirtMeasuring(frame)						# Process live video
			# output = tshirtMeasuring(original.copy())			# Process a saved image instead of live video
			cv2.imshow("Smart Table", output)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

getMeasurements()

import numpy as np
import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("test\WIN_20180403_081531.MP4")
original = cv2.imread("test\WIN_20180126_152758.JPG")

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frame = original.copy()
	if ret:
		# cv2.imshow("Original", frame)
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		gray = np.float32(gray)
		median = cv2.medianBlur(gray, 3)											# Median filtering(second parameter can only be an odd number)
		thresh = 220
		binary = cv2.threshold(median, thresh, 255, cv2.THRESH_BINARY_INV)[1]		# Convert image into black & white
		binary = cv2.erode(binary, None, iterations=2)								# Erosion - make smaller white area
		binary = cv2.dilate(binary, None, iterations=2)								# Dilation - make bigger white area
		# dst = cv2.cornerHarris(gray,2,3,0.04)
		dst = cv2.cornerHarris(binary,2,3,0.1)

		binary = cv2.resize(binary, (640,480))
		cv2.imshow("Original", binary)

		#result is dilated for marking the corners, not important
		dst = cv2.dilate(dst,None)

		# Threshold for an optimal value, it may vary depending on the image.
		frame[dst>0.01*dst.max()]=[0,0,255]
		# frame = cv2.resize(frame, (int(width*2.1),int(height*2.1)))
		frame = cv2.resize(frame, (640,480))
		cv2.imshow("Processed", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

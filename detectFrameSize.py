import numpy as np
import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("test\WIN_20180403_081531.MP4")

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	if ret:
		(height, width) = frame.shape[:2]
		print("height ", height, "width ", width)
		# cv2.imshow("Original", frame)
		frame = cv2.resize(frame, (int(width*0.5*2.2),int(height*0.5*2.2)))
		# rotation_matrix1 = cv2.getRotationMatrix2D((width/2, height/2), 270, 1)		# Rotation matrix ((centerOfRotation), Anti-ClockwiseRotationAngle, Scale)
		# rotation_matrix1[0,2] += int((height/2)-width/2)
		# rotation_matrix1[1,2] += int((width/2)-height/2)
		# frame = cv2.warpAffine(frame, rotation_matrix1, (height,width))				# Rotate filtered image (Image, RotationMatrix, NewImageDimensions)
		cv2.imshow("Resized", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# USAGE
	# python MultipleChoiceGrader.py --image images/test_01.png

# Import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# Construct the argument parse and parse the argument for the image
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,	help="path to the input image")
args = vars(ap.parse_args())

# Define the answer key which maps the question number to the correct answer
# Dictionary keys are question numbers. Values are integers 0-4, where 0 is answer A and 4 is answer E.

# Physics GRE Sample Exam 1 (2001):
#ANSWER_KEY1 = {0: 2, 1: 3, 2: 3, 3: 2, 4: 3, 5: 4, 6: 1, 7: 3, 8: 0, 9: 0, 10: 0, 11: 4, 12: 1, 13: 2, 14: 0, 15: 3, 16: 1, 17: 0, 18: 1, 19: 4, 20: 1, 21: 0, 22: 2, 23: 2, 24: 4}
#ANSWER_KEY2 = {0: 2, 1: 0, 2: 4, 3: 2, 4: 0, 5: 0, 6: 3, 7: 3, 8: 2, 9: 4, 10: 4, 11: 3, 12: 3, 13: 3, 14: 3, 15: 4, 16: 2, 17: 3, 18: 3, 19: 1, 20: 4, 21: 1, 22: 2, 23: 4, 24: 1}
#ANSWER_KEY3 = {0: 1, 1: 2, 2: 1, 3: 2, 4: 4, 5: 3, 6: 0, 7: 1, 8: 1, 9: 3, 10: 2, 11: 0, 12: 3, 13: 0, 14: 3, 15: 3, 16: 4, 17: 4, 18: 1, 19: 1, 20: 3, 21: 4, 22: 3, 23: 3, 24: 4}
#ANSWER_KEY4 = {0: 2, 1: 4, 2: 4, 3: 3, 4: 3, 5: 1, 6: 3, 7: 2, 8: 3, 9: 0, 10: 4, 11: 0, 12: 2, 13: 4, 14: 0, 15: 1, 16: 4, 17: 2, 18: 4, 19: 0, 20: 4, 21: 4, 22: 0, 23: 3, 24: 1}

# Physics GRE Sample Exam 2 (2008):
ANSWER_KEY1 = {0: 1, 1: 3, 2: 4, 3: 4, 4: 0, 5: 4, 6: 2, 7: 3, 8: 4, 9: 1, 10: 2, 11: 2, 12: 0, 13: 1, 14: 4, 15: 3, 16: 0, 17: 4, 18: 0, 19: 0, 20: 2, 21: 2, 22: 1, 23: 1, 24: 4}
ANSWER_KEY2 = {0: 3, 1: 2, 2: 3, 3: 2, 4: 3, 5: 2, 6: 0, 7: 4, 8: 2, 9: 1, 10: 0, 11: 4, 12: 4, 13: 2, 14: 1, 15: 1, 16: 4, 17: 3, 18: 3, 19: 2, 20: 3, 21: 3, 22: 2, 23: 3, 24: 2}
ANSWER_KEY3 = {0: 3, 1: 2, 2: 3, 3: 4, 4: 0, 5: 3, 6: 1, 7: 0, 8: 2, 9: 2, 10: 4, 11: 4, 12: 3, 13: 3, 14: 2, 15: 3, 16: 3, 17: 3, 18: 3, 19: 0, 20: 1, 21: 3, 22: 3, 23: 4, 24: 1}
ANSWER_KEY4 = {0: 1, 1: 2, 2: 1, 3: 3, 4: 2, 5: 1, 6: 3, 7: 4, 8: 4, 9: 1, 10: 1, 11: 3, 12: 3, 13: 3, 14: 3, 15: 2, 16: 4, 17: 1, 18: 2, 19: 3, 20: 3, 21: 4, 22: 3, 23: 4, 24: 4}

answerKey = []
answerKey.append(ANSWER_KEY1)
answerKey.append(ANSWER_KEY2)
answerKey.append(ANSWER_KEY3)
answerKey.append(ANSWER_KEY4)

# Number of columns on the bubble sheet
numColumns = 4

# Load the image, convert it to grayscale, blur it slightly, then find edges
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

# There are several lines that write intermediate images to disk. These have been commented out, but may be useful for debugging.

# cv2.imwrite("gray.png", gray)
# cv2.imwrite("blurred.png", blurred)
# cv2.imwrite("edged.png", edged)

# Find contours in the edge map, then initialize the contour that corresponds to the document
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

# Ensure that at least one contour was found
if len(cnts) > 0:
	# Sort the contours according to their size in descending order
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	# Loop over the sorted contours
	for c in cnts:
		# Approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		cv2.drawContours(image, c, -1, (0, 255, 0), 2)
		# If the approximated contour has four points, then we assume we have found the paper
		if len(approx) == 4:
			docCnt = approx
			break

cv2.drawContours(image, [docCnt], -1 ,(0, 255, 0), 2)
# cv2.imwrite("testing.png", image)

# apply a four point perspective transform to both the original image and grayscale image to obtain a top-down birds eye view of the paper
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))
# cv2.imwrite("warped.png", warped)
height, width = warped.shape

warpedImages=[]
paperImages=[]
for i in range(0,numColumns):
	warpedImages.append(warped[0:height, i*width/numColumns:(i+1)*width/numColumns])
	paperImages.append(paper[0:height, i*width/numColumns:(i+1)*width/numColumns])

#for i in range(0,numColumns):
#	cv2.imwrite("warped"+str(i)+".png", warpedImages[i])
#	cv2.imwrite("paper"+str(i)+".png", paperImages[i])

class TestColumn:
	def __init__(self, warpedImage, paperImage, answerKey):
		self.warped = warpedImage
		self.paper = paperImage
		self.answerKey = answerKey
		self.correct = 0
		self.thresh = cv2.threshold(self.warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	def gradeColumn(self):
		self.correct = 0
		cnts = 	cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		questionCnts = []

		for c in cnts:
			# compute the bounding box of the contour, then use the
			# bounding box to derive the aspect ratio
			(x, y, w, h) = cv2.boundingRect(c)
			ar = w / float(h)

			# in order to label the contour as a question, region
			# should be sufficiently wide, sufficiently tall, and
			# have an aspect ratio approximately equal to 1
			if w >= 20 and h >= 20 and ar >= 0.75 and ar <= 1.25:
				questionCnts.append(c)

		questionCnts = contours.sort_contours(questionCnts, method = "top-to-bottom")[0]
		for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
			# sort the contours for the current question from
			# left to right, then initialize the index of the
			# bubbled answer
			cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
			bubbled = None

			# loop over the sorted contours
			for (j, c) in enumerate(cnts):
				# construct a mask that reveals only the current
				# "bubble" for the question
				mask = np.zeros(self.thresh.shape, dtype="uint8")
				cv2.drawContours(mask, [c], -1, 255, -1)

				# apply the mask to the thresholded image, then
				# count the number of non-zero pixels in the bubble area
				mask = cv2.bitwise_and(self.thresh, self.thresh, mask=mask)
				total = cv2.countNonZero(mask)

				# if the current total has a larger number of total non-zero
				# pixels, then we are examining the currently bubbled-in answer
				if bubbled is None or total > bubbled[0]:
					bubbled = (total, j)

			# initialize the contour color and the index of the *correct* answer
			color = (0, 0, 255)
			k = self.answerKey[q]

			# Check to see if the bubbled answer is correct.
			if k == bubbled[1]:
				color = (0, 255, 0)
				self.correct += 1

			# Draw the outline of the correct answer on the test
			cv2.drawContours(self.paper, [cnts[k]], -1, color, 3)

columnList = []
for i in range(0,numColumns):
	columnList.append(TestColumn(warpedImages[i],paperImages[i],answerKey[i]))

finalColumnPapers=[]
totalCorrect = 0
# Call the grading method for each column:
for i in range(0,numColumns):
	columnList[i].gradeColumn()
	finalColumnPapers.append(columnList[i].paper)
	totalCorrect+= columnList[i].correct

final = cv2.hconcat(finalColumnPapers) # Assemble the graded columns into one image

# Inform the user of their total score by printing it to the command line and labelling the upper left corner of the graded bubble sheet.
print("[INFO] score: {:.2f}%".format(totalCorrect))
cv2.putText(final, "{:.2f}%".format(totalCorrect), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

# Assume the original reduced test sheet has an aspect ratio such that image height is the primary size limitation on a 16:9 screen
finalheight = 1000
scaleproportion = float(1000)/float(final.shape[0])
finalwidth = int(final.shape[1]*float(scaleproportion))
finaldisplay = cv2.resize(final, (finalwidth,finalheight))

# Show the graded bubble sheet and write it to disk as the original file name (minus the extension) followed by " GRADED.png"
cv2.imshow("Graded", finaldisplay)

# Writing to disk:
# cv2.imwrite("final.png",final)
fileNameList = list(args["image"].lower())
for i in range(len(fileNameList)-1,0,-1):
	if fileNameList[i]==".":
		del fileNameList[i]		
		break
	else:
		del fileNameList[i]
cv2.imwrite("".join(fileNameList)+" GRADED.png",final)

#cv2.imshow("Original", image)
#cv2.imshow("Exam", paper)

cv2.waitKey(0)
cv2.destroyAllWindows()

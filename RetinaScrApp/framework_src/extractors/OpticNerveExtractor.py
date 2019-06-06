import cv2
import numpy as np
import os
import matplotlib.pyplot as plt 

class OpticNerveExtractor:
	# class constructor
	def __init__(self, in_image):
		self.image = in_image.fundus

	def morph_extractor(self):
		# extract green channel
		img = self.image[:,:,1]

		# erode to remove defects in lighting around fundus boundary
		kernel = cv2.getStructuringElement(
			cv2.MORPH_ELLIPSE, (15, 15))
		img_input = cv2.erode(img ,kernel ,iterations = 1)

		# remove lighting variations in background

		# open and close to remove small bright regions
		r1 = cv2.morphologyEx(
			img_input, cv2.MORPH_OPEN, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(2,2)), iterations = 1)
		R1 = cv2.morphologyEx(
			r1, cv2.MORPH_CLOSE, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(2,2)), iterations = 1)

		r2 = cv2.morphologyEx(
			R1, cv2.MORPH_OPEN, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(4,4)), iterations = 1)
		R2 = cv2.morphologyEx(
			r2, cv2.MORPH_CLOSE, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(4,4)), iterations = 1)

		r3 = cv2.morphologyEx(
			R2, cv2.MORPH_OPEN, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(6,6)), iterations = 1)
		R3 = cv2.morphologyEx(
			r3, cv2.MORPH_CLOSE, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(6,6)), iterations = 1)

		r4 = cv2.morphologyEx(
			R3, cv2.MORPH_OPEN, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(8,8)), iterations = 1)
		img_morph = cv2.morphologyEx(
			r4, cv2.MORPH_CLOSE, cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE,(8,8)), iterations = 1)

		plt.hist(img_morph.ravel(), 256, [0,255])
		#plt.show()
		#print(type(img_morph))
		#print(img_morph.shape)
		#print(img_morph[450,600])

		# isolate areas with the highest intensity values
		# these are optic nerve candidates
		img_candid = img_morph
		for x in range(img_candid.shape[0]):
			for y in range(img_candid.shape[1]):
				if img_candid[x][y]<150:
					img_candid[x][y] = 0
		#img_candid = [0 if not x>=250 else x for x in img_candid]
		#img_candid = (x for x in img_morph if x<20 else 0)
		#print(img_candid)

		# locate centroid of the optic nerve using image moments

		# convert the grayscale image to binary image
		ret, thresh = cv2.threshold(img_candid,150,255,0)
		 
		# calculate moments of binary image
		M = cv2.moments(thresh)
		 
		# calculate x,y coordinate of center
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		
		img_output = img # original
		# put text and highlight the center
		cv2.circle(img_output, (cX, cY), 5, (0, 0, 0), -1)
		cv2.putText(img_output, "Optic Nerve Centroid", (cX - 25, cY - 25),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		
		#img_output = img_candid
		#cv2.imshow('input', self.image)
		return img_output

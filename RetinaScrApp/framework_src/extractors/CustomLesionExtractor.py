import numpy as np
import csv
import cv2

class CustomLesionExtractor:
    jpegImg = 0
    grayImg = 0
    curImg = 0

    def __init__(self):
        pass
    
    # BEGINNING OF EXTRACT FUNCTION
    def extract(self, fundus):
        self.jpegImg = fundus
        self.curImg = np.array(fundus)
        self.greenComp()
        self.applyCLAHE()
        self.applyDilation()
        self.applyThreshold()
        self.applyMedianFilter()
        
        # invert dark and bright values
        temp = self.curImg
        for i in range(temp.shape[0]):
            for j in range(temp.shape[1]):
                if self.curImg[i][j] == 0:
                    temp[i][j] = 255
                else:
                    temp[i][j] = 0
        return temp
    # END OF EXTRACT FUNCTION
        
    def greenComp(self):
    ###Extracting Green Component
        gcImg = self.curImg[:,:,1]
        self.curImg = gcImg

    def applyCLAHE(self):
    #Applying Contrast Limited Adaptive Histogram Equalization (CLAHE)
        clahe = cv2.createCLAHE()
        clImg = clahe.apply(self.curImg)
        self.curImg = clImg

    def applyDilation(self):
        #Creating Structurig Element
        strEl = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        #Dilation
        dilateImg = cv2.dilate(self.curImg, strEl)
        self.curImg = dilateImg

    def applyThreshold(self):
        #Thresholding with Complement/Inverse
        retValue, threshImg = cv2.threshold(self.curImg, 250, 250, cv2.THRESH_BINARY)
        self.curImg = threshImg

    def applyMedianFilter(self):
        #Median Filtering
        medianImg = cv2.medianBlur(self.curImg,5)
        self.curImg = medianImg

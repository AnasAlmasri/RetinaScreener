import numpy as np
import csv
import cv2

class ExudateExtractor:
    jpegImg = 0
    grayImg = 0
    curImg = 0

    def __init__(self, image):
        self.jpegImg = image.fundus
        self.curImg = np.array(image.fundus)
        
    def clahe_extractor(self):
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


class LesionExtractor:
    def __init__(self, image):
        self.original = image
        self.image = image.fundus
        t_height, t_width, t_channels = self.image.shape
        print("ORIGINAL: height: ", t_height, ", width: ", t_width, ", channels: ", t_channels)
 
    def morph_extractor(self):
        #extract green channel
        green_channel = self.image[:,:,1]
        #green_channel = green_channel * 2.5

        grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        grayscale_image = cv2.GaussianBlur(grayscale_image, (5,5), 0)

        # canny edge detection
        edges = cv2.Canny(grayscale_image, 70, 35)

        edge_test = grayscale_image + edges
        final = edges

        # close to find individual objects
        final = cv2.dilate(final, np.ones((3,3), np.uint8), iterations=2)
        final = cv2.erode(final, np.ones((3,3), np.uint8), iterations=1)

        final = cv2.dilate(final, np.ones((3,3), np.uint8), iterations=4)
        final = cv2.erode(final, np.ones((3,3), np.uint8), iterations=3)

        # detect large blobs
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 500 #define minimum area
        detector = cv2.SimpleBlobDetector_create(params)
        large_blobs = detector.detect(final)
        #cv2.imshow('test', final)
        # create a blank image to mask
        masked_image = np.zeros((grayscale_image.shape[0], grayscale_image.shape[1]))
        
        #draw the blob on the mask
        for blob in large_blobs:
            cv2.circle(
                masked_image, 
                (int(blob.pt[0]), int(blob.pt[1])),
                int(blob.size),
                (255, 255, 255)
                )

        final = final - masked_image
        #final = cv2.erode(final, np.ones((2,2), np.uint8), iterations=1)
        #final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)

        cv2.imshow('gray', final)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        lesions = None
        return lesions


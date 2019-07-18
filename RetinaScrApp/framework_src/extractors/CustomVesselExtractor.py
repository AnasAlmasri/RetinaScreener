import cv2
import numpy as np
import os
import csv

class CustomVesselExtractor:
    # class constructor
    def __init__(self):
        pass

    # BEGINNING OF EXTRACT FUNCTION
    def extract(self, fundus):
        vessels = None # initial value
        """
        function to perform vessel extraction/segmentation of vessels
        Inputs:  self - default object
                 fundus - image to segment [NumPy ndarray with 3 layers, BGR]
        Outputs: vessels - vessel features [Numpy ndarray with 1 layer, BW]

        Notes:
            - Output image should represent vessels in black and the rest in white
            - Make sure not to tamper with or modify 'self'
            - Try not to change the function definition and the return statement
            - You can find a full list of available libraries and their versions
            - Remember that you can define nested functions in python
        """

        # your code goes here


        return vessels
	# END OF EXTRACT FUNCTION
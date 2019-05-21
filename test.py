from imutils.paths import list_images

from detector import ObjectDetector
import numpy as np
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-d","--detector",required=True,help="path to trained detector to load...")
ap.add_argument("-i","--image",required=True,help="path to an image for object detection...")
ap.add_argument("-a","--annotate",default=None,help="text to annotate...")
args = vars(ap.parse_args())
detector = ObjectDetector(loadPath=args["detector"])
# imagePath = args["image"]
#imagePath = "./1.jpg"
#image = cv2.imread(imagePath)
for imagePath in list_images("./TestR"):
    #load image and create a BoxSelector instance
    image = cv2.imread(imagePath)
    #bs = BoxSelector(image,"Image")
    #cv2.imshow("Image",image)
    #cv2.waitKey(0)
    #order the points suitable for the Object detector
    #pt1,pt2 = bs.roiPts
    #(x,y,xb,yb) = [pt1[0],pt1[1],pt2[0],pt2[1]]
    #annotations.append([int(x), int(y), int(xb), int(yb)])
    #print(x,y,xb,yb)
    image = cv2.imread(imagePath)
    x=detector.detect(image,annotate=args["annotate"])
    print (x)

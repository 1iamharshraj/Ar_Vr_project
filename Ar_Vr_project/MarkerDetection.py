import cv2
import cv2 as cv
from cv2 import aruco
import numpy as np
import os

def findArucoMarker(img,markerSize=6,totalMarker=250,draw=True):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    key     = getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    arucoDict = aruco.getPredefinedDictionary(key)
    arucoParam= aruco.DetectorParameters()
    detector = aruco.ArucoDetector(arucoDict,arucoParam)
    corner,ids,rejectd = detector.detectMarkers(imgGray)

    #print(ids)
    if draw:
        aruco.drawDetectedMarkers(img,corner)

    return[corner,ids]

def augmentAruco(corner , id , img , imgAug , drawId=True):

    tl = corner[0][0][0], corner[0][0][1]
    tr = corner[0][1][0], corner[0][1][1]
    br = corner[0][2][0], corner[0][2][1]
    bl = corner[0][3][0], corner[0][3][1]

    h,w,c = imgAug.shape

    pts1 = np.array([tl,tr,br,bl])
    pts2 = np.float32([[0,0],[w,0],[w,h],[0,h]])
    matrix,_=cv.findHomography(pts2,pts1)
    imgOut = cv2.warpPerspective(imgAug,matrix,(img.shape[1],img.shape[0]))
    cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))
    imgOut = img+imgOut
    return imgOut


def main():
    imgAug = cv.imread(r"C:\Users\eyeha\PycharmProjects\Ar_Vr_project\Ar_Vr_project\img.png")
    cap = cv.VideoCapture(0)
    while True:
        sccuess , img = cap.read()
        if img is not None:
            arucoFound = findArucoMarker(img)
            if len(arucoFound[0])!=0:
                for corner,id in zip(arucoFound[0],arucoFound[1]):
                   img = augmentAruco(corner,id,img,imgAug)
            cv.imshow("image",img)
        else:
            break
        cv.waitKey(1)

if __name__ == "__main__":
    main()
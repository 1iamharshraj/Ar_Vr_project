import cv2
import numpy as np
from  object_loader import *
import math
import pickle
def main(filepath):
    markerpoints=np.array([[0,0],[300,0],[300,300],[0,300]],dtype=np.float32)
    dictonary=cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    pklfile1 = open(r'cameraMatrix.pkl', 'rb')
    pklfile2 = open(r'dist.pkl', 'rb')
    cam_matrix= pickle.load(pklfile1)
    distCoeffs= pickle.load(pklfile2)

    pklfile1.close()
    pklfile2.close()
    cam_matrix1 = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])


    obj = OBJ(filepath, swapyz=True)

    detector = cv2.aruco.ArucoDetector(dictonary)

    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        if not ret:
            print('frame not captured')
            return
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        corners,marker_ids,rej_corners=detector.detectMarkers(gray)
        if str(marker_ids) != "None":
            cv2.aruco.drawDetectedMarkers(image=frame, corners=corners, ids=marker_ids, borderColor=(0, 255, 0))
            for cor in corners:
                p1 = [cor[0][0][0], cor[0][0][1]]
                cv2.circle(frame, (int(p1[0]), int(p1[1])), 4, (255, 0, 0), 2)
                p2 = [cor[0][1][0], cor[0][1][1]]
                cv2.circle(frame, (int(p2[0]), int(p2[1])), 4, (0, 255, 0), 2)
                p3 = [cor[0][2][0], cor[0][2][1]]
                cv2.circle(frame, (int(p3[0]), int(p3[1])), 4, (0, 0, 255), 2)
                p4 = [cor[0][3][0], cor[0][3][1]]
                cv2.circle(frame, (int(p4[0]), int(p4[1])), 4, (0, 255, 255), 2)

            markerpoints_frame = np.array([p1, p2, p3, p4], dtype=np.float32)
            homography,mask=cv2.findHomography(markerpoints,markerpoints_frame,cv2.RANSAC)
            if homography is not None:

                try:
                    projection = projection_matrix(cam_matrix,homography)
                    print(projection)
                    frame=render(frame,obj,projection,True)

                except:
                    pass

        cv2.imshow('frame',frame)
        if cv2.waitKey(1)==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return 0


def render(img,obj,projection,colorr):
    vertices=obj.vertices
    scale_matrix=np.eye(3)*0.5
    h,w=300,300

    for face in obj.faces:
        face_vertices=face[0]
        points=np.array([vertices[vertex-1] for vertex in face_vertices])
        points=np.dot(points,scale_matrix)
        points=np.array([[p[0] + 150,p[1] +150,p[2]] for p in points])
        dst=cv2.perspectiveTransform(points.reshape(-1,1,3),projection)
        imgpts=np.int32(dst)
        if colorr is False:
            cv2.fillConvexPoly(img,imgpts,(200,27,11))
        else:
            color=''.join(str(tem) for tem in face[-1])
            color=hex_to_rgb(color)
            color=color[::-1]
            cv2.fillConvexPoly(img,imgpts,color)
    return img

def projection_matrix(cam_paramaters,homography):
    homography=homography*(-1)

    rot_and_trans=np.dot(np.linalg.inv(cam_paramaters),homography)
    col_1=rot_and_trans[:,0]
    col_2=rot_and_trans[:,1]
    col_3=rot_and_trans[:,2]
    ii=math.sqrt(np.linalg.norm(col_1,2)*np.linalg.norm(col_2,2))
    rot_1=col_1/ii
    rot_2=col_2/ii
    translation=col_3/ii
    c=rot_1+rot_2
    p=np.cross(rot_1,rot_2)
    d=np.cross(c,p)
    rot_1=np.dot(c / np.linalg.norm(c,2) + d/np.linalg.norm(d,2),1/math.sqrt(2))
    rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_3=np.cross(rot_1,rot_2)
    projection=np.stack((rot_1,rot_2,rot_3,translation)).T
    return np.dot(cam_paramaters,projection)

def hex_to_rgb(hex_color):
    hex_color=hex_color.lstrip('#')
    h_len=len(hex_color)
    return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))


"""
while(True):
    print("1. Record")
    print("2. Exit")
    n = int(input())
    if(n==1):
        animal = record_3d()
        if animal != None:
            dir = animalTo3d(animal)
            main(dir)
        else:
            print("the given voice of animal name isnt available at current moment")
    if(n==2):
        break
"""

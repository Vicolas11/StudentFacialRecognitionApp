import cv2, os
import logging as log
import datetime as dt
from time import sleep

def video_capture(department, level, matric_no):    
    if(os.path.exists('face_recognition_data/training_dataset/{}/{}/{}'.format(department, level, matric_no)) == False):
        os.makedirs('face_recognition_data/training_dataset/{}/{}/{}'.format(department, level, matric_no))
    
    directory = 'face_recognition_data/training_dataset/{}/{}/{}'.format(department, level, matric_no)
    cascPath = "face_recognition_data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    log.basicConfig(filename='webcam.log',level=log.INFO)
    video_capture = cv2.VideoCapture(0)
    anterior = 0

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        # Display the resulting frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            check, frame = video_capture.read()
            cv2.imshow("Capturing", frame)
            cv2.imwrite(filename=f'{directory}/{matric_no}.jpg', img=frame)
            video_capture.release()
            cv2.destroyAllWindows()
            break
        # cv2.imshow('Image Capture', frame)
    video_capture.release()
    cv2.destroyAllWindows()
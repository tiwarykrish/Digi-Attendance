import os
import cv2
import face_recognition
import numpy as np
import datetime


import mysql.connector as connector

class DBhelper:
    def __init__(self):
        self.con = connector.connect(host='localhost', port='3306', user='root', password='ashu', database='attendence')
        query = 'create table if not exists user(username varchar(50),login_time datetime)'
        cur=self.con.cursor()
        cur.execute(query)
        print("created")
    def insert_user(self,username, login_time):
        query="insert into user(username, login_time) values('{}','{}')".format(username,login_time) 
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("data is inserted!!!!")




path = "Resources/images"
images = []
images_names = []
count = 0
imagespath = os.listdir(path)
print(imagespath)
for img in imagespath:
    current_img = cv2.imread(f'{path}/{img}')
    images.append(current_img)
    images_names.append(os.path.splitext(img)[0])
print(images_names)

def Get_Attendance(Names):
    count = 0
    with open('Excel3.csv','r+') as E:
        Data = E.readlines()
        names = []
        for line in Data:
            entry = line.split(',')
            names.append(entry[0])
            if count == 0:
                now = datetime.datetime.now()
                datestr = now.strftime('%H:%M')
                E.writelines(f'\n{Names},{datestr}')
                count += 1

def findEncodings(images):
    encodelist = []
    for IMAGES in images:
        IMAGES = cv2.cvtColor(IMAGES,cv2.COLOR_BGR2RGB)
        faceEnc = face_recognition.face_encodings(IMAGES)[0]
        encodelist.append(faceEnc)
    return encodelist

Encodelistknown = findEncodings(images)

print("encodings complete")

cap = cv2.VideoCapture(0)
NAMES = []

while True:
    success, img = cap.read()
    imgs = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    facecurrentframe = face_recognition.face_locations(imgs)
    facecurrentenc = face_recognition.face_encodings(imgs,facecurrentframe)
    for faceloc,faceENC in zip(facecurrentframe,facecurrentenc):
        match = face_recognition.compare_faces(Encodelistknown,faceENC)
        dis = face_recognition.face_distance(Encodelistknown,faceENC)
        print(match)
    #cv2.rectangle(img,(facecurrentframe[3],facecurrentframe[0]),(facecurrentframe[1],facecurrentframe[2]),(0,0,255),3)
        match_index = np.argmin(dis)
        if match[match_index]:
            name = images_names[match_index].upper()
            y1,x2,x1,y2 = faceloc
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),1)
            cv2.putText(img,name,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),2)
            print(name)
            while(name not in NAMES):
                NAMES.append(name)
                Get_Attendance(name)
                helper= DBhelper()
                helper.insert_user(name,"03-18-2023 08:30:30")


    cv2.imshow("out", img)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break




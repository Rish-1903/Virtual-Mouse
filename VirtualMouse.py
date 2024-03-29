import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
wCam,hCam=640,480
frameR=100
smoothening=5
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0
plocX,plocY=0,0
clixX,clocY=0,0
detector=htm.handDetector(maxHands=1,detectionCon=0.85)
wScr,hScr=pyautogui.size()
while True:
    succes,img=cap.read()
    img=cv2.flip(img,1)
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        fingers=detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            pyautogui.moveTo(clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY
        if fingers[1]==1 and fingers[2]==1:
            length,img,lineInfo=detector.findDistance(8,12,img)
            if length<40:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(255,0,0),cv2.FILLED)
                pyautogui.click()
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)
    

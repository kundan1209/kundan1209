#you need to have handtrackingmodule and this in same python folder for this to work.
#for cv2 use 'pip install cv-python' in terminal

import cv2
import time
import mediapipe as mp
import os

import numpy as np
import pyautogui as pt
import HandTrackingModule as htm

detector = htm.handDetector(maxHands=1)
cap = cv2.VideoCapture(0)
pLocX, pLocY = 0, 0
cLocX, CLocY = 0, 0
wCam, hCam = 640, 480
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
wScr, hScr = pt.size()
frameR = 70
smoothening = 3

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1, y1, x2, y2)
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 255, 255), 2)

        #print(fingers)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            cLocX = pLocX + (x3 - pLocX) / smoothening
            cLocY = pLocY + (y3 - pLocY) / smoothening

            pt.moveTo(wScr - cLocX, cLocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            pLocX, pLocY = cLocX, cLocY

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (255, 0, 0), cv2.FILLED)
                pt.click()

    cv2.imshow("Image", img)
    cv2.waitKey(1)

#!/usr/bin/env python

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats 

import numpy
import cv2


def tuxiangshibie():
    u = 0
    v = 0
    uo = 0
    vo = 0
    pub = rospy.Publisher('rongheshuru', numpy_msg(Floats),queue_size=10)
    rospy.init_node('tuixiangshibie', anonymous=True)
    cap = cv2.VideoCapture(0)
    while (1):
        ret,img = cap.read()
        lower_blue = numpy.array([100, 43, 46])
        upper_blue = numpy.array([124, 255, 255])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        res1 = cv2.inRange(hsv, lower_blue, upper_blue)

        # lower_blue = numpy.array([0, 100, 40])
        # upper_blue = numpy.array([10, 255, 255])
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # res2 = cv2.inRange(hsv, lower_blue, upper_blue)
        # all = cv2.add(res1, res2)
        # res = cv2.bitwise_and(frame, frame, mask=mask)
        # img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        car_cascade = cv2.CascadeClassifier('/home/autolabor/catkin_ws/528che.xml')
        cars = car_cascade.detectMultiScale(res1, 1.1, 3)
        for (x, y, w, h) in cars:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                u = x + w/2
        
        # ren_cascade = cv2.CascadeClassifier('renhuibaicascade.xml')
        # peoples = ren_cascade.detectMultiScale(img_gray, 1.1, 2)
        # for (x, y, w, h) in peoples:
        #         cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #         v = x + w/2

        cv2.namedWindow('gaoda', cv2.WINDOW_NORMAL)
        cv2.imshow("gaoda1", res1)
        cv2.imshow("gaoda", img)
        cv2.waitKey(1)
        if(uo == 0 and u == 0 and vo == 0 and v == 0):
            a = numpy.array([1, u, 2, 0], dtype=numpy.float32)
            pub.publish(a)

        if(-1 > uo - u or uo - u > 1 or -1 > vo - v or vo - v > 1):
            # a = numpy.array([1, u, 2, v], dtype=numpy.float32)
            a = numpy.array([1, u, 2, 0], dtype=numpy.float32)
            pub.publish(a)
            uo = u
            vo = v
        else:
            a = numpy.array([1, uo, 2, 0], dtype=numpy.float32)
            pub.publish(a)
        # print(a)
        

if __name__ == '__main__':
    tuxiangshibie()

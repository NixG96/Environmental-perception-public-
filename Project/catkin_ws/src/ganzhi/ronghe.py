#!/usr/bin/env python

import rospy
import numpy
import math
import time
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from geometry_msgs.msg import Twist #this msg linear.x linear.y linear.z use to pub gangzhixinxi

global utan
utan = 0
global vtan
vtan = 0
global zhongduan
zhongduan = 0
global t1
t1 = 0
global t2
t2 = 0
global pipei
pipei = 0
global uo 
uo = 0
global vo
vo = 0

def callback(data):
    global zhongduan
    if(zhongduan == 0):
        global utan
        global vtan
        global t1
        global t2
        global pipei 
        global uo
        global vo
        r = 0.0019
        yuanshishuju = data.data
        t1 = yuanshishuju[0] 
        u = yuanshishuju[1]
        t2 = yuanshishuju[2]
        v = yuanshishuju[3]
        if(u == 0 and v == 0):
            zhongduan = 1
            pipei = 4
        elif(u != 0 and v == 0):
            uhudu = (u - 320) * r
            utan =  math.tan(uhudu)
            zhongduan = 1
            pipei = 1
            uo = u
        elif(u == 0 and v != 0):
            vhudu = (v - 320) * r
            vtan = math.tan(vhudu)
            zhongduan = 1
            pipei = 2
            vo = v
        elif(u != 0 and v != 0):
            uhudu = (u - 320) * r
            utan =  math.tan(uhudu)
            vhudu = (v - 320) * r
            vtan = math.tan(vhudu)
            zhongduan = 1
            pipei = 3
            uo = u
            vo = v
           
        # if(u != 0 or v != 0):
        #     uhudu = (u - 320) * r
        #     utan = math.tan(uhudu)
        #     print (utan)
        #     vhudu = (v - 320) *r
        #     vtan = math.tan(vhudu)
        #     zhongduan = 1


def callback_pointcloud(data):
    global zhongduan
    if(zhongduan == 1):
        global utan
        global vtan
        global t1
        global t2
        global pipei
        jiejintan = 5
        x = 0
        y = 0
        z = 0
        fasongx = 0
        fasongy = 0
        fasongt = 0
        ronghewucha = 0.001
        wucha = 1
        pub = rospy.Publisher('/ganzhixinxi', Twist,queue_size=10)
        assert isinstance(data, PointCloud2)
        gen = point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)
        time.sleep(0.1)
        # print type(gen)
        for p in gen:
            x = p[0]  
            y = p[1] 
            z = p[2]
            xtan = x/y

            if (utan - ronghewucha < xtan < utan + ronghewucha and -0.3<z<0.3 and y < 0):
                if(pipei == 1):
                    wucha = abs(xtan-utan)
                    if(wucha < jiejintan):
                        jiejintan = wucha
                        fasongt = 1
                        fasongx = x
                        fasongy = y
                        

                if (pipei == 2):
                    wucha = abs(xtan-vtan)
                    if(wucha < jiejintan):
                        jiejintan = wucha
                        fasongt = 2
                        fasongx = x
                        fasongy = y
                        
                
                if (pipei == 3):
                    wucha = abs(xtan-utan)
                    if(wucha < jiejintan):
                        jiejintan = wucha
                        fasongt = 1
                        fasongx = x
                        fasongy = y
                
                if(pipei == 4):
                    fasongt = 0
                    fasongx = 0
                    fasongy = 0


        if(fasongt != 0 and fasongx != 0 and fasongy != 0):
            msg = Twist()
            msg.linear.z=fasongt
            msg.linear.x=-(fasongx)
            msg.linear.y=-(fasongy)

            pub.publish(msg)
            print(t1, msg.linear.x, msg.linear.y)
            if(pipei == 1):
                utan = 0
                pipei = 0
                zhongduan = 0
            elif(pipei == 2):
                vtan = 0
                pipei = 0
                zhongduan = 0
            elif(pipei == 3):
                utan = 0
                pipei = 2
        else:
            msg = Twist()
            msg.linear.z=fasongt
            msg.linear.x=-(fasongx)
            msg.linear.y=-(fasongy)

            pub.publish(msg)
            print(msg.linear)
            utan = 0
            vtan = 0
            pipei = 0
            zhongduan = 0
            


        
def listener():
    rospy.init_node('ronghejiedian')
    rospy.Subscriber("rongheshuru", Floats, callback)
    rospy.Subscriber('/pandar_points', PointCloud2, callback_pointcloud)
    rospy.spin()


if __name__ == '__main__':
    listener()

        

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geometry_msgs.msg import Twist
import cv2
import numpy as np
import rospy, cv_bridge
from sensor_msgs.msg import Image
import time
import apriltag

from follow import follow_line, set_roi_forward

def range_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)

    ret,binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

    dilation = cv2.dilate(binary, element2, iterations=1)

    erosion = cv2.erode(dilation, element1, iterations=1)

    dilation2 = cv2.dilate(erosion, element2, iterations=2)

    region=[]
    _,contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area < 1000):
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int64(box)

        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        if (height > width*1.3):
            continue
        region.append(box)
    return region

def stop(id):
    index=id
    cmd_vel_pub=rospy.Publisher('cmd_vel'+str(index),Twist,queue_size=10)
    twist=Twist()
    twist.linear.x=0.0
    twist.angular.z=0.0 
    for i in range(20):
        cmd_vel_pub.publish(twist)
    time.sleep(2)

def do_match(frame):
    max=0.0

    template=cv2.imread(r"/home/chuan/Desktop/stopsign2.png",cv2.IMREAD_GRAYSCALE) ## Load the template image ##
    if template is None:
        raise FileNotFoundError("Template image not found at path: /home/chuan/Desktop/stopsign2.png")
    # Ensure the frame is grayscale
    if len(frame.shape) == 3:  # If the frame is colored (3 channels)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)## Convert the frame to grayscale ##
    frame=frame.astype(template.dtype)## Convert the frame to the same data type as the template image ##

    res=cv2.matchTemplate(frame,template,cv2.TM_CCOEFF_NORMED) ## Match the template image with the frame ##
    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
    if max_val>max:
        max=max_val
    return max
    pass
def image_callback(msg):
    global global_flag
    global id
    global tag_flag
    global delay
    global delay_time
    bridge=cv_bridge.CvBridge()
    img=bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')## Convert the image message to OpenCV image ##
    ## Detect the parking lot ##
    follow_line(img, b)
    match=do_match(img)
    #print("match: ",match)
    if match>0.67: ##0.67 is the threshold
        print("Stop!")
        stop(1)
        time.sleep(3)
        rospy.signal_shutdown("fin")
        pass########??????

def get_camera():
    rospy.Subscriber('/camera/zed/rgb/image_rect_color',Image,image_callback)
    pass

if __name__=='__main__':
    a=int(input("which parking lot to follow: 1 for yellow, 2 for blue, 3 for red, 4 for green\n"))
    color_index={1:"yellow",2:"blue",3:"red",4:"green"}
    b=color_index[a] ## color of the parking lot

    rospy.init_node('get_camera')
    get_camera()
    rospy.spin()
    pass
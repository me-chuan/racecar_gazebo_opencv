#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  imghdr
import rospy,cv2,cv_bridge,numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

def set_roi_forward(h,w,mask):
    search_top=int(0.6*h)## 60% of the height of the image
    search_bot=search_top+20 ## 20 pixels below the search_top
    mask[0:search_top,0:w]=0
    mask[search_bot:h,0:w]=0
    return mask
    pass

def follow_line(image,color):
    cmd_vel_pub=rospy.Publisher('cmd_vel',Twist,queue_size=10)

    #print(image.shape)
    #convert to HSV
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV",hsv)
    #cv2.namedWindow("HSV",0)

    if color=="yellow":
        lower_color=numpy.array([ 26, 43, 46])## lower limit of the yellow color
        upper_color=numpy.array([ 34, 255, 255])## upper limit of the yellow color
    elif color=="blue":
        lower_color=numpy.array([100,150,0])
        upper_color=numpy.array([140,255,255])
    elif color=="red":
        lower_red1 = numpy.array([0, 120, 70])
        upper_red1 = numpy.array([10, 255, 255])
        lower_red2 = numpy.array([170, 120, 70])
        upper_red2 = numpy.array([180, 255, 255])
    elif color=="green":    
        lower_color=numpy.array([ 35, 43, 46])
        upper_color=numpy.array([ 77, 255, 255])
    else:
        raise ValueError("Invalid color")
    # Convert to binary image
    if color == 'red':
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, lower_color, upper_color)
    #cv2.namedWindow("binary image",0)
    #cv2.imshow("binary image",mask)

    h,w=mask.shape
    #print(mask.shape)

    #set region of interest
    mask=set_roi_forward(h,w,mask)
    #cv2.namedWindow("ROI",0)
    #cv2.imshow("ROI",mask)
    M=cv2.moments(mask)
    if M['m00']>0:
        cx=int(M['m10']/M['m00'])## 235 is the center of the image(deleted)
        cy=int(M['m01']/M['m00'])
        cv2.circle(image,(cx,cy),20,(0,0,255),-1)
        err=cx-w/2## 50 is the center of the image(deleted)
        twist=Twist()
        twist.linear.x=0.1
        twist.angular.z=-float(err)/100
        print("Linear: ",twist.linear.x)
        print("Angular: ",twist.angular.z)
        print("Message From follow.py Published\n")
        cmd_vel_pub.publish(twist)
        pass
    cv2.namedWindow("Original",0)
    cv2.imshow("Original",image)
    cv2.waitKey(1)
    pass

def image_callback(msg):
    print("Received an image!")
    bridge=cv_bridge.CvBridge()
    image=bridge.imgmsg_to_cv2(msg,desired_encoding="bgr8")
    follow_line(image,b)
    pass

if __name__ == '__main__':
    a=int(input("which parking lot to follow: 1 for yellow, 2 for blue, 3 for red, 4 for green\n"))
    color_index={1:"yellow",2:"blue",3:"red",4:"green"}
    b=color_index[a] ## color of the parking lot

    rospy.init_node('line_follower')
    rospy.Subscriber("/camera/zed/rgb/image_rect_color",Image,image_callback)
    rospy.spin() 
    pass
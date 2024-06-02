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
    lower_yellow=numpy.array([ 26, 43, 46])## lower limit of the yellow color
    upper_yellow=numpy.array([ 30, 255, 255])## upper limit of the yellow color

    #convert to binary image
    mask=cv2.inRange(hsv,lower_yellow,upper_yellow)
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
        cx=int(M['m10']/M['m00'])-235 ## 235 is the center of the image
        cy=int(M['m01']/M['m00'])
        cv2.circle(image,(cx,cy),20,(0,0,255),-1)
        err=cx-w/2 -50 ## 50 is the center of the image
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
    follow_line(image,"yellow")
    pass

if __name__ == '__main__':
    rospy.init_node('line_follower')
    rospy.Subscriber("/camera/zed/rgb/image_rect_color",Image,image_callback)
    rospy.spin() 
    pass
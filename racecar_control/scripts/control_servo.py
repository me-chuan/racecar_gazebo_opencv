#!/usr/bin/env python

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import Twist
from math import *

###### Warning: May have bugs ######
def callback(msg):
    pub=rospy.Publisher("/vesc/ackermann_cmd_mux/input/teleop", AckermannDriveStamped, queue_size=10)

    akm=AckermannDriveStamped()

    if msg.linear.x==0:
        akm.drive.speed=0
        akm.drive.steering_angle=0
    else:
        akm.drive.speed=msg.linear.x*1.80 ## 1.80 is the conversion factor
        akm.drive.steering_angle=atan(0.133*msg.angular.z/msg.linear.x) ## 0.133 is the distance between the front and rear axles
    print("Speed: ", akm.drive.speed)
    print("Steering Angle: ", akm.drive.steering_angle)
    print("Message From control_servo.py Published\n")
    pub.publish(akm)
    pass

def cmd_to_akm():
    rospy.init_node('cmd_to_akm', anonymous=True)
    rospy.Subscriber("cmd_vel1", Twist, callback)
    rospy.spin()
    pass

if __name__ == '__main__':
    try:
        cmd_to_akm()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python
import rospy

from ackermann_msgs.msg import AckermannDriveStamped

import sys, select, termios, tty

#from std_msgs.msg import String
#import os


banner = """
Reading from the keyboard  and Publishing to AckermannDriveStamped!
---------------------------
Moving around:
        w
   a    s    d
anything else : stop
CTRL-C to quit
"""
"""
keyBindings = {
  'w':(1,0),
  'd':(1,-1),
  'a':(1,1),
  's':(-1,0),
}
"""
## Function to get the key from the keyboard
def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

settings = termios.tcgetattr(sys.stdin)

def pub_cmd():
    index = 1
    rospy.init_node("pub_cmd")
    #rospy.Subscriber("control_topic", String, control_callback)
    pub = rospy.Publisher('/vesc/ackermann_cmd_mux/input/teleop', AckermannDriveStamped, queue_size=10)
    akm=AckermannDriveStamped()## Create an object of the AckermannDriveStamped class ##
    while True:
        x = 0
        a = 0
        key = getKey()
        if key == 'w':
            x = 0.3
            a = 0
        elif key == 's':
            x = -0.3
            a = 0
        elif key == 'a':
            x = 0.3
            a = 0.7
        elif key == 'd':
            x = 0.3
            a = -0.7
        elif key == 'x':
            x = 0
            a = 0
        elif key == 'o':
            break
        else:
            continue

        akm.drive.speed = x
        print("Speed:",akm.drive.speed)
        akm.drive.steering_angle = a
        print("Steering_Angle:",akm.drive.steering_angle)
        pub.publish(akm)
        print("Message From key_op.py Published\n")

"""
def control_callback(msg):
    if msg.data =="switch":
        rospy.loginfo("Shutting down keyboard_control function")
        os.system("rosrun racecar_control parking.py &")
        rospy.signal_shutdown("switching nodes")
"""

if __name__=="__main__":
    try:
        pub_cmd()
    except:
        pass
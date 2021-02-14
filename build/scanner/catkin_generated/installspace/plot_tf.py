#!/usr/bin/env python2
import roslib
import rospy
import math
import tf
import geometry_msgs.msg
import matplotlib.pyplot as plt
import time
import os

if __name__ == "__main__":
    rospy.init_node("TF_plotter")

    listener = tf.TransformListener()
    y = []
    rot = [0, 0, 0, 0]
    prev_rot = rot
    while not rospy.is_shutdown():
        try:
            prev_rot = rot
            (trans, rot) = listener.lookupTransform('odom', 'uvc_plate_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        angle = round(tf.transformations.euler_from_quaternion(rot)[2]*180/math.pi, 3)
        if angle < 0:
            angle = 360 + angle 
        print(angle)    
        print("\n\n")
        os.system("clear")
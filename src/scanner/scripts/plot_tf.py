#!/usr/bin/env python
import roslib
import rospy
import math
import tf
import geometry_msgs.msg
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    rospy.init_node("TF_plotter")

    listener = tf.TransformListener()
    y = []
    rot = [0, 0, 0, 0]
    prev_rot = rot
    while not rospy.is_shutdown():
        try:
            prev_rot = rot
            (trans, rot) = listener.lookupTransform('base_link', 'odom', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
    
        for i in rot[2:4]:
            print round(i, 4)
        print "\n\n"
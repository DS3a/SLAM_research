import rospy
import tf
import time
from geometry_msgs.msg import Twist
from math import pi
import math


class Bot:
    def __init__(self, one_rot_ps=2*pi, one_mps=1, invert=True, factor=1):
        # i've defaulted invert to true, because it's like that in my bot
        if invert:
            self.invert = -1 * factor
        else:
            self.invert = 1 * factor
        self.twist = Twist()
        self.one_rot_ps = one_rot_ps
        self.one_mps = one_mps
# think of one_rot_ps and one_mps as the units that we multiply to the end of the speed/velocity


    def default_twist(self):
        self.twist = Twist()
        return self.twist

    def turn(self, rots, time, rewrite=False):
        if rewrite:
            self.default_twist()

        self.twist.angular.z = (float(rots)/float(time))*self.one_rot_ps * self.invert
        return self.twist

    def move(self, dist, time, rewrite=False):
        if rewrite:
            self.default_twist()

        self.twist.linear.x = (float(dist)/float(time))*self.one_mps * self.invert
        return self.twist

    @staticmethod
    def get_angle(tf_tup): # takes transform in quaternion value, and returns the angle in degrees
        tf_rot = tf_tup[1]
        tf_rot_angle = tf.transformations.euler_from_quaternion(tf_rot)[2] * (180/math.pi)
        if tf_rot_angle < 0:
            tf_rot_angle += 360
        tf_rot_angle = round(tf_rot_angle, 3)
        return tf_rot_angle

    @staticmethod
    def get_dist(tf_tup1, tf_tup2):
        tf_mv1 = tf_tup1[0]
        tf_mv2 = tf_tup2[0]

        dist = 0
        for x1, x2 in zip(tf_mv1, tf_mv2):
            dist += (x1 - x2) **2
        dist = math.sqrt(dist)
        return dist

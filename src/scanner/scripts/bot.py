#!/usr/bin/env python

import tf
import rospy
import time
from geometry_msgs.msg import Twist
from math import pi
import math

rospy.init_node("testing_with_vels", anonymous=False)
publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
listener = tf.TransformListener()


class Bot:
    def __init__(self, one_rot_ps=2*pi, one_mps=1, invert=True):
        # i've defaulted invert to true, because it's like that in my bot
        if invert:
            self.invert = -1
        else:
            self.invert = 1
        self.twist = Twist()
        self.one_rot_ps = one_rot_ps
        self.one_mps = one_mps
# think of one_rot_ps and one_mps as the units that we multiply to the end of the speed/velocity


    def default_twist(self):
        self.twist.angular.z = 0
        self.twist.linear.x = 0

    def turn(self, rots, time, rewrite=False):
        if rewrite:
            self.default_twist()

        self.twist.angular.z = (rots/time)*self.one_rot_ps * self.invert
        return self.twist

    def move(self, dist, time, rewrite=False):
        if rewrite:
            self.default_twist()

        self.twist.linear.x = (dist/time)*self.one_mps * self.invert
        return self.twist

class Test:
# assuming that there's a constant to multiply to the speed 
# to make the bot move at the standard units

    def __init__(self, tf_world, tf_bot_com):
        self.publisher = rospy.
        self.tf_world = tf_world
        self.tf_bot_com = tf_bot_com
        self.bot = Bot() # initializing with default vals

    def test_angular(self):
# moving 90 degrees, i.e 0.25 rotation, in 2 seconds, i.e speed of 2*pi / 8
        msg = self.bot.turn(0.25, 2)
        (trans_init, rot_init) = listener.lookupTransform(tf_bot_com, tf_world, rospy.Time(0))
        time_init = time.time()
        while time.time() - time_init <= 2:
            publisher.publish(msg)
        (trans_final, rot_final) = listener.lookupTransform(tf_bot_com, tf_world, rospy.Time(0))        
        msg = self.bot.default_twist()
        publisher.publish(msg)
        init_angle = 2 * math.asin(rot_init[2]) # multiplying by 2, becz
        # there's two quaternion multiplications, one to reset the other sphere
        # , while rotating the other one... izz complicated, checkout the video from 3b1b
        final_angle = 2 * math.asin(rot_final[2])
        theta = final_angle - init_angle
        print("Travelled ", theta, " in 2 seconds, with a speed of pi/4")

# moving 180 degrees, i.e 0.5 rotation, in 2 seconds, i.e speed of 2*pi / 4
        msg = self.bot.turn(0.5, 2)
        (trans_init, rot_init) = listener.lookupTransform(tf_bot_com, tf_world, rospy.Time(0))
        time_init = time.time()
        while time.time() - time_init <= 2:
            publisher.publish(msg)
        (trans_final, rot_final) = listener.lookupTransform(tf_bot_com, tf_world, rospy.Time(0))        
        msg = self.bot.default_twist()
        publisher.publish(msg)
        init_angle = 2 * math.asin(rot_init[2]) # multiplying by 2, becz
        # there's two quaternion multiplications, one to reset the other sphere
        # , while rotating the other one... izz complicated, checkout the video from 3b1b
        final_angle = 2 * math.asin(rot_final[2])
        theta = final_angle - init_angle
        print("Travelled ", theta, " in 2 seconds, with a speed of pi/2")

# doing it twice to check if the relationship is linear or not


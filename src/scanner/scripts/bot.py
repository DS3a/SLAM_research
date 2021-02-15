#!/usr/bin/env python

import rospy
import tf
import time
from geometry_msgs.msg import Twist
from math import pi
import math

rospy.init_node("testing_with_vels", anonymous=False)
publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
listener = tf.TransformListener()


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

class Test:
# assuming that there's a constant to multiply to the speed 
# to make the bot move at the standard units

    def __init__(self, tf_world, tf_bot_com):
        self.publisher = publisher
        self.tf_world = tf_world
        self.tf_bot_com = tf_bot_com
        self.bot = Bot(one_rot_ps=7.125*pi, one_mps=3.57)

        # don't make the robot spin at a speed higher than 0.25rps to avoid backlash 
#        self.bot = Bot() # initializing with default vals

    def test_angular(self, time_to_rot):

#        msg = self.bot.turn(0.25, 2) # will set a speed of pi/4 = 0.78539

        msg = self.bot.turn(0.25, time_to_rot, rewrite=True)
        try:
            tf_init = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))
        except:
            time.sleep(0.5)
            tf_init = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))


        init_angle = self.bot.get_angle(tf_init)
        print("init angle : ", init_angle)

        tf_current = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))
        current_angle = self.bot.get_angle(tf_current)
        time_init = time.time()
        time_taken = 0
        while abs(current_angle - init_angle) <= 90 or abs(current_angle - init_angle) >= 270:
            publisher.publish(msg)
            tf_current = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))
            current_angle = self.bot.get_angle(tf_current)
            time_taken = time.time() - time_init

        msg = self.bot.default_twist()
        publisher.publish(msg)
        final_angle = current_angle
        print("final angle : ", final_angle)
        print("time taken = ", time_taken)
        print "\n"
        return time_taken

    def test_linear(self, time_to_mov):
        msg = self.bot.move(1, time_to_mov, rewrite=True)

        try:
            tf_init = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))
        except:
            time.sleep(0.5)
            tf_init = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))

        print("init coords : ", tf_init[0])
        
        tf_current = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))
        time_init = time.time()
        time_taken = 0
        while self.bot.get_dist(tf_current, tf_init) <= 1:
            publisher.publish(msg)
            tf_current = listener.lookupTransform(self.tf_world, self.tf_bot_com, rospy.Time(0))
            time_taken = time.time() - time_init
        msg = self.bot.default_twist()
        publisher.publish(msg)

        print("final coords : ", tf_current[0])
        print("distance travelled : ", self.bot.get_dist(tf_init, tf_current))
        print("time taken : ", time_taken)
        print "\n"
        return time_taken

    def auto_calibrate_angular(self):
        factors = []
        for time_to_comp in range(5, 20, 5):
            time_taken = 0
            for i in range(3):
                time_taken += self.test_angular(time_to_comp)
            factor = (time_taken/3.0)/time_to_comp
            factors.append(factor)

        final_factor = 0
        for factor in factors:
            final_factor += factor
        final_factor = final_factor / 3
        print("The angular factor is : ", final_factor)
        return final_factor

    def auto_calibrate_linear(self):
        factors = []
        for time_to_comp in range(5, 20, 5):
            time_taken = 0
            for i in range(3):
                time_taken += self.test_linear(time_to_comp)
            factor = (time_taken/3.0)/time_to_comp
            factors.append(factor)

        final_factor = 0
        for factor in factors:
            final_factor += factor
        final_factor = final_factor / 3
        print("The linear factor is : ", final_factor)
        return final_factor



if __name__ == "__main__":
    test = Test(tf_world="odom", tf_bot_com="uvc_plate_1")
    test.auto_calibrate_angular()
    print "\n\n\n"
    test.auto_calibrate_linear()

# initial testing shows one_rot_ps speed to be 6.57*pi

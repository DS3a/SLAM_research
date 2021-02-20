#!/usr/bin/env python

import rospy
import time
from geometry_msgs.msg import Twist
from math import pi
import math
import tf
from bot import Bot

print("Initializing node")
rospy.init_node("scanner", anonymous=False)
#radial_turn_positioner = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
radial_turn_positioner = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
#position = rospy.

vel_msg = Twist()

def radial_scan():
    """
        We need the bot to move in a spiral, so I'll just keep the angular velocity constant
        And accelerate the linear velocity, so as to increase the radius of rotation
        so, we can find the velocity using the formula v = u + at

        The angular velocity z doesn't add any linear velocity, as the axis of rotation
        is about the centre of mass of the robot, which just makes it turn, 
        and not give any linear velocity at all
    """

    radius_to_scan = 2 # in metres, or whatever units are used in the gazebo thingy
    angular_speed = pi/10 # 1 rotation per 20 seconds

    time_to_complete = 360 # seconds

    v_initial = 0
    v_final = 2 * pi * radius_to_scan * angular_speed / (2*pi) 
    # angular_speed / angle covered in one rotation = 1 / time_taken
    # and, total distance travelled = 2 * pi * r in the final circle, so
    # v_final = 2*pi*r*(angular_speed/2*pi)

    acceleration = (v_final - v_initial)/time_to_complete
    print("The acceleration is : ", acceleration)

    v_current = 0
    vel_msg.angular.z = angular_speed

    time_at_start = time.time()
    while v_current <= v_final:
        v_current = v_initial + acceleration*(time.time()-time_at_start)
        if int(time.time()-time_at_start) % 2 == 0:
            print("moving with velocity : ", v_current) 
        vel_msg.linear.x = -v_current # cuz the bot's movement thingy has to be reversed
        radial_turn_positioner.publish(vel_msg)


def circle():
    radius = 1
    bot = Bot(one_rot_ps=7.125*pi, one_mps=3.57)
    publisher = radial_turn_positioner
    msg = bot.turn(0.5, 20) # angular_vel = (6.8/20)pi => time for one rot = 20
    angular_vel = bot.twist.angular.z
    time_for_one_rot = 40 # seconds
    msg = bot.move(2*pi*radius, time_for_one_rot)
#    msg = bot.move(0, time_for_one_rot)
    print(msg)
    time_init = time.time()
    while time.time() - time_init <= time_for_one_rot:
        publisher.publish(msg)
    msg = bot.default_twist()
    publisher.publish(msg)

if __name__ == "__main__":
#    while not rospy.is_shutdown():
    radial_scan()
    exit(0)
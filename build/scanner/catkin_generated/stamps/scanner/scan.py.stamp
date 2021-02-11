#!/usr/bin/env python3

import rospy
import time
from geometry_msgs.msg import Twist
from math import pi

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
    angular_speed = 2*pi # 1 rotation per second

    time_to_complete = 20 # seconds

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
        vel_msg.linear.x = v_current
        radial_turn_positioner.publish(vel_msg)

def turn_90():
    angular_speed = 200
    vel_msg.angular.z = angular_speed
    vel_msg.linear.x = 0

    time_to_rot = (pi/2)/angular_speed
    time_to_rot = 3

    print("it'll take ", time_to_rot, " seconds to rotate 90 degrees")
    time_init = time.time()
    while time.time() - time_init <= time_to_rot:
        radial_turn_positioner.publish(vel_msg)
    vel_msg.angular.z = 0
    radial_turn_positioner.publish(vel_msg)


if __name__ == "__main__":
#    while not rospy.is_shutdown():
    radial_scan()
#    turn_90()
    exit(0)
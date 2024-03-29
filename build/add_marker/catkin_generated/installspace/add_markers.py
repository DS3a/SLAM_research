#!/usr/bin/env python2

import roslib
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import String
import json
import tf


rospy.init_node("marker")

topic = "visualization_marker_array"
mine_topic = "mine_pose"
publisher = rospy.Publisher(topic, MarkerArray)
mines = []


def add_mine(pose):
"""
	code to convert whatever comes in to a dictionary like this {"X":x_val, "Y":y_val}
"""
	mine = json.loads(pose)
	mines.append({"X": pose["X"], "Y": pose["Y"]})

def json_to_marker(mine_pos):
	marker = Marker()
	marker.header.frame_id = "/odom"	
	marker.type = marker.CYLINDER
	marker.action = marker.ADD
	marker.scale.x = 0.10
	marker.scale.y = 0.10
	marker.scale.z = 1.0
    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 1.0

    marker.pose.orientation.w = 1.0
    marker.pose.position.x = mine_pos["X"]
    marker.pose.position.y = mine_pos["Y"]
    marker.pose.position.z = 0.5

    return marker


def mark_mines():
	mine_finder = rospy.Subscriber(mine_topic, Twist, add_mine)
	marker_array = MarkerArray()
	for mine in mines:
		marker_array.markers.append(json_to_marker(mine))

	publisher.publish(marker_array)

	rospy.spin()

if __name__ == "__main__":
	mark_mines()


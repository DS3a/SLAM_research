#!/usr/bin/env python

import roslib
import rospy
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import OccupancyGrid
import tf

rospy.init_node("MapAreaGraph", anonymous = True)
def area_covered(data):
    mapdata=data.data
    non_covered_cells= mapdata.count(-1)
    print(non_covered_cells)
    

def graph_area():
    rospy.Subscriber('/map',OccupancyGrid, area_covered)
    rospy.spin()
if __name__ == "__main__":
    try:
        graph_area()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python

import roslib
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int32
from nav_msgs.msg import OccupancyGrid
import tf

rospy.init_node("MapAreaGraph", anonymous = True)

topic = "map_covered"    
publisher = rospy.Publisher(topic, Int32,queue_size=1) 

def area_covered(data):
    mapdata=data.data
    totalcells=len(mapdata)
    non_covered_cells= mapdata.count(-1)
    area_covered_points=totalcells-non_covered_cells
    publisher.publish(area_covered_points)
    print(str(area_covered_points) + "/" + str(totalcells))
    

def graph_area():
    rospy.Subscriber('/map',OccupancyGrid, area_covered)
    rospy.spin()
if __name__ == "__main__":
    try:
        graph_area()
    except rospy.ROSInterruptException:
        pass

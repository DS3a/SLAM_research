#!/usr/bin/env python

import roslib
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import Float32MultiArray
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import Pose
import tf

marker_array = MarkerArray()
topic = "visualization_marker_array"    
publisher = rospy.Publisher(topic, MarkerArray,queue_size=10)       
objid=0 
rospy.init_node("marker", anonymous = True)
listener = tf.TransformListener() 
#rospy.wait_for_service("gazebo_msgs/SpawnModel")
#spawn_model = rospy.ServiceProxy("gazebo_msgs/SpawnModel", SpawnModel)
#spawn_pose=Pose()


def objtf(data1):
    
    print("New Message")
    print(data1)
    global marker_array

    for i in range(0,len(data1.data),12):
        objid = int(data1.data[i])
        print(objid)
        if objid == 3:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_3", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_3',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
            
        elif objid == 4:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_4", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_4',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
        elif objid == 5:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_5", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_5',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
        
        elif objid==6:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_6", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_6',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
        
        elif objid==7:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_7", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_7',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
        
        elif objid==8:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_8", now, rospy.Duration(0.5))
            (pos,rot) = listener.lookupTransform('/odom','/object_8',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
        
        elif objid==9:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_9", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_9',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    

            
        elif objid==10:
            
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_10", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_10',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
            
        
        elif objid==11:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/object_11", now, rospy.Duration(0.2))
            (pos,rot) = listener.lookupTransform('/odom','/object_11',now)
            print(pos)
            print(rot)
            marker1 = Marker()
            marker1=objpose_to_marker(pos,rot)                    
                           
        
        publisher.publish(marker_array)
        
        print("Marker Published")   
            

def spawn_gazebo(marker1):
    spawn_pose= marker1.pose
    item_name="Mine_Cone" 
    with open("/home/gautam/slam_ws/src/minefield_sim/models/construction_cone/model.sdf", "r") as f:
        product_xml = f.read()
    spawn_model(item_name, product_xml, "", spawn_pose, "minefield.world")
    
    
def objpose_to_marker(pose,rot):
    
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
    
    #marker.pose.orientation.x = rot[0]
    #marker.pose.orientation.y = rot[1]
    #marker.pose.orientation.z = rot[2]
    marker.pose.orientation.w = rot[3]
    marker.pose.position.x = pose[0]
    marker.pose.position.y = pose[1]
    marker.pose.position.z = pose[2]
    
    marker_array.markers.append(marker)
    print("Marker Added Successfully")
    spawn_gazebo(marker)
    return marker

    

def mark_mines():

      
    #topic = "visualization_marker_array"    
    #publisher = rospy.Publisher(topic, MarkerArray,queue_size=10)

    rospy.Subscriber('/objects',Float32MultiArray, objtf)
        
    #publisher.publish(marker_array)
    #print("Published sucessfully")
    rospy.spin()
         
if __name__ == "__main__":
    try:
        mark_mines()
    except rospy.ROSInterruptException:
        pass
        

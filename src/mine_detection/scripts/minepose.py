#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import QPointF
import cv2 
import tf

class Objects:

    def __init__(self):
        self.current_frame = None
        self.data1 = Float32MultiArray()
   
    def callback(self,data):
        br=CvBridge()
        self.current_frame = br.imgmsg_to_cv2(data)
        
    def show_boundingbox(self,data1):
        listener = tf.TransformListener()
        while not rospy.is_shutdown():
            try:
                (trans,rot) = listener.lookupTransform('base_link','object_43',rospy.Time(0))
                color = (0,255,0)
                #print(trans)
                print(data1.data)
                for i in range(0,len(data1.data),12):
                    #get data
                    objid = int(data1.data[i])
                    objectWidth = data1.data[i+1]
                    objectHeight = data1.data[i+2]

                    #Find corners Qt
                    
                    qtHomography=QTransform(data1.data[i+3], data1.data[i+4], data1.data[i+5], data1.data[i+6], data1.data[i+7], data1.data[i+8],data1.data[i+9], data1.data[i+10],data1.data[i+11])

                    qtTopLeft = QPointF()
                    qtTopRight = QPointF()
                    qtBottomLeft = QPointF()
                    qtBottomRight = QPointF()

                    qtTopLeft = qtHomography.map(QPointF(0,0))
                    qtTopRight = qtHomography.map(QPointF(objectWidth,0))
                    qtBottomLeft = qtHomography.map(QPointF(0,objectHeight))
                    qtBottomRight = qtHomography.map(QPointF(objectWidth,objectHeight))

                    tlx=int(qtTopLeft.x())
                    tly=int(qtTopLeft.y())
                    
                    image = cv2.rectangle(self.current_frame,(tlx,tly),(int(tlx+objectWidth),int(tly+objectHeight)),color,2)
                 
                    if objid == 46:
                        cv2.putText(image,'Coke',(tlx,tly-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
                    elif objid==51:
                        cv2.putText(image,'Glue',(tlx,tly-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
                    elif objid==48:
                        cv2.putText(image,'FPGA',(tlx,tly-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
                    elif objid==52:
                        cv2.putText(image,'Glue',(tlx,tly-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
		    elif objid==60:
                        cv2.putText(image,'Glue',(tlx,tly-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
	   	    elif objid==49:
                        cv2.putText(image,'FPGA',(tlx,tly-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
                
                cv2.imshow("DetectedObjects",image)
                cv2.waitKey(0)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")
            
def receive_message():
    rospy.init_node('BoundingBox', anonymous = True)
    objs = Objects()
    rospy.Subscriber('/camera/color/image_raw2', Image, objs.callback)
    rospy.Subscriber('/objects',Float32MultiArray, objs.show_boundingbox)
    
    rospy.spin()
    
    cv2.destroyAllWindows()
        
if __name__ == '__main__':
    try:
        receive_message()
        objs2 = Objects()
        objs.wait_for_subscribers()
    except rospy.ROSInterruptException:
        pass
    

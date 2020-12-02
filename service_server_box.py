#! /usr/bin/env python
import rospy                                           # the main module for ROS-python programs
from std_srvs.srv import Trigger, TriggerResponse      # we are creating a 'Trigger service'...
                                                       # ...Other types are available, and you can create
                                                       # custom types
import os
import time as t
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
import numpy as np

name = 'box'
box_i = 0

robot_proxy = None

def trigger_response(request):
    global box_i
    '''
    Callback function used by the service server to process
    requests from clients. It returns a TriggerResponse
    '''

    dropBoxBool = False
    
    a = getRobotLocation()
    x = a[0]
    y = a[1]

    b = getBoxLocation(x,y)
    if(b != None):
        if not checkBoxLocation(b[0],b[1]):
            dropBox(b[0], b[1])
            dropBoxBool = True

    return TriggerResponse(
        success=10.1,
        message="dt = "
    )

def delBox(bi):

    buff = "rosservice call gazebo/delete_model "+name+str(bi) + " &"
    os.system(buff)

def delBoxAll(bi):
    for i in range(bi):
        delBox(i)
        t.sleep(0.1)

def dropBox(x,y):
    global box_i
    saveBoxVal(x,y)
    b0 = "./drop_box.sh "
    b1 = str(x) + " "
    b2 = str(y) + " "
    b3 = name + str(box_i) + " "
    box_i += 1
    b4 = "&"
    buff = b0 + b1 + b2 + b3 + b4
    os.system(buff)


def getBoxLocation(x,y):

    #determine if it is inside of the 50m - 2m circle
    x0 = 0.0
    y0 = 0.0
    dist = np.sqrt( (x-x0)*(x-x0) + (y-y0)*(y-y0) )
    #rospy.loginfo("Dist = ", str(dist))
    if(dist < (50-2)):
        return None
    else:
        theta = np.arctan2(y,x)
        R = 50.0
        xn = np.cos(theta)*R
        yn = np.sin(theta)*R

        return (xn, yn)

    return

box_x = []
box_y = []
def saveBoxVal(x,y):
    global box_x, box_y
    box_x.append(x)
    box_y.append(y)
    return

def checkBoxLocation(x, y):
    global box_x, box_y
    for i in range(len(box_x)):
        xx = box_x[i]
        yy = box_y[i]
        d = np.sqrt((xx-x)*(xx-x) + (yy-y)*(yy-y))
        if d < 1.01:
            return True # return true if within 0.5m
    return False

def getRobotLocation():
    global robot_proxy
    a = GetModelStateRequest(model_name='dd_robot')
    a.model_name = "dd_robot"
    s = robot_proxy(a)
    #print a
    #print s
    x = s.pose.position.x
    y = s.pose.position.y
    print "x = "+ str(x) + "y = " + str(y)
    return (x,y)

rospy.init_node('service_example')      # initialize a ROS node
delBoxAll(7)
my_service = rospy.Service(       # create a service, specifying its name, 
    '/box', Trigger, trigger_response    # type, and callback
)
rospy.wait_for_service('/gazebo/get_model_state')
robot_proxy = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
rospy.spin()

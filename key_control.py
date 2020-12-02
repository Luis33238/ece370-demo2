import rospy
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties

msg_topic = '/gazebo/apply_joint_effort'
joint_left = 'dd_robot::left_wheel_hinge'
joint_right = 'dd_robot::right_wheel_hinge'

start_time = rospy.Time(0,0)

end_time = rospy.Time(1.0)

rospy.init_node('dd_ctrl', anonymous=True)
pub = rospy.ServiceProxy(msg_topic,ApplyJointEffort)
msg_topic_feedback = '/gazebo/get_joint_properties'

pub_feeback = rospy.ServiceProxy(msg_topic_feedback, GetJointProperties)

while True:
    data = raw_input("Input robot control: ")
    print data
    if(data == "w"):
        pub(joint_left, 1, start_time, end_time)
        pub(joint_right, 1, start_time, end_time)
    elif(data == "s"):
        pub(joint_left, -1, start_time, end_time)
        pub(joint_right, -1, start_time, end_time)
        print data + "in thing"
        val = pub_feeback(joint_left)
        print(val)
    elif(data == "a"):
        pub(joint_right, 1, start_time, end_time)
        pub(joint_left, -1, start_time, end_time)
    else:
        pub(joint_left, 1, start_time, end_time)
        pub(joint_right, -1, start_time, end_time)

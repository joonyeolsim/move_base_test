#! /usr/bin/python3

import rospy
import actionlib
import uuid
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def fb_callback(feedback):
    rospy.loginfo(feedback)


def move_base_client():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rate = rospy.Rate(5)

    client.wait_for_server()

    waypoints = [MoveBaseGoal() for _ in range(3)]

    for i, waypoint in enumerate(waypoints):
        waypoint.target_pose.header.frame_id = "robot_map"
        waypoint.target_pose.header.stamp = rospy.Time.now()
        waypoint.target_pose.pose.position.z = 0.0
        waypoint.target_pose.pose.orientation.x = 0.0
        waypoint.target_pose.pose.orientation.y = 0.0
        if i == 0:
            waypoint.target_pose.pose.position.x = 6.87822591107
            waypoint.target_pose.pose.position.y = 1.60042301926
            waypoint.target_pose.pose.orientation.z = -0.843253586084
            waypoint.target_pose.pose.orientation.w = 0.537515943537

        elif i == 1:
            waypoint.target_pose.pose.position.x = -3.88581387372
            waypoint.target_pose.pose.position.y = -23.7404345006
            waypoint.target_pose.pose.orientation.z = -0.861512936696
            waypoint.target_pose.pose.orientation.w = 0.507735620088

        elif i == 2:
            waypoint.target_pose.pose.position.x = 4.93597370986
            waypoint.target_pose.pose.position.y = -3.30991411081
            waypoint.target_pose.pose.orientation.z = 0.5019602212
            waypoint.target_pose.pose.orientation.w = 0.864890707739

    for i, waypoint in enumerate(waypoints):
        rospy.loginfo(f"Sending Goal: {waypoint}")

        client.send_goal(waypoint, feedback_cb=fb_callback)

        state_result = client.get_state()
        while state_result < 2:
            state_result = client.get_state()
            rate.sleep()

        if state_result == 3:
            rospy.logwarn(f"Action {i} Done. State Result : {client.get_result()}")
        else:
            rospy.logerr(f"Action {i} went wrong, State Result : {state_result}")


if __name__ == '__main__':
    try:
        rospy.init_node("move_base_client")
        import roslaunch

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)

        cli_args = ['/home/joonyeol/catkin_ws/src/turtlebot3_simulations/turtlebot3_gazebo/launch/turtlebot3_world.launch', 'vel:=2.19']
        roslaunch_args = cli_args[1:]
        roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]

        parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)

        parent.start()

        rospy.loginfo("started")
        #
        # move_base_client()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion")
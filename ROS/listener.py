# 订阅者程序
# !/usr/bin/env python
# 导入rospy库
import time
import rospy
# 导入ROS std_msgs标准消息中的String消息
from turtlesim.msg import Pose
from turtlesim.msg import Color


# 声明订阅器回调函数
def callback_pose(pose):
    rospy.loginfo('乌龟的位置：（%.2f,%.2f）,朝向角度：%.2f,线速度：%.2f,角速度：%.2f', pose.x, pose.y,
                  pose.theta, pose.linear_velocity, pose.angular_velocity)


def listener_pose():
    # 初始化ROS节点，命名节点为listener
    rospy.init_node('listener', anonymous=True)
    # rate = rospy.Rate(20)
    # 创建订阅器，收听/chatter话题，绑定callback回调函数
    rospy.Subscriber('/turtle1/pose', Pose, callback_pose)
    time.sleep(0.1)
    # 进入spin阻塞式回调循环，等待话题消息
    # rospy.spin()


def callback_rgb(rgb):
    rospy.loginfo('乌龟的背景颜色：r:%d,g:%d,b:%d', rgb.r, rgb.g, rgb.b)


def listener_rgb():
    # 初始化ROS节点，命名节点为listener
    rospy.init_node('listener', anonymous=True)
    # 创建订阅器，收听/chatter话题，绑定callback回调函数
    rospy.Subscriber('/turtle1/color_sensor', Color, callback_rgb)
    # time.sleep(0.017)
    # 进入spin阻塞式回调循环，等待话题消息
    # rospy.spin()


if __name__ == '__main__':
    listener_pose()

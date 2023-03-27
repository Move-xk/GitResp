# 发布者程序
# !/usr/bin/env python
# 导入rospy库
import rospy
# 导入ROS std_msgs标准消息中的String消息
from std_msgs.msg import String


def talker():
    # 初始化ROS节点，命名节点为talker
    rospy.init_node('talker', anonymous=True)
    # 创建发布器，向/chatter话题发布String类型消息
    pub = rospy.Publisher('chatter', String, queue_size=10)
    # 创建一个rospy.Rate对象，控制循环频率为10hz
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # 创建字符串
        hello_str = "hello world %s" % rospy.get_time()
        # 打印字符串
        rospy.loginfo(hello_str)
        # 利用发布器发布话题
        pub.publish(hello_str)
        # 控制循环频率
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

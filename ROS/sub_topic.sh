#!/bin/bash

check_file=/home/xk/PycharmProjects/pythonProject/ROS/pose.csv
if [ -e "$check_file" ];then
  rm -rf pose.csv
fi

echo '开始检查乌龟的Pose坐标输出'
timeout 1 rostopic echo /turtle1/pose > pose.csv
if [ -s "$check_file" ];then
  echo '获取乌龟Pose成功'
else
  echo '获取乌龟Pose失败，请检查节点情况'
fi
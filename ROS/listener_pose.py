import csv
import os

sub_pose = os.system('sh sub_topic.sh')
filename = 'pose.csv'
with open(filename) as f:
    n = 0
    for row in csv.reader(f):
        print(row[0])
        n += 1
        if n >= 5:
            print('乌龟坐标输出完成')
            break

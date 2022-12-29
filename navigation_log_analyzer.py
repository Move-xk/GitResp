#!/usr/bin/env python

# import rospy
# import tf
# import math
# import pandas as pd 
# import matplotlib as plt 
# import numpy as np 
# import re


# log_list = []
# log_file = "/home/ld/.forwardx_log/forwardx_move_base/forwardx_move_base.log"


# with open(log_file) as log_all:
#     for line in log_all:
#         if ": " in line:
#             log_list.append(re.findall(r'\[(.*?)\]', line.split(": ", 1)[0]) + re.findall(r'\[(.*?)\]', line.split(": ", 1)[1].split(" ", 1)[0]) + [line.split(": ", 1)[1].split(" ", 1)[1]])

# pd_log = pd.DataFrame(log_list)
# pd_log.columns=["Level", "Time", "Node", "Message"]
# pd_log.index.name = "Seq"

# pd_log['Level'].value_counts()
# # pd_log.loc[pd_log['Level'].isin(["ERROR"])]


import sys
from navigation_pose_analyzer import NavPoseAnalyzer


if __name__ == '__main__':
    # log_file = "/home/ld/.forwardx_log/forwardx_move_base/forwardx_move_base.log"
    # log_file = "/home/ld/Downloads/V1500L_move_base_log.log"
    analyzer_name = raw_input("Choose analyzer by entering index:  \n  1: NavPoseAnalyzer ")
    analyzer_map = {"1" : NavPoseAnalyzer, "" : NavPoseAnalyzer}
    item = "default"

    # for log_file in sys.argv[1:]:
    #     print log_file
    #     try:
    #         analyzer = analyzer_map[analyzer_name](True)
    #         analyzer.load_log(log_file)
    #         analyzer.analyze_all()
    #     except Exception as e:
    #         print "[ERROR] Illege log file for this analyzer. Please check log file and exception message below."
    #         print e

    #     while not analyzer.print_specific(raw_input("Enter specific item name to check, e.g. real-reached, enter 'all' to show all data. \nPress Enter directly to analyse next log. \n: ")):
    #         pass

    
    analyzer = analyzer_map[analyzer_name](True)
    analyzer.load_log(sys.argv[1:])
    analyzer.analyze_all()
    

    while not analyzer.print_specific(raw_input("Enter specific item name to check, e.g. real-reached, enter 'all' to show all data. \nPress Enter directly to end. \n: ")):
        pass
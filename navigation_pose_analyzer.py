#!/usr/bin/env python
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


class NavPoseAnalyzer:
    def __init__(self, brief):
        self.reached_flag = False
        self.brief = brief
        self.docking = -1
        # checking items should be in specific format like "pose_name-pose_name"
        self.check_list = ["goal-real", "real-reached", "reached-stopping", "stopping-stopped", "goal-stopped",
                           "goal-reached-position", "reached-stopped-position", "goal-stopped-position",
                           "goal-reached-theta", "reached-stopped-theta", "goal-stopped-theta"]
        self.check_list_position = ["goal-reached-position", "reached-stopped-position", "goal-stopped-position"]
        self.check_list_theta = ["goal-reached-theta", "reached-stopped-theta", "goal-stopped-theta"]
        self.pd_nav_test_results = pd.DataFrame()

    def get_pose(self, log_line):
        pose = []
        # in default, the first () data in line is pose
        data_list = re.findall(r'[(](.*?)[)]', log_line)[0].split(',')

        for data in data_list:
            pose.append(float(data))

        if abs(pose[2]) > math.pi - 0.00001:
            pose[2] = pose[2] - 2 * math.pi if pose[2] > 0 else pose[2] + 2 * math.pi

        return pose

    def calc_position_diff(self, pose_data_1, pose_data_2):
        try:
            return math.sqrt(
                math.pow((pose_data_1[0] - pose_data_2[0]), 2) + math.pow((pose_data_1[1] - pose_data_2[1]), 2))
        except OverflowError as e:
            print("[ERROR] Illege data at: " ". Please check log file and exception message below.")
            print(e)
            return np.nan

    def calc_theta_diff(self, pose_data_1, pose_data_2):
        theta_diff = abs(pose_data_1[2] - pose_data_2[2])
        if abs(theta_diff) > math.pi - 0.00001:
            theta_diff = theta_diff - 2 * math.pi if theta_diff > 0 else theta_diff + 2 * math.pi

        return abs(theta_diff)

    def calc_pose_diff(self, pose_data_1, pose_data_2):
        # [x, y, theta]
        # x_diff = math.sqrt( math.pow((pose_data_1[0] - pose_data_2[0]), 2) )
        # y_diff = math.sqrt( math.pow((pose_data_1[1] - pose_data_2[1]), 2) )
        # theta_diff = math.sqrt( math.pow((pose_data_1[2] - pose_data_2[2]), 2) )
        x_diff = abs(pose_data_1[0] - pose_data_2[0])
        y_diff = abs(pose_data_1[1] - pose_data_2[1])
        theta_diff = abs(pose_data_1[2] - pose_data_2[2])
        if abs(theta_diff) > math.pi - 0.00001:
            theta_diff = theta_diff - 2 * math.pi if theta_diff > 0 else theta_diff + 2 * math.pi

        return [x_diff, y_diff, theta_diff]

    def check_two_pose(self, check_item, pd_df):
        target = check_item.split("-")
        item_data = []
        item_position = []
        item_theta = []
        for i in pd_df.index:
            try:
                item_data.append(self.calc_pose_diff(pd_df[target[0]][i], pd_df[target[1]][i]))
                if target[2] == "position":
                    item_position.append(self.calc_position_diff(pd_df[target[0]][i], pd_df[target[1]][i]))
                    item_theta.append(np.nan)
                if target[2] == "theta":
                    item_theta.append(self.calc_theta_diff(pd_df[target[0]][i], pd_df[target[1]][i]))
                    item_position.append(np.nan)
            except TypeError:
                item_data.append([np.nan, np.nan, np.nan])
            except IndexError:
                item_position.append(np.nan)
                item_theta.append(np.nan)

        if len(target) == 2:
            item_data_s = pd.Series(item_data)
            return item_data_s
        else:
            if target[2] == "position":
                item_position_s = pd.Series(item_position)
                return item_position_s
            if target[2] == "theta":
                item_theta_s = pd.Series(item_theta)
                return item_theta_s

    def load_log(self, file_list):
        # goal(goal pose), real(real goal pose), reached(robot reached pose), 
        # stopping(robot stopping pose), stopped(robot stopped pose)
        nav_test_results = [[], [], [], [], [], []]
        for file_name in file_list:
            print("Load log file: " + file_name)
            try:
                with open(file_name) as log_all:
                    # for now those log sentences should be written in specific order like this in the log
                    for line in log_all:
                        if "Received a new Docking task" in line:
                            self.docking = int(line.split("mode: ")[-1])
                            print(self.docking)
                        if "Received a new navigation task from" in line:
                            self.docking = -1
                        if self.docking != 5 and self.docking != 8 and self.docking != -1:
                            continue

                        if "[Mpc controller] Goal reached! Goal:" in line:
                            self.reached_flag = True  # start reached log capturing 
                            nav_test_results[0].append(self.get_pose(line))
                            nav_test_results[5].append(self.docking)

                        if self.reached_flag is False:
                            # Not really reached, ignore stopping infos 
                            continue

                        if "[Mpc controller] Real Goal pose:" in line:
                            nav_test_results[1].append(self.get_pose(line))
                            continue
                        if "[Mpc controller] Reached pose:" in line:
                            nav_test_results[2].append(self.get_pose(line))
                            continue
                        if "Stopping, Robot current pose:" in line:
                            nav_test_results[3].append(self.get_pose(line))
                            continue
                        if "Robot stopped in real. Robot current pose:" in line:
                            nav_test_results[4].append(self.get_pose(line))
                            self.reached_flag = False  # end reached log capturing 
                            continue

                        if (
                                "Received a new navigation task from" in line or "Received a new Docking task" in line) and self.reached_flag is True:
                            # if reached here, means robot reached goal, but no real stopped before new task
                            nav_test_results[4].append([np.nan, np.nan, np.nan])  # complete stopped part
                            self.reached_flag = False

                    if self.reached_flag is True:
                        # if reached here, means robot reached goal, but no real stopped until log finished
                        nav_test_results[4].append([np.nan, np.nan, np.nan])  # complete stopped part
                        self.reached_flag = False

            except Exception as e:
                print("[ERROR] Illege log file for this analyzer. Please check log file and exception message below.")
                print(e)
                exit()

        self.pd_nav_test_results = pd.DataFrame(nav_test_results).T
        self.pd_nav_test_results.columns = ["goal", "real", "reached", "stopping", "stopped", "docking"]

    def analyze_all(self):
        if self.pd_nav_test_results.empty:
            print("  - No navigation task finished in this log.")
            return

        for check in self.check_list:
            # self.pd_nav_test_results[check] = self.func_map[check](self.pd_nav_test_results)
            self.pd_nav_test_results[check] = self.check_two_pose(check, self.pd_nav_test_results)

        if self.brief:
            print(self.pd_nav_test_results[self.check_list[-1]])
        else:
            print(self.pd_nav_test_results)

    def print_all(self):
        print(self.pd_nav_test_results)

    def print_specific(self, item):
        if item == "":
            return True
        if item == "all":
            print(self.pd_nav_test_results)
            return False
        if item == "show_all":
            for check in self.check_list_position:
                self.add_plot(self.pd_nav_test_results[check])
            for check in self.check_list_theta:
                self.add_plot(self.pd_nav_test_results[check])
            self.show_plot("Navigation Diff", "Diff")
            return False
        if item == "show_all_position":
            for check in self.check_list_position:
                if check == "goal-stopped-position":
                    self.add_plot(self.pd_nav_test_results[check], 'o')
                else:
                    self.add_plot(self.pd_nav_test_results[check])
            self.show_plot("Navigation Position Diff", "Position Diff (m)")
            return False
        if item == "show_all_theta":
            for check in self.check_list_theta:
                if check == "goal-stopped-theta":
                    self.add_plot(self.pd_nav_test_results[check], 'o')
                else:
                    self.add_plot(self.pd_nav_test_results[check])
            self.show_plot("Navigation Theta Diff", "Theta Diff (rad)")
            return False

        if item == "show_docking_5_position":
            for check in self.check_list_position:
                self.add_plot(self.pd_nav_test_results[self.pd_nav_test_results["docking"] == 5][check])
            self.show_plot("Navigation Position Diff", "Position Diff (m)")
            # print self.pd_nav_test_results[self.pd_nav_test_results["docking"]==8]
            return False
        if item == "show_docking_8_position":
            for check in self.check_list_position:
                self.add_plot(self.pd_nav_test_results[self.pd_nav_test_results["docking"] == 8][check])
            self.show_plot("Navigation Position Diff", "Position Diff (m)")
            # print self.pd_nav_test_results[self.pd_nav_test_results["docking"]==8]
            return False

        if item == "show":
            self.show_plot("Navigation Diff", "Diff")
            return False
        if item == "save_all":
            self.save_all()
            return False

        try:
            print(self.pd_nav_test_results[item])
            # self.add_plot(self.pd_nav_test_results[item])
        except:
            print("[ERROR] Wrong check item. ")
        return False

    def add_plot(self, pd_s, marker_="*"):
        pd_s.plot(marker=marker_)

    def show_plot(self, title, ylable):
        plt.title(title)
        plt.xlabel("Navigations")
        plt.ylabel(ylable)
        plt.legend()
        plt.xticks(np.arange(0, len(self.pd_nav_test_results), 1))
        plt.yticks(np.arange(0.0, 0.1, 0.005))
        plt.grid()
        plt.show()

    def save_all(self):
        self.pd_nav_test_results.to_excel("/home/ld/Documents/nav_log_analyzed.xlsx")


if __name__ == '__main__':
    log_file = "/home/ld/.forwardx_log/forwardx_move_base/forwardx_move_base.log"
    pose_analyzer = NavPoseAnalyzer()
    pose_analyzer.load_log(log_file)
    pose_analyzer.analyze_all()

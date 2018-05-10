#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang


import jenkins
import JenkinsAPI

class JenAPI(object):
    def __init__(self):
        self.server = jenkins.Jenkins('http://10.100.47.80:8080/', username='admin', password='admin')

    def create_cicd_job(self, name, cmd):
        self.server.create_job(name, JenkinsAPI.SAMXML.format(shell_cmd=cmd))

    def rebuild_cicd_job(self, name, cmd):
        self.server.reconfig_job(name, JenkinsAPI.SAMXML.format(shell_cmd=cmd))

    def start_cicd_job(self,name):
        self.server.build_job(name)




# print(JenAPI().server.get_job_config("test03"))

# print(JenAPI().server.get_build_console_output("test03", 7))

# print(JenAPI().server.get_running_builds())  #[{'name': 'test03', 'number': 7, 'url': 'http://10.100.47.80:8080/job/test03/7/', 'node': '(master)', 'executor': 1}]

# print(JenAPI().server.get_build_info("test03", 8))
#
# print(JenAPI().server.get_job_info("test03"))

#
# for i in dir(JenAPI().server):
#     print(i)
# cmd = '''#!/bin/bash
# # author: Gao Shao Yang
# # date: 2018-5-8
#
# mkdir haha
# touch haha.txt'''
#
# api.create_cicd_job("hahahaha", cmd)


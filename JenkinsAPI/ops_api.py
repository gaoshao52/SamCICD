#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang


import jenkins
import JenkinsAPI

class JenAPI(object):
    def __init__(self):
        self.server = jenkins.Jenkins('http://127.0.0.1:8080/', username='admin', password='admin')

    def create_cicd_job(self, name, cmd, file=None):
        self.server.create_job(name, JenkinsAPI.SAMXML.format(shell_cmd=cmd, file=file))

    def rebuild_cicd_job(self, name, cmd, file=None):
        self.server.reconfig_job(name, JenkinsAPI.SAMXML.format(shell_cmd=cmd, file=file))

    def start_cicd_job(self,name):
        self.server.build_job(name)

    def get_last_build_info(self, name):

        tmp_info = self.server.get_job_info(name)
        if not tmp_info.get("lastBuild"):  # 空项目，没有build
            return {"last_build_number": -1,
                    "building_status": -1,
                    "build_result": -1,
                    "timestamp": -1,
                    "duration": -1,
                    "estimatedDuration": -1,

                    }
        last_number = tmp_info.get("lastBuild").get("number")

        build_info = self.server.get_build_info(name, last_number)


        return {"last_build_number": last_number,
                "building_status": build_info.get("building"),
                "build_result": build_info.get("result"),
                "timestamp": build_info.get("timestamp"),
                "duration": build_info.get("duration"),
                "estimatedDuration": build_info.get("estimatedDuration"),

                }

    def get_last_build_log(self, name):
        tmp_info = self.server.get_job_info(name)
        if not tmp_info.get("lastBuild"):
            return []

        last_number = tmp_info.get("lastBuild").get("number")

        return self.server.get_build_console_output(name, last_number).split("\n")




if __name__ == '__main__':
    # print(JenAPI().server.get_job_config("aaa"))
    print(JenAPI().server.get_job_config("sds_build01"))
    # log_str = JenAPI().server.get_build_console_output("sds_build01", 28)
    # print(log_str)

    # print(JenAPI().server.get_running_builds())  #[{'name': 'test03', 'number': 7, 'url': 'http://10.100.47.80:8080/job/test03/7/', 'node': '(master)', 'executor': 1}]

    # print(JenAPI().server.get_build_info("test03", 8))
    # objs = JenAPI().server.get_build_info("test03", 9)
    #
    # print(JenAPI().server.get_job_info("test03"))
    # objs = JenAPI().server.get_job_info("test_empty")
    # for k,v in objs.items():
    #     print(k, ":", v)


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


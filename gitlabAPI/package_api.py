#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang


import requests
# from common.utils import ServerError

# BASE_URL = "http://10.100.218.203"
# PERSON_TOKEN = "j57ypsUJHsvuAeFkM7pW"

# PERSON_TOKEN = "j57ypsUJHsvuAeFkMuuuiW"

class GitLabAPI(object):
    def __init__(self, BASE_URL, headers=None, *args, **kwargs):
        self.BASE_URL = BASE_URL
        self.headers = headers

    def get_user_id(self, username):
        user_id = None
        res = requests.get("%(BASE_URL)s/api/v4/users?username=%(username)s"%({
                                                                            "BASE_URL": self.BASE_URL,
                                                                            "username": username,
                                                                        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise Exception("....")
        content = res.json()
        if content:
            user_id = content[0].get('id')
        return user_id

    def get_user_projects(self):
        res = requests.get("%(BASE_URL)s/api/v4/projects"%({
                                                            'BASE_URL': self.BASE_URL,
                                                        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise ValueError("连接失败")
        content = res.json()
        return content

    def get_user_projects_by_id(self, id):
        res = requests.get("%(BASE_URL)s/api/v4/projects/%(id)s/"%({
                                                            'BASE_URL': self.BASE_URL,
                                                            'id': id,
                                                        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise ValueError("连接失败")
        content = res.json()
        return content

    # def get_user_projects_member_by_id(self, id):
    #     res = requests.get("%(BASE_URL)s/api/v4/projects/%(id)s/members"%({
    #                                                         'BASE_URL': self.BASE_URL,
    #                                                         'id': id,
    #                                                     }), headers=self.headers, verify=False)
    #     status_code = res.status_code
    #     if status_code != 200:
    #         # raise ServerError(res.get('message'))
    #         raise ValueError("连接失败")
    #     content = res.json()
    #     return content


    def get_user_groups(self):
        res = requests.get("%(BASE_URL)s/api/v4/groups" % ({
            'BASE_URL': self.BASE_URL,
        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise ValueError(".......")
        content = res.json()
        groups_list = []
        for item in content:
            groups_list.append(item.get('name'))

        return groups_list

    def get_project_by_group(self, name):
        res = requests.get("%(BASE_URL)s/api/v4/groups/%(name)s" % ({
            'BASE_URL': self.BASE_URL,
            'name': name,
        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise ValueError(".....")
        content = res.json()
        return content



    def get_user_project_id(self, name):
        """
        :param name: 项目名称
        :return:
        """
        project_id = None
        projects = self.get_user_projects()
        if projects:
            for item in projects:
                if item.get('name') == name:
                    project_id = item.get('id')
        return project_id



    def get_project_branchs(self, project_id):
        branchs = []
        res = requests.get("%(BASE_URL)s/api/v4/projects/%(project_id)s/repository/branches"%({
                                                                            "BASE_URL": self.BASE_URL,
                                                                            "project_id": project_id,
                                                                        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise Exception("....")
        content = res.json()
        if content:
            for item in content:
                branchs.append(item.get('name'))
        return branchs

    def get_project_tags(self, project_id):
        tags = []
        res = requests.get("%(BASE_URL)s/api/v4/projects/%(project_id)s/repository/tags"%({
                                                                            "BASE_URL": self.BASE_URL,
                                                                            "project_id": project_id,
                                                                        }), headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            # raise ServerError(res.get('message'))
            raise Exception("....")
        content = res.json()
        if content:
            for item in content:
                tag_name = item.get('name')
                commit = item.get('commit')
                info = ''
                if commit:
                    commit_id = commit.get('id')
                    commit_info = commit.get('message')
                    info = "%s * %s"%(commit_id[:9], commit_info)
                tags.append("%s     %s"%(tag_name, info))
        return tags


if __name__ == "__main__":
    BASE_URL = "http://10.100.218.203"
    # BASE_URL = "https://git.tclab.lenovo.com"
    PERSON_TOKEN = "j57ypsUJHsvuAeFkM7pW"
    # PERSON_TOKEN = "KWzYGxDuxsqYjGMSCjER"
    headers = {'PRIVATE-TOKEN': PERSON_TOKEN} #你的gitlab账户的private token
    api = GitLabAPI(BASE_URL, headers=headers)
    # content = api.get_user_projects()
    #
    #
    #
    #
    # for index,item in enumerate(content):
    #     print("第%s："%index)
    #     for k, v in item.items():
    #         print(k, ":", v)

    print(api.get_user_projects_by_id(51))


    # print(pid)

    # content = api.get_project_by_group("nfv")

    # print(content)
    # for index,item in enumerate(content):
    #     print("第%s："%index)
    #     for k, v in item.items():
    #         print(k, ":", v)



    # print(content)
    #
    # user_id = api.get_user_id('liming')
    # print("user_id:", user_id)

    # project_id = api.get_user_project_id('building')
    # print("project:", project_id)

    # branchs = api.get_project_branchs('86')
    # print("project branchs:", branchs)
    #
    # tags = api.get_project_tags('345')
    # print("project tags:", tags)
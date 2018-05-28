#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang

from django.forms import Form, fields, widgets
from cicd import models


class AddGitForm(Form):
    title = fields.CharField(
        label="标题",
        widget = widgets.TextInput(attrs={"id": "person_title", "class": "form-control"}),
        error_messages={"required": "标题不能为空"},
    )
    url = fields.URLField(
        label="根URL",
        widget=widgets.URLInput(attrs={"id": "gitlab_url", "class": "form-control"}),
        error_messages={"required": "URL不能为空"},
    )
    person_token = fields.CharField(
        label="个人访问令牌",
        widget=widgets.TextInput(attrs={"id": "person_token", "class": "form-control"}),
        error_messages={"required": "个人访问令牌不能为空"},
    )
    myuser_id = fields.IntegerField(
        widget=widgets.HiddenInput,
    )

class BuildToolForm(Form):
    name = fields.CharField(
        label="项目名称",
        widget = widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={"required": "项目名称不能为空"},
    )
    shell_code = fields.CharField(
        label = "Execute shell",
        widget=widgets.Textarea(attrs={"class": "form-control"}),
    )
    codeserver_id = fields.ChoiceField(
        label = "GitLab服务器",
        choices = [],
        widget = widgets.Select(attrs={"class": "form-control"}),
    )

    # email = fields.EmailField(
    #     label = "邮件通知",
    #     widget = widgets.EmailInput(attrs={"class": "form-control"}),
    # )
    artifact = fields.CharField(
        label="存储文件",
        widget=widgets.TextInput(attrs={"class": "form-control"}),
    )


    def __init__(self, request, *args, **kwargs):
        super(BuildToolForm, self).__init__(*args, **kwargs)
        print("init build,,,,", request.user.id)
        objs = models.CodeServer.objects.filter(myuser_id=request.user.id).values_list("id", "title")

        print("objs----->", objs)
        self.fields["codeserver_id"].choices = objs






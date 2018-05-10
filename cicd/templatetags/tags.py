#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang

from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from gitlabAPI.package_api import GitLabAPI


register = template.Library()

@register.simple_tag
def get_user_id(request):
    '''获取用户id'''
    return request.user.id

@register.simple_tag
def display_gitlab_in_table(objs):
    '''生成gitlab连接表格'''
    if objs:
        title_name = objs.last()._meta.get_field('title').verbose_name
        url_name = objs.last()._meta.get_field('url').verbose_name
        token_name = objs.last()._meta.get_field('person_token').verbose_name



        table_ele = '''<tr><th>序号</th><th>%s</th><th>%s</th><th>%s</th><th>ACTION</th></tr>'''%(title_name, url_name, token_name)

        for index, obj in enumerate(objs):
            # delete_url = reverse("cicd_tools_delete", args=((obj.id,)))
            ele = '''<tr><td>%s</td><td target='title'>%s</td><td>%s</td><td>%s</td><td><button obj_id='%s' type="button" onclick="preConfirm(this);" class="btn btn-danger btn-xs" data-toggle="modal" data-target="#myModal">
      删除
    </button></td></tr>'''%(index+1, obj.title, obj.url, obj.person_token, obj.id)
            table_ele += ele

        return mark_safe(table_ele)

    return ""

@register.simple_tag
def display_build_in_table(objs):
    '''生成build连接表格'''

    print("tags build objs--->", objs)
    if objs:
        title_name = objs[0]._meta.get_field('name').verbose_name
        git_name = objs[0].codeserver._meta.verbose_name


        # <button type="button" class="btn btn-info btn-xs">查看</button>
        table_ele = '''<tr><th>序号</th><th>%s</th><th>%s</th><th style="width:187px;text-align:  center;">ACTION</th>'''%(title_name, git_name)

        for index, build_obj in enumerate(objs):
            # delete_url = reverse("cicd_tools_delete", args=((obj.id,)))
            url_path = reverse("code_configure", args=((build_obj.id,)))
            build_job_change = reverse("cicd_tools_build_change", args=((build_obj.id,)))
            build_job_look = reverse("cicd_tools_build_look", args=((build_obj.id,)))

            ele = '''<tr build_id="%s"><td>%s</td><td><a href="%s">%s</a></td><td><a href="%s">%s<a></td>
            <td style="text-align:  center;"><a href="%s" class="btn btn-info btn-xs">查看</a>
            <button type="button" onclick="triggerJob(this);" class="btn btn-success btn-xs">触发</button>
            <button type="button" class="btn btn-danger btn-xs">删除</button></td>
            </tr>'''%(build_obj.id, index+1, build_job_change,build_obj.name, url_path,build_obj.codeserver.title, build_job_look)
            table_ele += ele

        return mark_safe(table_ele)

    return ""


@register.simple_tag
def display_repo_in_table(project_objs, base_url, person_token):
    headers = {'PRIVATE-TOKEN': person_token}
    api = GitLabAPI(base_url, headers=headers)
    ele = '''<tr><td><input name="selected_item" type="checkbox"></td><td>{index}</td><td>{name}</td><td name="branch">{branch}</td>
    <td>{create_time}</td><td>{ssh}</td><td name="http_repo" style="display: none">{http}</td><td>{manifest}</td></tr>'''
    ele_list = []

    for index, item in enumerate(project_objs):
        branch_list = api.get_project_branchs(item.get('id'))
        default_branch = item.get("default_branch")
        branch_ele = '''<select class="form-control">'''
        for b_item in branch_list:
            if b_item == default_branch:
                sub_ele = '''<option name="%s" selected>%s</option>''' % (b_item, b_item)
            else:
                sub_ele = '''<option name="%s">%s</option>'''%(b_item, b_item)
            branch_ele += sub_ele
        branch_ele += "</select>"

        if_manifest_addr = item.get('ssh_url_to_repo').split("/")[-1]
        # print("manifest_addr:", manifest_addr)
        if if_manifest_addr == "manifests.git" or if_manifest_addr == "manifest.git":
            print("manifest--------->",item.get("id"))
            http_url  = item.get('http_url_to_repo')
            git_url = http_url.split("://")
            clone_url = git_url[0] + "://private_token:" + person_token + "@" + git_url[1]
            import os
            from SamCICD.settings import MANIFEST_DIR

            os.popen("git clone {url} {dir}".format(url=clone_url, dir=MANIFEST_DIR)).read()

            xml_list = os.listdir(MANIFEST_DIR)
            new_xml_list = []
            for aitem in xml_list:
                if aitem.endswith(".xml"):
                    new_xml_list.append(aitem)

            man_ele = '''<select id="samtest" class="form-control">'''
            for xml_index, xml_item in enumerate(new_xml_list):
                if xml_index == 0:
                    xml_sub_ele = '''<option name="%s" selected>%s</option>''' % (xml_item, xml_item)
                else:
                    xml_sub_ele = '''<option name="%s">%s</option>''' % (xml_item, xml_item)
                man_ele += xml_sub_ele
            man_ele += "</select>"
        else:
            man_ele = ""




        ele_list.append(ele.format(index=(index+1),
                                   name=item.get('name'),
                                   branch=branch_ele,
                                   create_time=item.get('created_at').split(".")[0],
                                   ssh=item.get('ssh_url_to_repo'),
                                   http=item.get('http_url_to_repo'),
                                   manifest = man_ele,
                                   ))

    return mark_safe("".join(ele_list))

@register.simple_tag
def display_code_project_in_look_table(build_branch_objs):

    ele_list = []
    for index, obj in enumerate(build_branch_objs):
        ele = "<tr><td>{index}</td><td>{name}</td><td>{branch}</td></tr>"
        name = obj.group + "/" + obj.git_repo.split("/%s/"%(obj.group))[1].rstrip(".git")
        ele_list.append(ele.format(index=index+1, name=name, branch=obj.branch))

    return mark_safe("".join(ele_list))




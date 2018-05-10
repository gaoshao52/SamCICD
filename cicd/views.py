from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from cicd import forms
from cicd import models
from gitlabAPI.package_api import GitLabAPI
from django.db.utils import IntegrityError
import json
from JenkinsAPI.ops_api import JenAPI
from django.core.cache import cache

# Create your views here.


@login_required
def index(request):

    git_objs = models.CodeServer.objects.filter(myuser_id=request.user.id)

    build_objs = models.BuildTools.objects.filter(myuser_id=request.user.id)
    # print("user_id,,,", request.user.id)
    # print("build_objs,,", build_objs)

    return render(request, "index.html", {"git_objs": git_objs,
                                          "build_objs": build_objs})

@login_required
def tools(request):
    a = []
    for i in range(2):
        a.append(i)

    return render(request, "tools.html", {"a": a})

@login_required
def tools_create(request):
    '''集成gitlab'''
    info = {}
    obj = forms.AddGitForm(initial={"myuser_id": request.user.id})

    if request.method == "POST":
        obj = forms.AddGitForm(request.POST)

        if obj.is_valid():
            data = obj.cleaned_data
            data["myuser_id"] = request.user.id

            # 连接gitlab
            BASE_URL = data['url']
            PERSON_TOKEN = data['person_token']
            headers = {'PRIVATE-TOKEN': PERSON_TOKEN}
            api = GitLabAPI(BASE_URL, headers=headers)

            try:
                content = api.get_user_projects()

                print(content)
                models.CodeServer.objects.create(**data)
                info['msg'] = "连接成功"
                info['color'] = "green"
            except IntegrityError as e:
                info['msg'] = "个人访问令牌已经存在"
                info['color'] = "green"

            except Exception as e:
                print(e)
                info['msg'] = "连接失败"
                info['color'] = "red"

        else:
            pass


    return render(request, "tools_code_server_create.html", {"obj": obj, "info": info})

@login_required
def tools_delete(request):

    info = {"status": False, "msg": ""}

    if request.method == "POST":

        obj_id = request.POST.get("obj_id")
        print("obj_id", obj_id)
        try:
            # raise ValueError("hhhhhh")
            models.CodeServer.objects.filter(id=obj_id).delete()
            info['status'] = True
        except Exception as e:
            return HttpResponse(json.dumps(info))

        return HttpResponse(json.dumps(info))


@login_required
def cicd_tools_build_create(request):
    info = {'info': ''}
    buildtool_form = forms.BuildToolForm(request)
    if request.method == "POST":
        buildtool_form = forms.BuildToolForm(request, request.POST)
        if buildtool_form.is_valid():
            data = buildtool_form.cleaned_data
            data['myuser_id'] = request.user.id
            print("cleaned_data", data)

            try:
                objs = models.BuildTools.objects.create(**data)  #  插入数据库
                JenAPI().create_cicd_job(data.get("name"), data.get('shell_code'))  # jenkins里创建工程

                return redirect(reverse("cicd_index"))

            except IntegrityError as e:
                print(e)
                info['info'] = "项目<%s>已存在"%buildtool_form.cleaned_data['name']




    return render(request, "tools_build_create.html", {"buildtool_form": buildtool_form,
                                                       "info": info},)

@login_required
def cicd_tools_build_change(request, build_id):
    info = {'info': ''}
    buildtool_obj = models.BuildTools.objects.get(id=build_id)

    if request.method == "POST":
        buildtool_form = forms.BuildToolForm(request, request.POST)
        if buildtool_form.is_valid():
            data = buildtool_form.cleaned_data

            if str(buildtool_obj.codeserver_id) != str(data.get("codeserver_id")): # 如果改变gitlab服务器，则删除该工程所有已选的代码工程
                models.BuildProjectAndBranch.objects.filter(buildtool_id=build_id, myuser_id=request.user.id).delete()

            try:
                models.BuildTools.objects.filter(id=build_id).update(**data)
                if buildtool_obj.name != data['name']:
                    JenAPI().server.rename_job(buildtool_obj.name, data['name'])
                JenAPI().rebuild_cicd_job(data['name'], data["shell_code"])
                return redirect(reverse("cicd_index"))
            except IntegrityError as e:
                print(e)
                info['info'] = "项目<%s>已存在"%buildtool_form.cleaned_data['name']


    else:
        buildtool_form = forms.BuildToolForm(request, initial={
            "name": buildtool_obj.name,
            "shell_code": buildtool_obj.shell_code,
            "codeserver_id": buildtool_obj.codeserver_id,
            "email": buildtool_obj.email
        })

    return render(request, "tools_build_change.html", {"buildtool_form": buildtool_form,
                                                       "info": info}, )



@login_required
def code_configure(request, build_id):
    buidtool_obj = models.BuildTools.objects.get(id=build_id)

    base_url = buidtool_obj.codeserver.url
    person_token = buidtool_obj.codeserver.person_token
    headers = {'PRIVATE-TOKEN': person_token}
    api = GitLabAPI(base_url, headers=headers)



    group_objs = api.get_user_groups()

    if group_objs:

        selected_group = request.GET.get("group", "")
        if selected_group in group_objs:
            project_objs = api.get_project_by_group(selected_group).get("projects")
        else:
            project_objs = api.get_project_by_group(group_objs[0]).get("projects")


        return render(request, "code_configure.html", {"project_objs": project_objs,
                                                       "group_objs": group_objs,
                                                       "selected_group": selected_group,
                                                       "base_url": base_url,
                                                        "person_token": person_token,
                                                       "build_id": build_id,
                                                       })
    else:
        return HttpResponse("没有groups")

@login_required
def save_repo(request):

    group = request.environ.get("HTTP_GROUP")
    print(group)

    build_id = request.environ.get("HTTP_BUILDID")

    print(build_id)


    info = {"status": False}

    if request.method == "POST":
        # delete data by group
        models.BuildProjectAndBranch.objects.filter(group=group).delete()

        print(request.POST)

        repo_objs = []
        for k,v in request.POST.items():
            repo_objs.append(models.BuildProjectAndBranch(
                git_repo = k,
                branch = v,
                group = group,
                buildtool_id = int(build_id),
                myuser_id = request.user.id
            ))

        models.BuildProjectAndBranch.objects.bulk_create(repo_objs)

        info['status'] = True

        # insert into db
        models.BuildProjectAndBranch.objects.filter()

    return HttpResponse(json.dumps(info))



def trigger_job(request):
    info = {"status": False}
    if request.method == "POST":
        build_id = request.POST.get("build_id")

        buidtool_obj = models.BuildTools.objects.get(id=build_id)

        person_token = buidtool_obj.codeserver.person_token
        build_name = buidtool_obj.name

        # from db
        code_project_objs = models.BuildProjectAndBranch.objects.filter(
            buildtool_id=build_id,
            myuser_id=request.user.id
        ).values_list("git_repo","branch")
        # print(code_project_objs)

        clone_list = ["export GIT_SSL_NO_VERIFY=1"]

        # handle db data
        for obj in code_project_objs:
            git_url = obj[0].split("://")
            clone_url = git_url[0] + "://private_token:"+person_token+"@"+git_url[1]

            if obj[1].endswith(".xml"):
                clone_list.append("~/bin/repo init -u {url} -m {man_xml}".format(url=clone_url, man_xml=obj[1].split(":")[1]))
                clone_list.append("~/bin/repo sync")
            else:
                clone_list.append("git clone -b {branch} {url}".format(branch=obj[1], url=clone_url))
        # print(clone_list)

        print("\n".join(clone_list) +"\n"+ buidtool_obj.shell_code)
        new_cmd = "\n".join(clone_list) +"\n"+ buidtool_obj.shell_code
        japi = JenAPI()
        japi.rebuild_cicd_job(build_name, new_cmd)
        japi.start_cicd_job(build_name)
        info['status'] = True

    return HttpResponse(json.dumps(info))




def cicd_tools_build_look(request, build_id):
    build_branch_objs = models.BuildProjectAndBranch.objects.filter(buildtool_id=build_id, myuser_id=request.user.id)

    return render(request, "tools_build_look.html", {'build_branch_objs': build_branch_objs})






def acc_login(request):
    '''登录'''
    errors = {}
    if request.method == "POST":
        _username = request.POST.get("email")
        _password = request.POST.get("password")

        user = authenticate(request, username=_username, password=_password)
        if user:  # 验证通过
            login(request, user)
            next_url = request.GET.get('next', reverse("cicd_index"))

            return redirect(next_url)

        else:
            errors['error'] = "错误的用户名或密码"

    return render(request, "login.html", {"errors": errors})


def acc_logout(request):
    '''注销'''
    logout(request)
    return redirect(reverse("acc_login"))


from django.contrib import admin
from django.urls import path, re_path, include
from cicd import views

urlpatterns = [
    re_path(r'^index/$', views.index, name="cicd_index"),
    re_path(r'^tools/$', views.tools, name="cicd_tools"),
    re_path(r'^tools/create_gitlab/$', views.tools_create, name="cicd_tools_create"),
    re_path(r'^tools/delete_gitlab/$', views.tools_delete, name="cicd_tools_delete"),
    re_path(r'^tools/create_build/$', views.cicd_tools_build_create, name="cicd_tools_build_create"),
    re_path(r'^build/change-(\d+)/$', views.cicd_tools_build_change, name="cicd_tools_build_change"),
    re_path(r'^build/code_configure-(\d+)/$', views.code_configure, name="code_configure"),
    re_path(r'^build/save_repo/$', views.save_repo, name="save_repo"),
    re_path(r'^build/trigger_job/$', views.trigger_job, name="trigger_job"),
    re_path(r'^build/look-(\d+)/$', views.cicd_tools_build_look, name="cicd_tools_build_look"),
]





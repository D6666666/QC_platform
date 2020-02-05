#!/usr/bin/env python 
# coding:utf-8 
#author:cq

from django.urls import path
from project_app import views

urlpatterns = [
    path('project_manage/', views.project_manage),
    path('add_project/', views.add_project),
    path('edit_project/<int:pid>/', views.edit_project),
    path('delete_project/<int:pid>/', views.delete_project),
]
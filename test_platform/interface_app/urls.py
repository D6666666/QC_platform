#!/usr/bin/env python 
# coding:utf-8 
#author:cq
from django.contrib import admin
from django.urls import path,include
from interface_app import views

urlpatterns = [
    path('case_manage/', views.case_manage),
    path('debug_case/', views.debug_case),
    path('add_case/', views.add_case),
    path('save_case/', views.save_case),
    path('update_case/', views.update_case),
    path('get_project_list/', views.get_project_list),
    path('search_case_name/', views.search_case_name),
    path('edit_case/<int:cid>/', views.edit_case),
    path('delete_case/<int:cid>/', views.delete_case),
    path('get_case_info/', views.get_case_info),
    path('api_assert/', views.api_assert),
]
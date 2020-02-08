#!/usr/bin/env python 
# coding:utf-8 
#author:cq
from django.contrib import admin
from django.urls import path,include
from interface_app import views

urlpatterns = [
    path('case_manage/', views.case_manage),
    path('api_debug/', views.api_debug),
    path('debug/', views.debug),
]
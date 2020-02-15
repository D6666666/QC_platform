#!/usr/bin/env python 
# coding:utf-8 
#author:cq

from django import forms
from interface_app.models import TestCase
from project_app.models import Project

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['module']
        # exclude = ['create_time']
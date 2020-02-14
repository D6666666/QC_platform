#!/usr/bin/env python 
# coding:utf-8 
#author:cq

from django import forms
from interface_app.models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['module']
        # exclude = ['create_time']
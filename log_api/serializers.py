# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 21:02:39 2020

@author: User
"""
from rest_framework import serializers
from .models import Logger

class LoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logger
        fields = ['date', 'date_range', 'info']
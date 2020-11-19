# -*- coding: utf-8 -*-

from django.urls import path
from log_api.views import LoggerAPIView, LoggerDateDetails, LoggerDateRangeDetails

urlpatterns = [
    path(r'api/', LoggerAPIView.as_view()),
    path('api/<str:date>/', LoggerDateDetails.as_view()),
    path(r'api/<str:date>/<str:date_range>/', LoggerDateRangeDetails.as_view()),
]
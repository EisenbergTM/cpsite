"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from cpsite.views import *

urlpatterns = [
    path('login/',login),
    path('index/',siteChannelList, name='site_channel_list'),
    path('index/do_line_option/',online_operator,name='online_operator'),
    path('add_config',add_config),
    path('config_format',xpath),
    path('config_opt',config_opt,name='config_opt'),
    path('test_opt',test_opt,name='test_opt'),
    path('id_delete',id_delete,name='id_delete'),
    url(r'^test_opt/detail_id/(.+)$',query_detail_byid),
    url(r'chart/(.+)',chart),
    path('index_weixin',index_weixin,name='weixin_app'),
    path('index_weixin/do_inline_option_app',online_operator_app,name='online_operator_app'),
    path('index_majiahao',majiahao,name='majiahao'),
    path('logout/',logout)
]

#!/usr/bin/env python3.8
# @Time:2022/5/4
# @Author:CarryLee
# @File:views.py
import sys
import os
from . import database
from django import forms
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import auth
# 导入上级模块
sys.path.append('..')
import draw_pyecharts_data as draw_data
import draw_pyecharts_standard as draw_standard
from header import get_dataset
from dataModel.models import *
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def get_original_data():
    return get_dataset('./../data/example.xlsx')


# 变量名语法:
# views:{"HTML变量名" : "views变量名"} 或 {"HTML变量名" : ["view变量名1","view变量名2"]}
# HTML:{{变量名}} 或 {{变量名.0}}{{变量名.1}}
# HTML过滤器:{{变量名|过滤器}},过滤器可选:lower、upper、first、truncatewords:"数字"、date、length、filesizeformat、safe
# HTML if/else:{% if condition1 %}
#                   ...
#              {% elif condition2 %}
#                   ...
#              {% else %}
#                   ...
#              {% endif %}
#    判断使用and、or、not
# HTML for:{% for item in item_list (reversed)%}
#               ...
#          {% empty %}(可选，在循环为空时执行)
#               ...
#          {% endfor %}
#    自带{{ forloop.counter }}、{{ forloop.counter0 }}、
#       {{ forloop.revcounter }}、{{ forloop.revcounter0 }}、
#       {{ forloop.first }}、{{ forloop.last }}
# HTML include:{% include “xxx.html” %}

class FUser(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=60)
    password = forms.CharField(max_length=20)


# 白洋淀卫星云图页面
def earthMap(request):
    article = Article.objects.all()
    user = request.session.get('user', False)
    context = {'title': '白洋淀生态监测数据关联分析可视化系统',
               'article1': article[0].context,
               'user': user,
               }
    return render(request, 'other/earthMap.html', context)


# 白洋淀未来生态发展建议页面
def suggestion(request):
    article = Article.objects.all()
    user = request.session.get('user', False)
    context = {'title': '白洋淀生态监测数据关联分析可视化系统',
               'article1': article[0].context,
               'user': user,
               }
    return render(request, 'other/suggestion.html', context)


# 首页页面
def index(request):
    article = Article.objects.all()
    user = request.session.get('user', False)
    context = {'title': '白洋淀生态监测数据关联分析可视化系统', 'user': user}
    for i in range(0, 12):
        name = 'article' + str(i + 1)
        context[name] = article[i].context
    return render(request, 'index.html', context)


def registerView(request):
    user = request.session.get("user", False)
    print(user)
    if not user:
        return render(request, 'login.html')
    else:
        return HttpResponseRedirect('index')


def register(request):
    check = False
    if request.method == "POST":
        form = FUser(request.POST)
        if form.is_valid():
            user = User(**form.cleaned_data)
            user.save()
            check = True
            return render(request, "immediate.html", {'check': check})
    return HttpResponseRedirect('index')


def login(request):
    user = request.POST['username']
    password = request.POST['password']
    try:
        result = User.objects.get(username=user, password=password)
        request.session['user'] = user
        return HttpResponseRedirect('index')
    except:
        return HttpResponse("登录失败!请<a href='index'>重试</a>")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('index')


# 相关概念页面
def concept(request):
    article = Article.objects.all()
    original_data = OriginalData.objects.all()
    user = request.session.get('user', False)
    context = {'title': '白洋淀生态监测数据关联分析可视化系统',
               'article1': article[0].context,
               'original_data': original_data.values_list(),
               'user': user,
               }
    for i in range(12, 64):
        name = 'article' + str(i + 1)
        context[name] = article[i].context
    return render(request, 'concept/index.html', context)


# 监测数据关联分析页面
def data(request):
    user = request.session.get('user', False)
    # 处理上传的文件
    if request.method == "POST":
        file_data = request.FILES.get("file", None)
        min_support = request.POST["min_support"]
        algorithm = request.POST["algorithm"]
        file_path = os.path.join(BASE_DIR, 'statics\\upload', file_data.name)
        output_path = os.path.join(BASE_DIR, 'templates\\resources\\')
        destination = open(file_path, 'wb+')
        for chunk in file_data.chunks():
            destination.write(chunk)
        destination.close()
        # 更新数据库中的频繁项集和关联规则
        database.upload_data(file_path, float(min_support), 1, algorithm)
        database.upload_data(file_path, float(min_support), 2, algorithm)
        draw_data.draw_bars_of_frequent_itemsets(file_path, output_path, float(min_support))
        draw_data.draw_graph_of_data_rules(file_path, output_path, float(min_support))
        draw_data.draw_parallel_of_data_rules(file_path, output_path, float(min_support))
        draw_data.draw_graph_of_data_itemsets(file_path, output_path, float(min_support))
    # 从数据库获取信息
    article = Article.objects.all()
    frequent_itemsets = FrequentItemsetsWithData.objects.all()
    association_rules = AssociationRulesWithData.objects.all()
    context = {'title': '白洋淀生态监测数据关联分析可视化系统',
               'article1': article[0].context,
               'frequent_itemsets': frequent_itemsets.values_list(),
               'association_rules': association_rules.values_list(),
               'user': user,
               }
    return render(request, 'data/index.html', context)


# 水质标准关联分析页面
def standard(request):
    user = request.session.get('user', False)
    # 处理上传的文件
    if request.method == "POST":
        file_data = request.FILES.get("file", None)
        min_support = request.POST["min_support"]
        algorithm = request.POST["algorithm"]
        file_path = os.path.join(BASE_DIR, 'statics\\upload', file_data.name)
        output_path = os.path.join(BASE_DIR, 'templates\\resources\\')
        destination = open(file_path, 'wb+')
        for chunk in file_data.chunks():
            destination.write(chunk)
        destination.close()
        # 更新数据库中的频繁项集和关联规则
        database.upload_data(file_path, float(min_support), 3, algorithm)
        database.upload_data(file_path, float(min_support), 4, algorithm)
        draw_standard.draw_pie_of_standard(file_path, output_path)
        draw_standard.draw_bars_of_frequent_itemsets(file_path, output_path, float(min_support))
        draw_standard.draw_graph_of_standard_itemsets(file_path, output_path, float(min_support))
        draw_standard.draw_parallel_of_standard_rules(file_path, output_path, float(min_support))
        draw_standard.draw_bar3D_of_standard_rules(file_path, output_path, float(min_support))
    # 从数据库获取信息
    article = Article.objects.all()
    frequent_itemsets = FrequentItemsetsWithStandard.objects.all()
    association_rules = AssociationRulesWithStandard.objects.all()
    context = {'title': '白洋淀生态监测数据关联分析可视化系统',
               'article1': article[0].context,
               'frequent_itemsets': frequent_itemsets.values_list(),
               'association_rules': association_rules.values_list(),
               'user': user,
               }
    return render(request, 'standard/index.html', context)

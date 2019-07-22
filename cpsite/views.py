# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from cpsite.forms import UserForm
from cpsite.operators.SiteChannelOperate import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import time
import json
import datetime
import logging


logger = logging.getLogger('django')

def login(req):
    #登录验证
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if req.method == 'GET':
        uf = UserForm(req.GET)
        print(uf)
        # return render(req, 'login.html', {'uf': uf,'nowtime': nowtime ,'password_is_wrong':False})
        return render(req, 'login.html', {'error_msg':'','uf': uf, 'nowtime': nowtime})
    else:
        print(req.method)
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = req.POST.get('username')
            password = req.POST.get('password')
            print('username: '+username + '; password: ' + password)
            user =  auth.authenticate(username=username,password=password)
            # if username == 'crawl' and password == 'crawl1234':
            print(user)
            if user is not None: #判断用户名密码是否正确
                if user.is_active:
                    print('通过认证')
                    auth.login(req, user)
                return redirect('/index')
            else:
                return render(req, 'login.html', {'error_msg':'用户名或密码错误','uf':uf,'nowtime': nowtime})
        else:
            return render(req, 'login.html', {'error_msg':'','uf': uf,'nowtime': nowtime })

@login_required(login_url='/login/')
def siteChannelList(request):
    if request.method == 'POST':
        print(request.body)
        pageSize = request.POST.get('pageSize')
        pageNumber = request.POST.get('pageNumber')
        siteName = request.POST.get('siteName')
        channel = request.POST.get('channel')
        test_status = request.POST.get('test_status')
        have_stop  = request.POST.get('have_stop')
        print(test_status,have_stop)
        op = SiteChannelOperate()
        return HttpResponse(op.query(siteName, channel, pageNumber, pageSize,test_status,have_stop))
    else:
        return render(request, 'index.html')

@login_required(login_url='/login/')
def online_operator(request):
    if request.method == 'GET':
        operate = request.GET.get('operate')
        siteName = request.GET.get('site_name')
        channel = request.GET.get('channel')
        url = request.GET.get('url')
        op = SiteChannelOperate()
        return HttpResponse(op.online_operator(operate,siteName,channel,url))

@login_required(login_url='/login/')
def online_operator_app(request):
    if request.method == 'GET':
        opt = request.GET.get('opt')
        app_name = request.GET.get('app_name')
        channel = request.GET.get('channel')
        op = SiteChannelOperate()
        return HttpResponse(op.online_operator_app(opt,app_name,channel))

@login_required(login_url='/login/')
def add_config(request):
    if request.method == 'GET':
       return render(request,'add_config.html')

@login_required(login_url='/login/')
def config_opt(request):
    if request.method == 'GET':
        return render(request,'config_opt.html')
    if request.method == 'POST':
        opt_name  = request.POST.get('opt_name')
        site_name = request.POST.get('site_name')
        channel   = request.POST.get('channel')
        print(opt_name,site_name,channel)
        if opt_name == '预览':
            oprt = SiteChannelOperate()
            data = oprt.update_config(opt_name,site_name,channel)
            return render(request,'config_opt.html',{'config':data,'site_name':site_name,'channel':channel})

        if opt_name == '更新':
            oprt = SiteChannelOperate()
            data = oprt.update_config(opt_name,site_name,channel)
            if 'failed' in str(data):
                return render(request,'config_opt.html',{'config':data,'site_name':'','channel':''})
            else:
                i = json.loads(data)
                a = config()
                print(i['config_start_url']['urllist']['xpath'],type(i['config_start_url']['urllist']['xpath']))
                a.start_url           = i['config_start_url']['url']
                a.timestamp           = i['config_start_url']['timestamp']
                a.start_web_type      = i['config_start_url']['web_type']
                a.start_url_req_type  = i['config_start_url']['request_type']
                a.start_headers       = i['config_start_url']['headers']
                a.urllist_re          = i['config_start_url']['urllist']['re']
                a.urllist_add         = i['config_start_url']['urllist']['add_str']
                a.urllist_xpath.extend(i['config_start_url']['urllist']['xpath'])
                a.urllist_reduce.extend(i['config_start_url']['urllist']['reduce_str'])
                a.imglist_xpath.extend(i['config_start_url']['imglist']['xpath'])
                a.imglist_url_add     = i['config_start_url']['imglist']['url_add_str']
                a.imglist_url_reduce.extend(i['config_start_url']['imglist']['url_reduce_str'])
                a.imglist_img_add     = i['config_start_url']['imglist']['img_add_str']
                a.imglist_img_reduce.extend(i['config_start_url']['imglist']['img_reduce_str'])
                a.img_sign            = i['config_start_url']['imglist']['img_sign']
                a.site_name           = i['config_detail_url']['site_name']
                a.channel             = i['config_detail_url']['channel']
                a.url_sign            = i['config_detail_url']['url_sign']
                a.detail_web_type     = i['config_detail_url']['web_type']
                a.detail_url_req_type = i['config_detail_url']['request_type']
                a.detail_url_headers  = i['config_detail_url']['headers']
                a.title_re            = i['config_detail_url']['title']['re']
                a.title_xpath.extend(i['config_detail_url']['title']['xpath'])
                a.title_add           = i['config_detail_url']['title']['add_str']
                a.title_reduce.extend(i['config_detail_url']['title']['reduce_str'])
                a.content_re          = i['config_detail_url']['content']['re']
                a.content_xpath.extend(i['config_detail_url']['content']['xpath'])
                a.reduce_node.extend(i['config_detail_url']['content']['reduce_node'])
                a.cont_reduce.extend(i['config_detail_url']['content']['reduce_str'])
                a.img_suffix          = i['config_detail_url']['content']['image']['suffix']
                a.img_add             = i['config_detail_url']['content']['image']['add_str']
                a.img_reduce.extend(i['config_detail_url']['content']['image']['reduce_str'])
                a.img_time_format     = i['config_detail_url']['content']['image']['time_format']
                a.next_page_sign      = i['config_detail_url']['next_page']['sign']
                a.next_page_re        = i['config_detail_url']['next_page']['re']
                a.next_page_xpath.extend(i['config_detail_url']['next_page']['xpath'])
                a.next_page_reduce.extend(i['config_detail_url']['next_page']['reduce_str'])
                a.next_page_format    = i['config_detail_url']['next_page']['next_page_format']
                a.pubtime_re          = i['config_detail_url']['pubtime']['re']
                a.pubtime_xpath.extend(i['config_detail_url']['pubtime']['xpath'])
                a.pubtime_reduce.extend(i['config_detail_url']['pubtime']['reduce_str'])
                a.pubtime_format      = i['config_detail_url']['pubtime']['time_format']
                a.tags_re             = i['config_detail_url']['tags']['re']
                a.tags_xpath.extend(i['config_detail_url']['tags']['xpath'])
                a.tags_reduce.extend(i['config_detail_url']['tags']['reduce_str'])
                a.tags_split          = i['config_detail_url']['tags']['split_str']
                a.author_re           = i['config_detail_url']['author']['re']
                a.author_xpath.extend(i['config_detail_url']['author']['xpath'])
                a.author_reduce.extend(i['config_detail_url']['author']['reduce_str'])
                a.categories.extend(i['config_detail_url']['categories'])
                if 'title' in str(i['config_clean']):
                    a.title_lowest        = i['config_clean']['title']['filter_type']['lowest_str']
                    a.title_is_num        = i['config_clean']['title']['filter_type']['is_num']
                    a.title_is_alphabet   = i['config_clean']['title']['filter_type']['is_alphabet']
                    a.title_del.extend(i['config_clean']['title']['filter_type']['delstr'])
                    a.title_string.extend(i['config_clean']['title']['string'])
                    a.content_lowest_str  = i['config_clean']['content']['filter_type']['lowest_str']
                    a.content_lowest_pic  = i['config_clean']['content']['filter_type']['lowest_pic']
                    a.content_highest_pic = i['config_clean']['content']['filter_type']['highest_pic']
                    a.content_del.extend(i['config_clean']['content']['filter_type']['delstr'])
                    a.image_reduce_method.extend(i['config_clean']['content']['image'])
                    a.content_string.extend(i['config_clean']['content']['string'])
                    a.content_string_node.extend(i['config_clean']['content']['string_node'])
                xpath_data = ''
                crawl_data = ''
            print('site_name:',a.site_name,'channel:',a.channel)
            return render(request, 'add_config.html',{'site_name': a.site_name, 'channel': a.channel, 'categories': a.categories, 'start_url': a.start_url,
                                                      'start_headers': a.start_headers,'urllist_re': a.urllist_re, 'urllist_xpath': a.urllist_xpath, 'urllist_add': a.urllist_add,
                                                      'urllist_reduce': a.urllist_reduce,'imglist_xpath': a.imglist_xpath, 'imglist_url_add': a.imglist_url_add,
                                                      'imglist_url_reduce': a.imglist_url_reduce,'imglist_img_add': a.imglist_img_add, 'imglist_img_reduce': a.imglist_img_reduce,
                                                      'img_sign': a.img_sign, 'url_sign': a.url_sign, 'detail_url_headers': a.detail_url_headers, 'title_re': a.title_re,
                                                      'title_xpath': a.title_xpath,'title_add': a.title_add,'title_reduce': a.title_reduce, 'content_re': a.content_re,
                                                      'content_xpath': a.content_xpath,'reduce_node': a.reduce_node, 'cont_reduce': a.cont_reduce, 'img_suffix': a.img_suffix,
                                                      'img_add': a.img_add,'img_reduce': a.img_reduce, 'img_time_format': a.img_time_format, 'next_page_sign': a.next_page_sign,
                                                      'next_page_re': a.next_page_re,'next_page_xpath': a.next_page_xpath, 'next_page_reduce': a.next_page_reduce,
                                                      'next_page_format': a.next_page_format, 'pubtime_re': a.pubtime_re, 'pubtime_xpath': a.pubtime_xpath,'pubtime_reduce': a.pubtime_reduce,
                                                      'pubtime_format': a.pubtime_format, 'tags_re': a.tags_re, 'tags_xpath': a.tags_xpath,'tags_reduce': a.tags_reduce,
                                                      'tags_split': a.tags_split,'author_re': a.author_re, 'author_xpath': a.author_xpath, 'author_reduce': a.author_reduce,
                                                      'title_lowest': a.title_lowest,'title_del': a.title_del,'title_string': a.title_string, 'content_lowest_str': a.content_lowest_str,
                                                      'content_lowest_pic': a.content_lowest_pic,'content_highest_pic': a.content_highest_pic, 'content_del': a.content_del,
                                                      'content_string': a.content_string, 'content_string_node': a.content_string_node,'xpath_data':xpath_data,
                                                      'crawl_data':crawl_data})

        if opt_name == '新增':
            print('add_new')
            a = config()
            xpath_data = ''
            crawl_data = ''
            return render(request, 'add_config.html',{'site_name': a.site_name, 'channel': a.channel, 'categories': a.categories, 'start_url': a.start_url,
                                                      'start_headers': a.start_headers,'urllist_re': a.urllist_re, 'urllist_xpath': a.urllist_xpath, 'urllist_add': a.urllist_add,
                                                      'urllist_reduce': a.urllist_reduce,'imglist_xpath': a.imglist_xpath, 'imglist_url_add': a.imglist_url_add,
                                                      'imglist_url_reduce': a.imglist_url_reduce,'imglist_img_add': a.imglist_img_add, 'imglist_img_reduce': a.imglist_img_reduce,
                                                      'img_sign': a.img_sign, 'url_sign': a.url_sign, 'detail_url_headers': a.detail_url_headers, 'title_re': a.title_re,
                                                      'title_xpath': a.title_xpath,'title_add': a.title_add,'title_reduce': a.title_reduce, 'content_re': a.content_re,
                                                      'content_xpath': a.content_xpath,'reduce_node': a.reduce_node, 'cont_reduce': a.cont_reduce, 'img_suffix': a.img_suffix,
                                                      'img_add': a.img_add,'img_reduce': a.img_reduce, 'img_time_format': a.img_time_format, 'next_page_sign': a.next_page_sign,
                                                      'next_page_re': a.next_page_re,'next_page_xpath': a.next_page_xpath, 'next_page_reduce': a.next_page_reduce,
                                                      'next_page_format': a.next_page_format, 'pubtime_re': a.pubtime_re, 'pubtime_xpath': a.pubtime_xpath,'pubtime_reduce': a.pubtime_reduce,
                                                      'pubtime_format': a.pubtime_format, 'tags_re': a.tags_re, 'tags_xpath': a.tags_xpath,'tags_reduce': a.tags_reduce,
                                                      'tags_split': a.tags_split,'author_re': a.author_re, 'author_xpath': a.author_xpath, 'author_reduce': a.author_reduce,
                                                      'title_lowest': a.title_lowest,'title_del': a.title_del,'title_string': a.title_string, 'content_lowest_str': a.content_lowest_str,
                                                      'content_lowest_pic': a.content_lowest_pic,'content_highest_pic': a.content_highest_pic, 'content_del': a.content_del,
                                                      'content_string': a.content_string, 'content_string_node': a.content_string_node,'xpath_data':xpath_data,
                                                      'crawl_data':crawl_data})

        if opt_name == '预览配置' or opt_name == '测试' or  opt_name == '提交':
            a = config()
            a.site_name                         = site_name
            a.channel                           = channel
            a.start_url                         = request.POST.get('start_url')
            a.timestamp                         = request.POST.get('timestamp')
            a.start_web_type                    = request.POST.get('start_web_type')
            a.start_url_req_type                      = request.POST.get('start_url_req_type')
            a.start_headers                      = request.POST.get('start_headers')
            a.urllist_re                      = request.POST.get('urllist_re')
            a.urllist_add                      = request.POST.get('urllist_add')
            a.urllist_xpath             = request.POST.get('urllist_xpath')
            a.urllist_reduce                = request.POST.get('urllist_reduce')
            a.imglist_xpath         = request.POST.get('imglist_xpath')
            a.imglist_url_add                      = request.POST.get('imglist_url_add')
            a.imglist_url_reduce            = request.POST.get('imglist_url_reduce')
            a.imglist_img_add                      = request.POST.get('imglist_img_add')
            a.imglist_img_reduce            = request.POST.get('imglist_img_reduce')
            a.img_sign                      = request.POST.get('img_sign')
            a.url_sign                      = request.POST.get('url_sign')
            a.detail_web_type                      = request.POST.get('detail_web_type')
            a.detail_url_req_type                      = request.POST.get('detail_url_req_type')
            a.detail_url_headers                      = request.POST.get('detail_url_headers')
            a.title_re                      = request.POST.get('title_re')
            a.title_xpath           = request.POST.get('title_xpath')
            a.title_add                      = request.POST.get('title_add')
            a.title_reduce           = request.POST.get('title_reduce')
            a.content_re                      = request.POST.get('content_re')
            a.content_xpath                      = request.POST.get('content_xpath')
            a.reduce_node                      = request.POST.get('reduce_node')
            a.cont_reduce                      = request.POST.get('cont_reduce')
            a.img_suffix                      = request.POST.get('img_suffix')
            a.img_add                      = request.POST.get('img_add')
            a.img_reduce                      = request.POST.get('img_reduce')
            a.img_time_format                      = request.POST.get('img_time_format')
            a.next_page_sign                      = request.POST.get('next_page_sign')
            a.next_page_re                      = request.POST.get('next_page_re')
            a.next_page_xpath                      = request.POST.get('next_page_xpath')
            a.next_page_reduce                      = request.POST.get('next_page_reduce')
            a.next_page_format                      = request.POST.get('next_page_format')
            a.pubtime_re                      = request.POST.get('pubtime_re')
            a.pubtime_xpath                      = request.POST.get('pubtime_xpath')
            a.pubtime_reduce                      = request.POST.get('pubtime_reduce')
            a.pubtime_format                      = request.POST.get('pubtime_format')
            a.tags_re                      = request.POST.get('tags_re')
            a.tags_xpath                      = request.POST.get('tags_xpath')
            a.tags_reduce                      = request.POST.get('tags_reduce')
            a.tags_split                      = request.POST.get('tags_split')
            a.author_re                      = request.POST.get('author_re')
            a.author_xpath                      = request.POST.get('author_xpath')
            a.author_reduce                      = request.POST.get('author_reduce')
            a.categories                      = request.POST.get('categories')
            a.title_lowest                      = request.POST.get('title_lowest')
            a.title_is_num                      = request.POST.get('title_is_num')
            a.title_is_alphabet                      = request.POST.get('title_is_alphabet')
            a.title_del                      = request.POST.get('title_del')
            a.title_string                      = request.POST.get('title_string')
            a.content_lowest_str                      = request.POST.get('content_lowest_str')
            a.content_lowest_pic                      = request.POST.get('content_lowest_pic')
            a.content_highest_pic                      = request.POST.get('content_highest_pic')
            a.content_del                      = request.POST.get('content_del')
            a.image_reduce_method                      = request.POST.get('image_reduce_method')
            a.content_string                      = request.POST.get('content_string')
            a.content_string_node                       = request.POST.get('content_string_node')
            json_str = a.to_Json()
            print(a.urllist_add,'这是urllist_add',request.POST.get('imglist_url_add'))
            if opt_name == '预览配置':
                return render(request, 'add_config.html',{'site_name': a.site_name, 'channel': a.channel, 'categories': a.categories, 'start_url': a.start_url,
                                                      'start_headers': a.start_headers,'urllist_re': a.urllist_re, 'urllist_xpath': a.urllist_xpath, 'urllist_add': a.urllist_add,
                                                      'urllist_reduce': a.urllist_reduce,'imglist_xpath': a.imglist_xpath, 'imglist_url_add': a.imglist_url_add,
                                                      'imglist_url_reduce': a.imglist_url_reduce,'imglist_img_add': a.imglist_img_add, 'imglist_img_reduce': a.imglist_img_reduce,
                                                      'img_sign': a.img_sign, 'url_sign': a.url_sign, 'detail_url_headers': a.detail_url_headers, 'title_re': a.title_re,
                                                      'title_xpath': a.title_xpath,'title_add': a.title_add,'title_reduce': a.title_reduce, 'content_re': a.content_re,
                                                      'content_xpath': a.content_xpath,'reduce_node': a.reduce_node, 'cont_reduce': a.cont_reduce, 'img_suffix': a.img_suffix,
                                                      'img_add': a.img_add,'img_reduce': a.img_reduce, 'img_time_format': a.img_time_format, 'next_page_sign': a.next_page_sign,
                                                      'next_page_re': a.next_page_re,'next_page_xpath': a.next_page_xpath, 'next_page_reduce': a.next_page_reduce,
                                                      'next_page_format': a.next_page_format, 'pubtime_re': a.pubtime_re, 'pubtime_xpath': a.pubtime_xpath,'pubtime_reduce': a.pubtime_reduce,
                                                      'pubtime_format': a.pubtime_format, 'tags_re': a.tags_re, 'tags_xpath': a.tags_xpath,'tags_reduce': a.tags_reduce,
                                                      'tags_split': a.tags_split,'author_re': a.author_re, 'author_xpath': a.author_xpath, 'author_reduce': a.author_reduce,
                                                      'title_lowest': a.title_lowest,'title_del': a.title_del,'title_string': a.title_string, 'content_lowest_str': a.content_lowest_str,
                                                      'content_lowest_pic': a.content_lowest_pic,'content_highest_pic': a.content_highest_pic, 'content_del': a.content_del,
                                                      'content_string': a.content_string, 'content_string_node': a.content_string_node,'xpath_data':json_str})
                # return render(request, 'add_config.html', {'xpath_data': json_str})

            if opt_name == '测试':
                url = 'http://192.168.1.33:9000/HttpService/crawl'
                body = '{"cmd":1,"data":'+json_str+'}'
                html = requests.post(url,data=body.encode('utf-8'))
                print(html.content.decode('utf-8'))
                crawl_data = html.content.decode('utf-8')
                return render(request, 'add_config.html',{'site_name': a.site_name, 'channel': a.channel, 'categories': a.categories, 'start_url': a.start_url,
                                                      'start_headers': a.start_headers,'urllist_re': a.urllist_re, 'urllist_xpath': a.urllist_xpath, 'urllist_add': a.urllist_add,
                                                      'urllist_reduce': a.urllist_reduce,'imglist_xpath': a.imglist_xpath, 'imglist_url_add': a.imglist_url_add,
                                                      'imglist_url_reduce': a.imglist_url_reduce,'imglist_img_add': a.imglist_img_add, 'imglist_img_reduce': a.imglist_img_reduce,
                                                      'img_sign': a.img_sign, 'url_sign': a.url_sign, 'detail_url_headers': a.detail_url_headers, 'title_re': a.title_re,
                                                      'title_xpath': a.title_xpath,'title_add': a.title_add,'title_reduce': a.title_reduce, 'content_re': a.content_re,
                                                      'content_xpath': a.content_xpath,'reduce_node': a.reduce_node, 'cont_reduce': a.cont_reduce, 'img_suffix': a.img_suffix,
                                                      'img_add': a.img_add,'img_reduce': a.img_reduce, 'img_time_format': a.img_time_format, 'next_page_sign': a.next_page_sign,
                                                      'next_page_re': a.next_page_re,'next_page_xpath': a.next_page_xpath, 'next_page_reduce': a.next_page_reduce,
                                                      'next_page_format': a.next_page_format, 'pubtime_re': a.pubtime_re, 'pubtime_xpath': a.pubtime_xpath,'pubtime_reduce': a.pubtime_reduce,
                                                      'pubtime_format': a.pubtime_format, 'tags_re': a.tags_re, 'tags_xpath': a.tags_xpath,'tags_reduce': a.tags_reduce,
                                                      'tags_split': a.tags_split,'author_re': a.author_re, 'author_xpath': a.author_xpath, 'author_reduce': a.author_reduce,
                                                      'title_lowest': a.title_lowest,'title_del': a.title_del,'title_string': a.title_string, 'content_lowest_str': a.content_lowest_str,
                                                      'content_lowest_pic': a.content_lowest_pic,'content_highest_pic': a.content_highest_pic, 'content_del': a.content_del,
                                                      'content_string': a.content_string, 'content_string_node': a.content_string_node,'xpath_data':json_str,
                                                      'crawl_data':crawl_data})
                # return render(request, 'add_config.html', {'xpath_data': json_str,'crawl_data':crawl_data})

            if opt_name == '提交':
                submit_message = '提交成功！'
                # submit_message = '提交失败！'
                return HttpResponse(submit_message)
                # return render(request, 'add_config.html', {'submit_message':submit_message})

@login_required(login_url='/login/')
def xpath(request):
    if request.method == 'GET':
        f = open('./cpsite/xpath.json','r',encoding='utf-8')
        o = f.read()
        f.close()
        return render(request,'xpath.html',{'datalist':o})

@login_required(login_url='/login/')
def test_opt(request):
    print(request.method)
    if request.method == 'POST':
        print('POST requests')
        print(request.POST)
        pageNumber = request.POST.get('pageNumber')
        pageSize = request.POST.get('pageSize')
        site_name = request.POST.get('site_name')
        channel  = request.POST.get('channel')
        id = request.POST.get('id')
        third_id = request.POST.get('third_id')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        app_id = request.POST.get('app_id')
        time_gt = request.POST.get('time_gt')
        time_lt = request.POST.get('time_lt')
        news_title = request.POST.get('news_title')
        author = request.POST.get('author')
        type = request.POST.get('type')
        sort = request.POST.get('sort')
        a = SiteChannelOperate()
        # print(id,site_name,channel,category,app_id,time_gt,time_lt,news_title,type,sort)
        return HttpResponse(a.query_es_list(site_name,channel,id,third_id,category,sub_category,app_id,time_gt,time_lt,news_title,author,type,sort,pageNumber,pageSize))
    else:
        print('GET requests')
        return render(request,'test_opt.html')

@login_required(login_url='/login/')
def id_delete(request):
    if request.method == 'GET':
        _id = request.GET.get('id')
        a = SiteChannelOperate()
        msg = a.delete_id(_id)
        return HttpResponse(msg)

@login_required(login_url='/login/')
def chart(request,_type):
    a = SiteChannelOperate()
    if str(_type) == 'article':
        qiyu_top_10 = a.chart_opt(_type,'site_name_qiyu_top_10')
        series_image = a.chart_opt(_type,'site_name_image')
        category = a.chart_opt(_type,'category')
        return render(request,'chart_article.html',{'data_qiyu_top_ten':qiyu_top_10[0],'series_qiyu_top_ten':qiyu_top_10[1],
                                                    'data_image':series_image[0],'series_image':series_image[1],
                                                    'data_qiyu_category':category[0],'series_qiyu_category':category[1]
                                                    })

    if str(_type) == 'audio':
        data = a.chart_opt(_type,'site_name')
        return render(request,'chart_audio.html',{'categories':data[0],'series':data[1]})
        # return render(request,'403.html')

    if str(_type) == 'video':
        data = a.chart_opt(_type,'site_name')
        return  render(request,'chart_video.html',{'categories':data[0],'series':data[1]})

    if str(_type) == 'all':
        data = a.chart_opt(_type,'all_type')
        data_complicate = a.chart_opt(_type,'total_num')
        return render(request,'chart_all.html',{'categories':data[0],'series':data[1],'category_complicate':data_complicate[0],'series_complicate':data_complicate[1]})

@login_required(login_url='/login/')
def index_weixin(request):
    if request.method == 'POST':
        print(request.body)
        opt = request.POST.get('opt')
        pageSize = request.POST.get('pageSize')
        pageNumber = request.POST.get('pageNumber')
        appname = request.POST.get('appname')
        categories = request.POST.get('categories')
        channel = request.POST.get('channel')
        test_status = request.POST.get('test_status')
        is_stop = request.POST.get('is_stop')
        has_account = request.POST.get('has_account')
        print(test_status, is_stop, has_account)
        op = SiteChannelOperate()
        return HttpResponse(op.query_crawl(opt,appname, categories, channel, pageNumber, pageSize, test_status, is_stop, has_account))
    else:
        return render(request,'index_weixin.html')

@login_required(login_url='/login/')
@csrf_exempt
def majiahao(request):
    if request.method == 'POST':
        if str(request.content_params) == '{}':
            print('=========',request.content_type)
            opt = request.POST.get('opt')
            majiahao = request.POST.get('majiahao')
            pageSize = request.POST.get('pageSize')
            pageNumber = request.POST.get('pageNumber')
            print('majiahao:',majiahao)
            op = SiteChannelOperate()
            return HttpResponse(op.query_majiahao(majiahao,opt,pageNumber,pageSize))
        else:
            #print(request.parse_file_upload, request.content_type, request.read, request.is_ajax)
            print(dir(request.body),type(request.body))
            print(request.body.decode('utf-8'))
            print(request.body.decode('utf8').split('\n'))
            data = request.body.decode('utf8').split('\n')[4]
            if 'WebKit' not in str(data):
                data_list = data.split(',')
                op = SiteChannelOperate()
                # print(data_list,type(data_list))
                if op.add_majiahao(data_list) == True:
                    return HttpResponse('success')
                else:
                    return HttpResponse('failed')
            else:
                return HttpResponse('empty')
    else:
        opt = request.GET.get('opt')
        print(request.body)
        majiahao = request.GET.get('majiahao')
        if opt == 'delete':
            print('delete  get  request', opt)
            op = SiteChannelOperate()
            op.query_majiahao(majiahao,opt,0,0)
        return render(request,'index_majiahao.html')

@login_required(login_url='/login/')
def query_detail_byid(request,_id):
    try:
        if _id != '':
            a = SiteChannelOperate()
            js = a.detail_id(_id)
            print(js)
            js = json.loads(js)
            title = js['news_title']
            content = js['content']
            print(time.localtime(int(js['create_time'])/1000))
            pubtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(js['create_time'])/1000))
            print(pubtime)
            site_name = js['site_name']
            org_url = js['org_url']
            return render(request,'detail_id.html',{'title':title,'content':content,'pubtime':pubtime,'site_name':site_name,'org_url':org_url})
    except BaseException:
        traceback.print_exc()
        return render(request,'403.html')

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    # return render(request,'logout.html')
    return redirect('/login')
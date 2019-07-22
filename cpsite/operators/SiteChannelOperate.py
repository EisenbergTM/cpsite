# -*- coding: utf8 -*-
from datetime import *
import os
import re
import time
import requests
import json
import random
import base64
import datetime
import traceback

class SiteChannelOperate():
    def __init__(self):
        self._dbproxy_url = 'http://114.215.18.7:26478/do_query'
        self._update_web_url = 'http://114.215.18.7:26478/do_upset'
        # self._es_url = 'http://114.215.18.7:23499/dbproxy'
        self._es_url = 'http://103.229.213.206:23499/dbproxy'
        self._mysql_url = 'http://103.229.213.206:23499/dbproxy'
        #self._mysql_url = 'http://114.215.18.7:23499/dbproxy'


    def query(self, site_name, channel, page_no, page_size,test_status,have_stop):
        print('site_name: ' + site_name + '; channel: '+channel)
        if int(page_no) >= 1:
            page_no = str((int)(page_no) - 1)
        jstr = '{\"cmd\":1,\"page_no\":' + str(page_no) \
            + ',\"page_size\":' + str(page_size)
        if site_name != '':
            jstr += ',\"site_name\":\"' + site_name + '\"'
        if channel != '':
            jstr += ',\"channel\":\"' + channel + '\"'
        jstr += '}'
        if str(test_status) == '0':
            jstr = '{"cmd":1,"page_no":'+str(page_no)+',"page_size":'+str(page_size)+',"test_status":0}'
        if str(have_stop) == '1':
            jstr = '{"cmd":1,"page_no":'+str(page_no)+',"page_size":'+str(page_size)+',"have_stop":1}'
        ret_jstr = '{'
        try:
            co = requests.post(self._dbproxy_url, jstr.encode('utf-8')).content
            rsp = json.loads(co)
            if rsp is not None and 'data' in rsp and 'total' in rsp:
                total = int(rsp['total'])
                ret_jstr += '\"total\": ' + str(rsp['total']) + ',\"rows\":['
                datas = rsp['data']
                i = 0
                for d in datas:
                    if 0 < i:
                        ret_jstr += ','
                    ret_jstr += '{\"URL\":\"'
                    if 'url' in d:
                        ret_jstr += str(d['url'])
                    ret_jstr += '\",\"site_name\":\"'
                    if 'site_name' in d:
                        ret_jstr += str(d['site_name'])
                    ret_jstr += '\",\"channel\":\"'
                    if 'channel' in d:
                        ret_jstr += str(d['channel'])
                    ret_jstr += '\",\"rpush_frequence\":'
                    if 'redis_push_frequency' in d:
                        ret_jstr += str(d['redis_push_frequency'])
                    else:
                        ret_jstr += '0'
                    ret_jstr += ',\"is_stop\":'
                    if 'is_stop' in d:
                        ret_jstr += str(d['is_stop'])
                    else:
                        ret_jstr += '1'
                    ret_jstr += ',\"test_status\":'
                    if 'test_status' in d:
                        ret_jstr += str(d['test_status'])
                    else:
                        ret_jstr += '0'
                    ret_jstr += '}'
                    i = i+1
        except Exception:
            pass
        ret_jstr += ']}'
        #print(ret_jstr)
        return ret_jstr

    def query_crawl(self,opt,appname, categories, channel, pageNumber, pageSize, test_status, is_stop, has_account):
        print(opt,appname, categories, channel, pageNumber, pageSize, test_status, is_stop, has_account)
        body = {"type": "mysql","method":"query","db_name":"crawl","body":""}
        callback = {"total":0,"rows":[]}
        if str(opt) == 'query':
            query_str = 'SELECT * FROM grab_app_account_info '
            if int(pageNumber) >= 1:
                pageNumber = str((int(pageNumber) - 1))
            if str(appname).strip() != '':
                query_str += 'WHERE app_name = "'+ appname+ '" '
            if str(categories) != '':
                if 'WHERE' in query_str:
                    query_str += 'and categories = "'+categories+'" '
                else:
                    query_str += 'WHERE categories = "'+categories+'" '
            if str(channel) != '':
                if 'WHERE' in query_str:
                    query_str += 'and channel = "'+channel+'" '
                else:
                    query_str += 'WHERE channel = "'+channel+'" '
            if str(has_account) != 'all':
                if 'WHERE' in query_str:
                    query_str += 'and has_account = "'+str(has_account)+'" '
                else:
                    query_str += 'WHERE has_account = "'+str(has_account)+'" '
            if str(is_stop) != 'all':
                if 'WHERE' in query_str:
                    query_str += 'and is_stop = "'+str(is_stop)+'" '
                else:
                    query_str += 'WHERE is_stop = "'+str(is_stop)+'" '
            if str(test_status) != 'all':
                if 'WHERE' in query_str:
                    query_str += 'and test_status = "'+str(test_status)+'" '
                else:
                    query_str += 'WHERE test_status = "'+str(test_status)+'" '
            query_str += 'LIMIT ' + str(int(pageNumber)*10) + ',' + str(pageSize)
            body['body'] = query_str
            print(body)
            html = requests.post(self._mysql_url,data=json.dumps(body).encode('utf-8')).json()
            for i in html['data']:
                item = {}
                item['app_name']      = i['col_3']
                item['app_channel']   = i['col_4']
                item['categories']    = i['col_5']
                item['channel']       = i['col_6']
                item['is_stop']       = i['col_7']
                item['test_status']   = i['col_8']
                item['from_sources']  = i['col_9']
                item['has_account']   = i['col_10']
                item['description']   = i['col_11']
                callback['rows'].append(item.copy())
            body['body'] = query_str.replace('*','count(*)').split('LIMIT')[0]
            print(body)
            html = requests.post(self._mysql_url, data=json.dumps(body).encode('utf-8')).json()
            print(html)
            callback['total'] = html['data'][0]['col_0']

            return json.dumps(callback,ensure_ascii=False)



    def query_majiahao(self,majiahao,opt,pagenum,pagesize):
        try:
            print(majiahao,opt,pagenum,pagesize)
            callback = {'total': 0, 'rows': []}
            body = { "type":"mysql", "method":'query', "db_name":"crawl", "body":""}
            if str(opt) == 'query' and str(majiahao) != '':
                body['method'] = 'query'
                body['body'] = 'select * FROM grab_majiahao_info WHERE majia_hao ="'+str(majiahao)+'"'
            elif str(opt) == 'delete' and str(majiahao) != '':
                body['method'] = 'delete'
                body['body'] = 'DELETE FROM grab_majiahao_info WHERE majia_hao="'+str(majiahao)+ '"'
            if str(opt) == 'query' and str(majiahao) == '':
                body['method'] = 'query'
                body['body'] = 'select count(*) FROM grab_majiahao_info '
                html = requests.post(self._mysql_url, data=json.dumps(body).encode('utf-8')).json()
                print(html)
                callback['total'] = html['data'][0]['col_0']
                body['body'] = 'select * FROM grab_majiahao_info LIMIT '+ str((int(pagenum)-1)*10)+ ', '+str(pagesize) + ';'
                
            print(body['body'])
            html = requests.post(self._mysql_url,data=json.dumps(body).encode('utf-8')).json()
            if 'data' in str(html):
                if callback['total'] == 0:
                    callback['total'] = len(html['data'])
                print(html)
                for i in html['data']:
                    callback['rows'].append({'majiahao':i['col_1']})
                print(json.dumps(callback,ensure_ascii=False))
            return json.dumps(callback,ensure_ascii=False)
        except BaseException:
            traceback.print_exc()

    def add_majiahao(self,majiahao):
        try:
            body = { "type":"mysql", "method":'insert', "db_name":"crawl", "body":""}
            insert_str = 'insert into grab_majiahao_info (majia_hao) VALUES '
            for i in majiahao:
                if i != '':
                    insert_str += '("'+str(i).strip()+'"),'
            insert_str = insert_str[:-1]+';'
            print(insert_str)
            body['body'] = insert_str
            html = requests.post(self._mysql_url, data=json.dumps(body).encode('utf-8')).json()
            print(html)
            if html['errmsg'] == 'success':
                return True
            else:
                return False
        except BaseException:
            traceback.print_exc()


    def online_operator(self,operator,site_name,channel,url):
        try:
            body = ''
            if operator == '上线':
                # print(site_name,channel,url)
                body = '{"cmd":2,"site_name":"'+str(site_name)+'","channel":"'+str(channel)+'","url":"'+str(url)+'","test_status":1}'
            elif operator == '下线':
                body = '{"cmd":2,"site_name":"'+str(site_name)+'","channel":"'+str(channel)+'","url":"'+str(url)+'","test_status":0}'
            elif operator == '停抓':
                body = '{"cmd":2,"site_name":"'+str(site_name)+'","channel":"'+str(channel)+'","url":"'+str(url) +'","is_stop":1}'
            elif operator == '启用':
                body = '{"cmd":2,"site_name":"'+str(site_name)+'","channel":"'+str(channel)+'","url":"'+str(url) +'","is_stop":0}'
            if body != '':
                html = requests.post(self._update_web_url,data=body.encode('utf-8')).json()
                print(html)
                return json.loads(html)
        except BaseException:
            traceback.print_exc()

    def online_operator_app(self,opt,app_name,channel):
        try:
            body = {"type":"mysql","method":"update","db_name":"crawl","body":""}
            if opt == '上线':
                body['body'] = 'UPDATE grab_app_account_info SET test_status=1 WHERE app_name="'+str(app_name)+'" and channel="'+str(channel)+'"'
            elif opt == '下线':
                body['body'] = 'UPDATE grab_app_account_info SET test_status=0 WHERE app_name="'+str(app_name)+'" and channel="'+str(channel)+'"'
            elif opt == '停抓':
                body['body'] = 'UPDATE grab_app_account_info SET is_stop=1 WHERE app_name="'+str(app_name)+'" and channel="'+str(channel)+'"'
            elif opt == '启用':
                body['body'] = 'UPDATE grab_app_account_info SET is_stop=0 WHERE app_name="'+str(app_name)+'" and channel="'+str(channel)+'"'
            if body['body'] != '':
                html = requests.post(self._mysql_url,data=json.dumps(body).encode('utf-8')).json()
                print(html)
                return html
        except BaseException:
            traceback.print_exc()

    def update_config(self,opt_name,site_name,channel):
        feed_back = {}
        if site_name != '' and channel != '':

            body = '{"cmd":30,"site_name":"'+str(site_name)+'","channel":"'+str(channel)+'"}'
            data = requests.post(self._dbproxy_url,data=body.encode('utf-8')).json()['data']
            if data == {}:
                feed_back['error'] = 'no such site_name + channel!'
            else:
                feed_back['config_start_url']  = json.loads(base64.b64decode(data['config_start_url']))
                feed_back['config_detail_url'] = json.loads(base64.b64decode(data['config_detail_url']))
                if data['config_clean'] != '':
                    feed_back['config_clean']  = json.loads(base64.b64decode(data['config_clean']))
                else:
                    feed_back['config_clean']  = {}
            return json.dumps(feed_back,ensure_ascii=False)
        else:
            return '{"failed":"parameters wrong"}'

    def query_es_list(self,site_name,channel,id,third_id,category,sub_category,app_id,time_gt,time_lt,news_title,author,type,sort,pageNumber,pageSize):
        print(site_name,channel,id,third_id,category,sub_category,app_id,time_gt,time_lt,news_title,author,type,sort,pageNumber,pageSize)
        msg = {'errno': 0, 'errmsg': 'success', 'total': 0, 'rows': []}
        body = {"type": "es", "method": "POST", "uri": "*/_search", "body": {}}
        es_dict = {"query": {"bool": {"filter": []}},'size':pageSize}
        if int(pageNumber) > 0:
            es_dict['from'] = (int(pageNumber)-1)*int(pageSize)
        else:
            es_dict['from'] = 0
        if str(sort) != 'no':
            es_dict['sort'] = {'create_time':{'order':sort }}
        if str(type) != '0':
            es_dict['query']['bool']['filter'].append({'term':{'type':type}})
        if str(id).strip() != '':
            es_dict['query']['bool']['filter'].append({'term':{'id':id}})
        if str(third_id).strip() != '':
            es_dict['query']['bool']['filter'].append({'term':{'third_id':third_id}})
        if str(site_name).strip() != '':
            es_dict['query']['bool']['filter'].append({'match_phrase':{'site_name':site_name}})
        if str(channel).strip() != '':
            es_dict['query']['bool']['filter'].append({'term':{'channel':channel}})
        if str(category).strip() != '':
            es_dict['query']['bool']['filter'].append({'multi_match':{'query':category,'fields':['categories']}})
        if str(sub_category).strip() != '':
            es_dict['query']['bool']['filter'].append({'term':{'sub_cagetory':sub_category}})
        if str(app_id).strip() != '':
            es_dict['query']['bool']['filter'].append({'multi_match':{'query':app_id,'fields':['from_sources']}})
        if str(author).strip() != '':
            es_dict['query']['bool']['filter'].append({'term':{'author':author}})
        if str(news_title).strip() != '':
            es_dict['query']['bool']['filter'].append({'match_phrase':{'news_title':news_title}})
        print(time_gt,time_lt)
        if str(time_gt).strip() != '' or str(time_lt).strip() != '':
            time_dict = {}
            if str(time_gt).strip() != '':
                time_dict['gt'] = int(time.mktime(time.strptime(time_gt,'%Y-%m-%dT%H:%M'))*1000)
            if str(time_lt).strip() != '':
                time_dict['lt'] = int(time.mktime(time.strptime(time_lt,'%Y-%m-%dT%H:%M'))*1000)
            es_dict['query']['bool']['filter'].append({'range':{'create_time':time_dict}})
        body['body'] = es_dict
        print(body)
        html = requests.post(self._es_url,data=json.dumps(body).encode('utf-8')).json()
        #失败重试
        if msg['errmsg'] != 'success':
            html = requests.post(self._es_url,data=json.dumps(body).encode('utf-8')).json()
        #再次重试
        if msg['errmsg'] != 'success':
            html = requests.post(self._es_url,data=json.dumps(body).encode('utf-8')).json()
        item = {}
        print(html)
        msg['errono'] = html['errno']
        msg['errmsg'] = html['errmsg']
        msg['total']  = html['data']['hits']['total']
        for i in html['data']['hits']['hits']:
            item['id']          = i['_source']['id']
            if i['_source']['list_images'] != []:
                item['list_image']  = i['_source']['list_images'][0]
            else:
                item['list_image']  = ''
            item['title']           = i['_source']['news_title']
            item['site_name']       = i['_source']['site_name']
            item['is_hot']          = i['_source']['is_hot']
            item['category']        = i['_source']['categories']
            item['sub_category']    = i['_source']['sub_cagetory']
            item['org_url']         = i['_source']['org_url']
            item['tags']            = i['_source']['tags']
            item['author']          = i['_source']['author']
            item['third_id']        = i['_source']['third_id']
            item['from_sources']    = i['_source']['from_sources']
            msg['rows'].append(item.copy())
        # print(json.dumps(msg,ensure_ascii=False))
        return json.dumps(msg,ensure_ascii=False)

    def delete_id(self,_id):
        if _id != '':
            print(_id)
            es_req = '{"type":"es","method":"POST","uri":"nm_*/_delete_by_query","body":{"query":{"bool": {"must": [ {"term":{"id":"'+ str(_id) +'"}}]}},"size": 1}}'
            html = requests.post(self._es_url,data=es_req.encode('utf-8')).json()
            return json.dumps(html['errmsg'])

    def detail_id(self,_id):
        url = 'http://103.229.213.250:23498/HttpService/get_news_detail2?nid='+ str(_id)
        print(_id)
        print(url)
        html = requests.get(url).json()
        return json.dumps(html,ensure_ascii=False)


    def chart_opt(self,_type,chart_name):
        color_list = ['rgba(255,0,0,0.25)','rgba(0,120,200,0.75)','rgba(220,220,220,0.75)','rgba(255,218,185,0.75)','rgba(255,218,185,0.75)','rgba(0,255,255,0.75)','rgba(0,0,0,0.75)','rgba(0,255,0,0.75)','rgba(25,25,122,0.75)','rgba(255,255,0,0.75)','rgba(160,32,240,0.75)','rgba(105,105,105,0.75)','rgba(0,139,139,0.75)','rgba(144,238,144,0.75)','rgba(255,131,250,0.75)']
        series = []
        x_list = []
        item = {'name':'','color':'','marker':{'radius':6},'lineWidth':2,'data':[]}
        today          = datetime.date.today()
        if str(_type) == 'all':
            if chart_name == 'all_type':
                item_video = {'name': 'video', 'color': random.choice(color_list), 'marker': {'radius': 6},'lineWidth': 2, 'data': []}
                color_list.pop(color_list.index(item_video['color']))
                item_audio = {'name': 'audio', 'color': random.choice(color_list), 'marker': {'radius': 6},'lineWidth': 2, 'data': []}
                color_list.pop(color_list.index(item_audio['color']))
                item_article = {'name': 'news', 'color': random.choice(color_list), 'marker': {'radius': 6},'lineWidth': 2, 'data': []}
                color_list.pop(color_list.index(item_article['color']))
                item_image = {'name': 'image', 'color': random.choice(color_list), 'marker': {'radius': 6}, 'lineWidth': 2, 'data': []}
                color_list.pop(color_list.index(item_image['color']))
                query_str = 'select * from grab_qiyu_total where date <=\'' + str(today) + '\' and date >=\''+ str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                html = requests.post(self._mysql_url,data=body.encode('utf-8')).json()
                if html['data'] != []:
                    for i in html['data']:
                        item_article['data'].append(int(i['col_3']))
                        item_video['data'].append(int(i['col_4']))
                        item_audio['data'].append(int(i['col_5']))
                        item_image['data'].append(int(i['col_6']))
                        x_list.append(i['col_2'])
                series = [item_article,item_audio,item_video,item_image]
                x_list = str(x_list).replace('[\'', '').replace('\']', '')
                series = str(series).replace('\'', '"')
                return x_list,series
            if chart_name == 'total_num':
                for i in range(7):
                    x_list.append(str(today + datetime.timedelta(days=-(i+1))))
                x_list.reverse()
                query_str = 'select * from grab_qiyu_total_num where date <=\'' + str(today) + '\' and date >=\''+ str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                html = requests.post(self._mysql_url,data=body.encode('utf-8')).json()
                for i in html['data']:
                    series.append(int(i['col_3']))
                x_list = str(x_list).replace('\'','"')
                return x_list,series

        if str(_type) == 'article':
            if str(chart_name) == 'category':
                site_name_list = x_list = []
                data = {'name': '', 'y': 0, 'drilldown': ''}
                query_str = 'select * from grab_qiyu_category_status where date =\'' + str(
                    today + datetime.timedelta(days=-1)) + '\''
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                print(body)
                html = requests.post(self._mysql_url, data=body.encode('utf-8')).json()
                for i in html['data']:
                    site_name_list.append(i['col_3'])
                    data['name'] = i['col_3']
                    data['y'] = int(i['col_4'])
                    data['drilldown'] = i['col_3']
                    x_list.append(data.copy())
                query_str = 'select * from grab_qiyu_category_status where date <\'' + str(
                    today) + '\' and date >=\'' + str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                print(body)
                html = requests.post(self._mysql_url, data=body.encode('utf-8')).json()
                for i in site_name_list:
                    data_series = {'name': '', 'id': '', 'data': []}
                    data_series['name'] = i
                    data_series['id'] = i
                    for p in html['data']:
                        if i == p['col_3']:
                            l_list = []
                            l_list.append(p['col_2'])
                            l_list.append(int(p['col_4']))
                            data_series['data'].append(l_list)
                    series.append(data_series.copy())
                return json.dumps(x_list, ensure_ascii=False), json.dumps(series, ensure_ascii=False)

            if str(chart_name) == 'site_name_image':
                site_name_list = x_list = []
                data = {'name': '', 'y': 0, 'drilldown': ''}
                query_str = 'select * from grab_qiyu_image_status where date =\'' + str(today + datetime.timedelta(days=-1)) + '\''
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                print(body)
                html = requests.post(self._mysql_url, data=body.encode('utf-8')).json()
                for i in html['data']:
                    site_name_list.append(i['col_3'])
                    data['name'] = i['col_3']
                    data['y'] = int(i['col_4'])
                    data['drilldown'] = i['col_3']
                    x_list.append(data.copy())
                query_str = 'select * from grab_qiyu_image_status where date <\'' + str(today) + '\' and date >=\'' + str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                print(body)
                html = requests.post(self._mysql_url, data=body.encode('utf-8')).json()
                for i in site_name_list:
                    data_series = {'name': '', 'id': '', 'data': []}
                    data_series['name'] = i
                    data_series['id'] = i
                    for p in html['data']:
                        if i == p['col_3']:
                            l_list = []
                            l_list.append(p['col_2'])
                            l_list.append(int(p['col_4']))
                            data_series['data'].append(l_list)
                    series.append(data_series.copy())
                return json.dumps(x_list, ensure_ascii=False), json.dumps(series, ensure_ascii=False)

            if str(chart_name) == 'site_name_qiyu_top_10':
                site_name_list = x_list = []
                data = {'name':'','y':0,'drilldown':''}
                query_str = 'select * from grab_qiyu_article_top_10 where date =\'' + str(today + datetime.timedelta(days=-1)) + '\''
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                print(body)
                html = requests.post(self._mysql_url,data=body.encode('utf-8')).json()
                for i in html['data']:
                    site_name_list.append(i['col_3'])
                    data['name'] = i['col_3']
                    data['y'] = int(i['col_4'])
                    data['drilldown'] = i['col_3']
                    x_list.append(data.copy())
                query_str = 'select * from grab_qiyu_article_top_10 where date <\'' + str(today) + '\' and date >=\'' + str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                print(body)
                html = requests.post(self._mysql_url, data=body.encode('utf-8')).json()
                for i in site_name_list:
                    data_series = {'name': '', 'id': '', 'data': []}
                    data_series['name'] = i
                    data_series['id'] = i
                    for p in html['data']:
                        if i == p['col_3']:
                            l_list = []
                            l_list.append(p['col_2'])
                            l_list.append(int(p['col_4']))
                            data_series['data'].append(l_list)
                    series.append(data_series.copy())
                return json.dumps(x_list,ensure_ascii=False),json.dumps(series,ensure_ascii=False)

        if str(_type) == 'audio':
            if str(chart_name) == 'site_name':
                query_str = 'select * from grab_qiyu_audio_status where date <=\'' + str(today) + '\' and date >=\'' + str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                html = requests.post(self._mysql_url,data=body.encode('utf-8')).json()
                if html['data'] != []:
                    site_name_list = []
                    for i in html['data']:
                        if i['col_2'] not in x_list:
                            x_list.append(i['col_2'])
                        if i['col_3'] not in site_name_list:
                            site_name_list.append(i['col_3'])
                    for i in site_name_list:
                        j = 0
                        k = len(site_name_list)
                        item['name'] = i
                        item['color'] = random.choice(color_list)
                        color_list.pop(color_list.index(item['color']))
                        flag = 0
                        for p in html['data']:
                            if x_list[j] == p['col_2']:
                                if i == p['col_3']:
                                    item['data'].append(int(p['col_4']))
                                    flag = 1
                            else:
                                j += 1
                                if flag == 0:
                                    item['data'].append(0)
                                flag = 1
                                if i == p['col_3']:
                                    item['data'].append(int(p['col_4']))
                                    flag = 1
                        if len(item['data']) +1 == len(x_list):
                            item['data'].append(0)
                        series.append(item.copy())
                        item['data'] = []
                x_list = str(x_list).replace('[\'', '').replace('\']', '')
                series = str(series).replace('\'', '"')
                return x_list,series

        if str(_type) == 'video':
            if str(chart_name) == 'site_name':
                query_str = 'select * from grab_qiyu_video_status where date <=\'' + str(today) + '\' and date >=\'' + str(today + datetime.timedelta(days=-7)) + '\' order by date ASC'
                body = '{"type":"mysql","method":"query","db_name":"crawl","body":"' + query_str + '"}'
                html = requests.post(self._mysql_url,data=body.encode('utf-8')).json()
                if html['data'] != []:
                    site_name_list = []
                    for i in html['data']:
                        if i['col_2'] not in x_list:
                            x_list.append(i['col_2'])
                        if i['col_3'] not in site_name_list:
                            site_name_list.append(i['col_3'])
                    for i in site_name_list:
                        j = 0
                        k = len(site_name_list)
                        item['name'] = i
                        item['color'] = random.choice(color_list)
                        color_list.pop(color_list.index(item['color']))
                        flag = 0
                        for p in html['data']:
                            if x_list[j] == p['col_2']:
                                if i == p['col_3']:
                                    item['data'].append(int(p['col_4']))
                                    flag = 1
                            else:
                                j += 1
                                if flag == 0:
                                    item['data'].append(0)
                                flag = 1
                                if i == p['col_3']:
                                    item['data'].append(int(p['col_4']))
                                    flag = 1
                        if len(item['data']) +1 == len(x_list):
                            item['data'].append(0)
                        series.append(item.copy())
                        item['data'] = []
                x_list = str(x_list).replace('[\'', '').replace('\']', '')
                series = str(series).replace('\'', '"')
                return x_list,series



class config():
    def __init__(self):
        self.site_name                  = ''
        self.channel                    = ''
        self.start_url                  = ''
        self.timestamp                  = 0
        self.start_web_type             = 'xpath'
        self.start_url_req_type         = 'GET'
        self.start_headers              = {}
        self.urllist_re                 = ''
        self.urllist_add                = ''
        self.urllist_xpath              = []
        self.urllist_reduce             = []
        self.imglist_xpath              = []
        self.imglist_url_add            = ''
        self.imglist_url_reduce         = []
        self.imglist_img_add            = ''
        self.imglist_img_reduce         = []
        self.img_sign                   = ''
        self.url_sign                   = ''
        self.detail_web_type            = 'xpath'
        self.detail_url_req_type        = 'GET'
        self.detail_url_headers         = {}
        self.title_re                   = ''
        self.title_xpath                = []
        self.title_add                  = ''
        self.title_reduce               = []
        self.content_re                 = ''
        self.content_xpath              = []
        self.reduce_node                = []
        self.cont_reduce                = []
        self.img_suffix                 = ''
        self.img_add                    = ''
        self.img_reduce                 = []
        self.img_time_format            = ''
        self.next_page_sign             = ''
        self.next_page_re               = ''
        self.next_page_xpath            = []
        self.next_page_reduce           = []
        self.next_page_format           = ''
        self.pubtime_re                 = ''
        self.pubtime_xpath              = []
        self.pubtime_reduce             = []
        self.pubtime_format             = ''
        self.tags_re                    = ''
        self.tags_xpath                 = []
        self.tags_reduce                = []
        self.tags_split                 = ''
        self.author_re                  = ''
        self.author_xpath               = []
        self.author_reduce              = []
        self.categories                 = []
        self.title_lowest               = 1
        self.title_is_num               = 1
        self.title_is_alphabet          = 1
        self.title_del                  = []
        self.title_string               = []
        self.content_lowest_str         = 50
        self.content_lowest_pic         = 0
        self.content_highest_pic        = 100
        self.content_del                = []
        self.image_reduce_method        = []
        self.content_string             = []
        self.content_string_node        = []


    def to_Json(self):
        p = ''
        with open('./cpsite/xpath.json','r',encoding='utf-8') as f:
            p += re.sub('\s+//.+','',f.read())
        js = json.loads(p)
        # print(js)
        js['start_url']['url']                              = self.start_url
        js['start_url']['timestamp']                        = self.timestamp
        js['start_url']['web_type']                         = self.start_web_type
        js['start_url']['request_type']                     = self.start_url_req_type
        js['start_url']['headers']                          = self.start_headers
        js['start_url']['urllist']['re']                    = self.urllist_re
        js['start_url']['urllist']['add_str']               = self.urllist_add
        js['start_url']['urllist']['xpath']                 = self.urllist_xpath
        js['start_url']['urllist']['reduce_str']            = self.urllist_reduce
        js['start_url']['imglist']['xpath']                 = self.imglist_xpath
        js['start_url']['imglist']['url_add_str']           = self.imglist_url_add
        js['start_url']['imglist']['url_reduce_str']        = self.imglist_url_reduce
        js['start_url']['imglist']['img_add_str']           = self.imglist_img_add
        js['start_url']['imglist']['img_reduce_str']        = self.imglist_img_reduce
        js['start_url']['imglist']['img_sign']              = self.img_sign
        js['detail_url']['url_sign']                        = self.url_sign
        js['detail_url']['web_type']                        = self.detail_web_type
        js['detail_url']['request_type']                    = self.detail_url_req_type
        js['detail_url']['headers']                         = self.detail_url_headers
        js['detail_url']['title']['re']                     = self.title_re
        js['detail_url']['title']['xpath']                  = self.title_xpath
        js['detail_url']['title']['add_str']                = self.title_add
        js['detail_url']['title']['reduce_str']             = self.title_reduce
        js['detail_url']['content']['re']                   = self.content_re
        js['detail_url']['content']['xpath']                = self.content_xpath
        js['detail_url']['content']['reduce_node']          = self.reduce_node
        js['detail_url']['content']['reduce_str']           = self.cont_reduce
        js['detail_url']['content']['image']['suffix']      = self.img_suffix
        js['detail_url']['content']['image']['add_str']     = self.img_add
        js['detail_url']['content']['image']['reduce_str']  = self.img_reduce
        js['detail_url']['content']['image']['time_format'] = self.img_time_format
        js['detail_url']['next_page']['sign']               = self.next_page_sign
        js['detail_url']['next_page']['re']                 = self.next_page_re
        js['detail_url']['next_page']['xpath']              = self.next_page_xpath
        js['detail_url']['next_page']['reduce_str']         = self.next_page_reduce
        js['detail_url']['next_page']['next_page_format']   = self.next_page_format
        js['detail_url']['pubtime']['re']                   = self.pubtime_re
        js['detail_url']['pubtime']['xpath']                = self.pubtime_xpath
        js['detail_url']['pubtime']['reduce_str']           = self.pubtime_reduce
        js['detail_url']['pubtime']['time_format']          = self.pubtime_format
        js['detail_url']['tags']['re']                      = self.tags_re
        js['detail_url']['tags']['xpath']                   = self.tags_xpath
        js['detail_url']['tags']['reduce_str']              = self.tags_reduce
        js['detail_url']['tags']['split_str']               = self.tags_split
        js['detail_url']['author']['re']                    = self.author_re
        js['detail_url']['author']['xpath']                 = self.author_xpath
        js['detail_url']['author']['reduce_str']            = self.author_reduce
        js['detail_url']['categories']                      = self.categories
        js['detail_url']['site_name']                       = self.site_name
        js['detail_url']['channel']                         = self.channel
        js['config_clean']['title']['filter_type']['lowest_str']        = self.title_lowest
        js['config_clean']['title']['filter_type']['is_num']            = self.title_is_num
        js['config_clean']['title']['filter_type']['is_alphabet']       = self.title_is_alphabet
        js['config_clean']['title']['filter_type']['delstr']            = self.title_del
        js['config_clean']['title']['string']                           = self.title_string
        js['config_clean']['content']['filter_type']['lowest_str']      = self.content_lowest_str
        js['config_clean']['content']['filter_type']['lowest_pic']      = self.content_lowest_pic
        js['config_clean']['content']['filter_type']['highest_pic']     = self.content_highest_pic
        js['config_clean']['content']['filter_type']['delstr']          = self.content_del
        js['config_clean']['content']['image']                          = self.image_reduce_method
        js['config_clean']['content']['string']                         = self.content_string
        js['config_clean']['content']['string_node']                    = self.content_string_node
        print(js)
        # js_str = json.dumps(js,ensure_ascii=False)
        js_str = json.dumps(js,ensure_ascii=False).replace('\"[','[').replace(']\"',']').replace('\\\"','"').replace('[\'','["').replace('\'],','\"],').replace('\',\'','","').replace('\"{}\"','{}')
        #print(js_str)
        return js_str

if __name__=='__main__':
    a = SiteChannelOperate()
    # a.query_es_list('搜狐搞笑','搞笑','')
    # a.query_es_list('','','20190401113159358565')
    # a.chart_opt('video','site_name')
    a.chart_opt('all','from_source')
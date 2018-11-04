#!/usr/bin/python
# -*- coding: UTF-8 -*-
#cookie为sfacg.com下'.SFCommunity'的值
#url为sf文章链接
import sys

reload(sys) 
sys.setdefaultencoding('utf8')
def sfnext(url):
    import re,urllib2
    html=urllib2.urlopen(urllib2.Request(url)).read()
    xyz1 =re.search('class="btn normal">下一章</a>', html, flags=0).span()
    xyz1=xyz1[0]
    xyz=html[:xyz1]
    xyz=xyz[-40:]
    xyz2=re.search('=',xyz,flags=0).span()
    xyz2=xyz2[1]
    xyz=xyz[xyz2:]
    xyz=xyz[1:][:-2]
    xyz="http://book.sfacg.com"+xyz
    return xyz
def sflast(url):
    import re,urllib2
    html=urllib2.urlopen(urllib2.Request(url)).read()
    syz1 = re.search('class="btn normal">上一章</a>', html, flags=0	).span()
    syz1=syz1[0]
    syz=html[:syz1]
    syz=syz[-200:]
    syz2=re.search('<a href=',syz,flags=0).span()
    syz2=syz2[1]
    syz=syz[syz2:]
    syz=syz[1:][:-2]
    syz="http://book.sfacg.com"+syz
    return syz
def sf (url,cookie):
    import re
    nv=re.search("Novel",url)
    vip=re.search("vip",url)
    if vip !=None:
        ret=sfvip(url,cookie)
    if nv !=None:
        ret=sfnv(url)
    return ret
def sfnv(url):
    import urllib2,re
    html=urllib2.urlopen(urllib2.Request(url)).read()

    nr1 = re.search('<div class="article-hd">', html, flags=0).span()
    nr1 = nr1[1]
    nr = html[nr1:]

    nr2 = re.search('</div>', nr, flags=0).span()
    nr2 = nr2[0]
    nr = nr[:nr2]

    bt1 = re.search('<h1 class="article-title">', nr, flags=0).span()
    bt1 = bt1[1]
    bt = nr[bt1:]
    a = re.search('<div class="article-content font16" id="ChapterBody" data-class="font16">', html, flags=0).span()
    b = a[-1]
    c = html[b:]
    ccc = re.search('<p>', c, flags=0).span()
    ccc = ccc[0]
    ccc = ccc - 7
    c = c[ccc:]
    d = re.search("</div>", c, flags=0).span()
    e = d[0]
    f = c[:e]
    bb = re.sub("</p>", "\n       ", f, count=0, flags=0)
    bb = re.sub("<p>", "", bb, count=0, flags=0)
    bb = re.sub("<br>", "", bb, count=0, flags=0)
    ret="----------------"+bt+"-------------------\n"+bb+"--------------------end---------------"
    return ret

def sfvip(url,cookie):
    import urllib2
    import time
    import urllib
    import json
    import hashlib
    import base64
    import re
    import requests
    import os
    from requests.cookies import RequestsCookieJar
# encoding=utf8 
    jar=RequestsCookieJar()
    jar.set('.SFCommunity',cookie,domain="sfacg.com",path='/')
    aa={'UserAgent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    }
    request=requests.get(url,headers=aa,cookies=jar)
    #print(request.text)
    html=request.text
    #获取文章信息
    nr1 = re.search('<div class="article-hd">', html, flags=0).span()
    nr1 = nr1[1]
    nr = html[nr1:]
    nr2 = re.search('</div>', nr, flags=0).span()
    nr2 = nr2[0]
    nr = nr[:nr2]
    bt1 = re.search('<h1 class="article-title">', nr, flags=0).span()
    bt1 = bt1[1]
    bt = nr[bt1:]
    bt2 = re.search('</h1>', bt, flags=0).span()
    bt2 = bt2[0]
    bt = bt[:bt2]
    wjm=bt
    #获取正文图片
    u=re.search("<img id='vipImage' src='/ajax/ashx/common.ashx?",html).span()
    if (re.search("<img id='vipImage' src='/ajax/ashx/common.ashx?",html)=="None"):
        print "获取失败此为vip章节，请确定你是否已经订阅该章节或者cookie是否正确。"
        input ("回车退出...")
        exit()
    html=html[u[1]:]
    n=re.search("' />",html).span()
    html=html[:n[0]]
    picurl='http://book.sfacg.com/ajax/ashx/common.ashx'+html
    #os.system('mkdir ~/sf/')
    html_str = requests.get(picurl,headers=aa,cookies = jar).content
    # 写入文件,采用二进制写入文件
    with open("./sf/"+wjm+".ashx",'wb') as f:
        f.write (html_str)
    #图片转文字
    os.system("ffmpeg -y -i './sf/"+wjm+".ashx' './sf/"+wjm+".jpg'")
    f = open("./sf/"+wjm+".jpg", 'rb')
    file_content = f.read()
    base64_image = base64.b64encode(file_content)
    body = urllib.urlencode({'image': base64_image})
    url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/recognize_document'
    api_key = '04899a747b0c2a9a8ab1001d75c9929e'
    param = {"engine_type": "recognize_document"}
    x_appid = '5bdd2410'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    result=eval(result)
    data=result["data"]
    data=data['document']
    data=data['blocks']
    zw=''
    for d in data:
        zw= zw+d['lines'][0]['text']+'\n'
    ret="----------------"+bt+"----------------\n(本文为vip章节，文字为讯飞图片转文字后结果可能会有不准确。)\n（原图片请在sf文件夹下查看)\n"+zw+"\n---------------end--------------"
    return ret

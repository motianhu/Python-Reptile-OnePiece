#!/usr/bin/python
# coding=utf-8
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

rootPath = '/home/motianhu/Desktop/onepiece/'
rootUrl = "https://manhua.fzdm.com/02/"

def haizeiwangPages(url):
    jujipages = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.1 (KHTML, like Gecko) '
                      'Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'
    }
    # get从网页获取信息
    requests.packages.urllib3.disable_warnings()
    res = requests.get(url, headers=headers, verify=False)
    # 解析内容
    soup = BeautifulSoup(res.content.decode('utf-8'), 'html5lib')
    juji_divs = soup.find_all('li', class_='pure-u-1-2 pure-u-lg-1-4')
    for juji_div in juji_divs:
        juji_as = juji_div.find_all('a')
        for juji_a in juji_as:
            if juji_a.has_attr("href"):
                jujipage = []
                print(juji_a)
                # 标题
                jujipage.append(juji_a.get_text())
                # 超链接
                jujipage.append(juji_a['href'])
                jujipages.append(jujipage)
    return jujipages


def haizeiwangPage(title, urlMiddlePath, suffix):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.1 (KHTML, like Gecko) '
                      'Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'
    }
    # get从网页获取信息
    requests.packages.urllib3.disable_warnings()
    webUrl = rootUrl + urlMiddlePath + suffix
    res = requests.get(webUrl, headers=headers, verify=False)
    soup = BeautifulSoup(res.content.decode('utf-8'), 'html5lib')

    # 匹配图片地址和图片主机
    patternAddr = re.compile(r'mhurl="(.*?)"', re.I | re.M)
    patternHost = re.compile(r'{mhss="(.*?)"}', re.I | re.M)

    for script in soup.findAll('script'):
        addr = patternAddr.findall(str(script))
        host = patternHost.findall(str(script))
        if len(addr) and len(host):
            fileDir = rootPath + title
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            print host[0] + "/" + addr[0]
            downloadPic(fileDir, addr[0], 'http://' + host[0] + "/" + addr[0])


def downloadPic(fileDir, path, url):
    print url
    path = path.replace('.jpg', '.png')
    imgPath = fileDir + '/' + path.replace('/', '_')
    print imgPath
    r = requests.get(url)
    with open(imgPath, 'wb') as f:
        f.write(r.content)


def getPicByPage(urls):
    for page in urls:
        haizeiwangPage(page + page[1] + 'index_1.html')


# 主函数
def main():
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print sys.getdefaultencoding()

    if not os.path.exists(rootPath):
        os.makedirs(rootPath)

    # 获取海贼王所有集数
    # jujipages[u'海贼王952话', u'952/']
    jujipages = haizeiwangPages(rootUrl)
    #[u'海贼王952话', u'952/']
    # 遍历每一集
    for jujipage in jujipages:
        haizeiwangPage(jujipage[0], jujipage[1], '')
        for i in range(1, 20):
            haizeiwangPage(jujipage[0], jujipage[1], '/index_' + str(i) + '.html')


if __name__ == '__main__':
    main()

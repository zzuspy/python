#-*-coding:utf-8-*-

import re
import urllib
import requests
import HTMLParser
import os


base_path = r'/home/dqj/picture/crawler/'

def judge(path) :
    if not os.path.exists(path) :
        os.mkdir(path)

class crawler:

    def __init__(self, url) :
        self.url = url

    def itoa(self, x) :
        if x < 10 :
            return '0' + str(x)
        else :
            return str(x)

    def find_all_pic_set(self) :    
        html = requests.get(self.url).text
        #获取美女相册的URL和标题
        pic_set_list = re.findall(r'jpg\' /></a><span><a href="(.*?)" target="_blank">(.*?)</a></span><span', html)
        #for each in pic_set_list :
            #print each[0] + " " + each[1]
        return pic_set_list

    def download(self, num, lurl, rurl, path) :
        judge(path)
        for i in range(1, num + 1) :
            down_url = lurl + self.itoa(i) + rurl
            pic_name = re.search( r'[0-9]{2}[a-z][0-9]{2}.jpg', down_url).group(0)
            print pic_name + " is loading"
            urllib.urlretrieve(down_url, '%s%s' % (path, pic_name) )
            
    def run(self) :
        pic_set_list = self.find_all_pic_set()
        judge(base_path)
        for pic_set in pic_set_list :
            url = pic_set[0]
            title = pic_set[1]
            html = requests.get(url=url).text
            path = base_path + title + '/'
            tmp = re.findall( url + '/[0-9]{2}', html)
            num = int(tmp[0][-2:])
            down_url = re.search( r'http://i.meizitu.net/20.*jpg', html).group(0)
            lurl = down_url[0:-6]
            rurl = down_url[-4:]
            print "download to :  " + path + "\nnums of picture :  " + str(num) + "\naddress of download :  " + url
            self.download(num, lurl, rurl, path)
            print "\n"
        print 'this is ok!'



'''
本代码爬取网站http://www.mzitu.com/的图片

这里是通过图片的url进行下载。

根据给出的url下载当前页面所有出现的美女目录的图片
'''

if __name__ == '__main__' :
    url = 'http://www.mzitu.com/hot'
    crawlers = crawler(url)
    crawlers.run()


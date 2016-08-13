#-*-coding:utf-8-*-

import re
import urllib

class crawler:

    def itoa(self, x) :
        if x < 10 :
            return '0' + str(x)
        else :
            return str(x)

    def download(self, num, lurl, rurl, location) :
        for i in range(1, num + 1) :
            url = lurl + self.itoa(i) + rurl
            pic_name = re.search( r'[0-9]{2}[a-z][0-9]{2}.jpg', url).group(0)
            print pic_name + " is loading"
            urllib.urlretrieve(url, '%s%s' % (location, pic_name) )
            



'''
本代码爬取网站http://www.mzitu.com/的图片

这里是通过图片的url进行简单的下载。
lurl,rurl指明图片地址
location指明下载位置。
'''

if __name__ == '__main__' :
    crawlers = crawler()
    
    lurl = 'http://i.meizitu.net/2016/08/11b'
    rurl = '.jpg'
    location = '/home/dqj/picture/crawler/xialingmang/'
    num = 50

    crawlers.download(num, lurl, rurl, location)

#-*-coding:utf-8-*-

'''
这是一个简单的图片爬虫程序
'''

import re
import urllib
import urllib2

class crawler:
    def getHTML(self, url) :
        page = urllib.urlopen(url)
        #html = urllib2.urlopen(urllib2.Request(url)).read()
        html = page.read()
        return html

    def getPic(self, html) :
        rule = r'img src="(.*?)"'
        pic = re.compile(rule)
        pics = re.findall(pic, html)
        for each in pics:
            print each
        return pics

    def download(self, pics) :
        cnt = 1
        for each in pics :
            print '%s loading ...' % each
            urllib.urlretrieve(each, './picture/%02s.jpg' % cnt)
            cnt = cnt + 1

    def run(self, url) :
        html = self.getHTML(url)
        pics = self.getPic(html)
        self.download(pics)


if __name__ == '__main__' :
    crawlers = crawler()
    crawlers.run('http://qz.100bt.com/touxiang/76410.html')
    


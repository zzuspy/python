#-*-coding:utf-8-*-

import re
import requests
import HTMLParser
import getpass
import os

#代码保存目录
if not os.path.exists('./POJ_code'):
    os.mkdir(r'./POJ_code')
base_path = r'./POJ_code/'



# 代码语言判断	
def lan_judge(language) :
    if language == 'G++':
	suffix = '.cpp'
    elif language == 'GCC':
	suffix = '.c'
    elif language == 'C++':
	suffix = '.cpp'
    elif language == 'C':
	suffix = '.c'
    elif language == 'Pascal':
	suffix = '.pas'
    elif language == 'Java':
	suffix = '.java'
    else:
	suffix = '.cpp'
    return suffix


class crawler : 

    def __init__(self, user, password) :

        # 一些url
        self.poj = 'http://poj.org/'
        self.post_url = 'http://poj.org/login'
        self.status_url = 'http://poj.org/status?result=0&user_id='
        self.code_url = 'http://poj.org/showsource?solution_id='
        
        # 一些规则
        self.runid_rule = re.compile(r'<tr align=center><td>(.*?)</td>', re.S)
        self.code_rule = re.compile(r'<pre class="sh_cpp" style="font-family:Courier New,Courier,monospace">(.+?)</pre>', re.S)
        self.lan_rule = re.compile(r'<td><b>Language:</b> (.*?)</td>', re.S)
        self.problem_rule = re.compile(r'<a href="problem\?id=(.*?)">', re.S)
        self.nexturl_rule = re.compile(r'Previous Page(.*?)<a href=(.*?)><font (.*?)Next Page', re.S)

        self.user = user
        self.password = password
        self.session = requests.session()
        self.cookies = dict(cookies_are='working')
        self.postData = {'user_id1':self.user, 'password1': self.password, 'B1' : 'login', 'url' : '.'}

    def login(self) :
        reponse = self.session.post(self.post_url, data=self.postData, cookies=self.cookies)
        #print reponse.text
    
    def download_code(self) :
        
        html_parser = HTMLParser.HTMLParser()

        status_url = self.status_url + self.user
        status_html = self.session.get(status_url, cookies=self.cookies).text

        while( True ) :
            
            print status_url
            #print status_html
            runid_list = self.runid_rule.findall(status_html)
            
            print len(runid_list)

            if len(runid_list) < 1 : 
                break
            
            for runid in runid_list : 
                #print runid
                code_url = self.code_url + runid
                code_html = self.session.get(code_url, cookies=self.cookies).text
                
                code = self.code_rule.search(code_html).group(1)
                code = html_parser.unescape(code).encode('utf-8')
                language = self.lan_rule.search(code_html).group(1)
                problemid = self.problem_rule.search(code_html).group(1)
                suffix = lan_judge(language)
                problem = 'poj' + problemid + suffix
                print 'runid: ' + runid + "----> " + problem + " is downloding..."
                open( base_path + problem, 'wb').write(code)
            
            print ''
            status_url = self.nexturl_rule.search(status_html).group(2)
            status_url = self.poj + status_url
            status_html = self.session.get(status_url, cookies=self.cookies).text
        
        print 'this is ok!'


    def run(self) :
        print '正在登陆POJ...'
        self.login()
        self.download_code() 



if __name__ == '__main__' :
    user = raw_input('input your username : ')
    password = getpass.getpass('input your password : ')
    
    work = crawler(user, password)
    work.run()



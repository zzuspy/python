#-*-coding:utf-8-*-

import re
import requests
import HTMLParser
import getpass
import os

# 代码保存目录
if not os.path.exists('./HDU_code'):
	os.mkdir(r'./HDU_code')
base_path = r'./HDU_code/'


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

    def __init__ (self, user, password) :
        #一些url
        self.host_url = r'http://acm.hdu.edu.cn/'
        self.post_url = r'http://acm.hdu.edu.cn/userloginex.php?action=login'
        self.status_url = 'http://acm.hdu.edu.cn/status.php?user='
        self.codebase_url = 'http://acm.hdu.edu.cn/viewcode.php?rid='
        
        # 正则表达式的一些匹配规则
        self.runid_rule = re.compile(r'<tr.*?align=center ><td height=22px>(.*?)</td>.*?</tr>',re.S)
        self.code_rule = re.compile(r'<textarea id=usercode style="display:none;text-align:left;">(.+?)</textarea>',re.S)
        self.lan_rule = re.compile(r'Language : (.*?)&nbsp;&nbsp',re.S)
        self.problem_rule = re.compile(r'Problem : <a href=.*?target=_blank>(.*?) .*?</a>',re.S)
        self.nextpage_rule = re.compile(r'Prev Page</a><a style="margin-right:20px" href="(.*?)">Next Page ></a>',re.S) 

        self.user = user
        self.password = password
        self.s = requests.session()
        self.cookies = dict(cookies_are='working')
        self.postData = {'username' : self.user , 'userpass' : self.password , 'login' : 'Sign In'}


    def login_HDUOJ(self) :
        response = self.s.post(self.post_url, data=self.postData, cookies=self.cookies)
        #print response.text
    

    def download_code(self) :
        
        # 用于处理html中的转义字符
	html_parser = HTMLParser.HTMLParser()
        
        status_url = self.status_url + self.user + '&status=5'
        status_html = self.s.get(status_url, cookies=self.cookies).text
        #print self.status_html
        
        while( True ) :
                runid_list = self.runid_rule.findall(status_html)

		for id in runid_list:
			code_url = self.codebase_url + id
			down_html = self.s.get(code_url,cookies=self.cookies).text

			down_code = self.code_rule.search(down_html).group(1)
			language = self.lan_rule.search(down_html).group(1)
			problemid = self.problem_rule.search(down_html).group(1)

			suffix = lan_judge(language)
			code = html_parser.unescape(down_code).encode('utf-8')
			code = code.replace('\r\n','\n')
			problem = 'hdu' + problemid + suffix
                        print problem + ' is downloading...'
                        open( base_path + problem,"wb").write(code)
		
		nexturl = self.nextpage_rule.search(status_html)
		if nexturl == None:
			break
		else:
			status_url = self.host_url + nexturl.group(1)
			status_html = self.s.get(status_url, cookies=self.cookies).text
        print 'this is ok!'


    def run(self) :
        print '正在登陆HDUOJ...'
        self.login_HDUOJ()
        self.download_code()
        



if __name__ == '__main__' : 
    user = raw_input('input your username : ')
    password = getpass.getpass('input your password : ')

    work = crawler(user, password)
    work.run()




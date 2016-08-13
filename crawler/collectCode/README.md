#利用Python爬取OJ上的代码（HDU，POJ）
###运行环境：
- ubuntu 14.04
- 需安装python2.7和API requests

###代码思想
- 首先模拟浏览器登陆OJ (我这里用的request,直接调用即可)
- 然后根据Solved Problem的那个status界面，利用正则表达式找出当前页所有ac的代码的runid
- 根据runid可以得到每个ac源代码
- 然后是换页，根据正则表达式找Next Page的URL，重复上面步骤，直到runid_list==0即可

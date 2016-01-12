#using this programme to login Sina WeiBo using Python 
#Writer:bjyhappy
#email:513431626@qq.com 

#coding=utf8
import rsa
import base64
import urllib2
import urllib
import re
import binascii
import cookielib

def WeiBo_Login(username, password):
    #get servertime,nonce,pubkey
    pubkey = ('EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC25306288'
          '2729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B35'
          '3F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A9'
          '28EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443')

    username = urllib.quote(username)
    username = base64.encodestring(username)[:-1]

    loginserver = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
    getfromserver = urllib2.urlopen(loginserver).read()

    regex = '({.+})'
    pattern = re.compile(regex)

    dict_info = eval(re.findall(pattern, getfromserver)[0])
    servertime = dict_info['servertime']
    nonce = dict_info['nonce']
    rsakv = dict_info['rsakv']

    #get encrypted password
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key) #加密
    passwd = binascii.b2a_hex(passwd)

#create postdata

    postdata = urllib.urlencode({
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        #'ssosimplelogin': '1',
        'pagerefer':'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
        'vsnf': '1',
        #'vsnval': '',
        'su': username,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv' : rsakv,
        'sp': passwd,
        'sr':'1366*768',
        'encoding': 'UTF-8',
        'prelt': '116',        
        'url': 'http://weibo.com/ajaxlogin.php?',
        'returntype': 'META'
    })
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

 # try to login
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    request = urllib2.Request(login_url,data = postdata,headers = headers)
    status = urllib2.urlopen(request).read()

    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    redirect = re.search("location.replace\('(.+)'\)", status)

    data = opener.open(redirect.groups()[0])
    print 'login successful'
    
if __name__ =='__main__':
    username = raw_input("please enter username:")
    password = raw_input("please enter password:")
    WeiBo_Login(username, password)

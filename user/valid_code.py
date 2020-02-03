# -*- coding: utf-8 -*-
import user.zhenzismsclient as smsclient
import random
code = ''
for num in range(1,7):
    code = code + str(random.randint(0, 9))
print(code)
client = smsclient.ZhenziSmsClient('http://sms_developer.zhenzikj.com','100931','ca7f2b7c-1778-4ef4-abc9-fa0206f499eb')
print(client.send('18270555672', '校园咨询网站欢迎您注册，您的验证码为'+code))

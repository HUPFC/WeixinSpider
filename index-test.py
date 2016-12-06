# -*- coding: utf-8 -*-

# python index-test.py 冷兔小行星 | tee -a log1.txt
import time
from urllib.parse import unquote

from lib.common import common
from weixin.sougouspider import SgWxSpider
import sys

key = unquote(sys.argv[1])
env = sys.argv[2]
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' start :'+key+" md5:"+common.md5(key))
if key :
    s = SgWxSpider(key,env)
    try:
        s.start()
    except:
        s.quit()
    print('success')
else:
    print('关键字不能为空')
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' end :'+key+" md5:"+common.md5(key))
exit()

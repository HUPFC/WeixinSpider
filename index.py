# -*- coding: utf-8 -*-
import time
from urllib.parse import unquote

from lib.common import common
from weixin.sougouspider import SgWxSpider
import sys

key = unquote(sys.argv[1])
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' start :'+key+" md5:"+common.md5(key))
if key :
    s = SgWxSpider(key,'prod')
    try:
        s.start()
        s.quit()
        print('success')
    except:
        print('error')
        s.quit()
else:
    print('关键字不能为空')
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' end :'+key+" md5:"+common.md5(key))
exit()

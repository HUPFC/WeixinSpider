# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import json
import random
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, sys

sys.path.append(os.getcwd()+'/../')
from weixin.dom import Dom
from lib.redisclass import RedisClass
from lib.common import common

'''
selenium chardet

create hupeng
time 20161017
搜狗微信爬虫
type 1 关键词爬取 通过微信搜狗浏览器首页输入关键字进行爬取
'''
class SgWxSpider(Dom):
    driver = False
    redis = False
    redis_key_pre = 'wx_'
    phantomjs_conf = {
        'dev':'phantomjs',
        #'test':'/Data/local/phantomjs-2.1/bin/phantomjs',
        #'prod':'/Data/local/phantomjs-2.1.1/bin/phantomjs',
    }
    key = False
    env = False

    def __init__(self,key,env):
        #获取参数
        self.key = key
        self.env = env

        #连接redis
        env_redis = RedisClass(self.env)
        self.redis = env_redis.get_conn()

        md5 = common.md5(self.key)
        #获取redis key
        self.wx_unique = self.redis_key_pre+'unique_'+md5
        self.wx_progress = self.redis_key_pre+'progress_'+md5
        self.wx_result = self.redis_key_pre+'result_'+md5


    def start(self):
        if self.redis == False:
            print('redis连接异常')
            return False

        self.send_progress(300, '正在打开浏览器')
        #dcap = dict(DesiredCapabilities.PHANTOMJS)
        ua = common.pcAgent()
        #ip1 = common.rand_ip()
        #ip2 = common.rand_ip()
        dcap = {
            "javascriptEnabled":True,
            "phantomjs.page.settings.userAgent":ua,
            'phantomjs.page.settings.loadImages':False,
            #'phantomjs.page.customHeaders.X-FORWARDED-FOR':ip1,
            #'phantomjs.page.customHeaders.CLIENT-IP':ip2,
        }

        proxy = [
            '--proxy=127.0.0.1:8888',
            '--proxy-type=http',
            '--ignore-ssl-errors=true',
            '--ssl-protocol=tlsv1'
        ]
        proxy = []
        self.driver = webdriver.PhantomJS(executable_path=self.phantomjs_conf[self.env],desired_capabilities=dcap)#,service_args=proxy)
        self.driver.set_window_size(1366,768)
        self.driver.implicitly_wait(25)
        self.sleep_random(1,3)
        self.send_progress(300,'正在打开首页')
        if self.search() == False:
            self.send_progress(500,'首页搜索打开失败')
            self.quit()
            return False

        self.send_progress(300, '开始输入关键字')
        if self.get_wx_info() == False:
            self.send_progress(500,'搜索页打开失败')
            self.quit()
            return False

        self.send_progress(300, '正在获取列表')
        if self.get_wx_list() == False:
            self.send_progress(500,'列表页打开失败')
            self.quit()
            return False

        self.quit()
        return True

    def search(self):
        self.driver.get(self.url)
        #url = 'http://weixin.sogou.com/weixin?type=1&query=' + str(self.key) + '&ie=utf8&_sug_=n&_sug_type_='
        #self.driver.get(url)
        #return True
        try:
            locator = (By.CLASS_NAME,self.element['index']['button']['class'])
            locator = (By.ID, self.element['index']['input']['id'])
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located(locator)) #智能元素等待死循环 原因未知
            self.sleep_random(6,8)
            self.send_progress(300, '开始搜索')
            try:
                self.sleep_random(1, 1)
                self.driver.find_element_by_id(self.element['index']['input']['id']).send_keys(self.key)
                self.sleep_random(1,1)
                self.driver.find_element_by_class_name(self.element['index']['button']['class']).click()
                self.sleep_random()
            except Exception as err:
                print(err)
                url = 'http://weixin.sogou.com/weixin?type=1&query='+str(self.key)+'&ie=utf8&_sug_=n&_sug_type_='
                print(url)
                self.driver.get(url)
                self.sleep_random()
            return True
        except Exception as err:
            print(err)
            self.screen()
            return False

    def get_wx_info(self):
        try:
            self.sleep_random(6,7)
            locator = (By.CLASS_NAME,self.element['search']['class'])
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located(locator))
            first = self.driver.find_element_by_xpath('//*[@class="news-box"]/ul/li[1]/div/div[2]/p/a').click()
            self.sleep_random()
            return True
        except Exception as err:
            print(err)
            self.screen()
            return False

    def get_wx_list(self):
        try:
            self.switch_window()
            self.sleep_random(6,8)
            list = self.driver.find_element_by_class_name(self.element['list']['class']).get_attribute('innerHTML')
            dic = {
                'url':self.driver.current_url,
                'list':list
            }
            str = json.dumps(dic,ensure_ascii=False)
            self.send_progress(300,'存储数据')
            self.send_redis(200,str)
            print('send_redis')
            return True
        except Exception as err:
            print(err)
            self.screen()
            return False

    def switch_window(self):
        current = self.driver.current_window_handle
        all = self.driver.window_handles
        for handle in all:
            if handle!= current:
                print('switch_windows success')
                self.driver.switch_to.window(handle)
                break
            else:
                print('switch_windows error')

    def send_redis(self,code,msg):
        self.redis.set(self.wx_result,msg,ex=3600*2)


    def send_progress(self,code,msg):
        dic = {
            'code': code,
            'msg': msg
        }
        str = json.dumps(dic, ensure_ascii=False)
        print(str)
        #self.redis.rpush(self.wx_progress,str)

    def sleep_random(self,start=2,end=4):
        num = random.uniform(start,end)
        print('sleep:'+str(num))
        time.sleep(num)

    def quit(self):
        print('退出浏览器')
        self.driver.quit()

    def screen(self,key=False):
        if self.env != 'prod':
            if key == False:
                key = self.wx_unique
            name = 'screen/'+key+ '.jpg'
            self.driver.get_screenshot_as_file(name)
        return True




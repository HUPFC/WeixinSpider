# WeixinSpider
       搜狗微信爬虫，模拟浏览器打开搜狗微信首页，填入关键字key，查询微信公众号，进入公众号信息列表页,并将列表页源码保存到redis。

1.简单执行
```
py index-dev.py 'key' 'prod|dev|testing'

```

2.环境依赖
```
	python3.5(redis selenium库)
	phantomjs (phantomjs执行路径配置在weixin/sougouspider)
	redis服务端 (redis配置在lib/redisclass)
```

3.已知问题&待改进功能
```
    1.selenium驱动click失去焦点BUG
    2.配置项需要统一管理
    3.只获取了列表页源码,详细内容需开发其他脚本获取
```
	

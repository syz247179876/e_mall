# 吃或商城

## **Version 1.0🐡：**

🐳基于后端框架Django和前端框架amazeui的前后段不分离开发。

🐉2020年4月2日---5月25日（已完成）


💃开发使用到的技术栈：Django+amzeui+layui+jquery+redis+celery+websocket+whoosh+mysql


🕺部署服务器用到的技术栈：nginx+uwsgi+channels


🤸一些第三方的服务：阿里云云服务器（学生机） + OSS + OCR身份识别 + 阿里云短信服务


🐠服务管理工具：supervisor

---

## **Version 2.0🐙：**

🐋重构Version1.0，基于后端框架Django+接口框架Django-Restful-Framework框架（正在开发，目前已开发80%的功能），前端欲打算使用Vue框架（才刚动工）,实现前后段分离式开发。


🐲2020年6月5日-----目前（正在开发中）


💃开发使用到的技术栈：Django+DRF+Vue+Jquery+Redis+Celery+Rabbitmq+Elasticsearch+Websocket+Mysql+Fastdfs+JWT


🕺部署服务器用到的技术栈：nginx+uwsgi+channels


🤸一些第三方的服务：阿里云云服务器（学生机） + OSS + OCR身份识别 + 阿里云短信服务


🐠服务管理工具：supervisor

---
#### **🥳主要修改🥳：**

1.传统前后端不分离===>基于restful风格接口开发  👀

2.whoosh搜索后端====>elasticsearch搜索后端👀

3.django自带的模板语言====>前端使用vue前端框架👀

4.由原来的redis作为消息队列====>增加消息队列rabbitmq👀

5.django默认的Storage本地存储=====>分布式fastdfs存储

6.django默认的传统session认证=====>JWT算法认证

---
#### **🥶目前已完成的功能🥶：**

目前已开发43个API

包括：

1.用户个人信息相关API
  
  (1) 绑定手机号
  
  (2) 修改个人用户名
  
  (3) 获取用户个人信息
  
  



1.基于JWT的会员用户民或邮箱登录。

2.基于JWT的商家登录。

3.基于OCR身份证识别的商家注册。

3.首页商品流加载显示

4.基于whoosh搜索引擎的搜索实现

5.基于alipay的支付功能

6.基于redis实现的收藏夹和购物车的显示

7.添加收藏夹

8.添加购物车

9.个人信息浏览修改

10.改绑手机

11.改绑邮箱

12.会员实名验证

13.订单状态浏览

14.下订单

15.添加删除收货地址，修改默认地址

16.基于celery的异步短信验证



### **个人技术博客**

  https://syzzjw.cn

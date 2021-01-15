# RMIPortScan
基于python的RMI分布式简易端口扫描工具



## 实现原理

子节点通过部署server.py 程序,向nsServer名称服务器注册节点

然后通过scheduler.py 根据端口数目进行均匀调度各个子节点来进行扫描。



## 效果如下

![image-20210115205044591](README.assets/image-20210115205044591.png)
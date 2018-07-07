# housespider
使用Scrapy,Redis,MongoDB实现的一个分布式网络爬虫,底层存储MongoDB,分布式使用Redis实现

## 摘要

基于 Python 分布式房源数据抓取系统为数据的进一步应用即房源推荐系统做数据支持。致力于解决单进程单机爬虫的瓶颈，打造一个基于 Redis 分布式多爬虫共享队列的主题爬虫。本系统采用 Python 开发的 Scrapy 框架来开发，使用 Xpath 技术对下载的网页进行提取解析，运用 Redis 数据库做分布式，使用MongoDB 数据库做数据存储，利用 Django web 框架对数据进行友好可视化，最后使用了Docker对爬虫程序进行部署。主要是针对 58 同城各大城市租房平台的分布式爬虫系统。

>  可视化和Docker部署将放在后面一段时间完成

## 系统分布式架构

分布式采用主从结构设置一个Master服务器和多个Slave服务器，Master端管理Redis数据库和分发下载任务，Slave部署Scrapy爬虫提取网页和解析提取数据，最后将解析的数据存储在同一个MongoDB数据库中 。

应用Redis数据库实现分布式抓取，基本思想是Scrapy爬虫获取的到的detail_request的urls都放到Redis Queue中，所有爬虫也都从指定的Redis Queue中获取requests，Scrapy-Redis组件中默认使用SpiderQueue来确定url的先后次序。因此，待爬队列的共享是爬虫可以部署在其他服务器上完成同一个爬取任务的一个关键点。为了解决Scrapy单机局限的问题，Scrapy将结合Scrapy-Redis组件进行开发，Scrapy-Redis总体思路就是这个工程通过重写Scrapu框架中的scheduler和spider类，实现了调度、spider启动和redis的交互。实现新的dupefilter和queue类，达到了判重和调度容器和redis的交互，因为每个主机上的爬虫进程都访问同一个redis数据库，所以调度和判重都统一进行统一管理，达到了分布式爬虫的目的。 在本系统中Scrapy-Redis组件是采用[崔庆才](https://cuiqingcai.com/)老师的[ScrapyRedisBloomFilter](https://github.com/Python3WebSpider/ScrapyRedisBloomFilter),ScrapyRedisBloomFilter做了Bloom Filter(**布隆过滤器** )集成

## 运行

1. Master

   在项目中找到main.py文件，直接运行

2. Slave

   在项目中找到start.py文件，直接运行（可启动多个）


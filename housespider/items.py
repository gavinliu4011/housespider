# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class HouseItem(scrapy.Item):
    collection = 'houses'

    id = Field()
    # 帖子名称
    title = Field()
    # 租金
    money = Field()
    # 租赁方式
    method = Field()
    # 所在区域
    area = Field()
    # 所在小区
    community = Field()
    # 帖子详情url
    targeturl = Field()
    # 帖子发布时间
    pub_time = Field()
    # 所在城市
    city = Field()
    # 联系电话
    phone = Field()
    # 图片1
    image = Field()

    crawled_at = Field()


class MasterRedisItem(scrapy.Item):
    url = scrapy.Field()

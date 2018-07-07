# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re, time

import logging
import pymongo
import redis

from housespider.items import HouseItem, MasterRedisItem


class TimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HouseItem):
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = now
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[HouseItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, HouseItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        return item


class RedisLinJiaPipeline(object):

    def __init__(self, host='localhost', port=6379,
                 db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            db=crawler.settings.get('REDIS_DB'),
            password=crawler.settings.get('REDIS_PASSWORD'),
        )

    def open_spider(self, spider):
        self.r = redis.Redis(self.host,self.port)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, MasterRedisItem):
            self.r.lpush('houses:start_urls', item['url'])
        return item

# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Selector, Request

from housespider.items import MasterRedisItem


class HouseSpider(scrapy.Spider):
    name = 'house'
    # allowed_domains = ['www.58.com', 'cd.58.com']
    start_urls = ['http://cd.58.com/chuzu']
    start_url = 'http://cd.58.com/chuzu'

    def start_requests(self):
        yield Request(url='http://cd.58.com/chuzu', callback=self.parse)

    def parse(self, response):
        response_url = re.findall('^http\:\/\/\w+\.58\.com', response.url)
        response_selector = Selector(response)
        areas = response_selector.xpath('//div[@class="search_bd"]/dl[1]/dd/a')
        for area in areas:
            area_url = response_url[0] + area.xpath('./@href').extract_first()
            print(area_url)
            yield Request(url=area_url, callback=self.parse_area_house_info)

    def parse_area_house_info(self, response):
        response_selector = Selector(response)
        page = response_selector.xpath('//*[@id="bottom_ad_li"]/div[2]/a[3]/span/text()').extract_first()
        base_url = response.url
        if page:
            print(page + '========')
            for i in range(int(page) + 1):
                item = MasterRedisItem()
                item['url'] = base_url + 'pn' + str(i)
                yield item
                # yield Request(base_url + 'pn' + str(i), callback=self.parse_detial)



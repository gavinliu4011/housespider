from scrapy import Selector, Request

from housespider.items import HouseItem
from scrapy_redis.spiders import RedisSpider


class HouseslaveSpider(RedisSpider):
    name = 'houseslave'
    redis_key = 'houses:start_urls'

    def parse(self, response):
        response_selector = Selector(response)
        detial_lis = response_selector.xpath(
            '//div[@class="listBox"]/ul[@class="listUl"]/li'
        )
        for li in detial_lis:
            detial_url = li.xpath('./div[2]/h2/a/@href').extract_first()
            logr = li.xpath('./@logr').extract_first()
            if detial_url:
                detial_url = 'http://' + detial_url
                yield Request(detial_url, callback=self.parse_detial, meta={'id': logr})

    def parse_detial(self, response):
        response_selector = Selector(response)
        item = HouseItem()

        item['id'] = response.meta.get('id')
        # 帖子名称
        item['title'] = response_selector.xpath(
            '//div[@class="main-wrap"]/div[@class="house-title"]/h1[@class="c_333 f20"]/text()').extract_first()

        # 租金
        item['money'] = response_selector.xpath(
            '//div[@class="house-pay-way f16"]/span[@class="c_ff552e"]/b/text()').extract_first()
        # 租赁方式
        item['method'] = response_selector.xpath(
            '//ul[contains(@class,"f14")]/li[1]/span[2]/text()').extract_first()
        # 所在小区
        item['community'] = response_selector.xpath(
            '//ul[contains(@class,"f14")]/li/span/a[contains(@class,"c_333")]/text()').extract_first()
        # 所在区域
        areas = response_selector.xpath('//ul[@class="f14"]/li[5]/span[2]/a')
        area_val = ''
        for area in areas:
            area_val += area.xpath('./text()').extract_first()
        item['area'] = area_val
        # 帖子详情url
        item['targeturl'] = response.url
        # 帖子所在城市
        item['city'] = response.url.split("//")[1].split('.')[0]
        item['image'] = response_selector.xpath('//div[@id="bigImg"]/img[@id="smainPic"]/@src').extract_first()
        yield item

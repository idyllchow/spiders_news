# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from hyperlink._url import unicode
from scrapy.loader import ItemLoader
from spidersnews.items import MynewsItem, NYItemLoader
from scrapy.loader.processors import MapCompose, Join


class NYSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["cn.nytimes.com"]
    start_urls = ["https://cn.nytimes.com/"]

    def parse(self, response):
        # l = NYItemLoader(item=MynewsItem(), response=response)
        # # l.add_xpath('title', '//h3/a/text()')
        # l.add_xpath('title', '//h3[@class="articleHeadline"]/text()')
        # l.add_xpath('urls', '//h3/a/@href')
        # # l.add_xpath('content', '//h3/a/text()')
        # l.add_xpath('content', '//div[@class="content chinese"]/p/text()')
        # l.add_xpath('image_urls', "//img[@class='img-lazyload']/@data-url")
        # l.add_xpath('author', '//meta[@name="byline"]/@content')
        # l.add_xpath('date', '//meta[@name="date"]/@content')
        # yield l.load_item()

        for sel in response.xpath('//ul/li'):
            # 遍历首页h3新闻标题
            links = sel.xpath('//h3/a/@href').extract()
            for link in links:
                next_page = response.urljoin(link)
                # yield scrapy.Request(next_page, callback=self.parse, dont_filter=False)
                yield scrapy.Request(next_page, self.parse_list)

    def parse_list(self, response):
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            yield scrapy.Request(url, self.parse_news)

    def parse_news(self, response):
        data = response.xpath("//div[@class='content chinese']")
        item = MynewsItem()
        item['title'] = data.xpath("//h3[@class='articleHeadline']/text()").extract_first()
        item['author'] = data.xpath("//meta[@name='byline']/@content").extract()
        item['date'] = data.xpath("//meta[@name='date']/@content").extract_first()
        content = data.xpath("//div[@class='content chinese']/p/text()").extract()
        ac = ''
        if (len(content) != 0):
            for c in content:
                ac = ac + c
        item['content'] = ac
        yield item

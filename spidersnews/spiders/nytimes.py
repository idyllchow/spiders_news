# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
import uuid
from hyperlink._url import unicode
from scrapy.loader import ItemLoader
from spidersnews.items import MynewsItem, NYItemLoader
from scrapy.loader.processors import MapCompose, Join


class NYSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["cn.nytimes.com"]
    start_urls = ["https://cn.nytimes.com/"]
    index = 0

    def parse(self, response):
        # add_xpath方式解析
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
        # add_xpath方式解析 end

        for sel in response.xpath('//ul/li'):
            # 遍历首页h3新闻标题
            links = sel.xpath('//h3/a/@href').extract()
            for link in links:
                next_page = response.urljoin(link) + 'dual/'
                print("next page===%s" % next_page)
                # yield scrapy.Request(next_page, callback=self.parse, dont_filter=False)
                yield scrapy.Request(next_page, self.parse_news_dual)

    def parse_list(self, response):
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            yield scrapy.Request(url, self.parse_news)

    def parse_news(self, response):
        data = response.xpath("//div[@class='content chinese']")
        item = MynewsItem()
        item['title'] = data.xpath("//h3[@class='articleHeadline']/text()").extract_first()
        item['author'] = data.xpath("//meta[@name='byline']/@content").extract()
        item['image_urls'] = data.xpath("//img[@class='img-lazyload']/@data-url").extract()
        item['date'] = data.xpath("//meta[@name='date']/@content").extract_first()
        content_cn = data.xpath("//div[@class='content chinese']/p/text()").extract()
        ac = ''
        if (len(content_cn) != 0):
            for c in content_cn:
                ac = ac + c + '\n'
        item['content_cn'] = ac
        yield item

    # 解析双语
    def parse_news_dual(self, response):
        item = MynewsItem()
        item['url'] = 'https://cn.nytimes.com/' + response.xpath("//div[@class='content chinese']/@href").extract_first()
        item['index'] = self.index
        data = response.xpath("//div[@class='bilingual cf']")
        item['title_cn'] = data.xpath("//div[@class='chinese']/h2[@class='articleHeadline']/text()").extract_first()
        item['title_en'] = data.xpath(
            "//div[@class='english article_en']/h2[@class='articleHeadline']/text()").extract_first()
        item['author'] = data.xpath("//meta[@name='byline']/@content").extract()
        item['image_urls'] = data.xpath("//img[@class='img-lazyload']/@data-url").extract()
        # item['date'] = data.xpath("//meta[@name='date']/@content").extract_first()
        item['date_cn'] = data.xpath("//div[@class='cf articleHead']/div[@class='chinese']/div[@class='kickerBox']/span[@class='date']/text()").extract_first()
        item['date_en'] = data.xpath("//div[@class='cf articleHead']/div[@class='english article_en']/div[@class='kickerBox']/span[@class='date']/text()").extract_first()
        content_cn = data.xpath("//div[@class='chinese']/p/text()").extract()
        content_en = data.xpath("//div[@class='english']/p/text()").extract()
        content_dual = data.xpath("//p[@class='paragraph']/text()").extract()
        ac = ''
        if (len(content_cn) != 0):
            for c in content_cn:
                ac = ac + c + '\n'
        item['content_cn'] = ac
        ac_en = ''
        if (len(content_en) != 0):
            for c in content_en:
                ac_en = ac_en + c + '\n'
        item['content_en'] = ac_en

        dual = ''
        if (len(content_dual) != 0):
            for dc in content_dual:
                dual = dual + dc + '\n'
        item['content_dual'] = dual

        if (len(item['content_cn']) != 0):
            self.index = self.index + 1
            yield item

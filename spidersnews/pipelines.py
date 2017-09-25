# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import scrapy
import json
import os

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MynewsPipeline(object):
    # 连接数据库
    collection_content_name = 'news_content'
    db_name = 'my_news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        mongodb_uri = os.environ.get('MONGODB_URI')
        if not mongodb_uri:
            print('================not mongo uri==============')
            return cls(
                mongo_uri=crawler.settings.get('MONGO_URI'),
                mongo_db=crawler.settings.get('MONGO_DATABASE', cls.db_name)
            )
        else:
            print('================has mongo uri==============%s: , mongo_db: %s: ', crawler.settings.get(mongodb_uri), crawler.settings.get('MONGO_DATABASE', cls.db_name))
            return cls(
                mongo_uri=crawler.settings.get(mongodb_uri),
                mongo_db=crawler.settings.get('MONGO_DATABASE', cls.db_name)
            )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 有内容则插入数据库
        if item['content'] is not None:
            self.db[self.collection_content_name].insert_one(dict(item))
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

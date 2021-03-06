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
    collection_name = 'news_content'
    db_name = 'news_items'
    # uri = 'mongodb://admin:111111@ds147902.mlab.com:47902/news_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 调用来创建一个爬虫管道实例，必须返回管道的一个新实例
    @classmethod
    def from_crawler(cls, crawler):
        # db_name = os.environ.get('MONGODB_DB_NAME')
        if not os.environ.get('MONGODB_URI'):
            # 存本地
            return cls(
                mongo_uri=crawler.settings.get('MONGO_URI'),
                mongo_db=crawler.settings.get('MONGO_DATABASE', cls.db_name)
            )
        else:
            # 存云端
            print("================has mongo uri: %s,====db_name: %s" % ((os.environ.get('MONGODB_URI')), cls.db_name))
            return cls(
                mongo_uri=os.environ.get('MONGODB_URI'),
                mongo_db=crawler.settings.get('MONGO_DATABASE', cls.db_name)
            )

    def open_spider(self, spider):
        print('===mongo uri===%s, mongo db===%s' % (self.mongo_uri, self.mongo_db))
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #删除原有数据
        print('mongo count %s' % (self.db[self.collection_name].count()))
        self.db[self.collection_name].count()
        self.db[self.collection_name].remove({})

    def close_spider(self, spider):
        spider.log("opened spider %s" % spider.name)
        self.client.close()

    def process_item(self, item, spider):
        # 有内容则插入数据库
        if item['content_cn'] is not None:
            self.db[self.collection_name].insert_one(dict(item))
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

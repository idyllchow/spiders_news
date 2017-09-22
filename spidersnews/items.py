import scrapy
from scrapy.loader import Identity
from scrapy.loader import ItemLoader


class Page(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    size = scrapy.Field()
    referer = scrapy.Field()
    newcookies = scrapy.Field()
    body = scrapy.Field()


class MynewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    urls = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    last_updated = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    images = scrapy.Field()


class NYItemLoader(ItemLoader):
    default_item_class = MynewsItem
    default_output_processor = Identity()

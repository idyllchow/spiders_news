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
    url = scrapy.Field()
    index = scrapy.Field()
    title_cn = scrapy.Field()
    title_en = scrapy.Field()
    urls = scrapy.Field()
    link = scrapy.Field()
    content_cn = scrapy.Field()
    content_en = scrapy.Field()
    content_dual = scrapy.Field()
    author = scrapy.Field()
    date_cn = scrapy.Field()
    date_en = scrapy.Field()
    last_updated = scrapy.Field()
    last_updated_en = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    images = scrapy.Field()


class NYItemLoader(ItemLoader):
    default_item_class = MynewsItem
    default_output_processor = Identity()

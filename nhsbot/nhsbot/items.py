# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NhsbotItem(scrapy.Item):
    source = scrapy.Field()
    crawled_epoch_date = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    meta = scrapy.Field()
    content = scrapy.Field()
    last_reviewed_epoch_date = scrapy.Field()

    pass

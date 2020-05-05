# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqvideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_name = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    author_name = scrapy.Field()
    desc = scrapy.Field()
    publish_time = scrapy.Field()
    series = scrapy.Field()

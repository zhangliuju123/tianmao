# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TianmaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    commodity_title = scrapy.Field()
    commodity_name = scrapy.Field()
    price = scrapy.Field()
    evaluate = scrapy.Field()
    integral = scrapy.Field()

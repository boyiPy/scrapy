# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangguangItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field() 
    href = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    content_img = scrapy.Field()

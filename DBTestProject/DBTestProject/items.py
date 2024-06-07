# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DbtestprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GetWordsItem(scrapy.Item):
    host = scrapy.Field()
    word_count = scrapy.Field()
    words = scrapy.Field()
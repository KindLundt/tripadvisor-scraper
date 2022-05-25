# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaProfilesItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    reviews = scrapy.Field()


    pass

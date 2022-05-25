# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaListingsItem(scrapy.Item):
    accommodation_name = scrapy.Field()
    accommodation_link = scrapy.Field()
    accommodation_id = scrapy.Field()
    accommodation_type = scrapy.Field()
    pass

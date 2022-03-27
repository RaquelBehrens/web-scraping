# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Machine(scrapy.Item):
    brand = scrapy.Field(value_type=str)
    cpu = scrapy.Field(value_type=str)
    memory = scrapy.Field(value_type=str)
    storage = scrapy.Field(value_type=str)
    bandwidth = scrapy.Field(value_type=str)
    price = scrapy.Field(value_type=str)


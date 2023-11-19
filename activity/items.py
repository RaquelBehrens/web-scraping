# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class City(scrapy.Item):
    nome = scrapy.Field(value_type=str)
    distancia_da_capital = scrapy.Field(value_type=str)
    area_total = scrapy.Field(value_type=str)
    populacao = scrapy.Field(value_type=str)
    densidade = scrapy.Field(value_type=str)
    altitude = scrapy.Field(value_type=str)
    idh = scrapy.Field(value_type=str)

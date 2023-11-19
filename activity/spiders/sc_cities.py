import json
import csv
import scrapy
import os
import html
import unicodedata
from activity.items import City
from scrapy import signals
from scrapy.signalmanager import dispatcher


class SCCities(scrapy.Spider):
    name = 'sc_cities'
    allowed_domains = ['pt.wikipedia.org']
    BASE_URL = 'https://pt.wikipedia.org'
    start_urls = ['https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Santa_Catarina']

    #defining default option
    option = '--save_json'

    def parse(self, response):       
        cities_elements = response.xpath('//td[position() = 2]/a')
        for city in cities_elements:

            name = city.xpath('./text()').extract_first()
            href = city.xpath('./@href').extract_first()
            
            yield scrapy.Request(f"{self.BASE_URL}{href}", callback=self.parse_city, meta={'city_name': name})


    def parse_city(self, response):
        city_name = response.meta['city_name']
        infobox_table = response.xpath('//table[contains(@class, "infobox")]')

        city = City(nome=city_name,
                            distancia_da_capital=self.decode_string(infobox_table.xpath('.//tr[.//*[contains(text(), "Distância até a")]]/td[2]/text()').extract_first()),
                            area_total=self.decode_string(infobox_table.xpath('.//tr[.//*[contains(text(), "rea total")]]/td[2]/text()').extract_first()),
                            populacao=self.decode_string(infobox_table.xpath('.//tr[.//*[contains(text(), "Popula")]]/td[2]/text()').extract_first()),
                            densidade=self.decode_string(infobox_table.xpath('.//tr[.//*[contains(text(), "Densidade")]]/td[2]/text()').extract_first()),
                            altitude=self.decode_string(infobox_table.xpath('.//tr[.//*[contains(text(), "Altitude")]]/td[2]/text()').extract_first()),
                            idh=self.decode_string(infobox_table.xpath('.//tr[.//*[contains(text(), "IDH")]]/td[2]/text()').extract_first()))

        yield city

    def decode_string(self, input_string):
        if type(input_string) is str:
            x = input_string.replace(u'\xa0', u'')
            x = input_string.replace(u'\n', u'')
            return x
        else:
            return ''

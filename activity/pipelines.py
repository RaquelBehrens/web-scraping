# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ActivityPipeline:
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('cities.json', 'w')
        self.file.write('[')
        self.items_written = False  # Add this line

    def close_spider(self, spider):
        if self.items_written:
            self.remove_trailing_comma()
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(line)
        self.items_written = True  # Add this line
        return item

    def remove_trailing_comma(self):
        self.file.seek(self.file.tell() - 2)  # Move the cursor two positions back
        self.file.truncate()  # Remove the comma and newline


class CSVWriterPipeline:
    def open_spider(self, spider):
        self.file = open('cities.csv', 'w', newline='', encoding='utf8')
        writer = csv.writer(self.file)
        writer.writerow(['Nome', 'Distância até a capital (Florianópolis)', 'Área Total', 'População', 'Densidade', 'Altitude', 'IDH']) # namedtuple breaks convention public fields have single underscore
        

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        writer = csv.writer(self.file)
        writer.writerow([item['nome'], item['distancia_da_capital'], item['area_total'], item['populacao'], item['densidade'], item['altitude'], item['idh']]) # namedtuple breaks convention public fields have single underscore
        return item

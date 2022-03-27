import json
import csv
import scrapy
import os

from activity.items import Machine


class VultrMachinesSpider(scrapy.Spider):
    name = 'vultr_machines'
    allowed_domains = ['www.vultr.com']
    start_urls = ['https://www.vultr.com/pricing/']

    #defining default option
    option = '--print'

    def parse(self, response):
        
        machines = []
        cloud_sections = response.xpath('//div[@class= "section"][contains(@id, "cloud")]')

        for section in cloud_sections:
            subsections = section.xpath('.//div[contains(@class, "pricing__subsection")][descendant::p[contains(text(), "SSD")]]')
            
            for subsection in subsections:
                brands = subsection.xpath('.//div[contains(@class, "pt pt--md-boxes is-animated")]')

                for brand in brands:
                    contents = brand.xpath('.//div[contains(@class, "pt__row-content")]')
                    brand_text = brand.xpath('./preceding-sibling::h4/text()').extract()

                    if brand_text:
                        brand_text = brand_text[-1]
                    
                    if brand_text not in ['Intel', 'AMD']:
                        brand_text = subsection.xpath('./p/text()').extract_first()
                        if 'Intel' in brand_text:
                            brand_text = 'Intel'
                        elif 'AMD' in brand_text:
                            brand_text = 'AMD'
                        else:
                            brand_text = 'Another Brand'

                    for content in contents:
                        machine = Machine(brand=brand_text,
                                            cpu=content.xpath('.//div[contains(text(), "CPU")]/strong/text()').extract_first(),
                                            memory=content.xpath('.//div[span[contains(text(), "Memory")]]/strong/text()').extract_first(),
                                            storage=content.xpath('.//div[span[contains(text(), "Storage")]]/strong/text()').extract_first(),
                                            bandwidth=content.xpath('.//div[span[contains(text(), "Bandwidth")]]/strong/text()').extract_first(),
                                            price=content.xpath('.//div[contains(text(), "/mo")]/strong/text()').extract_first().strip(" "))

                        machines.append(machine)
        
        self.operations(machines)
        yield machines

    def operations(self, machines):
        if self.option:
            if self.option == '--print':
                print(machines)
            elif self.option == '--save_json':
                if os.path.exists("dataset.json"):
                    os.remove("dataset.json")

                f = open('dataset.json', 'a')
                f.write('[\n')
                for machine in machines:
                    f.write(json.dumps(machine.__dict__.get("_values")))
                    f.write(',\n')

                f.write(']')
                f.close()
            elif self.option == '--save_csv':
                if os.path.exists("dataset.csv"):
                    os.remove("dataset.csv")
                
                with open('dataset.csv', 'w', newline='', encoding='utf8') as f:
                    writer = csv.writer(f)
                    for machine in machines:
                        writer.writerow([machine['brand'], machine['cpu'], machine['memory'], machine['bandwidth'], machine['price']]) # namedtuple breaks convention public fields have single underscore

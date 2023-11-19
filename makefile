run: execute

execute: 
	scrapy crawl sc_cities

install:
	sudo apt install python3-pip && sudo apt install python3 && sudo pip install Scrapy
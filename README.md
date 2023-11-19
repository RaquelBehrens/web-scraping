# INE5454

This application is a crawler that extracts data from [Wikipedia Santa Catarina's Page](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Santa_Catarina). 

Therefore, as a result from the spider's execution, the files below contain Santa Catarina's cities information:

`cities.csv` and `cities.json`

##

To run our application, please install the dependencies with the following command:

`make install`

Then, to run the spider, type the following command:

`make run`

or

`scrapy crawl sc_cities`

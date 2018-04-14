#encoding:utf-8

import scrapy


class AHospitalItem(scrapy.Item):
    crawl_time=scrapy.Field()
    website=scrapy.Field()
    dis_index = scrapy.Field()
    dis_name= scrapy.Field()
    dis_text=scrapy.Field()


#encoding:utf-8

import scrapy
from tutorial.items import AHospitalItem
import time


websit='ahospital'


class CrawlSpider(scrapy.Spider):
    name=websit
    allowed_domains = ["a-hospital.com"]

    def start_requests(self):
        gate_url='http://www.a-hospital.com/'+u'w/疾病'
        yield scrapy.Request(gate_url, callback=self.disease_index)

    def disease_index(self,response):
        dom = response.xpath('//div[@id="bodyContent"]/p[5]/a')
        for sel in dom:
            dis_index=''.join(sel.xpath('text()').extract())
            dis_index_url='http://www.a-hospital.com'+''.join(sel.xpath('@href').extract())
            metadata={'dis_index':dis_index}
            yield scrapy.Request(dis_index_url,meta={'metadata':metadata},callback=self.disease_list)

    def disease_list(self,response):
        metadata = response.meta['metadata']
        dom=response.xpath('//div[@id="bodyContent"]/ul/li')
        for sel in dom:
            disname=''.join(sel.xpath('a/text()').extract())
            dis_url='http://www.a-hospital.com'+''.join(sel.xpath('a/@href').extract())
            metadata_disname = dict({'disname': disname}, **metadata)
            yield  scrapy.Request(dis_url,meta={'metadata':metadata_disname},callback=self.disease_final)

    def disease_final(self,response):
        item = AHospitalItem()
        metadata=response.meta['metadata']
        dis_text= ''.join(response.xpath('//div[@id="bodyContent"]/p//text()').extract())
        crawl_time=(time.strftime("%d/%m/%Y"))
        item['crawl_time']=crawl_time
        item['website']=websit
        item['dis_index']=metadata['dis_index']
        item['dis_name']=metadata['disname']
        item['dis_text']=dis_text

        yield item




#encoding:utf-8
import requests
from lxml import etree
import codecs
import json

'''
问题描述：本程序主要抓取百科名医网站（http://www.baikemy.com）疾病大全以及每个疾病的词条，这部分数据，我要用后面的NLP处理；

技术概要：在爬虫环节，我主要展示页面跳转的问题，这次还是用之前的方式，较为简单；后面处理的复杂的，会用scrapy来实现；

后续概想：介绍scrapy的使用；
'''


def crawl():
    output_data = codecs.open('./data/crawl_baikemy.txt', 'w', encoding='utf-8')

    '''
    第一步还是分析url，网站的疾病列表页面起始位置是http://www.baikemy.com/disease/list/0/0，在尝试
    点击第几页观察url的变化，可以知道基本url是http://www.baikemy.com/disease/list/0/0?pageIndex=k，k=1-80
    url后面的'&pageCount='部分是多余的，不要是不影响链接
    '''
    n = 1
    for k in range(1,81):
        urlbase='http://www.baikemy.com/disease/list/0/0?pageIndex='+str(k)  #构造疾病列表url
        html = requests.get(urlbase).content
        selector = etree.HTML(html)

        #接下来是要获取每个疾病详细介绍页面的url
        for sel in selector.xpath('//div[@class="panel-body"]/div/ul/li'):

            items = {'dis_name': '',
                     'dis_text': '',
                     }

            dis_url='http://www.baikemy.com'+''.join(sel.xpath('a/@href'))
            dis_name=''.join(sel.xpath('a/text()'))

            #这次主要获取每个疾病的词条的文本，它对应的url是将'view'替换成'detail',然后后面加上'/1'
            words_url=dis_url.replace('view','detail')+'/1'
            words_html=requests.get(words_url).content
            words_selector = etree.HTML(words_html)
            words_text=''.join(words_selector.xpath('//div[@class="lemma-main"]//text()'))

            items['dis_name']=dis_name
            items['dis_text']=words_text

            output_data.write(json.dumps(items, ensure_ascii=False) + '\n')

            print 'download %dth data'%n
            n+=1

crawl()

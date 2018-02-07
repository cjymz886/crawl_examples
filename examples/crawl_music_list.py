#encoding:utf-8
import requests
from lxml import etree
import codecs
import json

'''
1.问题描述：本程序实现对落网（http://www.luoo.net/music/）的音乐推荐期刊的爬虫，涉及爬虫的内容有，每个期刊的名称，url，期刊号，关注人数，评论人数；
2.技术概要：主要利用requests与lxml两个包，另外定位页面元素使用xpath，细节可以查阅相关内容；
3.后续构想：会使用所抓的数据做些简单的分析；

'''

def crawl():
  
    output_data=codecs.open('./data/crawl_music_list.txt','w',encoding='utf-8')
    
    #首先需要对crawl的url进行分析，期刊的共有99页，每页10个，每页的url为：http://www.luoo.net/tag/?p=k,k=1-99
    for  k in range(1,100):
        urlbase='http://www.luoo.net/tag/?p='+str(k)  #构建每个页面的url
        html = requests.get(urlbase).content  #对页面进行请求
        selector = etree.HTML(html) #对页面进行解析
        
        '''
        接着，需要对每个页面里的10个期刊进行遍历，可以利用chrome浏览器来分析，
        发现10个期刊是<div class="vol-list"></div>块里每个<div class="item"></div>
        '''
        
        for sel in selector.xpath('//div[@class="vol-list"]/div[@class="item"]'):
            #定义每个期刊需要抓的内容
            items={'name':'',
                   'url':'',
                   'vol':'',
                   'attention_num':'',
                   'comment_num':''
            }
            #具体要crawl的item需要利用xpath，结合页面源码来定位
            items['name']=''.join(sel.xpath('a/@title'))  #使用join的好处就是若是没定位到，只会返回空，不会报错
            items['url']=''.join(sel.xpath('a/@href'))
            items['vol']=''.join(sel.xpath('div[@class="meta rounded clearfix"]/a/text()'))
            items['attention_num']=''.join(sel.xpath('div[@class="meta rounded clearfix"]/span[@class="favs"]/text()'))
            items['comment_num']=''.join(sel.xpath('div[@class="meta rounded clearfix"]/span[@class="comments"]/text()'))

            output_data.write(json.dumps(items,ensure_ascii=False)+'\n') #以json格式将数据一行行写入，便于后期处理数据

    output_data.close()


crawl()






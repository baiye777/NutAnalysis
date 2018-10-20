# -*- coding: utf-8 -*-
import scrapy
import json
import re
from jdbra.items import JdItem
import requests
import time
#分析网页的主要思路
    #（1）我们主要是为了获取商品的销售数据（评论数据），首先找到商品的销售数据，跟网页呈现的相同
    #（2）找到对应的链接，分析链接里面包含的主要信息：有商品的ID——ProductId、评论数据的页码——page
    #（3）接下来主要考虑不同的商品对应的ID，看网站的URL会发现有ProductID的信息，就可以以此确定通过京东搜索页面，
    #     输入关键字，我们可以基于呈现的页面来分析，可以获取商品的ProductID

#爬虫的主要思路：
    #（1）通过搜索商品关键字，来得到关于商品的页面，点击“销量”进行排序，基于该页面的URL完成，发送请求，获取商品ProductID
    #（2）得到商品ProductID之后，构建评论数据对应的链接，进行请求，获得该商品的评论数据最大页码maxpage
    #（3）得到最大页码之后，可以重新基于商品ProductId和页数page，重新构建评论数据的URL，进行请求，获得每个商品，每页下面的销售数据
    #（4）获得响应进行解析，提取感兴趣的数据，并进行保存。

class JdSpider(scrapy.Spider):
    name = 'jd'
    # allowed_domains = ['www.jd.com']
    # 初始请求url
    start_urls = ['https://search.jd.com/Search?keyword=%E5%9D%9A%E6%9E%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%9D%9A%E6%9E%9C&psort=3&stock=1&page=1&s=1&click=0']

    def start_requests(self):
        ji, ou = [], []
        for i in range(1, 3):
            if i % 2 == 0:
                ou.append(i)
            else:
                ji.append(i)
        for page in ji:
            url = 'https://search.jd.com/Search?keyword=%E5%9D%9A%E6%9E%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%9D%9A%E6%9E%9C&stock=1&page=' + str(page) + '&s=' + str(page*60-60) + '&click=0'
            res = requests.get(url)
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    # 解析获得产品id,构建url用来请求获得每个产品下的评论页码数
    def parse(self, response):

            #获取全部产品id
            productIds = list(set(response.css('li.gl-item::attr(data-sku)').extract()))
            #对每个产品进行请求，获得页码信息
            for productId in productIds:
                url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv257&productId='+productId+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
                yield scrapy.Request(url=url,meta={'productId':productId},callback=self.parse_page)


    # 解析获得页码数据
    def parse_page(self,response):
        #
        result = response.text.replace('fetchJSON_comment98vv257(','').replace(');','')
        maxpage=json.loads(result)['maxPage']#获取当前商品的评论页码数
        productId=response.meta['productId']#产品id
        # 进行翻页请求
        for page in range(0,maxpage):
        #     productId=re.search(r'productId=(.*?)&',response.url).group(1)
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv257&productId='+productId+'&score=0&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_item)

    #解析获取，产品销售数据
    def parse_item(self,response):
        result = response.text.replace('fetchJSON_comment98vv257(', '').replace(');', '')
        comments = json.loads(result)['comments']#评论数据
        for comment in comments:
            item = JdItem()
            item['content'] = comment['content']
            item['id'] = comment['id']
            item['referenceName'] = comment['referenceName']
            item['userClientShow'] = comment['userClientShow']
            yield item


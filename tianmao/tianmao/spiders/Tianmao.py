# -*- coding: utf-8 -*-

import scrapy
from head import create_bs_driver
from tianmao.items import TianmaoItem


class TianmaoSpider(scrapy.Spider):
    name = 'Tianmao'
    allowed_domains = ['tmall.com', 'detail.tmall.com', 'list.tmall.com']
    start_urls = ['https://www.tmall.com//']
    query_key = "口罩"

    def __init__(self):
        scrapy.Spider.__init__(self, self.name)
        self.driver = create_bs_driver(type="chrome")
        self.driver.set_page_load_timeout(50)

    def __del__(self):
        self.driver.quit()

    def start_requests(self):
        '''
            #重写初始化url请求，携带上信息，下载中间件能识别
        '''
        for url in self.start_urls:
            r = scrapy.Request(url=url, meta={'type': 'home', 'query_key': self.query_key}, callback=self.parse,
                               dont_filter=True)
            yield r

    def parse(self, response):
        '''
        该方法同于生产出详情页URL
        :param response:
        :return:
        '''
        print('回调成功,可以正常爬取')
        detail_list = response.xpath("//div[@class='productImg-wrap']//a/@href").extract()
        for detail in detail_list:
            detail_url = response.urljoin(detail)  # 拼上协议
            print(detail_url)
            detail_request = scrapy.Request(url=detail_url, meta={'type': 'detail'}, callback=self.detail_url,
                                            dont_filter=True)
            yield detail_request
        try:
            next_list = response.xpath("//a[@class=ui-page-next]/@href").extract()
            next_url = "https;//list.tmall.com/search_product.htm" + next_list
            next_request = scrapy.Request(url=next_url, meta={'type': 'next'}, callback=self.parse, dont_filter=True)
            yield next_request
        except Exception as e:
            print("没有下一页了")

    def detail_url(self, response):
        print('已经拿到详情页url,开始解析')
        commodity_title = response.xpath("//h1[@data-spm='1000983']/text()").extract_first()
        price = response.xpath("//span[@class='tm-price']/text()").extract_first()
        evaluate = response.xpath("//span[@class='tm-count']/text()")[0]
        integral = response.xpath("//span[@class='tm-count']/text()")[1]
        if response.xpath("//div[@class='name']").extract_first():
            commodity_name = response.xpath("//div[@class='name']/text()").extract_first()
        elif response.xpath("//div[@class='name'/text()]").extract_first():
            commodity_name = response.xpath("//div[@class='name'/text()]").extract_first()
        else:
            raise Exception('该名称不存在')
        url = response.xpath("//a[@class='ui-page-next']/@href").extract()
        next_url = response.urljoin(url)
        yield scrapy.Request(url=next_url, callback=self.detail_url)
        item = TianmaoItem(commodity_title=commodity_title, price=price, evaluate=evaluate, integral=integral,
                           commodity_name=commodity_name)
        yield item

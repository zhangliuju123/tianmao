# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import os
import random
import time

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse

from .settings import USER_AGENT_LIST


class TianmaoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TianmaoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    '''
    用户代理中间件（处于下载中间件位置）
    '''

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            print(f"User-Agent:{user_agent}")
        try:
            PROXY = []
            file_path = os.path.join(os.path.dirname(os.getcwd()), 'Ipproxys.txt')
            with open(file_path, 'r', encoding='utf8') as e:
                for i in e.readlines():
                    proxy_str = i.strip('\n')
                    PROXY.append(proxy_str)
            proxy = random.choice(PROXY)
            request.headers.setdefault('PROXY', proxy)
            print(f"proxy:{proxy}")
        except Exception as e:
            print(e)


class TianmaoSeleniumDownloaderMiddleWare(object):
    def process_request(self, request, spider):
        try:
            if spider.name == 'Tianmao' and request.meta.get('type', None) == 'home':
                print(spider.name)
                driver = spider.driver  # driver跟着requset一起到中间件
                query_key = request.meta.get('query_key', None)  # 获取到关键字
                driver.get(request.url)
                time.sleep(2)
                # 模拟用户登录
                json_path = os.path.join(os.path.dirname(os.getcwd()), 'cookies.json')
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf8') as f:
                        listCookies = json.loads(f.read())
                        for i in listCookies:
                            # 在request中加入cookie
                            driver.add_cookie(i)
                else:
                    driver.find_elements_by_xpath("//a[@class='sn-login']")[0].click()
                    time.sleep(5)
                    user_path = os.path.join(os.path.dirname(os.getcwd()), 'user.txt')
                    with open(user_path, 'r', encoding='utf8') as f:
                        user_list = f.readlines()
                        username = user_list[0].split(',')[0]
                        password = user_list[0].split(',')[1]
                        driver.switch_to.frame("J_loginIframe")  # 定位到iframe标签
                        # 模拟用户登录
                        driver.find_element_by_id("fm-login-id").send_keys(username)
                        driver.find_element_by_id("fm-login-password").send_keys(password)
                        driver.find_element_by_xpath("//button[@type='submit']").click()
                        # 保存cookies到本地
                        cookies = driver.get_cookies()
                        with open(json_path, 'a', encoding='utf8') as a:
                            a.write(json.dumps(cookies))
                        # driver.switch_to.default_content()
                    time.sleep(5)
                driver.find_element_by_name('q').send_keys(query_key)
                driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
                time.sleep(5)
                # js = "window.scrollTo(window.pageXOffset, document.body.scrollHeight)"
                # spider.driver.execute_script(js)
                # time.sleep(2)
                # return HtmlResponse(
                #     url=spider.driver.current_url,
                #     body=spider.driver.page_source,
                #     request=request,
                #     encoding="utf-8",
                # )
        except Exception as e:
            print(e)

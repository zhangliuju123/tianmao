# -*- coding: utf-8 -*-
__auto__ = 'zhangliujun'
__date__ = '2018/6/13 22:28'

from selenium import webdriver


def create_bs_driver(type="firefox", headless=False):
    '''
    :param type:
    :param headless:  是否为无头浏览器，True---无头，  False---有头
    :return:
    '''
    if type == "firefox":  # 火狐浏览器
        firefox_opt = webdriver.FirefoxOptions()
        firefox_opt.add_argument("--headless") if headless else None
        driver = webdriver.Firefox(firefox_options=firefox_opt)
    elif type == "chrome":  # 谷歌浏览器
        chrome_opt = webdriver.ChromeOptions()
        with open('G:\PythonWork\MyScrapy\stealth.min.js') as f:
            js = f.read()
        chrome_opt.add_argument(f'--window-position={217},{172}')
        chrome_opt.add_argument(f'--window-size={1200},{1000}')
        chrome_opt.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_opt.add_argument("--headless") if headless else None
        # chrome_opt.add_experimental_option("prefs",
        #                                    {"profile.managed_default_content_settings.images": 2})  # 加快请求速度,设置禁止加载图片
        driver = webdriver.Chrome(chrome_options=chrome_opt)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        # 屏蔽selenium检测,提前运行js的方法，把window.navigator.webdriver设为"undefined"
        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        # })
    else:
        return None
    return driver

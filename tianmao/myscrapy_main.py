# -*- coding: utf-8 -*-
__auto__ = 'zhangliujun'
__date__ = '2021/1/3 15:34'

import os, sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SPIDER_NAME = 'Tianmao'

execute(["scrapy", "crawl", SPIDER_NAME])

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import sys

sys.path.append("../..")
import scrapy
from FPP.items import BaiduBaike
from scrapy import Request
import pandas as pd
import re
import collections
import json
from utils.rw_excel import read_from_excel

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import sys
import scrapy
sys.path.append("../..")
from FPP.items import BaiduBaike
import pandas as pd
import re
import collections
import json
from utils.rw_excel import read_from_excel
from FPP.settings import USER_AGENT
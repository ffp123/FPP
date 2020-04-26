# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/22 17:19 
@Author      : tmooming
@File        : __init__.py.py 
@Description : NLP所有功能实现
"""
import sys

sys.path.append("..")
from utils.rw_excel import read_from_excel
import pandas as pd
import ast
import json
import numpy as np
from gensim.models import KeyedVectors, word2vec, Word2Vec
import jieba
import multiprocessing
import re
from sklearn.cluster import DBSCAN, KMeans
import matplotlib
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
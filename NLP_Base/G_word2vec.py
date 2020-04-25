# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/22 17:47 
@Author      : tmooming
@File        : G_word2vec.py
@Description : 使用gensim工具包进行词向量训练
"""
from random import sample

import numpy as np
import pandas as pd
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

file_prox = '../docs/'




class G_Word2Vec(object):
    def __init__(self,model_path):
        self.model_path = model_path



    def train(self):
        # 可以用BrownCorpus,Text8Corpus或lineSentence来构建sentences，一般大语料使用这个

        sentences = list(word2vec.LineSentence(file_prox + '分词结果/data.txt'))
        # sentences = list(word2vec.Text8Corpus('data.txt'))

        # 小语料可以不使用
        # sentences = sentences_cut
        print(sentences)

        # 训练方式1
        model = Word2Vec(sentences, size=100, min_count=1, window=5, sg=0, workers=multiprocessing.cpu_count(),hs=0)
        model.save(self.model_path+'.model')

        model.wv.save_word2vec_format(self.model_path+'.vector')

    def update_train(self):
        model = Word2Vec.load(self.model_path+'.model')
        print(model)
        new_sentence = [
            '我喜欢吃苹果',
            '大话西游手游很好玩',
            '人工智能包含机器视觉和自然语言处理'
        ]
        sentences = list(word2vec.LineSentence(file_prox + '分词结果/data.txt'))
        # 增量训练word2vec
        model.build_vocab(sentences, update=True)  # 注意update = True 这个参数很重要
        model.train(sentences, total_examples=model.corpus_count, epochs=10)
        model.save(self.model_path+'.model')
        model.wv.save_word2vec_format(self.model_path+'.vector')
        print(model)

    def julei_3D(self):
        model = Word2Vec.load(self.model_path+'.model')
        # words = sample(model.wv.index2word, 200)
        # vectors = [model[word] for word in words]
        df = pd.read_excel('../docs/期货词频统计/期货词频统计.xlsx', '期货相关词统计(按词性)')
        all_words = [word.split('|')[0] for lists in ['能源期货专有词', '农产品期货专有词', '金属期货专有词'] for word in
                     df[lists].values.tolist() if word is not np.nan and 'n' in word]
        words, not_word, vectors = [], [], []
        for word in all_words:
            if word in model.wv.index2word:
                words.append(word)
                vectors.append(model[word])
            else:
                not_word.append(word)
        tsne = TSNE(n_components=3)
        vectors = tsne.fit_transform(vectors)

        # pca = PCA(n_components=3)
        # vectors = pca.fit_transform(vectors)
        # ----------------------------------词向量聚类----------------------------------
        # 基于密度的DBSCAN聚类
        # labels = DBSCAN(eps=0.24, min_samples=3).fit(vectors).labels_
        labels = KMeans(n_clusters=3).fit(vectors).labels_
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 显示负号
        fig = plt.figure()
        ax = mplot3d.Axes3D(fig)  # 创建3d坐标轴
        colors = ['red', 'blue', 'green','black']  # 分为三类
        # 绘制散点图 词语 词向量 类标(颜色)
        for word, vector, label in zip(words, vectors, labels):
            ax.scatter(vector[0], vector[1], vector[2], c=colors[label], s=30, alpha=0.3)
            ax.text(vector[0], vector[1], vector[2], word, ha='center', va='center')
        plt.show()
    def julei_2D(self):
        model = Word2Vec.load(self.model_path+'.model')
        # words = sample(model.wv.index2word, 200)
        # vectors = [model[word] for word in words]
        df = pd.read_excel('../docs/期货词频统计/期货词频统计.xlsx', '期货相关词统计(按词性)')
        all_words = [word.split('|')[0] for lists in ['能源期货专有词', '农产品期货专有词', '金属期货专有词'] for word in
                 df[lists].values.tolist() if word is not np.nan and 'n' in word]
        words,not_word,vectors = [],[],[]
        for word in all_words:
            if word in model.wv.index2word:
                words.append(word)
                vectors.append(model[word])
            else:
                not_word.append(word)
        print(not_word)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 显示负号
        tsne = TSNE(n_components=2)
        vectors = tsne.fit_transform(vectors)

        clf = KMeans(n_clusters=3)  # 设定k  ！！！！！！！！！！这里就是调用KMeans算法
        clf.fit(vectors)  # 加载数据集合

        numSamples = len(vectors)
        centroids = clf.labels_
        print(centroids, type(centroids))  # 显示中心点
        print(clf.inertia_)  # 显示聚类效果
        mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
        # 画出所有样例点 属于同一分类的绘制同样的颜色

        for i in range(numSamples):
            # markIndex = int(clusterAssment[i, 0])
            #plt.scatter(vectors[i][0], vectors[i][1], mark[clf.labels_[i]])
            plt.plot(vectors[i][0], vectors[i][1], mark[clf.labels_[i]])  # mark[markIndex])
        mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
        # 画出质点，用特殊图型
        centroids = clf.cluster_centers_
        for i in range(3):
            plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize=12)
            # print centroids[i, 0], centroids[i, 1]


        # pca = PCA(n_components=2)
        # vectors = pca.fit_transform(vectors)
        # 可视化展示
        # plt.scatter(vectors[:, 0], vectors[:, 1],)
        for i, word in enumerate(words):
            plt.annotate(word, xy=(vectors[i, 0], vectors[i, 1]))
        plt.show()


    def predict(self):
        # model = KeyedVectors.load_word2vec_format('D:\study_data\graduate_content\Futures\sgns.baidubaike.bigram-char', binary=False, unicode_errors='ignore')
        model = Word2Vec.load(self.model_path+'.model')
        #vec = model['生物医药']
        # print(vec)
        result = model.wv.similarity('钢铁', '新能源')

        # result = model.wv.similarity('钢铁', '新能源')
        print(model.wv.similarity('钢铁', '新能源'))
        print(model.wv.similarity('钢铁', '动力'))
        print(model.wv.similarity('钢铁', '玉米'))
        print(model.wv.similarity('钢铁', '生铁'))
        print(model.wv.similarity('钢铁', '炼钢'))
        print(model.wv.similarity('钢铁', '螺纹钢'))
        res2 = model.wv.most_similar("钢铁", topn=10)  # 10个最相关的
        print(u"和 [钢铁] 最相关的词有：\n")
        for item in res2:
           print(item[0], item[1])

    def run(self):
        # self.jieba_cut()
        # self.train()
        # self.update_train()
        self.julei_3D()
        # self.predict()



if __name__ == "__main__":
    # sentences_list = [
    #     '详细了解园区规划，走访入驻企业项目，现场察看产品研发和产业化情况。他强调，',
    #     '要坚持规划先行，立足高起点、高标准、高质量，科学规划园区组团，提升公共服务水平，',
    #     ]
    model_path ='models/word2vec_100'
    # df = pd.read_excel('../docs/期货词频统计/期货词频统计.xlsx','期货相关词统计(按词性)')
    # words = [word.split('|')[0] for lists in ['能源期货专有词','农产品期货专有词','金属期货专有词'] for word in df[lists].values.tolist() if word is not np.nan and 'n' in word]

    # words.append(word for word in df['能源期货专有词'].values.tolist() if word is not np.nan)
    # words.append(word for word in  df['农产品期货专有词'].values.tolist() if word is not np.nan)
    # words.append(word for word in  df['金属期货专有词'].values.tolist() if word is not np.nan)
    # words = [word  for word in words if word is not np.nan]
    G_word = G_Word2Vec(model_path)
    G_word.run()
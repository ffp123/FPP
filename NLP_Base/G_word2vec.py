# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/22 17:47 
@Author      : tmooming
@File        : G_word2vec.py
@Description : 使用gensim工具包进行词向量训练
"""
from random import sample

from gensim.models import KeyedVectors, word2vec, Word2Vec
import jieba
import multiprocessing
import re
from sklearn.cluster import DBSCAN, KMeans
import matplotlib
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

file_prox = '../docs/'

class G_Word2Vec(object):
    def __init__(self, sentences_list ):
        self.stopwords = self.stopwordslist()
        self.sentences_list = sentences_list

    def stopwordslist(self):
        """
        加载去停词表
        :return:
        """
        stopwords = [line.strip() for line in
                     open(file_prox + 'stopwords/baidu_stopwords.txt', encoding='utf-8').readlines()]
        return stopwords

    def jieba_cut(self):
        """
        使用jieba分词
        :return:
        """
        sentences_cut = []
        punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
        for ele in self.sentences_list:
            ele = re.sub(r"[%s]+" %punc, "",ele)
            if len(ele)<1:
                continue
            cuts = jieba.cut(ele, cut_all=False)
            res = ' '.join([cut for cut in cuts if cut not in self.stopwords])
            sentences_cut.append(res)
        print(sentences_cut)
        # 分词后的文本保存在data.txt中
        with open(file_prox + '分词结果/data.txt', 'w', encoding='utf-8') as f:
            for ele in sentences_cut:
                ele = ele + '\n'
                f.write(ele)
            f.close()

    def train(self):
        # 可以用BrownCorpus,Text8Corpus或lineSentence来构建sentences，一般大语料使用这个

        sentences = list(word2vec.LineSentence(file_prox + '分词结果/data.txt'))
        # sentences = list(word2vec.Text8Corpus('data.txt'))

        # 小语料可以不使用
        # sentences = sentences_cut
        print(sentences)

        # 训练方式1
        model = Word2Vec(sentences, size=100, min_count=2, window=5, sg=0, workers=multiprocessing.cpu_count(),hs=0)
        print(model)
        model.save('models/word2vec_100.model')
        model.wv.save_word2vec_format('models/word2vec_100.vector')

    def update_train(self):
        model = Word2Vec.load('word2vec.model')
        print(model)
        new_sentence = [
            '我喜欢吃苹果',
            '大话西游手游很好玩',
            '人工智能包含机器视觉和自然语言处理'
        ]
        sentences_cut = []
        # 结巴分词
        for ele in new_sentence:
            cuts = jieba.cut(ele, cut_all=False)
            new_cuts = []
            for cut in cuts:
                if cut not in self.stopwords:
                    new_cuts.append(cut)
            res = ' '.join(new_cuts)
            sentences_cut.append(res)
        # 增量训练word2vec
        model.build_vocab(sentences_cut, update=True)  # 注意update = True 这个参数很重要
        model.train(sentences_cut, total_examples=model.corpus_count, epochs=10)
        model.save('models/word2vec.model')
        model.wv.save_word2vec_format('models/word2vec.vector')
        print(model)

    def julei(self):
        model = Word2Vec.load('models/word2vec_100.model')
        vectors = [model[word] for word in model.wv.index2word]
        vectors = sample(vectors, 200)
        # ----------------------------------词向量聚类----------------------------------

        # 基于密度的DBSCAN聚类

        # labels = DBSCAN(eps=0.24, min_samples=3).fit(vectors).labels_
        labels = KMeans(n_clusters=4).fit(vectors).labels_
        print(labels)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 显示负号
        fig = plt.figure()
        ax = mplot3d.Axes3D(fig)  # 创建3d坐标轴
        colors = ['red', 'blue', 'green','black']  # 分为三类
        # 绘制散点图 词语 词向量 类标(颜色)
        for word, vector, label in zip(model.wv.index2word, vectors, labels):
            ax.scatter(vector[0], vector[1], vector[2], c=colors[label], s=30, alpha=0.3)
            ax.text(vector[0], vector[1], vector[2], word, ha='center', va='center')
        plt.show()

    def predict(self):
        # model = KeyedVectors.load_word2vec_format('D:\study_data\graduate_content\Futures\sgns.baidubaike.bigram-char', binary=False, unicode_errors='ignore')
        model = Word2Vec.load('models/word2vec_100.model')
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
        self.train()
        # self.update_train()
        # self.julei()
        self.predict()



if __name__ == "__main__":
    # sentences_list = [
    #     '详细了解园区规划，走访入驻企业项目，现场察看产品研发和产业化情况。他强调，',
    #     '要坚持规划先行，立足高起点、高标准、高质量，科学规划园区组团，提升公共服务水平，',
    #     ]
    sentences_list = []
    for fi in ['农产品期货','能源期货','金属期货']:
        for line in open('../docs/期货文档/'+fi+'.txt',encoding='utf-8').readlines():
            sentences_list.append(line.strip())
    G_word = G_Word2Vec(sentences_list)
    G_word.run()

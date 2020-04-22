# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/22 17:47 
@Author      : tmooming
@File        : G_word2vec.py
@Description : 使用gensim工具包进行词向量训练
"""

from gensim.models import KeyedVectors, word2vec, Word2Vec
import jieba
import multiprocessing

file_prox = '../docs/'


class G_Word2Vec(object):
    def __init__(self, sentences_list):
        self.stopwords = self.stopwordslist()
        self.sentences_list = sentences_list

    def stopwordslist(self):
        stopwords = [line.strip() for line in
                     open(file_prox + 'stopwords/baidu_stopwords.txt', encoding='utf-8').readlines()]
        return stopwords

    def jieba_cut(self):
        sentences_cut = []
        for ele in self.sentences_list:
            cuts = jieba.cut(ele, cut_all=False)
            res = ' '.join([cut for cut in cuts if cut not in self.stopwords])
            sentences_cut.append(res)
        print(sentences_cut)
        # 分词后的文本保存在data.txt中
        with open(file_prox + '分词结果/data.txt', 'w', encoding='utf-8') as f:
            for ele in sentences_cut:
                ele = ele + '\n'
                f.write(ele)

    def train(self):
        # 可以用BrownCorpus,Text8Corpus或lineSentence来构建sentences，一般大语料使用这个

        sentences = list(word2vec.LineSentence(file_prox + '分词结果/data.txt'))
        # sentences = list(word2vec.Text8Corpus('data.txt'))

        # 小语料可以不使用
        # sentences = sentences_cut
        print(sentences)

        # 训练方式1
        model = Word2Vec(sentences, size=256, min_count=1, window=5, sg=0, workers=multiprocessing.cpu_count())
        print(model)
        model.save('models/word2vec.model')
        model.wv.save_word2vec_format('models/word2vec.vector')

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

    def predict(self):
        w2v = KeyedVectors.load_word2vec_format('D:\study_data\graduate_content\Futures\sgns.baidubaike.bigram-char', binary=False, unicode_errors='ignore')
        # model = Word2Vec.load('models/word2vec.model')
        #vec = model['生物医药']
        # print(vec)
        result = w2v.wv.similarity('钢铁', '新能源')

        # result = model.wv.similarity('钢铁', '新能源')
        print(w2v.wv.similarity('钢铁', '新能源'))
        print(w2v.wv.similarity('钢铁', '动力'))
        print(w2v.wv.similarity('钢铁', '玉米'))
        print(w2v.wv.similarity('钢铁', '生铁'))
        print(w2v.wv.similarity('钢铁', '炼钢'))
        print(w2v.wv.similarity('钢铁', '螺纹钢'))
        print(w2v.wv.similarity('钢铁', '热轧卷板'))

    def run(self):
        # self.jieba_cut()
        # self.train()
        # self.update_train()
        self.predict()



if __name__ == "__main__":
    # sentences_list = [
    #     '详细了解园区规划，走访入驻企业项目，现场察看产品研发和产业化情况。他强调，',
    #     '要坚持规划先行，立足高起点、高标准、高质量，科学规划园区组团，提升公共服务水平，',
    #     ]
    sentences_list = []
    for fi in ['农产品期货','能源期货','金属期货']:
        for line in open(file_prox+'期货文档/'+fi+'.txt',encoding='utf-8').readlines():
            sentences_list.append(line.strip())
    G_word = G_Word2Vec(sentences_list)
    G_word.run()

# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/24 19:25 
@Author      : tmooming
@File        : jieba_api.py 
@Description : jieba分词
"""
from NLP_Base import *
file_prox = '../docs/'


class Jieba_api(object):
    def __init__(self, sentences_list):
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
            ele = re.sub(r"[%s]+" % punc, "", ele)
            if len(ele) < 1:
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


if __name__ == "__main__":
    sentences_list = []
    for fi in ['农产品期货', '能源期货', '金属期货', 'scrapy_items']:
        for line in open('../docs/期货文档/' + fi + '.txt', encoding='utf-8').readlines():
            sentences_list.append(line.strip())
    jieba_api = Jieba_api(sentences_list)

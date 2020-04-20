# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/19 21:19 
@Author      : tmooming
@File        : NLP_api.py
@Description : 使用NLP_API进行词性标注、分词、实体识别
"""
import sys
import pandas as pd
import os
from pyltp import Segmentor, Postagger, NamedEntityRecognizer

sys.path.append("../..")
from FPP.utils.rw_excel import write_to_excel, read_from_excel


class Baidu_API(object):
    def __init__(self, excel_path, from_sheet):
        self.yuanwen = self.get_yuanwen(excel_path, from_sheet)

    def get_yuanwen(self, excel_path, from_sheet):
        return pd.read_excel(excel_path, from_sheet).iloc[:, 0:4]


class LTP(object):
    def __init__(self, LTP_DATA_DIR, excel_path, from_sheet):
        self.LTP_DATA_DIR = LTP_DATA_DIR
        self.result_df = self.get_data(excel_path, from_sheet)

    def get_data(self, excel_path, from_sheet):
        df = pd.read_excel(excel_path, from_sheet).loc[:, ['id', '语料原文']]
        data = pd.DataFrame(columns=['id', '语料原文', '分词结果', '词性标注', '实体识别', 'nz_名词'], index=[i for i in range(len(df))])
        data.loc[:, ['id', '语料原文']] = df
        return data

    def cws(self):
        cws_model_path = os.path.join(self.LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        segmentor = Segmentor()  # 初始化实例
        segmentor.load(cws_model_path)  # 加载模型
        for item in self.result_df.itertuples():
            word = getattr(item, '语料原文')
            self.result_df.loc[self.result_df['id'] == getattr(item, 'id'), '分词结果'] = '\t'.join(segmentor.segment(word))
            # self.result_df['分词结果'].append('  '.join(segmentor.segment(word)))
        # words = segmentor.segment("在包含问题的所有解的解空间树中，按照深度优先搜索的策略，从根节点出发深度探索解空间树。")
        # print(' | '.join(words))  # 分词结果
        # 分词结果的后处理
        # postdict = {'解 | 空间': '解空间', '深度 | 优先': '深度优先'}  # 矫正一些分词错误
        # seg_sent = ' | '.join(words)
        # for key in postdict:
        #     seg_sent = seg_sent.replace(key, postdict[key])  # string的replace方法
        # print(seg_sent)
        # print(postdict['解 | 空间'])
        segmentor.release()  # 释放模型

    def pos(self):
        pos_model_path = os.path.join(self.LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
        postagger = Postagger()  # 初始化实例
        postagger.load(pos_model_path)  # 加载模型
        print(self.result_df)
        for item in self.result_df.itertuples():
            word = getattr(item, '分词结果')
            postags = postagger.postag(word.split('\t'))  # 词性标注
            self.result_df.loc[self.result_df['id'] == getattr(item, 'id'), '词性标注'] = '\t'.join(postags)
        # words = ['元芳', '你', '怎么', '看']  # 分词结果
        # postags = postagger.postag(words)  # 词性标注
        #
        # print('\t'.join(postags))

        postagger.release()  # 释放模型

    def ner(self):
        ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
        recognizer = NamedEntityRecognizer()  # 初始化实例
        recognizer.load(ner_model_path)  # 加载模型
        for item in self.result_df.itertuples():
            words = getattr(item, '分词结果').split('\t')
            postags = getattr(item, '词性标注').split('\t')
            nz_word = []
            for index, postag in enumerate(postags):
                if 'n' in postag:
                    nz_word.append(words[index])
            netags = recognizer.recognize(words, postags)  # 命名实体识别

            self.result_df.loc[self.result_df['id'] == getattr(item, 'id'), '实体识别'] = '\t'.join(
                list(set([words[ind] for ind, ne in enumerate(netags) if ne != 'O'])))
            self.result_df.loc[self.result_df['id'] == getattr(item, 'id'), 'nz_名词'] = '\t'.join(list(set(nz_word)))
        recognizer.release()  # 释放模型

    def run(self):
        self.cws()
        self.pos()
        self.ner()
        print(self.result_df)


if __name__ == "__main__":
    excel_path = "../data/结果比较.xlsx"
    from_sheet = '原文'
    # badiu_api = Baidu_API(excel_path, from_sheet)
    # print(badiu_api.yuanwen)
    LTP_DATA_DIR = 'D:/study_data/graduate_content/Futures/ltp_data_v3.4.0'  # ltp模型目录的路径

    ltp = LTP(LTP_DATA_DIR, excel_path, from_sheet)
    ltp.run()
    write_to_excel(ltp.result_df, excel_path, sheet_name='LTP')

import sys

sys.path.append("..")
import Levenshtein
from utils import *
from utils.fun_tongji import get_alpha_str

class similarity(object):

    #加载字向量
    def load_wordvector(self,embedding_path):
        file = open(embedding_path,'r',encoding='utf-8')
        embed = file.readlines()
        vector_dic = {}
        vacab = []
        for i in range(1,len(embed)):
            word1 = embed[i].replace('\n', '').split(' ')[0]
            vec1 = embed[i].replace('\n', '').split(' ')[1:]
            #print(len(vec1))
            for i in range(len(vec1)):
                vec1[i] = float(vec1[i])
            vec1 = np.array(vec1)
            vacab.append(word1)
            vector_dic[word1] = vec1
        return vacab,vector_dic


    #形成热词的词向量
    def get_reci_vec(self,vocab,vecdict,recilist):

        recivec_dict = {}
        for reci in recilist:
            reci_vec = np.zeros(768)
            for onestr in reci:
                if onestr in vocab:
                    reci_vec += vecdict[onestr]
                else:
                    print(reci)
                    print(onestr)
            recivec_dict[reci] = reci_vec / len(reci)

        return recivec_dict

    #余弦相似度
    def cossim(self,vec1, vec2):
        sim3 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        return sim3

    #jaccard相似度
    def jaccard(self,p, q):
        c = [v for v in p if v in q]
        return float(len(c) / (len(p) + len(q) - len(c)))

    def get_word_vec(self,word,vocab,vector_dic):
        word_vec = np.zeros(768)
        for onestr in word:
            if onestr in vocab:
                word_vec += vector_dic[onestr]
            else:
                print(onestr)
                print(word)
        word_vec = word_vec / len(word)
        return word_vec

class wordmine(object):

    #获取预料原文全文
    def getalltext(self,alldir):
        dirs = os.listdir(alldir)
        print(dirs)
        textlist = []
        text = ''
        for dir in dirs:
            if dir in ['农产品期货.xlsx', '能源期货.xlsx', '金属期货.xlsx']:
                file = openpyxl.load_workbook(alldir + '\\' + dir)
                worksheets = file.sheetnames
                for ws in worksheets:

                    if ws != '交易手册划分汇总':
                        wb = file[ws]
                        # text = ''
                        for i in range(2, wb.max_row + 1):
                            if wb.cell(i, 2).value not in ['None', ''] and wb.cell(i, 2).value != None:
                                text += wb.cell(i, 2).value.replace('\n', '')
                                # text = wb.cell(i, 2).value
        textlist.append(text)
        return textlist

    #根据词性查找词组
    def findcizu(self,allvocab, allvocabflag, word):
        wordzuhe = []
        for k in range(len(allvocab)):

            loc = [i for i, x in enumerate(allvocab[k]) if x == word]
            # print(len(loc))
            for i in loc:
                word = allvocab[k][i]
                if i != 0:
                    for j in range(i - 1, -1, -1):
                        front = allvocabflag[k][j]
                        fs = get_alpha_str(front)
                        frontword = front.replace(fs, '')
                        if fs in ['a', 'ag', 'an', 'ad', 'al', 'g', 'h', 'j', 'k', 'l', 'n', 'ns', 'nr', 'nt', 'nz',
                                  'nrt', 's', 'vn', 'vg'] or frontword in ['和', '与', '及', '以及', '及其', '并且']:
                            front = front.replace(fs, '')
                            # wordzuhe.append(str(front+word))
                            word = front + word
                        else:
                            break
                if i != len(allvocabflag[k]) - 1:
                    for j in range(i + 1, len(allvocabflag[k]) - 1):
                        behind = allvocabflag[k][j]
                        bs = get_alpha_str(behind)
                        behindword = behind.replace(bs, '')
                        if bs in ['ag', 'an', 'ad', 'al', 'g', 'h', 'j', 'k', 'l', 'n', 'ns', 'nr', 'nt', 'nz', 'nrt',
                                  's', 'vn', 'vg'] \
                                or behindword in ['和', '与', '及', '以及', '及其', '并且']:
                            behind = behind.replace(bs, '')
                            # wordzuhe.append(str(front+word+behind))
                            word = word + behind
                        else:
                            break
                wordzuhe.append(word)
        return wordzuhe


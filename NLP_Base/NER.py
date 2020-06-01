import jieba
import jieba.analyse
import jieba.posseg as pseg
import openpyxl


num_ncp=15
num_ny=17
num_js=5

stop = open('baidu_stopwords.txt', 'r+', encoding='utf-8')
stopword = stop.read().split("\n")

def baikezhishijiagong():
    p = open(r'玉米1.txt', 'r', encoding = 'utf-8')
    q = open(r'玉米识别结果1.txt', 'w', encoding = 'utf-8')
    r = open(r'玉米识别结果21.txt', 'w', encoding = 'utf-8')
    resultlist=[]
    for line in p.readlines():
        words = pseg.cut(line)
        for word, flag in words:
            if flag in ['n','ng','nr','nrfg','nrt','ns','nt','nz','s','t','tg']:
                r.write(str(word) + str(flag) + '\t')
                resultlist.append(str(word) + str(flag))
        r.write('\n')
    resultlist=list(set(resultlist))
    for item in resultlist:
        q.write(item+'\t')
    p.close()
    q.close()
    r.close()

def jiaoyishouce():
    file1=openpyxl.load_workbook('E:\\桌面\\期货\\研报ocr\\能源期货.xlsx')
    worksheets=file1.sheetnames
    print(worksheets)
    for ws in worksheets:
        if ws!='交易手册划分汇总':
            wb2=file1[ws]
            wb2.cell(row=1, column=1, value='相关因素')
            wb2.cell(row=1, column=2, value='语料原文')
            wb2.cell(row=1, column=3, value='分词结果')
            wb2.cell(row=1, column=4, value='名词识别')
            wb2.cell(row=1, column=5, value='关键词提取（TF-IDF）')
            wb2.cell(row=1, column=6, value='关键词提取（textrank）')
            wb2.cell(row=1, column=7, value='相关因素(分词)')

            for i in range(2,wb2.max_row+1):
                factor=wb2.cell(i,1).value
                fac_list2 = pseg.cut(factor)
                facresult2 = []
                for word, flag in fac_list2:
                    # if flag not in ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wm','wn','ws','wp','wb','wh']:
                    if flag != 'x':
                        facresult2.append(str(word))
                wb2.cell(row=i, column=7, value=str(facresult2))
                context=wb2.cell(i,2).value

                seg_list2 = pseg.cut(context)
                segresult2 = []
                for word,flag in seg_list2:
                    #if flag not in ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wm','wn','ws','wp','wb','wh']:
                    if flag!='x':
                        segresult2.append(str(word))
                wb2.cell(row=i, column=3, value=str(segresult2))
                entity_list=[]
                words=pseg.cut(context)
                for word, flag in words:
                    #print(word,flag)
                    if flag in ['n','ng','nr','nrfg','nrt','ns','nt','nz','s','t','tg','vn'] and word not in stopword:
                        entity_list.append(str(word) + str(flag))
                entity_freq_list={}
                for item in entity_list:
                    if item not in entity_freq_list:
                        entity_freq_list[item]=1
                    else:
                        entity_freq_list[item]+=1
                wb2.cell(row=i, column=4, value=str(entity_freq_list))
                keywords1 = jieba.analyse.extract_tags(context, topK=30, withWeight=True, allowPOS=('n','ng','nr','nrfg','nrt','ns','nt','nz','s','t','tg','vn'))
                keywordlist1={}
                for item in keywords1:
                    keywordlist1[item[0]]=item[1]
                wb2.cell(row=i, column=5, value=str(keywordlist1))
                keywords2 = jieba.analyse.textrank(context, topK=30, withWeight=True, allowPOS=(
                'n', 'ng', 'nr', 'nrfg', 'nrt', 'ns', 'nt', 'nz', 's', 't', 'tg', 'vn'))
                keywordlist2 = {}
                for item in keywords2:
                    keywordlist2[item[0]]=item[1]
                wb2.cell(row=i, column=6, value=str(keywordlist2))

    file1.save('E:\\桌面\\期货\\研报ocr\\能源期货.xlsx')

jiaoyishouce()
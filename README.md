# FPP

------

### 项目结构

```
FPP
│  README.md
│  result.txt
│  scrapy.cfg
│  
├─.idea
│          
├─docs
│  │  bert_embedding.txt
│  │  聚类汇总.xlsx
│  │  
│  ├─google_trends
│  │      google_indexs.csv
│  │      
│  ├─stopwords
│  │      baidu_stopwords.txt
│  │      cn_stopwords.txt
│  │      hit_stopwords.txt
│  │      README.md
│  │      scu_stopwords.txt
│  │      
│  ├─分词结果
│  │      data.txt
│  │      yian_data.txt
│  │      
│  ├─图谱相关
│  │      Concept_1.0.xlsx
│  │      entity_20200427.xlsx
│  │      relation_20200427.xlsx
│  │      
│  ├─待爬词汇
│  │      hot words.txt
│  │      热词表.txt
│  │      
│  ├─期货文档
│  │  │  scrapy_items.txt
│  │  │  农产品期货.txt
│  │  │  农产品期货.xlsx
│  │  │  能源期货.txt
│  │  │  能源期货.xlsx
│  │  │  金属期货.txt
│  │  │  金属期货.xlsx
│  │  │  
│  │  ├─交易手册
│  │  │      农产品期货.txt
│  │  │      农产品期货.xlsx
│  │  │      能源期货.txt
│  │  │      能源期货.xlsx
│  │  │      金属期货.txt
│  │  │      金属期货.xlsx
│  │  │      
│  │  └─研报ocr
│  │          农产品期货.xlsx
│  │          相似度计算结果.xlsx
│  │          能源期货.xlsx
│  │          词频统计.xlsx
│  │          金属期货.xlsx
│  │          
│  └─期货词频统计
│          期货词频统计.xlsx
│          结果比较.xlsx
│          统计结果20200427.xlsx
│          
├─FPP
│  │  items.py
│  │  middlewares.py
│  │  pipelines.py
│  │  README.md
│  │  save_data.py
│  │  settings.py
│  │  __init__.py
│  │  
│  ├─spiders
│  │  │  baidubaike.py
│  │  │  baidubce.py
│  │  │  baiduindex.py
│  │  │  google_trends.py
│  │  │  nongyezhishi.py
│  │  │  start_baidu_index.py
│  │  │  test.py
│  │  │  __init__.py
│  │  │  
│  │  ├─baidu_index
│  │  │  │  baidu_index.py
│  │  │  │  config.py
│  │  │  │  extended_baidu_index.py
│  │  │  │  utils.py
│  │  │  │  __init__.py
│  │  │  │  
│  │  │  └─__pycache__
│  │  │          baidu_index.cpython-36.pyc
│  │  │          config.cpython-36.pyc
│  │  │          extended_baidu_index.cpython-36.pyc
│  │  │          utils.cpython-36.pyc
│  │  │          __init__.cpython-36.pyc
│  │  │          
│  │  └─__pycache__
│  │          
│  └─__pycache__
│          
├─Future_Price
│  │  config.py
│  │  finance_googleIndex.py
│  │  FP_Sql.py
│  │  readmat.py
│  │  test.py
│  │  __init__.py
│  │  
│  ├─model
│  │      FuturesDataCon.mat
│  │      
│  └─__pycache__
|
├─graph
│      entity_relation.py
│      graph_update.py
│      
├─NLP_Base
│  │  analysis.py
│  │  G_similar.py
│  │  G_word2vec.py
│  │  jieba_api.py
│  │  NER.py
│  │  NLP_api.py
│  │  phrasemine.py
│  │  similarity.py
│  │  test.py
│  │  __init__.py
│  │  
│  ├─models
│  │      word2vec_100.model
│  │      word2vec_100.vector
│  │      
│  └─__pycache__
│          
└─utils
    │  dataframe_opt.py
    │  excel2text.py
    │  fun_tongji.py
    │  graph_tool.py
    │  rw_excel.py
    │  sim_tool.py
    │  __init__.py
    │  
    └─__pycache__
```

``` python
部分命令：
生成项目树： tree . /f > ./result.txt
生成requirements.txt : pipreqs ./ --encoding=utf8
```
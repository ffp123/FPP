# FPP

------

### 项目结构

```
FPP
├─.idea
│  │  deployment.xml
│  │  encodings.xml
│  │  FPP.iml
│  │  misc.xml
│  │  modules.xml
│  │  vcs.xml
│  │  webServers.xml
│  │  workspace.xml
│  │  
│  ├─dictionaries
│  │      tmoom.xml
│  │      
│  └─inspectionProfiles
│          Project_Default.xml
│          
├─docs
│  │  char_N_20190215.txt
│  │  data.txt
│  │  症状词标准化结果.xlsx
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
│  ├─期货文档
│  │      scrapy_items.txt
│  │      农产品期货.txt
│  │      农产品期货.xlsx
│  │      能源期货.txt
│  │      能源期货.xlsx
│  │      金属期货.txt
│  │      金属期货.xlsx
│  │      
│  └─期货词频统计
│          期货词频统计.xlsx
│          结果比较.xlsx
│          
├─FPP
│  │  items.py
│  │  middlewares.py
│  │  pipelines.py
│  │  settings.py
│  │  
│  ├─spiders
│  │  │  baidubaike.py
│  │  │  baidubce.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          
│  └─__pycache__
│          
├─NLP_Base
│  │  G_similar.py
│  │  G_word2vec.py
│  │  jieba_api.py
│  │  NER.py
│  │  NLP_api.py
│  │  test.py
│  │  __init__.py
│  │  
│  └─models
│          word2vec_100.model
│          word2vec_100.vector
│          yian_word2vec_100.model
│          yian_word2vec_100.vector
│          
├─utils
│   │  excel2text.py
│   │  rw_excel.py
│   │  __init__.py
│          
│  README.md
│  requirements.txt
│  scrapy.cfg
```

``` python
部分命令：
生成项目树： tree . /f > ./result.txt
生成requirements.txt : pipreqs ./ --encoding=utf8
```
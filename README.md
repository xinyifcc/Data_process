# Data_process
### Release Notes
* 01/04/17 First-Edition : 通过['检查结论'],设置规则,按月将数据分为positive和negative; CHECKED :+1:
* 01/06/17 Second-Edition : 添加['病人来源'],创建pos和neg文件夹,按照来源再次细分数据;	CHECKED :+1:
* 01/06/17 Third-Edition : 将按月份/有病没病/病人来源细分的数据与CT图片链接,创建分类文件夹,并将图片按类别复制至新的文件夹.(	Code not been implement!!) UNCHECKED
* 01/10/17 Third-Edition Checked
* 01/12/17 ADD img_mean.py : Resize the image first and then get their means
* 01/12/17 gen_xml.py : Change the inital .jpg file into .xml file, also random the bbox location for making normal.
More updates later


### Dependencies

Basic Data Process: python.pandas
V2_updated: pinyin, sys, os, cv2, numpy
12/01 update:
```javascript
import os
import random
import lxml.etree
from xml.etree import ElementTree
import lxml.builder
import xml.etree.cElementTree as ET
import scipy.misc as misc
```

### Descriptions

Row Data Separation: Positive & Negative

 * python & pandas are used 
 * Rules based on the row data in Nov&Dec 2016
 * More rules will be added

All defined functions:

 * isKeywordIn(): rules will be update !!
 * foo() --Updated to rule()
 * readData()
 * processData() --New Updated
 * main()

And here's main_function code! :+1:

```javascript
def main():
    path = './'
    df = readData(path + 'filename', ['检查编号','检查结论'])
    pos, neg = processData(df)
    pos.to_csv(path + 'filename', sep='\t')
    neg.to_csv(path + 'filename', sep='\t')    
```
#### V2_updated:
```javascript
#读取数据,只需修改path(path内根目录应有month目录):
def processData(month):
    path = './Dec/'
    df = readData('{0}cz_data_{1}.xls'.format(path, month), ['检查编号','检查结论','病人来源'])
    
#分别创建pos和neg的文件夹:
    if not os.path.exists(path + 'pos/'):
        os.mkdir(path + 'pos/')
    if not os.path.exists(path + 'neg/'):
        os.mkdir(path + 'neg/')
        
#分别以病人来源首字母命名已分类的数据并分别存在以上新建文件夹中:
   	for src in sourceList:
        srcName = py.get_initial(src, '')
        pos.to_csv('{0}pos/{1}_pos_{2}.tsv'.format(path, month, srcName), sep='\t', index=False)
        neg.to_csv('{0}neg/{1}_neg_{2}.tsv'.format(path, month, srcName), sep='\t', index=False)
```

### Other implementations

##### Package installation help:
 * pandas : pip install pandas
 * pinyin : sudo pip install pinyin -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

### MORE UPDATES IS ON THE WAY ...


# -*- coding: utf-8 -*-
import pandas as pd
import pinyin as py
import sys
import os
import shutil


def isKeywordsIn(li):
    kwList = ['a', 'b', 'c', 'd']
    for each in kwList:
        if each in li:
            return True
    return False


def rule(x):
    for L in x:
        if 'A' not in L or isKeywordsIn(L):
            return False
    return True


def readData(filename, columns):
    df = pd.read_excel(filename, usecols=columns)
    return df.dropna()


def makeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def copyFiles(files, to_dir):
    for each in files:
        if os.path.exists(each):
            shutil.copy(each, to_dir)
        else:
            print ('No such file', each)


def processData(month):
    path = './data_all/{}'.format(month)
    imgPath = './img'
    df = readData('{0}/cz_data_{1}.xls'.format(path, month), ['1','2','3'])
    df['c'] = df['1'].apply(lambda x: [item.strip() for item in x.split()])
    df['1'] = df['c'].apply(lambda x: ' '.join(x))
    sourceList = list(set(df['3']))
    criterion = df['c'].map(rule)

    for d in ['pos', 'neg']:
        makeDir('/'.join([path, d]))
        makeDir('/'.join([imgPath, '..', month]))
        makeDir('/'.join([imgPath, '..', month, d]))
        for src in sourceList:
            makeDir('/'.join([imgPath, '..', month, d, py.get(src, format='strip')]))

    for src in sourceList:
        sdf = df[df['3'] == src] 
        pos = sdf[~criterion].drop('c', axis=1)
        neg = sdf[criterion].drop('c', axis=1)
        srcName = py.get_initial(src, '')
        pos.to_csv('{0}/pos/{1}_pos_{2}.tsv'.format(path, month, srcName), sep='\t', index=False)
        neg.to_csv('{0}/neg/{1}_neg_{2}.tsv'.format(path, month, srcName), sep='\t', index=False)

        posPicNameList = [''.join([imgPath, '/', x, '.jpg']) for x in pos['1'].tolist()]
        negPicNameList = [''.join([imgPath, '/', x, '.jpg']) for x in neg['1'].tolist()]

        copyFiles(posPicNameList, '/'.join([imgPath, '..', month, 'pos', py.get(src, format='strip')]))
        copyFiles(negPicNameList, '/'.join([imgPath, '..', month, 'neg', py.get(src, format='strip')]))


if __name__ == '__main__':
    processData('Dec')

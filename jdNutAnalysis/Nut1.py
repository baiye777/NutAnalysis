import pandas as pd
import matplotlib as plt
from wordcloud import WordCloud,STOPWORDS
import re,jieba,json,csv
import numpy as np
from jdNutAnalysis.worldcloud import get_rate_img,get_stop_list

def get_pie():
    pass


def price_evaluate():
    pass

def get_reference(reference):#坚果类型统计
    word_stop = get_stop_list()  # 获得停用词
    jianguo, Nut_count=['松子','榛子','板栗','杏仁','开心果','莲子','葵花子','桃仁'],{}
    for name in reference:
        if name !='' and name in jianguo and name not in word_stop:
            Nut_count[name]+=1
    print(Nut_count)

def test(reference):
    Nut_count = ['松子', '榛子', '板栗', '杏仁', '开心果', '莲子', '葵花子', '桃仁']
    for Nut in Nut_count:
        for ref in reference:

def get_content_hope(series):#深入分析评论
    word_stop = get_stop_list()  # 获得停用词
    select_wodrd=['差评','希望','京东','买','买']
    content_analysis,conetent_hope,conetent_negative={'期待':0,'差评':0,'坏的':0},{},{}
    for content in series:
        if '期待' in content or '希望' in content :
            content_analysis['期待']+=1
            pattern = re.compile('[^\u4e00-\u9fa5]', re.S)  # 这个是提取中文的代码
            contenth = pattern.sub('', content)
            contenth = list(jieba.cut(contenth))  # 结巴分词
            for ch in contenth:
                if ch != '' and ch not in word_stop and ch not in select_wodrd:
                    if ch in conetent_hope.keys():
                        conetent_hope[ch]+=1
                    else:
                        conetent_hope[ch]=1
        elif '差评' in content:
            content_analysis['差评'] += 1
            pattern = re.compile('[^\u4e00-\u9fa5]', re.S)  # 这个是提取中文的代码
            contentn = pattern.sub('', content)
            contentn = list(jieba.cut(contentn))  # 结巴分词
            for ch in contentn:
                if ch != '' and ch not in word_stop and ch not in select_wodrd:
                    if ch in conetent_negative.keys():
                        conetent_negative[ch]+=1
                    else:
                        conetent_negative[ch]=1
        elif '坏的' in content:
            content_analysis['坏的'] += 1
    print(content_analysis)
    print(conetent_hope)
    print(conetent_negative)
    get_rate_img(conetent_hope,'评论期望')
    get_rate_img(conetent_negative,'评论差评原因')


def get_content(data):#处理评价内容
    content=data.replace('哈哈',' ').replace('京东',' ').replace('包装',' ').replace('零食','')
    pattern = re.compile('[^\u4e00-\u9fa5]', re.S)  # 这个是提取中文的代码
    content = pattern.sub('', content)
    # print(description)
    content = list(jieba.cut(content))  # 结巴分词
    return content

def get_content_rate(contents):#得到评论的词云图
    word_stop  = get_stop_list() # 获得停用词
    word_dict ={}
    word_li = ['不错', '好吃', '吃', '买', '购买', '特别','东西','收到','非常','物流','没有']
    for content in contents:  # 每一个岗位的描述
        for word in content:
            if  word != '' and  word not in word_stop and word not in word_li:
                if  word in word_dict.keys():  # 字典赋值的一个用法，很有意思，检测word是否在字典里
                    word_dict[ word] += 1  # 在，则word对应的值加1
                else:
                    word_dict[ word] = 1  # 不在则等于1，即赋值建立字典的key和values
    print(word_dict)
    return word_dict

def get_id(strs):
    d=re.search(r'\d+',strs,re.S).group(0)

    return d

def main():
    col=['noid','id','content','reference']
    data = pd.read_csv("data/Nut.csv",error_bad_lines=False,header=None,names=col)
    data=pd.DataFrame(data)
    # data=data.drop(['noid'],axis=1)
    print(data.columns)
    print(data.info())
    print(data.head())
    data['id']=data['id'].map(get_id)#处理id
    data['content']=data['content'].str.split(':').str[1]#处理content
    data['reference'] = data['reference'].str.split(':').str[1].str.split('}').str[0]#处理reference

    # contents=data['content'].apply(get_content)#获得坚果评论的词云
    # content_rate=get_content_rate(contents)
    # get_rate_img(content_rate,'评论统计分析')

    # get_content_hope(data['content'])#处理顾客期待做什么

    # reference=data['reference'].apply(get_content)#处理坚果种类
    # get_reference(reference)#对各种坚果的统计
    test(data['reference'])

if __name__ == '__main__':
    main()

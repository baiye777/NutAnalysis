#coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import re,jieba
import numpy as np
from matplotlib.font_manager import FontManager, FontProperties
from jdNutAnalysis.plt画图 import get_plot,get_scatter,get_hist,get_bar,get_pie
from jdNutAnalysis.worldcloud import get_rate_img,get_stop_list

# '''
# n2_1：是否自营对商品销量的影响
# n2_2：商品价格对商品销量(评论)的影响
# n2_3：商品的搜索的名称对商品销量影响
# n2_4：各个品牌的坚果销量情况（前10名）
# '''

# def getFont():
#     return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')#中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']#中文显示
plt.rcParams['axes.unicode_minus'] = False



def get_word_rate(series):
    '''
    统计词频
    :param series:Series对象
    :return: 词频字典
    '''
    word_stop=get_stop_list()#获得停用词
    word_dict={}
    word_li = ['数据','数据分析','分析','工作','优先','要求']
    for description in list(series):#每一个岗位的描述
        for word in description:#描述里面的每一个词
            word = word.strip().upper()#大写
            #判断词不为空，不是停用词，不在word_li列表里面，就进行词频统计
            if word !='' and word not in word_stop and word not in word_li:
                if word in word_dict.keys():#字典赋值的一个用法，很有意思，检测word是否在字典里
                    word_dict[word] += 1#在，则word对应的值加1
                else:
                    word_dict[word]=1#不在则等于1，即赋值建立字典的key和values
    return word_dict

def self_support(d3,d2):#d3是自营，d2是评论数
    ziyin = {'自营': 0, '非自营': 0}
    zy,fzy=0,0
    for i3 in list(d3):
        for i2 in list(d2):
            if i3.strip() in ziyin.keys():
                zy=int(zy+i2)
            else:
                fzy=int(fzy+i2)
    series=np.array([[zy],[fzy]])

    data=pd.DataFrame(series,index=['自营','非自营'],columns=['评论数'])
    print(data['评论数'],type(data['评论数']))
    print(list(data.index),type(list(data.index)),list(data.index)[0])
    print((data/data.sum()).round(4))
    get_pie(data['评论数'],title='是否为京东自营',filename='是否为京东自营的评论数',choice='n2_3')


def price_evaluate(d1,d2):#价格分布图

    # get_bar(d1,d2,title='坚果价格分布情况区间',ylabel='商品价格分布',filename='坚果价格分布区间情况',choice='n2_2')
    # get_hist(d1,d2,title='坚果价格状况',ylabel='商品价格分布',filename='坚果价格分布密度',choice='n2_2')
    # get_scatter(d1,d2,title='坚果价格与评论',ylabel='商品评论',filename='坚果价格与评论',choice='n2_2')
    # get_plot(d1,d2,title='坚果价格与评论',ylabel='商品评论',filename='坚果价格与评论线状分布',choice='n2_2')
    pass

def brand_world(d2,series):#series是data['title']

    brand_count={}#对品牌名的统计
    for title in series:
        name = (title.split(' '))[0][0:4].strip('【').strip('(').strip()
        if name =='京东超市':
            name = (title.split(' '))[0][4:8].strip('【').strip('(').strip()
        pattern = re.compile('[^\u4e00-\u9fa5]', re.S)  # 这个是提取中文的代码
        brand = pattern.sub('', name)#brand是品牌
        if brand !=''  and brand in brand_count.keys() and brand !='洽洽' and brand !='满':
            brand_count[brand] += 1
        elif brand=='洽洽':
            brand_count['洽洽坚果'] += 1
        else:
            brand_count[brand]=1
    print(brand_count)

    xx=pd.Series(brand_count,index=brand_count.keys())
    # print(xx)
    print(xx.sum())
    print(xx.sort_values(ascending=True).tail(12))
    return brand_count

def brand_evaluate(data):#data是全部数据
    brand_co = {'臻味':0,'甘源':0,'俏香阁':0,'良品铺子': 0, '三只松鼠': 0, '百草味': 0, '新农哥': 0, '洽洽坚果': 0, '沃隆': 0,  '粒上皇': 0, '爱心东东': 0, '美国进口': 0}  # 对品牌名的统计
    brand_commit,title_commit,titles,commits={},{},data['title'],data['commit']
    for key, value in zip(titles, commits):#建立一个title:commit的字典
        title_commit[key] = value

    for title in title_commit.keys():#得到各个品牌的评论
        name = (title.split(' '))[0][0:4].strip('【').strip('(').strip()
        if name == '京东超市':
            name = (title.split(' '))[0][4:8].strip('【').strip('(').strip()
        pattern = re.compile('[^\u4e00-\u9fa5]', re.S)  # 这个是提取中文的代码
        brand = pattern.sub('', name)  # brand是品牌
        if brand != '' and brand in brand_commit.keys() and brand != '洽洽' and brand != '满':
            brand_commit[brand] += title_commit[title]
        elif brand == '洽洽':
            brand_commit['洽洽坚果'] += title_commit[title]
        else:
            brand_commit[brand] = 1

    print(brand_commit)
    bc = pd.Series(brand_commit, index=list(brand_commit.keys()))
    print(bc.sort_values(ascending=False).head(10))
    d1,d2=bc.sort_values(ascending=False).head(10),bc.index#输入坚果前十的销量
    get_bar(d1,d2,title='各个品牌的坚果销量情况',ylabel='坚果品牌',filename='各个品牌的坚果销量情况',choice='n2_4')

def test(d2,d3,series):
    pass


def title_description():
    pass

def commit(s):#把评论的万和+去掉
    da=str(s).strip().replace('.','').replace('万','0000').replace('+','')
    ta=float(da)
    return ta

def price(s):
    if s<300:
        return s


def main():
    data=pd.read_csv('data/Nut2.csv',encoding='gb18030')
    data=data.fillna({'icon':'非'})
    print(data.info())
    data['price'] = data['price'].map(price)
    data['commit']=data['commit'].map(commit)
    d1,d2= data['price'],data['commit']
    print(data.head())

    # 坚果的价格和评论数的关系和分布
    # price_evaluate(d1,d2)#d1是价格，d2是评论数

    #是否自营对商品销量的影响
    # self_support(data['icon'],d2)#d2是评论数

    # 商品的搜索的品牌对商品销量影响
    word_dict=brand_world(d2,data['title'])#统计各种品牌的出现评率
    # get_rate_img(word_dict, filename='品牌名的统计')
    # brand_evaluate(d2,word_dict,data['title'])

    # 商品的搜索的描述对商品销量影响
    title_description()
    brand_evaluate(data)

if __name__ == '__main__':
    main()

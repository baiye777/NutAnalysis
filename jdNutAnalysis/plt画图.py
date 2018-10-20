#coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import re,jieba
import numpy as np
from matplotlib.font_manager import FontManager, FontProperties

def getFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')#中文字体
plt.rcParams['font.sans-serif'] = ['Simhei']#中文显示
plt.rcParams['axes.unicode_minus'] = False

def get_plot(d1,d2,title,ylabel,filename,choice):#画线状图plt.figure(figsize=(8, 8))  # 设置图片大小
    plt.figure(figsize=(8, 8))  # 设置图片大小
    plt.plot(d1,d2,color='r',marker='s',markersize=4,linestyle='-.',linewidth=4)#线状图
    plt.ylabel('%s' % ylabel, fontsize=15, fontproperties=getFont())
    plt.title('%s' % title, fontsize=20, fontproperties=getFont())
    plt.savefig('figure/%s.png' % filename, dpi=400)  # 保存图片

def get_scatter(d1,d2,title,ylabel,filename,choice):
    plt.figure(figsize=(8, 8))  # 设置图片大小
    plt.scatter(d1, d2, marker='x', color='#D02090')  # 散点图
    plt.ylabel('%s' % ylabel, fontsize=15, fontproperties=getFont())
    plt.title('%s' % title, fontsize=20, fontproperties=getFont())
    plt.savefig('figure/%s.png' % filename, dpi=400)  # 保存图片

def get_hist(d1,d2,title,ylabel,filename,choice):
    plt.figure(figsize=(8, 8))  # 设置图片大小
    d1.hist(bins=30,density=True)#画直方图
    d1.plot(kind='kde', style='b--')#画线
    plt.grid(True)#画网格
    plt.ylabel('%s' % ylabel, fontsize=15, fontproperties=getFont())
    plt.title('%s' % title, fontsize=20, fontproperties=getFont())
    plt.savefig('figure/%s.png' % filename, dpi=400)  # 保存图片

def get_pie(series,title,filename,choice):#圆饼图
    plt.figure(figsize=(8, 8))  # 设置图片大小
    serie=(series/series.sum()).round(4)
    values = list(serie * 100)
    labels = list(serie.index)  # 标签
    plt.pie(values,labels=labels,autopct='%.2f%%')  # 饼状图
    plt.title(title, fontsize=20)  # 标题
    plt.savefig('figure/%s'%filename, dpi=400, bbox_inches='tight')  # 保存，dpi是密度，bbox是英尺

def get_bar(d1,label,title,ylabel,filename,choice):
    if choice=='n2_2':
        s = pd.cut(list(d1), bins=[0, 10, 40, 70, 100, 130, 180, 299]).value_counts()
        # 绘图
        plt.figure(figsize=(10, 8))
        s.plot(kind='bar')
        labels = ['10元以下', '10-40元', '30-70元', '70-100元', '100-130元', '130-180元', '180元以上']  # 标签名
        plt.xticks(range(len(s)), labels, rotation=30, fontsize=12,fontproperties=getFont())  # 设置倾斜度
        plt.ylabel('%s'%ylabel, fontsize=15,fontproperties=getFont())
        plt.title('%s'%title, fontsize=20,fontproperties=getFont())
        plt.savefig('figure/%s.png'%filename, dpi=400,bbox_inches='tight')  # 保存图片
    elif choice=='n2_4':
        # 绘图
        plt.figure(figsize=(10, 8))
        d1.plot(kind='barh',alpha=0.7)
        plt.yticks(range(len(d1)),rotation=30, fontsize=12, fontproperties=getFont())  # 设置倾斜度
        plt.xticks(list(range(0,25000000,5000000)),rotation=30, fontsize=12, fontproperties=getFont())  # 设置倾斜度
        plt.ylabel('%s' % ylabel, fontsize=15, fontproperties=getFont())
        plt.title('%s' % title, fontsize=20, fontproperties=getFont())
        plt.savefig('figure/%s.png' % filename, dpi=400,bbox_inches='tight')  # 保存图片
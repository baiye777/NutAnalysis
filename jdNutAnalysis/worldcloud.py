import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import re,jieba

def get_rate_img(word_dict,filename):
    backgroud_Image = plt.imread('data/back.jpg')  # 读取背景图片
    wc = WordCloud(
        background_color='white',  # 背景颜色
        mask=backgroud_Image,  # 设置背景图片
        font_path='/System/Library/Fonts/PingFang.ttc',  # 字体
        max_words=1000,  # 设置最大现实的字数
        max_font_size=150,  # 设置字体最大值
        colormap='Set1',  # 颜色,参考链接：https://matplotlib.org/examples/color/colormaps_reference.html
    )
    wc.generate_from_frequencies(word_dict)  # 根据词频生成词云
    plt.imshow(wc)  # 将词云图通过plt来显示
    # plt.show()
    plt.axis('off')  # 去掉坐标轴
    plt.savefig('figure/' + filename, dpi=400, bbox_inches='tight')  # 保存图片

def get_stop_list(filename='data/中文停用词库.txt'):
    '''
    获取常用停用词（常用的停用词）
    :param filename:
    :return:
    '''
    stop_word_list=[]
    for line in open(filename,'r',encoding='gb18030'):#逐行读取
        stop_word_list.append(line.strip())
    return stop_word_list
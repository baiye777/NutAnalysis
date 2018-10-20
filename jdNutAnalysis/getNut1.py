import pandas as pd
import matplotlib as plt
from wordcloud import WordCloud,STOPWORDS
import re,jieba,json,csv
import numpy as np

def main():
    col=['noid','id','content','reference']
    data = []
    id, content, reference = [], [], []  # 设置要获取的信息
    # data = pd.read_csv("data/Nut1.csv",delimiter='\t',sep=';',error_bad_lines=False)
    data.append(col)
    with open("data/Nut.csv") as f:
        for i in f:
            x=json.loads(i)
            id.append(x['id']['$numberLong'])
            content.append(x['content'])
            reference.append(x['referenceName'])
            info = {
                'id': id,
                'content': content,
                'referenceName': reference
            }
            print(info)
            df = pd.DataFrame(info)
            df.to_csv('data/Nut1.csv',encoding='gb18030')

if __name__ == '__main__':
    main()

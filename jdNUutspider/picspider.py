# prices=list(set(response.css('div.p-price strong i::text').extract()))
#             #获取评论数
#             commits = list(set(response.css('div.p-commit strong a::text').extract()))
#             #是否自营
#             icons=list(set(response.css('div.p-icons strong i::text').extract()))
#             pci={'prices':prices,'commits':commits,'icons':icons}
# for price in prices:
#     for commit in commits:
#         for icon in icons:
import pymongo
import requests
import time
from bs4 import BeautifulSoup
import re,os
MONGO_URL='localhost'
MONGO_DB='JDBAR'
MONGO_TABLE = 'Nut'

def spider():
    for page in range(1,201,2):
        url = 'https://search.jd.com/Search?keyword=%E5%9D%9A%E6%9E%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%9D%9A%E6%9E%9C&stock=1&page=' + str(page) + '&s=' + str(page*60-60) + '&click=0'
        # urlt='https://search.jd.com/Search?keyword=%E5%9D%9A%E6%9E%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%9D%9A%E6%9E%9C&stock=1&page=7&s=178&click=0'
        html = requests.get(url)
        html.encoding='utf-8'
        res=html.text
        soup=BeautifulSoup(res,'html.parser')
        pics=soup.select('li.gl-item')
        time.sleep(1)
        ye=(int(page)+1)%2#第几页
        print('第%d页'%ye)
        with open('data/Nut2.csv', 'a', encoding='gb18030') as f:
            for pic in pics:
                # id=pic.find(class_='gl-item')['data-sku']#id
                # price=pic.find(class_='p-price').strong.em.i.get_text().strip()#价格
                titles=pic.find(class_='p-name').a.em.get_text().strip()#标题
                icons=pic.find(class_='p-icons').get_text().strip()#是否自营
                imgurl ='http:'+pic.find(class_='p-img').a.img['source-data-lazy-img']#找出图片的地址
                pic=str(pic)
                id=re.search(r'.*?class="gl-item".*?data-sku="(.*?)".*?>',pic,re.S|re.I)#商品id
                prices=re.search(r'.*?class="p-price".*?<i>(.*?)</i>.*?',pic,re.S|re.I)#商品价格
                commits=re.search(r'.*?class="p-commit".*?target="_blank">(.*?)</a>.*?',pic,re.S|re.I)#商品评论
                pid,price,commit=id.group(1),prices.group(1),commits.group(1)

                ic,ts=icons[0:2],titles.split(',')
                icon,title=ic," ".join(str(y) for y in ts)

                img = requests.get(imgurl).content
                with open('img/%s.png'%pid, 'wb') as im:
                    im.write(img)
                im.close()
                print(pid, price, commit, icon, title,imgurl)


                Nut2=str(pid)+','+str(price)+','+str(commit)+','+icon+','+title+'\n'
                f.write(Nut2)  # 逐行写入表文件
            f.close()

#主体函数
def main():
    if not os.path.exists('data'):#判断文件是否存在
        os.mkdir('data')#如果不存在，就创建文件夹
    # 首先创建表文件，并加入第一列的列名
    with open('data/Nut2.csv','w') as f:
        col = 'id'+','+'price'+','+'commit'+','+'icon'+','+'title'+'\n'#逗号用于隔开，写入的是标题
        f.write(col)
    f.close()
    spider()

if __name__=='__main__':
    main()
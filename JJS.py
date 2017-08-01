# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import xlwt
import matplotlib
import matplotlib.pyplot as plt


base_url='http://shenzhen.jjshome.com/zf/?n='
def getPages(number):
    url=base_url+str(number)
    content=requests.get(url).text
    soup=BeautifulSoup(content,"html.parser")
    patternPayment = re.compile(
        'payment=(.*?),',re.S);
    patternPrice = re.compile(
        'rentPrice=(.*?),',re.S);

    if "PageInfo" in soup.text:
        prices = re.findall(patternPrice, soup.text)
        payments=re.findall(patternPayment, soup.text)
    listbox=soup.select(".text")
    listboxTemp=[]
    for i in range(0,len(listbox)):
        info={}
        item=listbox[i]
        if item.text:
            info["标题"]=item.select(".tit")[0].text.strip()
            attrs=item.select(".attr")
            first=attrs[0].select("span")
            second=attrs[1].select("span")
            third=attrs[2].select("span")
            info["户型"]=first[0].text
            info["朝向"]=first[1].text
            info["建筑面积"]=first[2].text
            info["楼层"]=second[1].text
            info["区"]=third[1].text
            labs=item.select(".lab")
            labsLen=len(labs)
            if labsLen>0:
                if labsLen==1:
                    info["交通"]=labs[0].text
                elif labsLen==2:
                    info["看房方式"]=labs[1].text
                else:
                    info["电梯"]=labs[2].text
            if i<len(prices):
                info["租金"]=prices[i]
            if i<len(payments):
                info["租赁方式"]=payments[i]
            listboxTemp.append(info)

    return listboxTemp
    pass
def pandas_to_xlsx(info):
    pd_look = pd.DataFrame([info])
    pd_look.to_excel('jjs.xlsx',sheet_name='jjs')

def main():
    result=[]
    book = xlwt.Workbook()
    ws = book.add_sheet('data',cell_overwrite_ok=True)
    for i in range(0,99):
        infos=getPages(i)
        for j in infos:
            result.append(j)
            print(str(i)+"==="+str(j))
    print("len of result==="+str(len(result)))
    print(result)
    pandas_to_xlsx(result)
    for i in range(0,len(result)):
        item=result[i]
        if item:
            if "标题" in item:
                ws.write(i, 0, item["标题"])
            if "户型" in item:
                ws.write(i, 1, item["户型"])
            if "朝向" in item:
                 ws.write(i, 2, item["朝向"])
            if "建筑面积" in item:
                ws.write(i, 3, item["建筑面积"])
            if "楼层" in item:
                ws.write(i, 4, item["楼层"])
            if "区" in item:
                ws.write(i, 5, item["区"])
            if "电梯" in item:
                ws.write(i, 6, item["电梯"])
            if "租金" in item:
                ws.write(i, 7, str(item["租金"]))
            if "租赁方式" in item:
                ws.write(i, 8, str(item["租赁方式"]))




        # for key,value in item.items():
        #     ws.write(i, key, value)
    book.save("jjs1.xlsx")

    pass


def read():
    df = pd.read_excel("jjs1.xlsx")
    data = list(df.ix[:, 7])
    prices=[]
    for item in data:
        if not str(item)=="nan":
            prices.append(int(item))
    print(prices[0:100])

    matplotlib.style.use('ggplot')#使用ggplot样式

    ts = pd.Series(prices[0:100], index=pd.date_range('1/1/2000', periods=100))
    plt.figure()
    df.plot.hist(alpha=0.5)
    plt.legend()
    plt.show()
    pass


if __name__ == '__main__':
    # main()
    read()

#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import md5
import threading
import urllib
baseUrl="http://www.mmjpg.com/home/1"
# url="http://www.mmjpg.com/mm/945"

def main():
    pages=getPageContent(baseUrl)
    result=getDetitals(pages)

    i=0
    for k in result:
        if i<10:
            dowmloadPic(k,result[k])
        i=i+1


    pass

# 获取每页中的相册列表
def getPageContent(baseUrl):
    urls=[]
    pageContent=requests.get(baseUrl)
    pageContent.encoding="utf-8"
    pageSoup=BeautifulSoup(pageContent.text,"html.parser")
    picRes=pageSoup.select(".pic")

    for items in picRes:
        a=items.select("a")
        if not a is None:
         for url in a:
            tempUrl=url.get("href")
            if "http" in tempUrl and tempUrl not in urls:
                urls.append(tempUrl)
    return urls

def getDetitals(pages):
    result={}
    for url in pages:
        pageContent=requests.get(url)
        pageContent.encoding="utf-8"
        pageSoup=BeautifulSoup(pageContent.text,"html.parser")
        titleTemp=pageSoup.select(".article")
        title=titleTemp[0].select("h2")[0].text
        totalCount=0
        gallery=0
        # 获取页数
        countTemp=pageSoup.select(".page")
        for c in countTemp:
            a=c.select("a")
            t=a[-2]
            href=t.get("href")
            n=href.split("/")
            totalCount=n[len(n)-1]
            gallery=n[len(n)-2]
        # imgUrl="http://img.mmjpg.com/2017/"+gallery+"/"+totalCount+".jpg"
        imgUrl="http://img.mmjpg.com/2017/{}/{}.jpg"
        urls=[]
        for j in range(1,int(totalCount)+1):
            src=imgUrl.format(str(gallery),str(j))
            # print(src)
            urls.append(src)
            result[title]=urls


    return result
    pass


def dowmloadPic(dirName,url):
    for i in range(0,len(url)):
        each=url[i]
        t=threading.Thread()
        pic= requests.get(each)
        m2 = md5.new()
        m2.update(each)
        name=m2.hexdigest()
        # print(dirName,url)
        print(dirName)
        save_img(each,name,"image/"+dirName)
    pass

def save_img(img_url,file_name,file_path):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(file_path)
        #获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path.encode("utf-8"),os.sep,file_name,file_suffix)
       #下载图片，并保存到文件夹中
        urllib.urlretrieve(img_url,filename=filename)
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)

    pass
if __name__ == '__main__':
    main()
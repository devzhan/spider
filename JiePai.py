# -*- coding: UTF-8 -*-
import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import  BeautifulSoup
import re
import json
from config import *
import os
import pymongo
from hashlib import  md5
client=pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]
table=db[MONGO_TABLE]
from multiprocessing import Pool
def get_page_index(offset,keyword ):
    data={
        "offset":offset,
        "format":"json",
        "keyword":keyword,
        "autoload":"true",
        "count":20,
        "cur_tab":3
    }
    url="http://www.toutiao.com/search_content/?"+urlencode(data)
    response=requests.get(url)
    try:
        if response.status_code==200:
            return response.text
        else:
            return None
    except RequestException:
        print("请求错误")
        return None




def parse_page_index(html):
    data=json.loads(html)
    if data and "data" in data.keys():
        for item in data.get("data"):
            yield item.get("article_url")

def get_page_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        else:
            return None
    except Exception:
        print("请求页出错",url)
        return None

def parse_page_detail(html,url):
    soup=BeautifulSoup(html,"html.parser")
    title=soup.select("title")[0].get_text()
    image_pattern=re.compile('var gallery =(.*?);',re.S)
    result=re.search(image_pattern,html)
    if result:
        data=json.loads(result.group(1))
        if data and "sub_images" in data.keys():
            sub_images=data.get("sub_images")
            images=[item.get("url") for  item in sub_images]
            for image in images:
                download_image(image)
            return {
               "title":title,
               "url":url,
               "images":images
            }

def save_to_mongo(result):
    if table.insert_one(result):
        print("保存成功",result)
        return True
    else:
        return False

def main(offset):
   html= get_page_index(offset,"街拍")

   for url in parse_page_index(html):
       html=get_page_detail(url)
       if html:
           result=parse_page_detail(html,url)
           # print(result)
           if result:
            save_to_mongo(result)
def download_image(url):
    response=requests.get(url)
    try:
        if response.status_code==200:
            saveImage(response.content)
        else:
            return None
    except RequestException:
        print("请求图片错误")
        return None
def saveImage(content):
    file_name="{0}/{1}.{2}".format(os.getcwd()+"/image",md5(content).hexdigest(),"jpg")
    if not os.path.exists(file_name):
        with open(file_name,"wb") as f:
            f.write(content)
            f.close()

if __name__ == '__main__':
    groups=[x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool=Pool()
    try:
        pool.map(main,groups)
    except Exception:
        print("下载异常")





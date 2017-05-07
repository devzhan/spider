#-*- coding: UTF-8 -*-
import re
import requests

def getBookDetials():
    response=requests.get("https://book.douban.com/")
    pe='<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>'
    pattern=re.compile(pe,re.S)
    results=re.findall(pattern,response.text)

    for result in  results:
        url,name,author,date=result
        author=re.sub("\s","",author)
        date=re.sub("\s","",date)
        print(url,name,author,date)

    pass

if __name__=="__main__":
    getBookDetials()
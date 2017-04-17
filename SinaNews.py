#-*- coding: UTF-8 -*-
import requests;
from bs4 import BeautifulSoup
import json

#  获取新闻title 和url
def getTitleUrl():
    url = "http://news.sina.com.cn/china/"
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    sour = soup.select(".blk122")
    newsBean = {}
    for news in sour:
        a = news.select("a")
        for i in a:
            title = i.text
            href = i["href"]
            newsBean[title] = href
    return newsBean



# 获取新闻详细内容
def getDetial(newsUrl):
    resNews = requests.get(newsUrl)
    resNews.encoding = "utf-8"
    soupNews = BeautifulSoup(resNews.text, "html.parser")
    newsBean = {}
    news=[]
    if len(soupNews)>0:
        artile = []
        if len(soupNews.select("#artibodyTitle"))>0:
            newsTitle = soupNews.select("#artibodyTitle")[0].text

            timeSource = soupNews.select(".time-source")[0].contents[0].strip()
            newsSource = soupNews.select(".time-source span a")[0].text
            newsBody = soupNews.select("#artibody p")[:-1]
            for p in newsBody:
                artile.append(p.text.strip())
            for t in artile:
                "@".join(artile)
            creator = soupNews.select(".article-editor")[0].text.strip("")
            count= getCommentCount(newsUrl)
            print(newsTitle)
            newsBean["newsTitle"]=newsTitle
            newsBean["timeSource"]=timeSource

            newsBean["newsSource"]=newsSource
            newsBean["newsBody"]=newsBody
            newsBean["creator"]=creator
            newsBean["count"]=count
            news.append(newsBean)
    return news





# 获取评论数量
def getCommentCount(url):

    commentUrl="http://comment5.news.sina.com.cn/page/info?version=1&format=js" \
           "&channel=gn&newsid=comos-{}&group=&compress=0" \
           "&ie=utf-8&oe=utf-8&page=1&page_size=20"
    m=url.split("/")[-1].rstrip(".shtml").lstrip("doc-i")
    comments=requests.get(commentUrl.format(m))
    jd=json.loads(comments.text.strip("var data="))
    commentCount=0
    if(jd.has_key("result")):
        r=(jd["result"])
        if(r.has_key("count")):
            t=r["count"]
            if(t.has_key("total")):

                commentCount=(jd["result"]["count"]["total"])
    return commentCount


def main():
    result=getTitleUrl();
    for k in result:
        value=result[k]
        news=getDetial(value)
        print(news)





    pass

if __name__ == '__main__':
    main()
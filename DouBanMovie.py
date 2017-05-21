#-*- coding: UTF-8 -*-
import requests;
import DouBanMovieBean
import DouBanUser
from bs4 import BeautifulSoup
import xlwt
from datetime import datetime
def getMovies():
    url="https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=0"
    pageContent=requests.get(url)
    pageContent.encoding="utf-8"
    jsonStr=pageContent.json()
    listData=jsonStr.get("subjects")
    movies=[]
    for ditTemp in listData:
        dbm=DouBanMovieBean.Movie()
        dbm.rate=ditTemp.get("rate")
        dbm.cover_x=ditTemp.get("cover_x")
        dbm.is_beetle_subject=ditTemp.get("is_beetle_subject")
        dbm.title=ditTemp.get("title")
        dbm.url=ditTemp.get("url")
        dbm.playable=ditTemp.get("playable")
        dbm.cover=ditTemp.get("cover")
        dbm.id=ditTemp.get("id")
        dbm.cover_y=ditTemp.get("cover_y")
        dbm.is_new=ditTemp.get("cover_y")
        movies.append(dbm)
    movies.sort(key=lambda obj:obj.rate, reverse=True)
    result=[]
    # 考虑性能问题，暂时取10条
    for i in range(0,10):
        result.append(movies[i])
        getComments(movies[i])

    # getComments(movies)



    pass


def getComments(Movie ):
    commenturl="https://movie.douban.com/subject/"+Movie.id+"/comments?status=P"
    pageContent=requests.get(commenturl)
    soup=BeautifulSoup(pageContent.text,"html.parser")
    soup.attrs
    mod_bd=soup.select(".mod-bd")
    users=[]
    for commentitems in mod_bd:
        item=commentitems.select(".comment-item")
        for commentInfos in  item:
            userInfos=commentInfos.select(".avatar")
            userCommet=commentInfos.select(".comment")
            createTimes=userCommet[0].select(".comment-info")
            commentContent=userCommet[0].select(". ")
            print(commentContent[0].text)
            userName=commentContent[0].text.strip()
            content=userCommet[0].p.text.strip()
            createT=""
            for createtime in createTimes:
                time=createtime.select(".comment-time ")
                createT=time[0].text.strip()
            print(userName,content,createT)
            user=DouBanUser.User()
            user.username=userName
            user.content=content
            user.time=createT
            users.append(user)
    print(users)
    saveExcel(Movie.title,users)
    pass




# 生成excel 文件
def saveExcel(title,users):
    # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    # style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet(title)
    for i in range(0,len(users)):
        user=users[i]

        ws.write(i, 0, user.username)
        ws.write(i, 1, user.content)
        ws.write(i, 2, user.time)
    wb.save(title+".xls")


if __name__=="__main__":
    getMovies()

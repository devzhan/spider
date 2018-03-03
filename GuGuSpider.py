# coding: utf8
import re
import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import random

class GuGu(object):
    def __init__(self, headers):
        self.headers = headers;
        self.session = requests.session()
        pass

    def search(self):
        # 获取ids
        try:

            for pageIndex in range(0,50):
                pagePost={
                        'Pg_input':pageIndex,

                    }
                searchUrl = "http://www.gu-gu.com/search.aspx"
                resp = self.session.post(searchUrl, headers=self.headers,data=pagePost)
                pageSoup=BeautifulSoup(resp.text,"html.parser")
                tds=pageSoup.find_all('input')
                resultId=[]
                for td in tds:
                    if td['name']=="CK":
                        resultId.append(td['value'])
                ids = list(set(resultId))
                ids.sort(key=resultId.index)
                print(ids)
                # 根据id请求名片
                descUrl='http://www.gu-gu.com/chkqx.aspx'
                for index in range(0,len(ids)):
                    postData={
                        'Action':'post',
                        'mpid':ids[index],
                        'ran':random.random()

                    }
                    desc = self.session.post(descUrl, headers=self.headers,data=postData)
                    descOK=desc.text.replace('OK:',"")
                    print(descOK)
                    flashUrl='http://www.gu-gu.com/ShowImg.aspx?filename='+descOK+'&uid=25219'
                    flash = self.session.get(flashUrl)
                    picPattern = re.compile('\/Upload(.*?)";',re.S);
                    picUrl=re.findall(picPattern,flash.text)
                    print("正在下载第"+str(pageIndex)+"页的"+"第"+str(index)+"张名片")

                    if picUrl is not None:
                        print('http://www.gu-gu.com/Upload/'+picUrl[0])
                        urlretrieve('http://www.gu-gu.com/Upload/'+picUrl[0],str(pageIndex)+"_"+str(index)+".jpg")
                        # time.sleep(1)
        except Exception as e:
            print ('错误 ：',e)
def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Cookie':'UM_distinctid=161e20a475145d-09c670c3496186-326d7a05-fa000-161e20a4752526; LiveWSLUT40915487=1519915780335460354971; NLUT40915487fistvisitetime=1519915780372; NLUT40915487visitecounts=1; NLUT40915487IP=%7C58.60.153.60%7C; ASP.NET_SessionId=ngd4sb5qmjvuivbgjlwlr5av; NLUT40915487lastvisitetime=1519916079763; NLUT40915487visitepages=3; CNZZDATA2187431=cnzz_eid%3D1000595861-1519915779-%26ntime%3D1520045819',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',}
    gugu = GuGu(headers=headers)
    gugu.search()

    pass


if __name__ == '__main__':
    main()
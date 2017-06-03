# -*- coding: UTF-8 -*-
#正则表达式抓取猫眼电影 多进程 文件读写 request 正则
import json
import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool


def getOnePageContent(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parseOnePage(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S);
    items = re.findall(pattern, html)
    for item in items:
        yield {
            "index":item[0],
            "image":item[1],
            "title":item[2],
            "star" :item[3].strip()[3:],
            "time" :item[4].strip()[5:],
            "socre":item[5]+item[6]
        }

def write_to_file(content):
    with open("result.txt","a",encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = getOnePageContent(url)
    for item in parseOnePage(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # for i in range(0,10):
    #     # main(i*10)
    pool=Pool()#多进程
    pool.map(main,[i*10 for i in range(10)])

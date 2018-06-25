# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS



base_url='http://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E7%94%B2/p1?aid=22887982&cpt=22887982'
headers = {
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E7%94%B2/p1?aid=22887982&cpt=22887982'
}
shop_sites=[]
def getPages():
    pageContent = requests.get(base_url,headers = headers)
    pageContent.encoding = "utf-8"
    soup = BS(pageContent.text,"html.parser")
    items = soup.find_all('a',attrs={'data-click-name':'shop_info_groupdeal_click'})
    for item in items:
        shop_address = item.get('href')
        shop_sites.append(shop_address)

    print(shop_sites)
    pass
def getDetials(url):
    shopContent = requests.get(url,headers = headers)
    shopContent.encoding = "utf-8"
    soupShop = BS(shopContent.text,"html.parser")
    print (soupShop)
    shop = soupShop.find(_class = 'main')
    print (shop)

    pass

def main():
    # getPages()
    getDetials('http://t.dianping.com/deal/11857842')
    pass





if __name__ == '__main__':
    main()


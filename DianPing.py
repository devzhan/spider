# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

# base_url='http://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E7%94%B2/p1?aid=22887982&cpt=22887982'
base_url = 'http://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E7%94%B2/p'

headers = {
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://www.dianping.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

# 获取分野
def getPages(index):
    shop_sites = []
    url = base_url + str(index) + '?aid=22887982&cpt=22887982'
    print(url)
    pageContent = requests.get(url, headers=headers)
    # pageContent.encoding = "utf-8"
    print(pageContent)
    soup = BS(pageContent.text, "html.parser")
    # print(soup)
    items = soup.find_all('a', attrs={'data-hippo-type': 'shop'})
    print(items)
    for item in items:
        shop_address = item.get('href')
        shop_sites.append(shop_address)
    print(shop_sites)
    return shop_sites


def getDetials(url):
    shop = []
    shopContent = requests.get(url, headers=headers)
    shopContent.encoding = "utf-8"
    soupShop = BS(shopContent.text, "html.parser")
    shopDiv = soupShop.find('div', id='basic-info')
    if shopDiv is not None:
        shopNameTemp = shopDiv.find('h1').text.strip()
        shopName = ''
        if '添加分店' in shopNameTemp:
            shopName = shopNameTemp.replace('添加分店', '')
        else:
            shopName = shopNameTemp
        address = shopDiv.find('span', attrs={'itemprop': 'street-address'}).text.strip()
        number = shopDiv.find('span', attrs={'itemprop': 'tel'}).text.strip()
        shop.append(shopName)
        shop.append(number)
        shop.append(address)
    return shop

# 保存文件
def saveToexcel(datas):
    # datas=[['MiuMiu日式美甲美睫工作室\n        ', '0755-22218430', '金田路金中环商业大厦主楼A1130(会展中心地铁站E出口)'],
    #  ['Magic nail日式美甲店\n        ', '13651446298', '金田路金中环商务大厦主楼A座1306(会展中心E出口乘坐住楼底区电梯)'],
    #  ['初心はつ こころ日式美甲美睫沙龙\n        ', '0755-23915585', '金田路3037号金中环国际商务大厦A810(会展中心  皇庭广场  连城新天地)'],
    #  ['Sin Nail芯日式美甲美睫店(壹方城店)\n        ', '15323773995', '兴华一路壹方城L1-J023B(壹方城购物中心)'],
    #  ['十指紧寇美甲工作室(保利文化广场店)\n        其它2家分店', '0755-86559320', '文兴五路保利文化广场B区1楼34号铺神童乐园收银台(后海站E1出口保利必胜客肯德基旁边通道)'],
    #  ['美捺子日式美甲·美睫·美颜\n        ', '0755-26676507', '蛇口海上世界望海路双玺花园商铺102'], ['森日式美甲沙龙MORI NAIL\n        ', '18588206263',
    #                                                                       '金田路3037号金中环商务大厦B1129室（A座电梯上11楼与B座连接空中走廊处）(金中环商务大厦A座低区电梯上11楼后通往B座的空中走廊处)'],
    #  ['Forall艾芙罗美睫\n        ', '0755-83179302', '福华五路卓越世纪中心3号楼A座1307室(近会展中心)'],
    #  ['IMP 印奈儿·美甲美睫美肤(高新园旗舰店)\n        ', '0755-86533967', '高新园地铁A出口大冲城市花园1a栋7c(高新园地铁A出口 万象天地)'],
    #  ['S&L; fashion beauty 美甲美睫网红店(华强北店)\n        其它1家分店', '13714064726', '华强北深南中路3018号世纪汇都会轩2716室(华强路地铁站B出口，靠近世纪汇)'],
    #  ['Sissi NaiL 自然卷日式美甲美睫\n        ', '18664919690', '中航路九方世纪汇都会轩3107室(九方Gap对面)'],
    #  ['Dream Beauty日式美甲美睫\n        ', '18652679237', '公园道大厦A座501(太平洋咖啡楼上)'],
    #  ['唯兔 ·日式美甲美睫(梅林店)\n        其它1家分店', '13570869486', '广康路上梅林御锦公馆A栋28楼A09室(上梅林地铁站B出口斜对面，近卓越城)'],
    #  ['Clear love美甲美睫\n        ', '18702029695', '侨香路香蜜时代A栋20Q(近侨香地铁站A出口，深国投广场斜对面)'],
    #  ['鹿儿岛·Deer isle专业日式美甲美睫(大冲店)\n        ', '18681467707', '高新园B出口大冲新城花园2栋2D3001房(高新园地铁B出口)']]
    if datas is not None:
        data = pd.DataFrame(datas, columns=['店名', '电话', '地址'])
        data.to_excel('dianping2.xlsx', sheet_name='shop')
    pass


def main():
    shops = []
    for i in range(0, 1):
        shopAddress = getPages(i)
        print(shopAddress)

        print('正在获取第' + str(i) + '页的店铺数据')
        for site in shopAddress:
            shop = getDetials(site)
            if shop is not None and len(shop) != 0:
                shops.append(shop)
                print(shops)


    saveToexcel(shops)


if __name__ == '__main__':
    main()

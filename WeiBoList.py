#-*- coding: UTF-8 -*-
base_url = 'https://m.weibo.cn/api/container/getIndex?'

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq

def getPage(page,uid):
    headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/'+str(uid),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
    params = {
        'type': 'uid',
        'value': uid,
        'containerid': '107603'+str(uid),
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
    pass
def parse_page(json):
    if json:
        items = json.get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo

def main():
    page=20
    json=getPage(page,"5187664653")
    results = parse_page(json)
    for result in results:
        print(result)

    pass


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup

session = requests.Session()

login_url = 'https://www.douban.com/accounts/login'

comment_url = 'https://www.douban.com/'

params = {'source': 'index_nav', 'form_email': 'secret', 
    'form_password': 'secret', 'remember': 'on'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Origin': 'https://www.douban.com'}


# 登录豆瓣
index_page = session.post(login_url, headers=headers, data=params).text
soup = BeautifulSoup(index_page, 'html5lib')
token_tag = soup.find('input', attrs={'name': 'ck'})
# token_tags = soup.select('#db-isay input[name=ck]')
ck = token_tag['value']
params = {'ck': ck, 'comment': '超级大可乐post'}
resp = session.post(comment_url, headers=headers, data=params)
print('success')
import requests
from bs4 import BeautifulSoup
from PIL import Image
import time
import random


LOGIN_URL = 'https://www.douban.com/accounts/login'
COMMENT_URL = 'https://www.douban.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Origin': 'https://www.douban.com'}

session = requests.Session()
params = {'source': 'index_nav', 'form_email': 'secret', 
    'form_password': 'secret', 'remember': 'on'}

# 登录豆瓣
index_page = session.post(LOGIN_URL, headers=headers, data=params).text
soup = BeautifulSoup(index_page, 'html5lib')
# 获取验证码
captcha_image = soup.find('img', attrs={'id': 'captcha_image'})
if captcha_image is not None:
    captcha_id = soup.find('input', attrs={'name': 'captcha-id'})['value']
    img_content = session.get(captcha_image['src'], headers=headers).content
    with open('captcha.jpg', 'wb') as im:
        im.write(img_content)
    im = Image.open('captcha.jpg')
    im.show()
    solution = input('please input captcha:')
    im.close()
    params.update({'captcha-solution': solution, 'captcha-id': captcha_id})
    index_page = session.post(LOGIN_URL, headers=headers, data=params).text
# 登录后页面
soup = BeautifulSoup(index_page, 'html5lib')
ck = soup.find('input', attrs={'name': 'ck'})['value']
for i in range(5):
    params = {'ck': ck, 'comment': random.random()}
    session.post(COMMENT_URL, headers=headers, data=params)
    time.sleep(5)
print('success')
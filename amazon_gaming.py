#!/usr/bin/python3.10
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep

from bs4 import BeautifulSoup
import re

import requests
import json

from datetime import datetime


# selenium初期化
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# ターゲット♡
driver.get('https://gaming.amazon.com/home')
sleep(5)

# スクショ
#driver.set_window_size(1280,1024)
#driver.save_screenshot('screenshot.png')

# BSさん出番です
soup = BeautifulSoup(driver.page_source, 'lxml')
# ダータゲームリスト取得
ul_tag = soup.find('ul', attrs={'class':re.compile('grid-carousel__content')})

for li_tag in ul_tag.find_all('li'):
    # ガッチャ！
    url = 'https://gaming.amazon.com' + li_tag.find('a').get('href').split('?')[0]

    # ダータゲーム詳細画面から配布終了日(deadline)を取ってくる、ゲームリストに含めておけよメンドくせーな！
    driver.get(url)
    sleep(3)

    # スクショ
#    driver.set_window_size(1280,1024)
#    driver.save_screenshot('screenshot.png')

    # 日付だけ取ってくりゃいーよ
    detail_soup = BeautifulSoup(driver.page_source, 'lxml')
    _date = detail_soup.find('div', {'class': 'availability-date'}).find('span', {'class': 'tw-amazon-ember tw-amazon-ember-bold tw-bold tw-font-size-6'}).get_text()
    date = datetime.strptime(_date, '%b %d, %Y').date()

#    print(date)
#    print(url)

# お掃除
driver.close()
driver.quit()

# 速報くんに連絡だ！
"""
for f in free_game:
    #print(f)
#    print('https://www.epicgames.com' + f.get('href') + f.find('time', attrs={'data-component':'Time'}).get('datetime'))
#    print('https://www.epicgames.com' + f.get('href'))
#    print(f.find('time', attrs={'data-component':'Time'}).get('datetime'))
#    print(f.find('div', attrs={'data-testid':'direction-auto'}).get_text())
    data = json.dumps({
        'unique_check' : 'https://www.epicgames.com' + f.get('href') + f.find('time', attrs={'data-component':'Time'}).get('datetime'),
        'url'          : 'https://www.epicgames.com' + f.get('href'),
        'date'         : f.find('time', attrs={'data-component':'Time'}).get('datetime'),
        'name'         : f.find('div', attrs={'data-testid':'direction-auto'}).get_text(),
        'platform'     : 'epic',
        'delivery'     : False,
    })
    result = requests.post("https://localhost:8000/games/", data)
    print(result)


# kill `ps ax | grep chrome | awk '{print $1}'`

"""

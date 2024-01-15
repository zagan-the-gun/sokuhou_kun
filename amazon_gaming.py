#!/usr/bin/python3.10
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from time import sleep

from bs4 import BeautifulSoup
import re

import requests
import json

from datetime import datetime


# selenium初期化
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')

#CHROME_BIN = "./chrome-linux64/chrome"
#options.binary_location = CHROME_BIN
#CHROME_DRIVER = "./chromedriver-linux64/chromedriver"
#service = Service(executable_path=CHROME_DRIVER)
#driver = webdriver.Chrome(service=service, options=options)

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

_game_list=[]
_game_dict={}
for li_tag in ul_tag.find_all('li'):
    # ガッチャ！
    url = 'https://gaming.amazon.com' + li_tag.find('a').get('href').split('?')[0]
    _game_dict['url'] = url

    # ダータゲーム詳細画面から配布終了日(deadline)を取ってくる、ゲームリストに含めておけよメンドくせーな！
    driver.get(url)
    sleep(3)

    # スクショ
#    driver.set_window_size(1280,1024)
#    driver.save_screenshot('screenshot.png')

    # 日付取る
    detail_soup = BeautifulSoup(driver.page_source, 'lxml')
    _date = detail_soup.find('div', {'class': 'availability-date'}).find('span', {'class': 'tw-amazon-ember tw-amazon-ember-bold tw-bold tw-font-size-6'}).get_text()
    date = datetime.strptime(_date, '%b %d, %Y').date()
    _game_dict['date'] = str(date)
    # ゲーム名
    _name = detail_soup.find('div', {'data-a-target': 'buy-box_title'}).find('h1').text
    _game_dict['name'] = _name

    _game_list.append(_game_dict.copy())

    print(url)
    print(date)
    print(_name)

# お掃除
driver.close()
driver.quit()

# 速報くんに連絡だ！
for g in _game_list:
    data = json.dumps({
        'url'      : g['url'],
        'deadline' : g['date'],
        'name'     : g['name'],
        'platform' : 'amazon',
        'is_sent'  : False
    })
    result = requests.post("http://192.168.1.5/games/", data)
    print(result)

# バグでプロセスが死に切らない時の対応
#kill `ps ax | grep chromium | awk '{print $1}'`

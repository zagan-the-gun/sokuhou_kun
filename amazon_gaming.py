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

import os
import sys

# Settings
DOMAIN_FILE = './DOMAIN'
AMAZON_GAMING_URL = 'https://gaming.amazon.com/home'
JSON_HEADERS = {
    'url': 'url',
    'deadline': 'date',
    'name': 'name',
    'platform': 'amazon',
    'is_sent': False
}


# get token
def settings():
    if len(sys.argv) >= 2:
        return sys.argv[1]
    elif os.path.isfile(DOMAIN_FILE):
        with open(DOMAIN_FILE, 'r') as f:
            return f.read().splitlines()[0]
    else:
        print('DOMAIN not found')
        sys.exit(1)


def driver():
    # selenium初期化
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')

    # CHROME_BIN = "./chrome-linux64/chrome"
    # options.binary_location = CHROME_BIN
    # CHROME_DRIVER = "./chromedriver-linux64/chromedriver"
    # service = Service(executable_path=CHROME_DRIVER)
    # driver = webdriver.Chrome(service=service, options=options)

    driver = webdriver.Chrome(options=options)

    # ターゲット♡
    # driver.get('https://gaming.amazon.com/home')
    # sleep(5)
    # スクショ
    # driver.set_window_size(1280,1024)
    # driver.save_screenshot('screenshot.png')

    return driver


def scrap_game_details(driver, li_tag):
    # ガッチャ！
    url = 'https://gaming.amazon.com' + li_tag.find('a').get('href').split('?')[0]
    # ダータゲーム詳細画面から配布終了日(deadline)を取ってくる、ゲームリストに含めておけよメンドくせーな！
    driver.get(url)
    sleep(3)
    detail_soup = BeautifulSoup(driver.page_source, 'lxml')
    # 日付取る
    date_string = detail_soup.find('div', {'class': 'availability-date'}).find('span', {
        'class': 'tw-amazon-ember tw-amazon-ember-bold tw-bold tw-font-size-6'}).get_text()
    date = datetime.strptime(date_string, '%b %d, %Y').date()
    # ゲーム名
    name = detail_soup.find('div', {'data-a-target': 'buy-box_title'}).find('h1').text
    return {
        'url': url,
        'date': str(date),
        'name': name
    }


def scrap_webpage(driver):
    # BSさん出番です
    soup = BeautifulSoup(driver.page_source, 'lxml')
    games = []
    # ダータゲームリスト取得
    ul_tag = soup.find('ul', attrs={'class': re.compile('grid-carousel__content')})
    for li_tag in ul_tag.find_all('li'):
        game = scrap_game_details(driver, li_tag)
        games.append(game)
    return games


def post_to_reporter(games, domain):
    for game in games:
        data = {
            'url': game['url'],
            'deadline': game['date'],
            'name': game['name'],
            'platform': 'amazon',
            'is_sent': False
        }
        result = requests.post(f"http://{domain}/games/", json.dumps(data))
        print(result)


driver = driver()
game_list = scrap_webpage(driver)
# お掃除
driver.close()
driver.quit()
discord_token = settings()
post_to_reporter(game_list, discord_token)

# バグでプロセスが死に切らない時の対応
# kill `ps ax | grep chromium | awk '{print $1}'`

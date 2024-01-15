#!/usr/bin/python3.10
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep

from bs4 import BeautifulSoup
import re

import requests
import json


# selenium
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver', options=options)

driver.get('https://www.epicgames.com/store/ja/free-games')
epic_html = driver.page_source
#print(epic_html)
driver.close()
driver.quit()

# BSさん出番です
soup = BeautifulSoup(epic_html, 'lxml')
#free_game = soup.find_all('a', role='link')
#free_game = soup.find_all('a', attrs={'aria_label':re.compile(r'現在無料')})
#free_game = soup.find_all('a', attrs={'role':'link'})
#free_game = soup.find_all('a', attrs={'aria-label':'無料ゲーム, 2 の 1, 現在無料, Brothers - A Tale of Two Sons, 現在無料- 2月25日、01:00, 1480'})
free_game = soup.find_all('a', attrs={'aria-label':re.compile('現在無料')})

#print(free_game)
for f in free_game:
    #print(f)
    print('https://www.epicgames.com' + f.get('href') + f.find('time', attrs={'data-component':'Time'}).get('datetime'))
    print('https://www.epicgames.com' + f.get('href'))
    print(f.find('time', attrs={'data-component':'Time'}).get('datetime'))
    print(f.find('div', attrs={'data-testid':'direction-auto'}).get_text())
    data = json.dumps({
        'unique_check' : 'https://www.epicgames.com' + f.get('href') + f.find('time', attrs={'data-component':'Time'}).get('datetime'),
        'url'          : 'https://www.epicgames.com' + f.get('href'),
        'date'         : f.find('time', attrs={'data-component':'Time'}).get('datetime'),
        'name'         : f.find('div', attrs={'data-testid':'direction-auto'}).get_text(),
        'platform'     : 'epic',
        'delivery'     : False,
    })
    result = requests.post("https://dev-common.maskapp.club/games/", data)
    print(result)


# kill `ps ax | grep chrome | awk '{print $1}'`


#!/usr/bin/python3.10
# -*- coding: utf8 -*-

import requests
import json
import os
import sys


# TOKENチェック
if len(sys.argv) >= 2:
    DISCORD_TOKEN = sys.argv[1]
elif os.path.isfile('./DISCORD_TOKEN'):
    with open('./DISCORD_TOKEN', 'r') as f:
        DISCORD_TOKEN = f.read().splitlines()[0]
else:
    print('DISCORD_TOKEN not found')
    sys.exit(1)

# ドメインチェック
if len(sys.argv) >= 3:
    DISCORD_TOKEN = sys.argv[2]
elif os.path.isfile('./DOMAIN'):
    with open('./DOMAIN', 'r') as f:
        DISCORD_TOKEN = f.read().splitlines()[0]
else:
    print('DOMAIN not found')
    sys.exit(1)

target_url = "http://" + DOMAIN + "/games/?skip=0&limit=100&is_sent=false"
response = requests.get(target_url)
game = json.loads(response.text)
for g in game:
    print(g)

    # discordに投げる
    headers = {'content-type': 'application/json'}
    data = json.dumps({
        'username'   : '速報くん',
        #'content'    : '**' + g['name'] + '** : ' + g['url'],
        'content'    : '**' + g['url'] + '**',
        })
    result = requests.post('https://discord.com/api/webhooks/' + DISCORD_TOKEN, data, headers=headers)
    print(result)

    # 送信済みフラグを立てる
    headers = {'content-type': 'application/json'}
    data = json.dumps({
        'is_sent': True,
        })
    result = requests.put("http://" + DOMAIN + "/games/" + str(g['id']), data, headers=headers)
    print(result)


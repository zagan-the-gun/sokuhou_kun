#!/usr/bin/python3.7
# -*- coding: utf8 -*-

import requests
import json



target_url = "https://dev-common.maskapp.club/games/?skip=0&limit=100&delivery=false"
response = requests.get(target_url)
game = json.loads(response.text)
for g in game:
    print(g)

    # discordに投げる
    headers = {'content-type': 'application/json'}
    data = json.dumps({
        'username'   : '速報くん',
        'content'    : '**' + g['name'] + '** : ' + g['url'],
        })
    result = requests.post("https://discordapp.com/api/webhooks/566122139501985817/Gi0obOGCSx14aEiMGyCXo_7vFW30KI7BuLbEcr9UAx19Re0hqV_y5bF2x4-XzTE_YQCO", data, headers=headers)
    print(result)

    # 送信済みフラグ
    headers = {'content-type': 'application/json'}
    data = json.dumps({
        'delivery': True,
        })
    result = requests.put("https://dev-common.maskapp.club/games/" + str(g['id']), data, headers=headers)
    print(result)


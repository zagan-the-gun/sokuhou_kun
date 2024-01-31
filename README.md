# sokuhou_kun
無料ゲーム頂き男子のためのツール  
私たちは貰わされた！

# 登場人物
## amazon_gaming.pyなど
ヘッドレスな selenium で ゲーム配りおぢ から無料ゲームの情報をまるっと頂き男子！  
FastAPIに無料ゲーム情報をPOSTする  
crontab で実行する  

## FastAPI
おぢから頂いた新着無料ゲーム情報をストックする  
新規追加なら未配信フラグを付与して保存する  
別に外部に公開する必要はない、どころかこんなもんローカルファイルに直接書けばいいんじゃないの？  
まー、将来の拡張性に備えてね？  

## discord.py
FastAPI に未配信の新着無料ゲーム情報があればディスコに流す  
crontab で実行する  

# 使い方
DISCORDに通知を投げる場合はAPIトークンをDISCORD_TOKENというファイルに保存しよう
```
$ vi DISCORD_TOKEN
```

FastAPIのドメインやIPをDOMAINというファイルに保存しよう
192.168.1.5とかね！
```
$ vi DOMAIN
```

# ローカルにインストール

## FastAPIなどインストール
考えるな！感じろ！
```
$ python3.10 -m venv venv3.10
$ source venv3.10/bin/activate
(venv3.10)$ pip install -r requirements.txt
```

## FastAPI 起動
自分で適当にデーモン化しよう！
```
$ uvicorn sql_app.main:app --reload
```

## 必要パッケージのインストール
Seleniumなどを動かすのに必要なパッケージ群のインストール
```
$ sudo apt install build-base libffi-dev libpq-dev python3-dev libnss3-dev libatk1.0-0 libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libgbm1 libpango-1.0-0 libcairo2 libasound2
```

## chromedriver のインストール
このようなページから  
https://chromedriver.chromium.org/home  
このようなファイルをDLして使っても良い  
https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip  
https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip  
  
コンソールにhtmlが表示されれば成功!  
```
$ ./chrome --headless --disable-gpu --dump-dom http://the-menz.com/
```
  
面倒ならサクッとapt install
```
$ apt install chromium chromium-chromedriver
```
  
# Dockerでインストール
インストール自分でやるのめんどくさいなーって場合は手っ取り早く Docker で起動しちゃおう！  
因みにM1 Macとかだとダメなはず、インテル入ってる？
```
$ docker compose up
```

# Alembic インストールメモ
インストール
```
$ pip install alembic
```

初期化
```
$ alembic init alembic
```

マイグレーション
```
$ alembic revision -m "create games table"
```

alembic/versions/ 配下に新規作成されたファイルを編集
```
$ alembic upgrade head
```


自分で適当にサービス化しよう！
```
$ uvicorn sql_app.main:app --reload
```

# Tips
## バグでプロセスが死に切らない時の対応

```shell
kill `ps ax | grep chromium | awk '{print $1}'`
```

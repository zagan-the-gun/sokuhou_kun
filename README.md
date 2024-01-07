# sokuhou_kun
無料ゲーム頂き男子のためのツール  
私たちは貰わされた！

# インストール
考えるな！感じろ！
```
$ python3.11 -m venv venv3.11
$ source venv3.11/bin/activate
(venv3.11)$ pip install -r requirements.txt
```

# 登場人物
## amazon_gaming.pyなど
ヘッドレスな selenium で ゲーム配りおぢ から新着無料ゲームの情報をまるっと頂き男子！  
FastAPIに新着無料ゲーム情報をPOSTする  
新規追加なら未配信フラグが付与される  
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

## chromedriver のインストール
ChromeDriverのページ
https://chromedriver.chromium.org/home

CHromeとCHromeDriverのセット
https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip


$ wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip
$ unzip chrome-linux64.zip

$ ./chrome
./chrome: error while loading shared libraries: libnss3.so: cannot open shared object file: No such file or directory
$ sudo apt install libnss3-dev

$ ./chrome 
./chrome: error while loading shared libraries: libatk-1.0.so.0: cannot open shared object file: No such file or directory
$ sudo apt install libatk1.0-0

$ ./chrome
./chrome: error while loading shared libraries: libatk-bridge-2.0.so.0: cannot open shared object file: No such file or directory
$ sudo apt install libatk-bridge2.0-0

$ ./chrome
./chrome: error while loading shared libraries: libcups.so.2: cannot open shared object file: No such file or directory
$ sudo apt install libcups2-dev

$ ./chrome
./chrome: error while loading shared libraries: libxkbcommon.so.0: cannot open shared object file: No such file or directory
$ sudo apt install libxkbcommon-x11-0

$ sudo apt search libxdamage-dev
$ sudo apt install libgbm1
$ sudo apt install libpango-1.0-0
$ sudo apt install libcairo2
$ sudo apt install libasound2
$ ./chrome --headless --disable-gpu --dump-dom http://the-menz.com/
htmlが表示されれば成功!










自分で適当にサービス化しよう！
```
$ uvicorn sql_app.main:app --reload
```

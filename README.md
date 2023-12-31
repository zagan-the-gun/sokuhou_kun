# sokuhou_kun
EPICおぢから無料ゲーム頂きおぢのためのツール  
私たちは貰わされた！

# インストール
考えるな！感じろ！
```
$ python3.10 -m venv venv3.10
$ source venv3.10/bin/activate
(venv3.10)$ pip install -r requirements.txt
```

# 仕組み
## epic.py
ヘッドレスな selenium で EPICおぢ から新着無料ゲームの情報をまるっと頂きおぢ！
FastAPIに新着無料ゲーム情報をPOSTする
新規追加なら未配信フラグが付与される
crontab で実行する

## FastAPI
EPICおぢから頂いた新着無料ゲーム情報をストックする
新規追加なら未配信フラグを付与して保存する
別に外部に公開する必要はない、どころかこんなもんDBに直接書けばいいんじゃないの？
まー、将来の拡張性に備えてね？

## discord.py
FastAPI から頂いた未配信の新着無料ゲーム情報があればディスコに流す
crontab で実行する

# 使い方
自分で適当にサービス化しよう！
```
$ uvicorn sql_app.main:app --reload
```

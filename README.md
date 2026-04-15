# sokuhou_kun
無料ゲーム頂き男子のためのツール  
私たちは貰わされた！

## 仕組み
1. Amazon Gaming / Epic Games Store / GamerPower API から無料ゲーム情報を取得
2. SQLite に保存して重複チェック
3. 新着があれば Discord に通知

GitHub Actions で月水金 JST 12:00 に自動実行される。

## 構成
| ファイル | 役割 |
|----------|------|
| `main.py` | エントリポイント |
| `amazon_gaming.py` | Playwright で Amazon Gaming をスクレイプ |
| `epic_games.py` | Epic の公開 API から無料ゲームを取得 |
| `gamerpower.py` | GamerPower API から Steam / GOG / Ubisoft / itch.io 等の無料ゲームを取得 |
| `db.py` | SQLite 直接操作 |
| `notifier.py` | Discord Webhook 通知 |

## ローカルで動かす

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

`.env` を作成:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxx/yyyy
```

実行:
```bash
python main.py
```

## GitHub Actions
- 月水金 JST 12:00 に自動実行（手動実行も可）
- `DISCORD_WEBHOOK_URL` を Repository Secrets に登録すること
- 実行後、DB に変更があればリポジトリに自動コミットされる

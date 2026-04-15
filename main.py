"""速報くん - 無料ゲーム配布通知ツール"""

import os
import sys
from dotenv import load_dotenv

import db
from amazon_gaming import fetch_free_games as fetch_amazon
from epic_games import fetch_free_games as fetch_epic
from gamerpower import fetch_free_games as fetch_gamerpower
from notifier import send_to_discord


def main():
    load_dotenv()
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("エラー: DISCORD_WEBHOOK_URL が設定されていません (.env を確認してください)")
        sys.exit(1)

    db.init()

    # --- スクレイプ ---
    print("=== Amazon Gaming ===")
    try:
        amazon_games = fetch_amazon()
        print(f"  取得: {len(amazon_games)} 件")
        for g in amazon_games:
            is_new = db.upsert_game(**g)
            print(f"  {'[新着]' if is_new else '[既存]'} {g['name']}")
    except Exception as e:
        print(f"  Amazon Gaming の取得に失敗: {e}")

    print("=== Epic Games ===")
    try:
        epic_games = fetch_epic()
        print(f"  取得: {len(epic_games)} 件")
        for g in epic_games:
            is_new = db.upsert_game(**g)
            print(f"  {'[新着]' if is_new else '[既存]'} {g['name']}")
    except Exception as e:
        print(f"  Epic Games の取得に失敗: {e}")

    print("=== GamerPower ===")
    try:
        gp_games = fetch_gamerpower()
        print(f"  取得: {len(gp_games)} 件")
        for g in gp_games:
            is_new = db.upsert_game(**g)
            print(f"  {'[新着]' if is_new else '[既存]'} {g['name']}")
    except Exception as e:
        print(f"  GamerPower の取得に失敗: {e}")

    # --- Discord 通知 ---
    unsent = db.get_unsent_games()
    if not unsent:
        print("\n新着ゲームはありません")
        return

    print(f"\n=== Discord 通知 ({len(unsent)} 件) ===")
    sent_ids = send_to_discord(webhook_url, unsent)
    db.mark_as_sent(sent_ids)
    print(f"\n完了: {len(sent_ids)} 件を通知しました")


if __name__ == "__main__":
    main()

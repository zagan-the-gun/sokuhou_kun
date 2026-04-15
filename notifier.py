"""Discord Webhook 通知"""

import requests


def send_to_discord(webhook_url: str, games: list[dict]):
    """未通知ゲームのリストを Discord に送信する。送信成功した game の id リストを返す。"""
    sent_ids = []

    for game in games:
        platform = game["platform"].upper()
        name = game["name"]
        url = game["url"]
        deadline = game.get("deadline") or "不明"

        content = f"🎮 **【{platform}】{name}**\n{url}\n期限: {deadline}"

        payload = {"username": "速報くん", "content": content}
        resp = requests.post(webhook_url, json=payload, timeout=15)

        if resp.ok:
            sent_ids.append(game["id"])
            print(f"  [OK] {name}")
        else:
            print(f"  [NG] {name} - {resp.status_code}: {resp.text}")

    return sent_ids

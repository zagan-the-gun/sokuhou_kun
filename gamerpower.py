"""GamerPower API 経由で無料ゲーム情報を取得"""

from __future__ import annotations

import requests

_API_URL = "https://www.gamerpower.com/api/filter"

PLATFORMS = ["steam", "gog", "ubisoft", "itchio"]


def fetch_free_games(platforms: list[str] | None = None) -> list[dict]:
    target = platforms or PLATFORMS
    resp = requests.get(
        _API_URL,
        params={
            "platform": ".".join(target),
            "type": "game",
        },
        timeout=15,
    )

    if resp.status_code == 201:
        return []
    resp.raise_for_status()

    data = resp.json()
    if not isinstance(data, list):
        return []

    games = []
    for item in data:
        if item.get("status") != "Active":
            continue

        url = item.get("open_giveaway_url", "")
        name = item.get("title", "Unknown")
        end_date = item.get("end_date")
        deadline = end_date if end_date and end_date != "N/A" else None

        raw_platforms = item.get("platforms", "")
        platform = _normalize_platform(raw_platforms)

        games.append({
            "url": url,
            "name": name,
            "platform": platform,
            "deadline": deadline,
        })

    return games


def _normalize_platform(raw: str) -> str:
    """GamerPower の platforms 文字列から代表プラットフォーム名を返す。"""
    lower = raw.lower()
    for keyword, label in [
        ("steam", "steam"),
        ("gog", "gog"),
        ("ubisoft", "ubisoft"),
        ("itch.io", "itchio"),
        ("battlenet", "battlenet"),
        ("origin", "origin"),
        ("drm-free", "drm-free"),
    ]:
        if keyword in lower:
            return label
    return "pc"


if __name__ == "__main__":
    for g in fetch_free_games():
        print(g)

"""Epic Games Store 無料ゲーム取得 (公開 API)"""

import requests
from datetime import datetime, timezone


_API_URL = (
    "https://store-site-backend-static-ipv4.ak.epicgames.com"
    "/freeGamesPromotions?locale=ja&country=JP&allowCountries=JP"
)


def _is_currently_free(promotions: dict | None) -> tuple[bool, str | None]:
    """現在無料配布中かどうかと、終了日を返す。"""
    if not promotions:
        return False, None

    for promo_group in promotions.get("promotionalOffers", []):
        for offer in promo_group.get("promotionalOffers", []):
            if offer.get("discountSetting", {}).get("discountPercentage") == 0:
                end_date = offer.get("endDate")
                return True, end_date

    return False, None


def fetch_free_games() -> list[dict]:
    resp = requests.get(_API_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    games = []
    elements = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

    for elem in elements:
        is_free, end_date = _is_currently_free(elem.get("promotions"))
        if not is_free:
            continue

        slug = (
            elem.get("catalogNs", {}).get("mappings", [{}])[0].get("pageSlug")
            or elem.get("urlSlug", "")
        )
        url = f"https://store.epicgames.com/ja/p/{slug}" if slug else ""

        deadline = None
        if end_date:
            try:
                dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                deadline = dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
            except ValueError:
                deadline = end_date

        games.append({
            "url": url,
            "name": elem.get("title", "Unknown"),
            "platform": "epic",
            "deadline": deadline,
        })

    return games


if __name__ == "__main__":
    for g in fetch_free_games():
        print(g)

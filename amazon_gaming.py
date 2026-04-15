"""Amazon Gaming 無料ゲーム取得 (Playwright)"""

from playwright.sync_api import sync_playwright


def fetch_free_games() -> list[dict]:
    games = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://gaming.amazon.com/home", wait_until="networkidle", timeout=30_000)

        cards = page.query_selector_all('[data-a-target="offer-list-FGWP_FULL"] .item-card__action')

        for card in cards:
            link = card.query_selector("a")
            if not link:
                continue

            href = link.get_attribute("href")
            if not href:
                continue

            url = "https://gaming.amazon.com" + href.split("?")[0]

            title_el = card.query_selector("h3")
            name = title_el.inner_text().strip() if title_el else "Unknown"

            date_el = card.query_selector("time")
            deadline = date_el.get_attribute("datetime") if date_el else None

            games.append({"url": url, "name": name, "platform": "amazon", "deadline": deadline})

        browser.close()

    return games


if __name__ == "__main__":
    for g in fetch_free_games():
        print(g)

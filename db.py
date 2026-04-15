import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sokuhou.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                url      TEXT    NOT NULL,
                name     TEXT    NOT NULL,
                platform TEXT    NOT NULL,
                deadline TEXT,
                is_sent  INTEGER NOT NULL DEFAULT 0,
                created_at TEXT  NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS uq_games_url_platform
            ON games (url, platform)
        """)


def upsert_game(url: str, name: str, platform: str, deadline: str | None = None) -> bool:
    """ゲームを登録する。新規なら True、既存なら False を返す。"""
    with _connect() as conn:
        existing = conn.execute(
            "SELECT 1 FROM games WHERE url = ? AND platform = ?",
            (url, platform),
        ).fetchone()

        conn.execute(
            """
            INSERT INTO games (url, name, platform, deadline)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (url, platform) DO UPDATE SET
                name     = excluded.name,
                deadline = excluded.deadline
            """,
            (url, name, platform, deadline),
        )
        return existing is None


def get_unsent_games() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, url, name, platform, deadline FROM games WHERE is_sent = 0"
        ).fetchall()
        return [dict(r) for r in rows]


def mark_as_sent(game_ids: list[int]):
    if not game_ids:
        return
    with _connect() as conn:
        placeholders = ",".join("?" * len(game_ids))
        conn.execute(
            f"UPDATE games SET is_sent = 1 WHERE id IN ({placeholders})",
            game_ids,
        )

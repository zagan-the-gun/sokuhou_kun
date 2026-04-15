import db


def test_upsert_returns_true_for_new_game(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init()

    assert db.upsert_game(url="https://example.com/a", name="Game A", platform="epic") is True


def test_upsert_returns_false_for_existing_game(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init()

    db.upsert_game(url="https://example.com/a", name="Game A", platform="epic")
    assert db.upsert_game(url="https://example.com/a", name="Game A", platform="epic") is False


def test_upsert_same_url_different_platform_is_new(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init()

    db.upsert_game(url="https://example.com/a", name="Game A", platform="epic")
    assert db.upsert_game(url="https://example.com/a", name="Game A", platform="steam") is True


def test_upsert_updates_name_and_deadline(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init()

    db.upsert_game(url="https://example.com/a", name="Old Name", platform="epic", deadline="2026-01-01")
    db.upsert_game(url="https://example.com/a", name="New Name", platform="epic", deadline="2026-12-31")

    games = db.get_unsent_games()
    assert len(games) == 1
    assert games[0]["name"] == "New Name"
    assert games[0]["deadline"] == "2026-12-31"


def test_get_unsent_returns_only_unsent(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init()

    db.upsert_game(url="https://example.com/a", name="Game A", platform="epic")
    db.upsert_game(url="https://example.com/b", name="Game B", platform="steam")

    unsent = db.get_unsent_games()
    assert len(unsent) == 2

    db.mark_as_sent([unsent[0]["id"]])

    unsent_after = db.get_unsent_games()
    assert len(unsent_after) == 1
    assert unsent_after[0]["name"] == unsent[1]["name"]


def test_mark_as_sent_with_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init()

    db.upsert_game(url="https://example.com/a", name="Game A", platform="epic")
    db.mark_as_sent([])

    assert len(db.get_unsent_games()) == 1

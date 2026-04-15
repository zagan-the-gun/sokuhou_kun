from gamerpower import _normalize_platform


def test_steam():
    assert _normalize_platform("PC, Steam") == "steam"


def test_gog():
    assert _normalize_platform("PC, GOG") == "gog"


def test_ubisoft():
    assert _normalize_platform("PC, Ubisoft Connect") == "ubisoft"


def test_itchio():
    assert _normalize_platform("PC, Itch.io") == "itchio"


def test_battlenet():
    assert _normalize_platform("PC, Battlenet") == "battlenet"


def test_origin():
    assert _normalize_platform("PC, Origin") == "origin"


def test_drm_free():
    assert _normalize_platform("PC, DRM-Free") == "drm-free"


def test_unknown_falls_back_to_pc():
    assert _normalize_platform("PC") == "pc"
    assert _normalize_platform("SomeNewPlatform") == "pc"


def test_case_insensitive():
    assert _normalize_platform("pc, steam") == "steam"
    assert _normalize_platform("PC, STEAM") == "steam"


def test_steam_wins_when_multiple():
    assert _normalize_platform("PC, Steam, GOG") == "steam"

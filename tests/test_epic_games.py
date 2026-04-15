from epic_games import _is_currently_free


def test_free_when_discount_is_zero():
    promotions = {
        "promotionalOffers": [
            {
                "promotionalOffers": [
                    {
                        "discountSetting": {"discountPercentage": 0},
                        "endDate": "2026-04-17T15:00:00.000Z",
                    }
                ]
            }
        ]
    }
    is_free, end_date = _is_currently_free(promotions)
    assert is_free is True
    assert end_date == "2026-04-17T15:00:00.000Z"


def test_not_free_when_discount_is_nonzero():
    promotions = {
        "promotionalOffers": [
            {
                "promotionalOffers": [
                    {
                        "discountSetting": {"discountPercentage": 50},
                        "endDate": "2026-04-17T15:00:00.000Z",
                    }
                ]
            }
        ]
    }
    is_free, end_date = _is_currently_free(promotions)
    assert is_free is False
    assert end_date is None


def test_not_free_when_promotions_is_none():
    assert _is_currently_free(None) == (False, None)


def test_not_free_when_promotions_is_empty():
    assert _is_currently_free({}) == (False, None)


def test_not_free_when_no_promotional_offers():
    promotions = {"promotionalOffers": []}
    assert _is_currently_free(promotions) == (False, None)


def test_free_without_end_date():
    promotions = {
        "promotionalOffers": [
            {
                "promotionalOffers": [
                    {"discountSetting": {"discountPercentage": 0}}
                ]
            }
        ]
    }
    is_free, end_date = _is_currently_free(promotions)
    assert is_free is True
    assert end_date is None

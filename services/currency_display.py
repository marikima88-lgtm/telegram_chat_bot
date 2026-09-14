from i18n import DEFAULT_LANGUAGE, t

CURRENCY_FLAGS = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "RUB": "🇷🇺",
    "KGS": "🇰🇬",
    "CNY": "🇨🇳",
    "GBP": "🇬🇧",
    "CHF": "🇨🇭",
    "UZS": "🇺🇿",
    "JPY": "🇯🇵",
    "TRY": "🇹🇷",
    "AED": "🇦🇪",
    "THB": "🇹🇭",
    "INR": "🇮🇳",
    "KRW": "🇰🇷",
    "VND": "🇻🇳",
    "IDR": "🇮🇩",
    "GEL": "🇬🇪",
    "CZK": "🇨🇿",
    "AZN": "🇦🇿",
    "AMD": "🇦🇲",
    "AUD": "🇦🇺",
    "CAD": "🇨🇦",
    "MXN": "🇲🇽",
    "OMR": "🇴🇲",
    "PLN": "🇵🇱",
    "QAR": "🇶🇦",
    "SAR": "🇸🇦",
    "SGD": "🇸🇬",
    "TJS": "🇹🇯",
    "UAH": "🇺🇦",
    "GOLD1": "🥇",
}

CURRENCY_DISPLAY_ORDER = [
    "USD", "EUR", "RUB", "KGS", "CNY", "GBP", "CHF", "UZS",
    "JPY", "TRY", "AED", "THB", "INR", "KRW", "VND", "IDR",
]

CURRENCY_NAME_KEYS = {
    "GOLD1": "gold_1g",
}


def get_currency_flag(code: str) -> str:
    return CURRENCY_FLAGS.get(code.upper(), "💱")


def get_currency_label(code: str, lang: str = DEFAULT_LANGUAGE) -> str:
    key = CURRENCY_NAME_KEYS.get(code.upper())
    return t(key, lang) if key else code.upper()


def sort_currency_codes(codes: list[str]) -> list[str]:
    codes = list(codes)
    is_gold = "GOLD1" in codes
    if is_gold:
        codes.remove("GOLD1")

    ordered = [code for code in CURRENCY_DISPLAY_ORDER if code in codes]
    remaining = sorted(code for code in codes if code not in CURRENCY_DISPLAY_ORDER)

    result = ordered + remaining
    if is_gold:
        result.append("GOLD1")
    return result

import re

PHONE_MASK_EXAMPLE = "+77777777777"
PHONE_PATTERN = re.compile(r"\+7\d{10}$")


def normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    digits = re.sub(r"[^\d+]", "", raw)
    if digits.startswith("+7") and len(digits) == 12:
        candidate = digits
    elif digits.startswith("7") and len(digits) == 11:
        candidate = "+" + digits
    elif digits.startswith("8") and len(digits) == 11:
        candidate = "+7" + digits[1:]
    else:
        return None
    return candidate if PHONE_PATTERN.fullmatch(candidate) else None

import re

def normalize_number(value: str):
    if not value:
        return None
    value = value.replace(" ", "").replace(",", ".")
    try:
        return float(value)
    except:
        return None

def extract_first(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return None
    return m.group(1) if m.group(1) else m.group(0)

def parse_ocr_text(text: str):
    clean = " ".join(text.split())

    # -------------------------
    # TICKER
    # -------------------------
    ticker = extract_first(r"\b[A-Z]{3,6}\b", clean)

    # -------------------------
    # INTERWAŁ
    # -------------------------
    interval = extract_first(r"\b(M1|M5|M15|M30|H1|H4|D1|W1)\b", clean)

    # -------------------------
    # CZAS
    # -------------------------
    time = extract_first(r"\b\d{2}:\d{2}\b", clean)

    # -------------------------
    # O / H / L / C
    # -------------------------
    O = normalize_number(extract_first(r"O[: ]?(\d[\d\s,\.]*)", clean))
    H = normalize_number(extract_first(r"H[: ]?(\d[\d\s,\.]*)", clean))
    L = normalize_number(extract_first(r"L[: ]?(\d[\d\s,\.]*)", clean))
    C = normalize_number(extract_first(r"C[: ]?(\d[\d\s,\.]*)", clean))

    # -------------------------
    # MA20
    # -------------------------
    MA20 = normalize_number(extract_first(r"MA ?20(?: close)?[: ]?(\d[\d\s,\.]*)", clean))

    # -------------------------
    # DEMA9
    # -------------------------
    DEMA9 = normalize_number(extract_first(r"DEMA ?9[: ]?(\d[\d\s,\.]*)", clean))

    # -------------------------
    # RSI
    # -------------------------
    RSI = normalize_number(extract_first(r"RSI ?14[: ]?(\d[\d\s,\.]*)", clean))

    # -------------------------
    # Wolumen
    # -------------------------
    VOL = normalize_number(extract_first(r"(?:Wolumen|Volume)[: ]?(\d[\d\s,\.]*)", clean))

    # -------------------------
    # SANITY CHECK O/H/L/C
    # -------------------------
    if O and H and O > H:
        O, H = H, O
    if L and H and L > H:
        L, H = H, L
    if L and O and L > O:
        L, O = O, L

    return {
        "ticker": ticker,
        "interval": interval,
        "time": time,
        "O": O,
        "H": H,
        "L": L,
        "C": C,
        "MA20": MA20,
        "DEMA9": DEMA9,
        "RSI": RSI,
        "VOL": VOL
    }

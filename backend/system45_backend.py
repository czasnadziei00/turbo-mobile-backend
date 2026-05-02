def system45_backend(d: dict, entry: float | None):
    """
    d = {
        'O','H','L','C','MA20','DEMA9','RSI','VOL','ticker','interval','time'
    }
    entry = float lub None
    """

    # -------------------------
    # Pobranie danych
    # -------------------------
    O = d.get("O")
    H = d.get("H")
    L = d.get("L")
    C = d.get("C")
    MA20 = d.get("MA20")
    D9 = d.get("DEMA9")

    # -------------------------
    # SYGNAŁ
    # -------------------------
    if not MA20 or not D9 or not C:
        signal = "CZEKAJ"
        className = "signal-czekaj"
    else:
        if C > MA20 and C > D9 and D9 > MA20:
            signal = "BUY"
            className = "signal-buy"

        elif C > MA20 and C > D9 and abs(D9 - MA20) < 0.05:
            signal = "PRAWIE BUY"
            className = "signal-prawiebuy"

        elif C < MA20 and C < D9:
            signal = "RESET"
            className = "signal-reset"

        else:
            signal = "CZEKAJ"
            className = "signal-czekaj"

    # -------------------------
    # WIDEŁKI
    # -------------------------
    if not O or not H or not L or not C:
        widelki = "—"
    else:
        mid = (H + L) / 2
        low = mid - (mid * 0.02)
        high = mid + (mid * 0.02)
        widelki = f"{low:.3f} – {high:.3f}"

    # -------------------------
    # TP
    # -------------------------
    if not C:
        tp1 = tp2 = tp3 = "—"
    else:
        tp1 = f"{C * 1.003:.3f}"
        tp2 = f"{C * 1.006:.3f}"
        tp3 = f"{C * 1.009:.3f}"

    # -------------------------
    # KOMENTARZ PRO
    # -------------------------
    komentarz = []
    komentarz.append(f"Ticker: {d.get('ticker') or '-'}")
    komentarz.append(f"Interwał: {d.get('interval') or '-'}")
    komentarz.append(f"Czas: {d.get('time') or '-'}")
    komentarz.append(f"O/H/L/C: {O}/{H}/{L}/{C}")
    komentarz.append(f"MA20: {MA20}, DEMA9: {D9}")
    if d.get("RSI") is not None:
        komentarz.append(f"RSI14: {d.get('RSI')}")
    if entry:
        komentarz.append(f"ENTRY: {entry}")
    komentarz.append(f"Sygnał: {signal}")
    komentarz.append(f"Widełki: {widelki}")
    komentarz.append(f"TP1/TP2/TP3: {tp1}/{tp2}/{tp3}")

    return {
        "signal": signal,
        "className": className,
        "widelki": widelki,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "komentarz": "\n".join(komentarz)
    }

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import tempfile
import uvicorn

from parser import parse_ocr_text
from system45_backend import system45_backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ładujemy EasyOCR tylko raz
ocr = easyocr.Reader(['en'], gpu=False)


# ---------------------------------------------------------
# 1) /analyze-image — analiza screena
# ---------------------------------------------------------
@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    entry: float | None = Form(default=None)
):
    # zapis tymczasowy
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # OCR
    result = ocr.readtext(tmp_path, detail=0)
    text = "\n".join(result)

    # PARSER
    parsed = parse_ocr_text(text)

    # SYSTEM45
    sys = system45_backend(parsed, entry)

    return {
        "raw_text": text,
        "parsed": parsed,
        "system45": sys
    }


# ---------------------------------------------------------
# 2) /analyze-data — analiza bez OCR
# ---------------------------------------------------------
@app.post("/analyze-data")
async def analyze_data(
    O: float = Form(...),
    H: float = Form(...),
    L: float = Form(...),
    C: float = Form(...),
    MA20: float = Form(...),
    DEMA9: float = Form(...),
    RSI: float | None = Form(default=None),
    VOL: float | None = Form(default=None),
    ticker: str | None = Form(default=None),
    interval: str | None = Form(default=None),
    time: str | None = Form(default=None),
    entry: float | None = Form(default=None)
):
    d = {
        "O": O,
        "H": H,
        "L": L,
        "C": C,
        "MA20": MA20,
        "DEMA9": DEMA9,
        "RSI": RSI,
        "VOL": VOL,
        "ticker": ticker,
        "interval": interval,
        "time": time
    }

    sys = system45_backend(d, entry)

    return {
        "parsed": d,
        "system45": sys
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

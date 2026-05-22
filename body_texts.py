from pathlib import Path

RAW_TEXTS_DIR = Path(__file__).parent / "raw_texts"

def get_text_by_name(name: str, language: str = "en") -> str:
    return (RAW_TEXTS_DIR / language / f"{name}.txt").read_text(encoding="utf-8")
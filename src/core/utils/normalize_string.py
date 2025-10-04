import unicodedata
import re


def normalize_string(text: str) -> str :
    text = unicodedata.normalize("NFKC", text)
    text = text.strip()
    text = re.sub(r"\s+" ," ", text)
    return text.lower()


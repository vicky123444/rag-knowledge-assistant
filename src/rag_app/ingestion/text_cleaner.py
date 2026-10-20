import re
from typing import Iterable


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return normalize_whitespace(text)


def iter_lines(text: str) -> Iterable[str]:
    for line in text.splitlines():
        line = line.strip()
        if line:
            yield line

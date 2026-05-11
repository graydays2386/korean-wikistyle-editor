# -*- coding: utf-8 -*-
# -----------------------------
# 1) 형태소 분석기 준비 (Mecab 우선, 없으면 Okt)
# -----------------------------
class PythonMecabTokenizer:
    """
    Adapter for python-mecab-ko.
    Provides a KoNLPy-like .pos(text) interface.
    """

    def __init__(self):
        from mecab import MeCab
        self._mecab = MeCab()

    def pos(self, text: str):
        return self._mecab.pos(text)


def get_tokenizer():
    """
    Returns a tokenizer-like object with a .pos(text) -> List[Tuple[str, str]] interface.
    Prefers python-mecab-ko, falls back to KoNLPy Okt.
    """
    try:
        return PythonMecabTokenizer()
    except Exception:
        try:
            from konlpy.tag import Okt  # type: ignore
            return Okt()
        except Exception:
            return None


TOKENIZER = get_tokenizer()
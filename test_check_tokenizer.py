# -*- coding: utf-8 -*-
"""
Tokenizer contract 점검 모듈.

이 모듈은 tokenizer provider가 다음과 같은 최소 인터페이스를
만족하는 객체를 반환하는지 확인한다.

    tokenizer.pos(text) -> list[tuple[str, str]]

각 반환 항목은 다음 형식이어야 한다.

    (surface_token: str, pos_tag: str)

이 테스트의 목적은 "프로젝트가 요구하는 tokenizer contract를 만족하는가"를 검증하는 것이다.
"""

import sys
from typing import Any


TEST_TEXT = "한국어 문장 분리 테스트입니다."


def _print_failure(message: str, error: Exception | None = None) -> None:
    """실패 메시지를 일관된 형식으로 출력한다."""
    print(f"[FAIL] {message}")
    if error is not None:
        print(f"       error_type={type(error).__name__}")
        print(f"       error_message={error}")


def _validate_pos_result(result: Any) -> bool:
    """
    tokenizer.pos(text)의 반환값이 기대 형식을 만족하는지 검증한다.

    기대 형식:

        [
            ("한국어", "NNG"),
            ("문장", "NNG"),
            ...
        ]

    여기서는 정확한 형태소 분석 결과 자체를 검증하지 않는다.
    형태소 분석기는 구현체에 따라 한국어 문장을 서로 다르게 분절할 수 있기 때문이다.

    이 함수는 오직 반환값의 구조만 확인한다.

        1. 반환값이 list인가
        2. 비어 있지 않은가
        3. 각 항목이 tuple인가
        4. 각 tuple은 길이 2인가
        5. token과 tag가 모두 비어 있지 않은 문자열인가
    """
    if not isinstance(result, list):
        _print_failure(f"pos() 반환값은 list여야 합니다. 실제 타입: {type(result).__name__}")
        return False

    if len(result) == 0:
        _print_failure("pos() 반환값은 비어 있으면 안 됩니다.")
        return False

    for index, item in enumerate(result):
        if not isinstance(item, tuple):
            _print_failure(
                f"pos() 결과의 #{index} 항목은 tuple[str, str]이어야 합니다. "
                f"실제 타입: {type(item).__name__}, 값: {item!r}"
            )
            return False

        if len(item) != 2:
            _print_failure(
                f"pos() 결과의 #{index} 항목은 길이 2의 tuple이어야 합니다. "
                f"실제 길이: {len(item)}, 값: {item!r}"
            )
            return False

        token, tag = item

        if not isinstance(token, str):
            _print_failure(
                f"#{index} 항목의 token은 str이어야 합니다. "
                f"실제 타입: {type(token).__name__}, 값: {token!r}"
            )
            return False

        if not isinstance(tag, str):
            _print_failure(
                f"#{index} 항목의 tag는 str이어야 합니다. "
                f"실제 타입: {type(tag).__name__}, 값: {tag!r}"
            )
            return False

        if token == "":
            _print_failure(f"#{index} 항목의 token은 빈 문자열이면 안 됩니다.")
            return False

        if tag == "":
            _print_failure(f"#{index} 항목의 tag는 빈 문자열이면 안 됩니다.")
            return False

    return True


def check_tokenizer_contract() -> bool:
    """
    프로젝트 tokenizer가 기대 contract를 만족하는지 순차적으로 점검한다.

    점검 항목:

        1. 프로젝트의 get_tokenizer()를 import할 수 있는가
        2. get_tokenizer()가 None이 아닌 tokenizer 객체를 반환하는가
        3. tokenizer에 호출 가능한 .pos(text) 메서드가 있는가
        4. .pos(text)의 반환값이 list[tuple[str, str]] 형식인가

    반환값:
        True  - 모든 점검 통과
        False - 하나 이상의 점검 실패
    """
    print("=== 1. 프로젝트 tokenizer provider import 확인 ===")

    try:
        from app.util.s_splitter.common.tokenizer import get_tokenizer
    except Exception as e:
        _print_failure("프로젝트 tokenizer 모듈에서 get_tokenizer를 import하지 못했습니다.", e)
        return False

    print("[OK] get_tokenizer import 성공")

    print("\n=== 2. tokenizer 객체 생성 확인 ===")

    try:
        tokenizer = get_tokenizer()
    except Exception as e:
        _print_failure("get_tokenizer() 실행 중 예외가 발생했습니다.", e)
        return False

    if tokenizer is None:
        _print_failure("get_tokenizer()가 None을 반환했습니다.")
        return False

    print(f"[OK] tokenizer 객체 생성 성공: {type(tokenizer).__module__}.{type(tokenizer).__name__}")

    print("\n=== 3. .pos(text) 메서드 확인 ===")

    pos_method = getattr(tokenizer, "pos", None)

    if pos_method is None:
        _print_failure("tokenizer 객체에 .pos 메서드가 없습니다.")
        return False

    if not callable(pos_method):
        _print_failure("tokenizer.pos 속성이 존재하지만 호출 가능한 메서드가 아닙니다.")
        return False

    print("[OK] tokenizer.pos 호출 가능")

    print("\n=== 4. .pos(text) 반환 형식 확인 ===")
    print(f"test_text: {TEST_TEXT}")

    try:
        result = tokenizer.pos(TEST_TEXT)
    except Exception as e:
        _print_failure("tokenizer.pos(TEST_TEXT) 실행 중 예외가 발생했습니다.", e)
        return False

    print(f"pos_result: {result}")

    if not _validate_pos_result(result):
        return False

    print("[OK] tokenizer.pos(text)가 기대 contract를 만족합니다.")
    return True


if __name__ == "__main__":
    success = check_tokenizer_contract()
    sys.exit(0 if success else 1)
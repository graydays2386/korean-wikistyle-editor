# -*- coding: utf-8 -*-
import json
import re
from typing import Any

def parse_llm_json(raw: str) -> Any:
    """
    LLM 출력에서 JSON을 최대한 안전하게 추출한다.

    처리 대상:
    1. 순수 JSON
    2. ```json ... ``` 코드펜스가 붙은 JSON
    3. 설명문 앞뒤에 JSON object가 섞인 출력

    주의:
    - 이 함수는 JSON object 또는 JSON array를 반환할 수 있다.
    - 현재 Agent A/B에서는 주로 dict 반환을 기대한다.
    """
    if raw is None:
        raise ValueError("LLM returned None")

    text = raw.strip()

    if not text:
        raise ValueError("LLM returned empty response")

    # ```json ... ``` 또는 ``` ... ``` 제거
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    # 1차: 그대로 파싱
    try:
        return json.loads(text)
    except json.JSONDecodeError as first_error:
        pass

    # 2차: JSON object 추출
    object_match = re.search(r"\{.*\}", text, re.DOTALL)
    if object_match:
        json_part = object_match.group(0)
        try:
            return json.loads(json_part)
        except json.JSONDecodeError:
            pass

    # 3차: JSON array 추출
    array_match = re.search(r"\[.*\]", text, re.DOTALL)
    if array_match:
        json_part = array_match.group(0)
        try:
            return json.loads(json_part)
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Failed to parse LLM JSON. Raw output starts with: {text[:500]!r}"
    ) from first_error
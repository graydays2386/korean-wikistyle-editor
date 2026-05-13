import json

from app.util.agents_new.json_utils import parse_llm_json


class TocArchitectAgent:
    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, sentences: dict) -> list[dict]:
        return [
            {
                "role": "user",
                "content": f"""
You are a Document Architect specializing in Information Structuring for a Wiki Knowledge Management System.

Task:
Analyze a JSON object containing indexed Korean sentences.
Group them by semantic similarity.
Create a hierarchical Table of Contents.

Rules:
1. The first section MUST be "## 1. 개요".
2. The overview section MUST have sentence_indices: [].
3. Use the exact original sentence keys as integer indices.
4. Do NOT write body text.
5. Do NOT summarize.
6. Do NOT add external knowledge.
7. Return ONLY a valid JSON object.
8. Section titles must describe only explicit facts in the input. Do not use a noun that implies an event not present in the input, such as production, creation, battle, treaty, or reform, unless the input explicitly says so.

Output Schema:
{{
  "toc_structure": [
    {{
      "section_title": "## 1. 개요",
      "sentence_indices": []
    }}
  ]
}}

Input:
{json.dumps(sentences, ensure_ascii=False)}
""".strip()
            }
        ]

    def run(self, sentences: dict) -> dict:
        raw = self.llm.generate_chat(
            self.build_prompt(sentences),
            max_new_tokens=2048,
            do_sample=False,
        )

        print("\n[DEBUG agent_b raw]")
        print(repr(raw))
        print("[/DEBUG agent_b raw]\n")

        return parse_llm_json(raw)
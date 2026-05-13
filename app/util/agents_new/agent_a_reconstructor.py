import json
from app.util.agents_new.json_utils import parse_llm_json

class SentenceReconstructorAgent:
    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, chunks: list[str]) -> list[dict]:
        print("Agent_A Reconstructor Activated")
        return [
            {
                "role": "user",
                "content": f"""
You are a specialized Text Reconstruction Engine for a Knowledge Management System (KMS).

Task:
Convert the given fragmented Korean text chunks into complete, independent Korean sentences.

Rules:
1. Restore omitted subjects only when clearly recoverable from the input.
2. Convert endings to Korean plain style ending with "-다".
3. Do NOT add external knowledge.
4. Preserve logical and causal relations.
5. Return ONLY one valid JSON object.
6. Do NOT use Markdown.
7. Do NOT wrap the answer in ```json or ```.
8. The first character of your answer must be {{.
9. The last character of your answer must be }}.
10. Use numeric string keys: "1", "2", "3", ...

Output schema:
{{
  "1": "첫 번째 완성 문장이다.",
  "2": "두 번째 완성 문장이다."
}}

User Input:
{json.dumps(chunks, ensure_ascii=False)}
""".strip()
            }
        ]

    def run(self, candidates) -> dict:
        chunks = [c.text for c in candidates]
        print("chunks for Agent A", chunks)

        messages = self.build_prompt(chunks)

        raw = self.llm.generate_chat(
            messages,
            max_new_tokens=2048,
            do_sample=False,
        )

        print("\n[DEBUG agent_a raw]")
        print(repr(raw))
        print("[/DEBUG agent_a raw]\n")

        return parse_llm_json(raw)
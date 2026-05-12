import json


class SentenceReconstructorAgent:
    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, chunks: list[str]) -> list[dict]:
        return [
            {
                "role": "user",
                "content": f"""
You are a specialized Text Reconstruction Engine for a Knowledge Management System (KMS).
Your goal is to convert a list of fragmented text chunks into a list of complete, independent Korean sentences.

Guidelines:
1. Restore omitted subjects from context.
2. Convert endings to Korean plain style ending with "-다".
3. Do NOT add external knowledge.
4. Preserve logical and causal relations.
5. Return ONLY a valid JSON object with numeric string keys.

User Input:
{json.dumps(chunks, ensure_ascii=False)}
""".strip()
            }
        ]

    def run(self, candidates) -> dict:
        chunks = [c.text for c in candidates]

        messages = self.build_prompt(chunks)

        raw = self.llm.generate_chat(
            messages,
            max_new_tokens=2048,
            do_sample=False,
        )

        return json.loads(raw)
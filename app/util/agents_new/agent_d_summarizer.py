class SummaryAgent:
    def __init__(self, llm):
        self.llm = llm

    def build_one_sentence_prompt(self, body: str) -> list[dict]:
        return [
            {
                "role": "user",
                "content": f"""
You are a strict summarizer.
Summarize the text into EXACTLY ONE Korean sentence.

Rules:
1. Use plain Korean "-다" style.
2. No evaluation.
3. Only facts.
4. Do NOT add external knowledge.
5. Do not force conjunctions. If a sentence-level conjunction is necessary, use only "그리고" or "또한". Do not use "그리고" immediately after "-고". Do not use awkward forms such as "-고 그리고".

User Input:
{body}
""".strip()
            }
        ]

    def build_three_sentence_prompt(self, body: str) -> list[dict]:
        return [
            {
                "role": "user",
                "content": f"""
You are a strict summarizer.
Summarize the text into EXACTLY THREE Korean sentences.

Rules:
1. Use only "그리고" or "또한" as conjunctions.
2. Do NOT use "따라서" or "결과적으로".
3. Each sentence must end with "-다".
4. No evaluation.
5. Only facts.
6. Do NOT add external knowledge.

User Input:
{body}
""".strip()
            }
        ]

    def run(self, body: str, sentence_count: int) -> str:
        if sentence_count < 6:
            messages = self.build_one_sentence_prompt(body)
            max_new_tokens = 512
        else:
            messages = self.build_three_sentence_prompt(body)
            max_new_tokens = 1024

        return self.llm.generate_chat(
            messages,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
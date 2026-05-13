import json


class BodyCompilerAgent:
    def __init__(self, llm):
        self.llm = llm

    def build_prompt(self, sentences: dict, toc: dict) -> list[dict]:
        return [
            {
                "role": "user",
                "content": f"""
You are a Technical Content Compiler.

Task:
Generate a structured Markdown document by assembling a Sentence Library and a Table of Contents.

Rules:
1. Convert every section_title into a Markdown header.
2. For "## 1. 개요", generate a 2-3 sentence meta-description.
3. For all other sections, retrieve the sentences by sentence_indices.
4. Concatenate sentences strictly in the order listed.
5. Do NOT rewrite, summarize, or alter the sentences.
6. Return ONLY the final Markdown content.
7. All generated Korean prose, including the overview section, must use plain Korean "-다" style.

sentences = {json.dumps(sentences, ensure_ascii=False)}
toc = {json.dumps(toc, ensure_ascii=False)}
""".strip()
            }
        ]

    def run(self, sentences: dict, toc: dict) -> str:
        return self.llm.generate_chat(
            self.build_prompt(sentences, toc),
            max_new_tokens=4096,
            do_sample=False,
        )
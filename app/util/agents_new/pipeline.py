from app.util.agents_new.llm_runtime import Gemma4Env
from app.util.agents_new.agent_a_reconstructor import SentenceReconstructorAgent
from app.util.agents_new.agent_b_toc_architect import TocArchitectAgent
from app.util.agents_new.agent_c_body_compiler import BodyCompilerAgent
from app.util.agents_new.agent_d_summarizer import SummaryAgent
from app.util.s_splitter.core import rule_based_candidate_split

def run_pipeline(raw_text: str, llm=None) -> dict:
    candidates = rule_based_candidate_split(raw_text)
    return run_agent_pipeline(candidates, llm=llm)


def run_agent_pipeline(candidates, llm=None) -> dict:
    if llm is None:
        llm = Gemma4Env()

    agent_a = SentenceReconstructorAgent(llm)
    agent_b = TocArchitectAgent(llm)
    agent_c = BodyCompilerAgent(llm)
    agent_d = SummaryAgent(llm)

    sentences = agent_a.run(candidates)
    print("agent_a:", sentences)
    toc = agent_b.run(sentences)
    print("agent_b:", toc)
    body = agent_c.run(sentences, toc)
    print("agent_c:", body)
    abstract = agent_d.run(body, sentence_count=len(sentences))
    print("agent_d:", abstract)

    return {
        "abstract": abstract,
        "toc": toc,
        "body": body,
    }
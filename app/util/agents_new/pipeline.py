from app.util.agents_new.llm_runtime import Gemma4Env
from app.util.agents_new.agent_a_reconstructor import SentenceReconstructorAgent
from app.util.agents_new.agent_b_toc_architect import TocArchitectAgent
from app.util.agents_new.agent_c_body_compiler import BodyCompilerAgent
from app.util.agents_new.agent_d_summarizer import SummaryAgent
from app.util.s_splitter.core import rule_based_candidate_split
from app.util.agents_new.latency import measure_latency, print_latency_report
import time

def run_pipeline(raw_text: str, llm=None) -> dict:
    metrics = {}
    total_start = time.perf_counter()

    with measure_latency(metrics, "splitter.rule_based_candidate_split"):
        candidates = rule_based_candidate_split(raw_text)

    result = run_agent_pipeline(candidates, llm=llm, metrics=metrics)

    metrics["pipeline.total"] = round(time.perf_counter() - total_start, 4)
    result["latency"] = metrics

    print_latency_report(metrics)

    return result


def run_agent_pipeline(candidates, llm=None, metrics: dict | None = None) -> dict:
    if metrics is None:
        metrics = {}
        total_start = time.perf_counter()
    else:
        total_start = None

    if llm is None:
        with measure_latency(metrics, "llm.init"):
            llm = Gemma4Env()
    else:
        metrics["llm.init"] = 0.0

    with measure_latency(metrics, "agent_init"):
        agent_a = SentenceReconstructorAgent(llm)
        agent_b = TocArchitectAgent(llm)
        agent_c = BodyCompilerAgent(llm)
        agent_d = SummaryAgent(llm)

    with measure_latency(metrics, "agent_a.reconstruct_sentences"):
        sentences = agent_a.run(candidates)
    print("agent_a:", sentences)

    with measure_latency(metrics, "agent_b.build_toc"):
        toc = agent_b.run(sentences)
    print("agent_b:", toc)

    with measure_latency(metrics, "agent_c.compile_body"):
        body = agent_c.run(sentences, toc)
    print("agent_c:", body)

    with measure_latency(metrics, "agent_d.summarize"):
        abstract = agent_d.run(body, sentence_count=len(sentences))
    print("agent_d:", abstract)

    if total_start is not None:
        metrics["pipeline.total"] = round(time.perf_counter() - total_start, 4)

    return {
        "abstract": abstract,
        "toc": toc,
        "body": body,
        "latency": metrics,
    }
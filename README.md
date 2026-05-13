# korean-wikistyle-editor

Korean wiki-style document editing pipeline using rule-based sentence candidate splitting and local LLM-based document reconstruction.

This project converts loosely written Korean notes into structured wiki-style documents.  
It first splits informal Korean text into offset-preserving candidate spans, then uses a multi-agent LLM pipeline to reconstruct sentences, build a table of contents, compile a Markdown body, and generate an abstract.

## Overview

Korean informal notes often contain incomplete sentence endings, omitted subjects, loose clause boundaries, and inconsistent punctuation.  
A punctuation-only sentence splitter is often insufficient for this type of text.

This project uses a hybrid pipeline:

1. Rule-based candidate span splitting
2. LLM-based sentence reconstruction
3. LLM-based table-of-contents generation
4. Markdown body compilation
5. LLM-based abstract generation
6. Latency measurement for each stage

The current implementation is designed for local experimentation with a quantized local LLM.

## Current Pipeline

```text
raw_text
  ↓
rule_based_candidate_split
  ↓
CandidateSpan[]
  ↓
Agent A: SentenceReconstructorAgent
  ↓
indexed sentence JSON
  ↓
Agent B: TocArchitectAgent
  ↓
toc_structure JSON
  ↓
Agent C: BodyCompilerAgent
  ↓
Markdown body
  ↓
Agent D: SummaryAgent
  ↓
abstract
```

The final result is returned as a dictionary:

```
{
  "abstract": "...",
  "toc": {
    "toc_structure": []
  },
  "body": "...",
  "latency": {}
}
```

## Main Components

### 1. Rule-based splitter

The splitter generates candidate spans from Korean informal text while preserving substring offsets.

Each candidate span contains:
```
   text
   reason
   start
   end
```

The splitter intentionally allows some over-segmentation because downstream LLM agents are expected to merge or reconstruct fragmented spans.

### 2. Agent A: Sentence Reconstruction

SentenceReconstructorAgent converts fragmented candidate spans into complete Korean sentences.

Expected output:
```
{
  "1": "첫 번째 완성 문장이다.",
  "2": "두 번째 완성 문장이다."
}
```

### 3. Agent B: TOC Architecture

TocArchitectAgent groups indexed sentences and generates a hierarchical table of contents.

Expected output:
```
{
  "toc_structure": [
    {
      "section_title": "## 1. 개요",
      "sentence_indices": []
    },
    {
      "section_title": "## 2. 본문",
      "sentence_indices": [1, 2, 3]
    }
  ]
}
```

### 4. Agent C: Body Compilation

BodyCompilerAgent assembles a Markdown document from the sentence library and TOC structure.

### 5. Agent D: Summary

SummaryAgent generates either a one-sentence or three-sentence Korean abstract depending on the number of reconstructed sentences.

### 6. Latency Measurement

The pipeline records latency for major stages:
```
   splitter.rule_based_candidate_split
   llm.init
   agent_init
   agent_a.reconstruct_sentences
   agent_b.build_toc
   agent_c.compile_body
   agent_d.summarize
   pipeline.total
```
## Model Runtime

The current LLM runtime uses: google/gemma-4-E4B-it

The model is loaded with 4-bit quantization through BitsAndBytesConfig.

Current runtime dependencies include:
```
   torch
   transformers
   accelerate
   bitsandbytes
   huggingface_hub
   safetensors
   sentencepiece
```
A CUDA-enabled PyTorch installation is recommended.

## Installation

Clone the repository:

```bash
git clone https://github.com/graydays2386/korean-wikistyle-editor.git
cd korean-wikistyle-editor
```

Create and activate a virtual environment:
```
   python -m venv .venv
   .\.venv\Scripts\activate
```

Install runtime dependencies:
```
   python -m pip install -U pip
  python -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121
```

Note: requirements.txt currently pins CUDA 12.1 PyTorch packages. If your local CUDA version is different, install the appropriate PyTorch build from the official PyTorch index before or after installing the remaining dependencies.

Install CUDA-enabled PyTorch according to your local CUDA environment.

Check the installation:
```
   python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"
   python -c "import transformers; print(transformers.__version__)"
```
This repository is currently intended to be run from the project root.  
You do not need to install `korean-wikistyle-editor` as a Python package.

## Hugging Face Access

The runtime downloads the model from Hugging Face Hub.

Unauthenticated requests may work but can be rate-limited.
For more stable downloads, log in with a Hugging Face token:
```
huggingface-cli login
```

## Usage
## Run with an input file
```
python main.py --input-file examples/alcmadea.txt
```

## Run with direct text
```
python main.py --text "알크마이온 가문은 원래부터 명망이 높았지만..."
```

## Run with standard input
```
Get-Content examples/alcmadea.txt -Raw | python main.py --stdin
```

## Print only the generated Markdown body
```
python main.py --input-file examples/alcmadea.txt --print-body
```

## Save full JSON result
```
   python main.py --input-file examples/alcmadea.txt --output-json outputs/alcmadea.result.json
```

## Save generated Markdown body
```
   python main.py --input-file examples/alcmadea.txt --output-md outputs/alcmadea.body.md
```

## Save both JSON and Markdown
```
python main.py `
  --input-file examples/alcmadea.txt `
  --output-json outputs/alcmadea.result.json `
  --output-md outputs/alcmadea.body.md
```

## CLI Options
| Option               | Description                                  |
| -------------------- | -------------------------------------------- |
| `--input-file`, `-i` | Read input text from a UTF-8 text file       |
| `--text`, `-t`       | Pass raw text directly from the command line |
| `--stdin`            | Read input text from standard input          |
| `--output-json`      | Save full pipeline result as JSON            |
| `--output-md`        | Save only the generated Markdown body        |
| `--encoding`         | Set input/output encoding. Default: `utf-8`  |
| `--print-body`       | Print only the generated Markdown body       |

Only one input source can be used at a time:
   --input-file
   --text
   --stdin

## Example Input
```
알크마이온 가문은 원래부터 명망이 높았지만 알크마이온과 그 아들 메가클레스 때부터 명망이 더 높아짐. 크로이소스가 델포이에 신탁을 보낼 때 알크마이온이 여러모로 도와줌. 이에 크로이소스는 알크마이온을 사르디스로 초청해서 그가 한 몸에 가져갈 수 있을 만큼의 금을 선물로 주겠다고 함.
```

## Example Output Structure
The pipeline returns:
```
{
  "abstract": "알크마이온 가문은 원래부터 명망이 높았고...",
  "toc": {
    "toc_structure": [
      {
        "section_title": "## 1. 개요",
        "sentence_indices": []
      }
    ]
  },
  "body": "# 목차\n\n...",
  "latency": {
    "llm.init": 19.3408,
    "agent_a.reconstruct_sentences": 84.2307,
    "pipeline.total": 339.4621
  }
}
```

## Project Structure
```
korean-wikistyle-editor/
├─ main.py
├─ examples/
│  └─ alcmadea.txt
├─ outputs/
├─ app/
│  ├─ cli/
│  │  ├─ args.py
│  │  └─ io.py
│  └─ util/
│     ├─ s_splitter/
│     │  └─ core.py
│     └─ agents_new/
│        ├─ pipeline.py
│        ├─ llm_runtime.py
│        ├─ agent_a_reconstructor.py
│        ├─ agent_b_toc_architect.py
│        ├─ agent_c_body_compiler.py
│        ├─ agent_d_summarizer.py
│        ├─ json_utils.py
│        └─ latency.py
```
## Design Notes

### Why use rule-based candidate splitting?

The splitter is not intended to produce final sentence boundaries.
Instead, it produces candidate spans that preserve offsets and expose possible semantic boundaries.

This allows the downstream LLM agent to reconstruct more complete and independent sentences.

### Why use JSON parsing utilities?

LLMs may return JSON in slightly different formats, including:
   pure JSON
   Markdown code fences
   JSON with surrounding explanation

The shared JSON parsing utility is used to make Agent A and Agent B more robust against these output variations.

### Why measure latency?

The current pipeline uses multiple LLM calls.
Latency measurement helps identify bottlenecks across:
   model initialization
   sentence reconstruction
   TOC generation
   body compilation
   summary generation

In local testing, body compilation may become a major bottleneck.
Some steps may later be replaced with deterministic Python logic to reduce latency.

## Known Limitations
   The current pipeline may over-segment short Korean endings such as 함., 줌., or 됨..
   Agent A may incorrectly restore omitted subjects in ambiguous Korean sentences.
   Agent B may generate section titles that are semantically plausible but not strictly grounded in the input.
   Agent C currently uses an LLM for Markdown assembly, although much of this step could be deterministic.
   Agent D may produce awkward conjunction patterns depending on the prompt.
   The current local runtime can be slow because each agent call invokes generation on a quantized local model.

## Development Roadmap

Possible next steps:

   1. Improve short-fragment merging in the rule-based splitter.
   2. Strengthen Agent A subject-restoration rules.
   3. Make Agent B section titles more conservative and input-grounded.
   4. Replace part or all of Agent C with deterministic Markdown assembly.
   5. Improve Agent D summary prompt to avoid awkward conjunctions.
   6. Refine dependency management by separating CUDA-specific PyTorch packages from general Python dependencies.
   7. Consider adding `pyproject.toml` if the project is later packaged as an installable Python application.
   8. Add small unit tests for:
      - splitter behavior
      - JSON parsing
      - CLI input loading
      - Markdown output saving

## License
TBD

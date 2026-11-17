# Contract Clause Search Workbench

A local TF-IDF search tool for finding contract passages. The search results are review aids and are not legal advice.

## CUAD retrieval benchmark

Evaluated against the official contract-disjoint test split from the [Contract Understanding Atticus Dataset (CUAD)](https://github.com/The-Atticus-Project/cuad). CUAD includes lawyer-annotated clause answer spans and is distributed under CC BY 4.0 by [The Atticus Project](https://www.atticusprojectai.org/cuad/). The benchmark preserves the 102-contract test split, creates overlapping 1,200-character passages, asks the CUAD clause-detail text as the query, and marks a passage relevant when it overlaps an annotated answer span. The input test JSON SHA-256 is \`007b6a40b0c65247f881627375c3d2e9b6aeeb5dfa89957494feed0765a1a073\`.

| Metric | TF-IDF baseline | Random candidate baseline |
|---|---:|---:|
| Recall@1 | 1.13% | 0.04% |
| Recall@5 | 4.18% | 0.22% |
| Recall@10 | 6.75% | 0.43% |
| MRR | 0.034 | — |

This sparse lexical baseline beats random candidate selection but has low absolute retrieval recall. It needs a stronger retrieval system and sentence-aware chunking before it is useful for legal review. CUAD relevance labels are not legal correctness judgments; this benchmark does not validate legal advice or contract interpretation. No contract text or answer spans are published. See [aggregate results](reports/benchmark.json).

## Run the search tool

\`\`\`bash
python -m pip install -r requirements.txt
python main.py --input data/clauses.csv --query "termination for convenience" --id clause_id --text text --top-k 10
\`\`\`

## Reproduce the benchmark

Download CUAD from its [official repository](https://github.com/The-Atticus-Project/cuad), extract the test split, then run:

\`\`\`bash
python benchmark.py --input path/to/test.json --out outputs
\`\`\`

Contract text and query outputs remain local. The repository does not redistribute source documents.

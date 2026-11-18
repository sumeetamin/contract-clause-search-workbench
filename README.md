# Contract Clause Search Workbench

A local TF-IDF search tool for finding contract passages. Search results are review aids, not legal advice.

## CUAD retrieval benchmark

Evaluated on the official contract-disjoint test split from the [Contract Understanding Atticus Dataset (CUAD)](https://github.com/The-Atticus-Project/cuad), which provides annotated clause answer spans. The 102-contract input has SHA-256 `007b6a40b0c65247f881627375c3d2e9b6aeeb5dfa89957494feed0765a1a073`.

Each CUAD question is associated with its source contract. Candidate passage ranking is restricted to that contract; identical clause-detail queries from different contracts are not treated as interchangeable. The runner creates overlapping 1,200-character passages with 900-character stride. A passage is relevant when it overlaps an annotated answer span.

| Metric | TF-IDF | Random candidate |
|---|---:|---:|
| Hit rate@1 | 37.30% | 6.96% |
| Hit rate@5 | 65.35% | 28.92% |
| Hit rate@10 | 77.49% | 49.24% |
| MRR | 0.502 | — |

Hit rate@k means at least one relevant passage is retrieved, not the fraction of all relevant passages found. This lexical baseline has moderate hit rates, but it does not assess legal correctness, contract interpretation or legal advice. Overlapping character chunks are not sentence-aware; no reranker or production latency evaluation is included. See [aggregate results](reports/benchmark.json).

## Run the search tool

```bash
python -m pip install -r requirements.txt
python main.py --input data/clauses.csv --query "termination for convenience" --id clause_id --text text --top-k 10
```

## Reproduce the benchmark

Download CUAD from its [official repository](https://github.com/The-Atticus-Project/cuad), extract the test split, then run:

```bash
python benchmark.py --input path/to/test.json --out outputs
```

Contract text and query outputs remain local; source documents are not redistributed here.

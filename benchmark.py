"""Evaluate TF-IDF clause retrieval on the contract-disjoint CUAD holdout."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def build_chunks(document, size=1200, stride=900):
    """Return overlapping character chunks and their source offsets."""
    chunks = []
    for start in range(0, len(document), stride):
        end = min(start + size, len(document))
        if end <= start:
            continue
        chunks.append((start, end, document[start:end]))
        if end == len(document):
            break
    return chunks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CUAD SQuAD-format test.json")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    source = Path(args.input)
    dataset = json.loads(source.read_text(encoding="utf-8"))
    chunks, queries = [], []
    contracts = 0
    for contract in dataset["data"]:
        for paragraph in contract["paragraphs"]:
            context = paragraph["context"]
            offsets = build_chunks(context)
            if not offsets:
                continue
            contracts += 1
            chunk_indices = []
            for start, end, text in offsets:
                chunk_indices.append(len(chunks))
                chunks.append(text)
            for qa in paragraph["qas"]:
                answers = qa.get("answers", [])
                if qa.get("is_impossible") or not answers:
                    continue
                gold = set()
                for answer in answers:
                    start = int(answer["answer_start"])
                    end = start + len(answer["text"])
                    for chunk_index, (chunk_start, chunk_end, _) in zip(chunk_indices, offsets):
                        if start < chunk_end and end > chunk_start:
                            gold.add(chunk_index)
                if not gold:
                    continue
                detail = qa["question"].split("Details:", 1)[-1].strip()
                queries.append({"query": detail, "gold": gold})

    if not chunks or not queries:
        raise SystemExit("No candidate passages or answerable CUAD questions found.")

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words="english")
    document_matrix = vectorizer.fit_transform(chunks)
    query_matrix = vectorizer.transform([item["query"] for item in queries])
    similarities = (query_matrix @ document_matrix.T).toarray()

    hits, reciprocal_ranks = {1: 0, 5: 0, 10: 0}, []
    chance_hits = {k: 0.0 for k in hits}
    for row, item in zip(similarities, queries):
        ranked = np.argsort(-row)
        first_rank = next((rank + 1 for rank, candidate in enumerate(ranked) if candidate in item["gold"]), None)
        reciprocal_ranks.append(0.0 if first_rank is None else 1.0 / first_rank)
        for k in hits:
            hits[k] += int(any(candidate in item["gold"] for candidate in ranked[:k]))
            chance_hits[k] += min(1.0, k * len(item["gold"]) / len(chunks))

    report = {
        "dataset": "Contract Understanding Atticus Dataset v1 (CUAD) official test split",
        "source_url": "https://github.com/The-Atticus-Project/cuad",
        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "holdout_contracts": int(contracts),
        "candidate_passages": int(len(chunks)),
        "answerable_queries": int(len(queries)),
        "chunk_chars": 1200,
        "chunk_stride_chars": 900,
        "retriever": "word unigram/bigram TF-IDF; English stop words; sublinear TF; min_df=2; cosine similarity",
        "query_source": "CUAD question detail text (template instructions removed)",
        "relevance_source": "CUAD annotated answer character spans; any overlapping passage is relevant",
        "recall_at_k": {str(k): hits[k] / len(queries) for k in hits},
        "mrr": float(np.mean(reciprocal_ranks)),
        "random_candidate_recall_at_k": {str(k): chance_hits[k] / len(queries) for k in chance_hits},
        "limitations": "Retrieval benchmark only; CUAD labels identify clause spans, not legal correctness. Contract-disjoint test split is preserved. Overlapping character chunks are not sentence-aware; no reranker or production latency evaluation is included. This is not legal advice.",
    }
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    (output / "benchmark.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

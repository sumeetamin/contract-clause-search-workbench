# Contract Clause Search Workbench

Retrieve relevant local contract clauses with TF-IDF and preserve clause identifiers for citation and human review.

> **Portfolio prototype.** Source code is provided; no benchmark results are claimed until you run it on the cited data and record the output.

## Use case

Retrieve relevant local contract clauses with TF-IDF and preserve clause identifiers for citation and human review. The CLI consumes local files, emits reproducible reports, and keeps data out of the repository.

## Data and provenance

[CUAD contract review dataset (optional; follow its source license and terms)](https://github.com/TheAtticusProject/cuad). A local CSV with clause_id and text columns. The script stores no documents; do not commit confidential contracts. Source files are not bundled. Respect source terms and cite the dataset when publishing results.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Download/prepare the source data locally, then run:
python main.py --input data/clauses.csv --query 'termination for convenience' --id clause_id --text text --top-k 10 --out outputs
```

## Outputs

Generated results are saved under `outputs/`; file names and metrics are printed or documented by the CLI. The repository excludes downloaded data and artifacts.

## Evaluation and operating notes

Lexical similarity is not legal advice, entailment, or clause interpretation. Verify every retrieved passage against the original document and have qualified counsel review.

For production use, add a frozen reference period, out-of-time evaluation, monitoring ownership, and a documented rollback or escalation path. This project is a local baseline, not a deployed service.

## License

No code license file is included yet. Third-party data remains subject to its source terms.

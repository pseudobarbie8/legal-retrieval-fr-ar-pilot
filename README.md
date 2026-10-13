# French/Arabic Legal Retrieval: Pilot

**Status: pilot, not yet a benchmark.** Small first version, data and results will change.

Goal: an open French/Arabic legal retrieval benchmark, with questions tied to exact articles of public legal texts and raw runs anyone can reproduce.

## Limits

- Questions were written by me from the articles. No legal professional has reviewed them or the labels.
- It tests whether retrieval finds the source article, not legal correctness.
- Too small to compare systems. Don't cite the results.

## Contents

- `data/passages.jsonl`: `id`, `lang`, `source`, `article`, `url`, `text`
- `data/questions.jsonl`: `id`, `lang`, `question`, `gold` (passage ids, empty if unanswerable)
- `data/SOURCES.md`: sources, access dates, reuse terms
- `eval/evaluate.py`: BM25 baseline, Recall@5 and MRR per language
- `results/`: raw runs

## Run

```sh
pip install -r requirements.txt
bash scripts/run_eval.sh
```

Saves `report.json` and `runs.jsonl` under `results/`. The baseline has no Arabic normalization, so expect weak Arabic scores.

## Next

- Arabic normalization
- Dense retriever vs BM25
- Score threshold to abstain on unanswerable questions

## Becomes a benchmark when

- [ ] Enough data, with sources and reuse terms documented
- [ ] A legal professional has reviewed a sample (reviewer and agreement rate listed here)
- [ ] Two or more baselines with raw runs committed
- [ ] Known biases written down

## Help wanted

Legal training in French or Arabic law? Open an issue to review a sample. You'll be credited by name.

## License

Code: MIT. Data: see `data/SOURCES.md`.

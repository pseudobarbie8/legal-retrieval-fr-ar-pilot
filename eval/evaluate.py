import json
import os
import sys
from rank_bm25 import BM25Okapi

K = 5

def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def tokenize(text):
    return text.lower().split()

def main(out_dir):
    passages = load("data/passages.jsonl")
    questions = load("data/questions.jsonl")
    runs, report = [], {}

    for lang in sorted({p["lang"] for p in passages}):
        corpus = [p for p in passages if p["lang"] == lang]
        bm25 = BM25Okapi([tokenize(p["text"]) for p in corpus])
        qs = [q for q in questions if q["lang"] == lang and q["gold"]]
        hits, rr = 0, 0.0

        for q in qs:
            scores = bm25.get_scores(tokenize(q["question"]))
            order = sorted(range(len(corpus)), key=lambda i: -scores[i])
            ranked = [corpus[i]["id"] for i in order]
            runs.append({"qid": q["id"], "lang": lang, "ranked": ranked[:20]})
            gold = set(q["gold"])
            hits += bool(gold & set(ranked[:K]))
            first = next((r for r, pid in enumerate(ranked, 1) if pid in gold), None)
            rr += 1 / first if first else 0.0

        n = len(qs)
        report[lang] = {
            "n_questions": n,
            f"recall@{K}": hits / n if n else None,
            "mrr": rr / n if n else None,
        }

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(out_dir, "runs.jsonl"), "w", encoding="utf-8") as f:
        for r in runs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/latest")

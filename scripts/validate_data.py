import json
import sys

def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

passages = load("data/passages.jsonl")
questions = load("data/questions.jsonl")
errors = []
if not passages or not questions:
    errors.append("data files are empty")
if not passages or not questions:
    errors.append("data files are empty")

pids = [p["id"] for p in passages]
if len(pids) != len(set(pids)):
    errors.append("duplicate passage ids")

qids = [q["id"] for q in questions]
if len(qids) != len(set(qids)):
    errors.append("duplicate question ids")

lang_of = {p["id"]: p["lang"] for p in passages}
for q in questions:
    for g in q["gold"]:
        if g not in lang_of:
            errors.append(f"{q['id']}: unknown gold id {g}")
        elif lang_of[g] != q["lang"]:
            errors.append(f"{q['id']}: gold {g} is in a different language")

for lang in sorted({p["lang"] for p in passages}):
    n_p = sum(p["lang"] == lang for p in passages)
    n_a = sum(q["lang"] == lang and bool(q["gold"]) for q in questions)
    n_u = sum(q["lang"] == lang and not q["gold"] for q in questions)
    print(f"{lang}: {n_p} passages, {n_a} answerable, {n_u} unanswerable")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("data OK")

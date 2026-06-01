"""刷题软件 - Flask Backend"""
import json
import random
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load question bank
JSON_PATH = os.path.join(os.path.dirname(__file__), "questions.json")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    BANK = json.load(f)

# Build global lookup by qid
LOOKUP = {}
for btype in ["single", "multi", "judge"]:
    for q in BANK[btype]:
        LOOKUP[q["qid"]] = q


def check_one(qid, user_answer):
    """Check a single answer. Returns dict with result info."""
    q = LOOKUP.get(qid)
    if not q:
        return {"error": "not_found"}

    correct = q["answer"].strip().upper()
    ua = user_answer.strip().upper()

    if q["type"] == "multi":
        is_correct = sorted(ua) == sorted(correct)
    elif q["type"] == "judge":
        if ua in ("对", "T", "TRUE", "A", "是"):
            ua = "对"
        elif ua in ("错", "F", "FALSE", "B", "否"):
            ua = "错"
        is_correct = (ua == correct)
    else:
        is_correct = (ua == correct)

    return {
        "qid": qid,
        "type": q["type"],
        "question": q["question"],
        "options": q.get("options", {}),
        "user_answer": user_answer.strip().upper(),
        "correct_answer": q["answer"],
        "is_correct": is_correct,
    }


@app.route("/")
def index():
    data = {
        "counts": BANK["counts"],
        "single": BANK["single"],
        "multi": BANK["multi"],
        "judge": BANK["judge"],
    }
    return render_template("index.html", data=data)


@app.route("/api/submit", methods=["POST"])
def submit():
    """Submit answers and get results."""
    body = request.get_json()
    answers = body.get("answers", {})
    qid_list = body.get("qid_list", [])

    if not qid_list:
        qid_list = list(answers.keys())

    results = []
    correct_count = 0
    stats = {"single": [0, 0], "multi": [0, 0], "judge": [0, 0]}  # [correct, total]

    for qid in qid_list:
        ua = answers.get(qid, "")
        r = check_one(qid, ua)
        if "error" in r:
            continue
        results.append(r)
        if r["is_correct"]:
            correct_count += 1
            stats[r["type"]][0] += 1
        stats[r["type"]][1] += 1

    total = len(results)
    return jsonify({
        "total": total,
        "correct_count": correct_count,
        "score": round(correct_count / total * 100, 1) if total else 0,
        "single_correct": stats["single"][0],
        "single_total": stats["single"][1],
        "multi_correct": stats["multi"][0],
        "multi_total": stats["multi"][1],
        "judge_correct": stats["judge"][0],
        "judge_total": stats["judge"][1],
        "results": results,
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

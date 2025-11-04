import re
from typing import Dict, Any


def evaluate_answer(correct_answer_json: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
    user_answer_normalized = user_answer.lower().strip()

    # Intrebare cu raspuns multiplu
    if "answer" in correct_answer_json:
        correct_answer_text = correct_answer_json["answer"].lower().strip()
        is_correct = user_answer_normalized == correct_answer_text
        score = 100.0 if is_correct else 0.0
        details = {"match_type": "exact"}

        return {"is_correct": is_correct, "score": score, "details": details}

    # Intrebare cu text scris
    elif "keywords" in correct_answer_json:
        keywords = correct_answer_json.get("keywords", [])
        if not keywords:
            return {"is_correct": False, "score": 0.0, "details": {"error": "No keywords to evaluate against"}}

        matches = 0
        details = {"keywords_found": [], "keywords_missed": []}

        for kw in keywords:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', user_answer_normalized):
                matches += 1
                details["keywords_found"].append(kw)
            else:
                details["keywords_missed"].append(kw)

        score = (matches / len(keywords)) * 100.0 if keywords else 0.0
        is_correct = score >= 80.0

        return {"is_correct": is_correct, "score": score, "details": details}

    else:
        return {"is_correct": False, "score": 0.0, "details": {"error": "Unknown correct_answer format"}}


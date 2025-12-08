from typing import Dict, Any
import spacy

nlp = spacy.load("ro_core_news_md")

def evaluate_answer(correct_answer_json: Dict[str, Any], user_answer: str, question_type: str) -> Dict[str, Any]:
    user_answer_norm = user_answer.lower().replace(" ", "").strip()

    if question_type == "CSP_PROBLEM":
        correct_raw = correct_answer_json.get("answer", "").lower().replace(" ", "")

        if correct_raw and correct_raw in user_answer_norm:
            return {
                "is_correct": True,
                "score": 100.0,
                "details": {"match_type": "csp_contains", "expected": correct_raw}
            }
        else:
            return {
                "is_correct": False,
                "score": 0.0,
                "details": {"match_type": "csp_contains", "expected": correct_raw}
            }

    if "answer" in correct_answer_json and "reference_text" not in correct_answer_json:
        correct_answer_text = correct_answer_json["answer"].lower().strip()
        is_correct = user_answer_norm == correct_answer_text.replace(" ", "")
        return {
            "is_correct": is_correct,
            "score": 100.0 if is_correct else 0.0,
            "details": {"match_type": "exact_multiple_choice"}
        }

    if "reference_text" in correct_answer_json:
        reference_text = correct_answer_json["reference_text"]
        user_doc = nlp(user_answer)
        ref_doc = nlp(reference_text)

        semantic_score = 0.0
        if user_doc.has_vector and ref_doc.has_vector:
            semantic_score = user_doc.similarity(ref_doc)

        final_score = max(0, min(100, semantic_score * 120))
        return {
            "is_correct": final_score >= 70,
            "score": final_score,
            "details": {
                "match_type": "semantic_similarity",
                "semantic_similarity_score": round(semantic_score, 4)
            }
        }

    return {"is_correct": False, "score": 0.0, "details": {"error": "invalid_format"}}

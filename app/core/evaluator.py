from typing import Dict, Any
import spacy

nlp = spacy.load("ro_core_news_md")

def evaluate_answer(correct_answer_json: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
    
    user_answer_normalized = user_answer.lower().strip()

    if "answer" in correct_answer_json and "reference_text" not in correct_answer_json:
        correct_answer_text = correct_answer_json["answer"].lower().strip()
        is_correct = user_answer_normalized == correct_answer_text
        score = 100.0 if is_correct else 0.0
        details = {"match_type": "exact_multiple_choice"}

        return {"is_correct": is_correct, "score": score, "details": details}

    elif "reference_text" in correct_answer_json:
        
        reference_text = correct_answer_json["reference_text"]

        user_doc = nlp(user_answer)
        reference_doc = nlp(reference_text)
        semantic_score = 0.0
        
        if user_doc.has_vector and reference_doc.has_vector and user_doc.vector_norm and reference_doc.vector_norm:
            semantic_score = user_doc.similarity(reference_doc)
        
        if len(user_doc) < 5: 
            semantic_score *= 0.8
            
        final_score = semantic_score * 120.0
        if final_score > 100:
            final_score = 100
        if final_score < 0:
            final_score = 0
        is_correct = final_score >= 70

        details = {
            "match_type": "nlp_semantic_only",
            "semantic_similarity_score": round(semantic_score, 4)
        }

        return {"is_correct": is_correct, "score": final_score, "details": details}

    else:
        return {"is_correct": False, "score": 0.0, "details": {"error": "Unknown correct_answer format (missing 'answer' or 'reference_text')"}}
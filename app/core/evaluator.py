from typing import Dict, Any,Tuple,Optional
import spacy
import re 
import unicodedata

#model folosit pentru similaritate semantica
nlp = spacy.load("ro_core_news_md")

def normalize_text(text: str) -> str:
    """elimina diacritice, normalizeaza textul"""
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text.lower()


def evaluate_answer(correct_answer_json: Dict[str, Any], user_answer: str, question_type: str) -> Dict[str, Any]:
    """
    Evalueaza rapsunsul in functie de tipul intrebarii
    """
    #normalizare
    user_answer_norm = user_answer.lower().replace(" ", "").strip()

    #intrebare de tip minmax
    if question_type == "MINIMAX_TREE":
        #valorile corecte
        correct_root = correct_answer_json.get("root_value")
        correct_leaves = correct_answer_json.get("visited_leaves")

        if correct_root is None or correct_leaves is None:
            if "reference_text" not in correct_answer_json:
                return {
                    "is_correct": False,
                    "score": 0.0,
                    "details": {"error": "missing_correct_answer_data"}
                }

            ref_text = correct_answer_json["reference_text"]
            # Extragem cele doua nr corecte
            nums = re.findall(r"\d+", ref_text)
            if len(nums) >= 2:
                correct_root = int(nums[0])
                correct_leaves = int(nums[1])
            else:
                return {
                    "is_correct": False,
                    "score": 0.0,
                    "details": {"error": "invalid_reference_format"}
                }

        # Extragem nr din raspunsul studentului
        user_nums = re.findall(r"\d+", user_answer)
        #versiune normalizata a raspunsului
        user_answer_lower = user_answer.lower()
        user_answer_normalized = normalize_text(user_answer)
        
        # Cuvinte cheie
        root_keywords = [
            "radacina", "root",
            "valoare", "maxim", "minim", "max", "min",
            "rezultat", "scor"
        ]
        leaves_keywords = [
            "frunza","frunze", "leaf", "leaves",
            "noduri", "nod final", "terminal", "vizitate"
        ]

        #daca utilizatorul nu a scirs niciun numar -> raspuns imposibil de evaluat
        if len(user_nums) == 0:
            return {
                "is_correct": False,
                "score": 0.0,
                "details": {
                    "match_type": "minimax_no_numbers",
                    "expected": {"root": correct_root, "leaves": correct_leaves},
                    "got": None
                }
            }
        
        #impart textul în propoziții
        sentences = re.split(r'[.!?;]', user_answer_lower)
        sentences_normalized = [normalize_text(s) for s in sentences]
        
        def find_number_with_context(num_str: str) -> Tuple[Optional[str], str]:
            """
            Găsește contextul unei cifre în text NORMALIZAT.
            Returnează (tip_identificat, propoziția_completă)
            """
            for i, sentence_norm in enumerate(sentences_normalized):
                if num_str in sentence_norm:
                    #verific propozitia conține cuvinte cheie
                    has_root = any(kw in sentence_norm for kw in root_keywords)
                    has_leaves = any(kw in sentence_norm for kw in leaves_keywords)
                    
                    if has_root and not has_leaves:
                        return ("root", sentences[i].strip())
                    elif has_leaves and not has_root:
                        return ("leaves", sentences[i].strip())
                    else:
                        return (None, sentences[i].strip())
            return (None, "")
        
        #construiesc maparea numar -> context
        number_contexts = {}
        for num_str in user_nums:
            context_type, sentence = find_number_with_context(num_str)
            number_contexts[int(num_str)] = {
                "type": context_type,
                "sentence": sentence
            }
        
        # Cazul cu 1 numar
        if len(user_nums) == 1:
            user_val = int(user_nums[0])
            ctx = number_contexts[user_val]

            #nr reprezina radacina si e corect-> 50%
            if ctx["type"] == "root" and user_val == correct_root:
                return {
                    "is_correct": False,
                    "score": 50.0,
                    "details": {
                        "match_type": "minimax_partial_root_only",
                        "expected": {"root": correct_root, "leaves": correct_leaves},
                        "got": {"root": user_val, "leaves": None}
                    }
                }
            #nr reprezinta frunza si e corect -> 50%
            elif ctx["type"] == "leaves" and user_val == correct_leaves:
                return {
                    "is_correct": False,
                    "score": 50.0,
                    "details": {
                        "match_type": "minimax_partial_leaves_only",
                        "expected": {"root": correct_root, "leaves": correct_leaves},
                        "got": {"root": None, "leaves": user_val}
                    }
                }
            #nr corect dar context ambiguu -> 40%
            elif user_val in [correct_root, correct_leaves]:
                return {
                    "is_correct": False,
                    "score": 40.0,
                    "details": {
                        "match_type": "minimax_partial_ambiguous",
                        "expected": {"root": correct_root, "leaves": correct_leaves},
                        "got": user_val,
                        "message": "Un număr corect, dar nu este clar dacă este rădăcina sau frunzele"
                    }
                }
            #nr gresit -> 0%
            else:
                return {
                    "is_correct": False,
                    "score": 0.0,
                    "details": {
                        "match_type": "minimax_partial_incorrect",
                        "expected": {"root": correct_root, "leaves": correct_leaves},
                        "got": user_val
                    }
                }
        
        # Cazul cu 2 numere
        elif len(user_nums) == 2:
            u1 = int(user_nums[0])
            u2 = int(user_nums[1])

            #contextele fiecarui numar
            ctx1 = number_contexts.get(u1, {})
            ctx2 = number_contexts.get(u2, {})
            
            type1 = ctx1.get("type")
            type2 = ctx2.get("type")
            
            #identific ce număr corespunde la ce
            identified_root = None
            identified_leaves = None
            
            if type1 == "root":
                identified_root = u1
            if type1 == "leaves":
                identified_leaves = u1
            if type2 == "root":
                identified_root = u2
            if type2 == "leaves":
                identified_leaves = u2
            
            # CAZUL 1: Ambele identificate clar
            if identified_root is not None and identified_leaves is not None:
                #corect 100%
                if identified_root == correct_root and identified_leaves == correct_leaves:
                    return {
                        "is_correct": True,
                        "score": 100.0,
                        "details": {
                            "match_type": "minimax_explicit_correct",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": {"root": identified_root, "leaves": identified_leaves}
                        }
                    }
                #nr identificate corect dar inversate 70%
                elif identified_root == correct_leaves and identified_leaves == correct_root:
                    return {
                        "is_correct": False,
                        "score": 70.0,
                        "details": {
                            "match_type": "minimax_inverted",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": {"root": identified_root, "leaves": identified_leaves},
                            "message": "Numerele sunt corecte, dar rădăcina și frunzele sunt inversate"
                        }
                    }
                #complet gresit
                else:
                    return {
                        "is_correct": False,
                        "score": 0.0,
                        "details": {
                            "match_type": "minimax_incorrect",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": {"root": identified_root, "leaves": identified_leaves}
                        }
                    }
            
            # CAZUL 2: Doar unul identificat
            elif identified_root is not None and identified_leaves is None:
                if identified_root == correct_root:
                    other_num = u2 if identified_root == u1 else u1
                    if other_num == correct_leaves:
                        return {
                            "is_correct": True,
                            "score": 85.0,
                            "details": {
                                "match_type": "minimax_one_labeled_correct",
                                "expected": {"root": correct_root, "leaves": correct_leaves},
                                "got": {"root": identified_root, "leaves": other_num},
                                "message": "Rădăcina este etichetată corect, celălalt număr este corect dar neetichetat"
                            }
                        }
                    #doar root e corect -> 50%
                    else:
                        return {
                            "is_correct": False,
                            "score": 50.0,
                            "details": {
                                "match_type": "minimax_partial_root_identified",
                                "expected": {"root": correct_root, "leaves": correct_leaves},
                                "got": {"root": identified_root, "leaves": None}
                            }
                        }
                    #radacina identificata gresit
                else:
                    return {
                        "is_correct": False,
                        "score": 0.0,
                        "details": {
                            "match_type": "minimax_partial_root_incorrect",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": {"root": identified_root, "leaves": None}
                        }
                    }
            #doar frunzele sunt identificate
            elif identified_leaves is not None and identified_root is None:
                if identified_leaves == correct_leaves:
                    other_num = u2 if identified_leaves == u1 else u1
                    if other_num == correct_root:
                        return {
                            "is_correct": True,
                            "score": 85.0,
                            "details": {
                                "match_type": "minimax_one_labeled_correct",
                                "expected": {"root": correct_root, "leaves": correct_leaves},
                                "got": {"root": other_num, "leaves": identified_leaves},
                                "message": "Frunzele sunt etichetate corect, celălalt număr este corect dar neetichetat"
                            }
                        }
                    else:
                        return {
                            "is_correct": False,
                            "score": 50.0,
                            "details": {
                                "match_type": "minimax_partial_leaves_identified",
                                "expected": {"root": correct_root, "leaves": correct_leaves},
                                "got": {"root": None, "leaves": identified_leaves}
                            }
                        }
                else:
                    return {
                        "is_correct": False,
                        "score": 0.0,
                        "details": {
                            "match_type": "minimax_partial_leaves_incorrect",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": {"root": None, "leaves": identified_leaves}
                        }
                    }
            
            # CAZUL 3: Niciunul identificat
            else:
                #daca utilizatorul scrie fix cele 2 numere ->75%
                if {u1, u2} == {correct_root, correct_leaves}:
                    return {
                        "is_correct": True,
                        "score": 75.0,
                        "details": {
                            "match_type": "minimax_correct_unlabeled",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": (u1, u2),
                            "message": "Numerele sunt corecte, dar nu sunt etichetate clar"
                        }
                    }
                #altfel 0%
                else:
                    return {
                        "is_correct": False,
                        "score": 0.0,
                        "details": {
                            "match_type": "minimax_incorrect_unlabeled",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": (u1, u2)
                        }
                    }
        
        # Cazul cu 3+ numere
        else:
            potential_root = None
            potential_leaves = None

            #cautam daca macar un numar apare in context corect
            for num_str in user_nums:
                num = int(num_str)
                ctx = number_contexts.get(num, {})
                
                if ctx.get("type") == "root" and num in [correct_root, correct_leaves]:
                    potential_root = num
                elif ctx.get("type") == "leaves" and num in [correct_root, correct_leaves]:
                    potential_leaves = num

            #daca ambele sunt identificate corect
            if potential_root is not None and potential_leaves is not None:
                if potential_root == correct_root and potential_leaves == correct_leaves:
                    return {
                        "is_correct": True,
                        "score": 90.0,
                        "details": {
                            "match_type": "minimax_correct_with_extra_numbers",
                            "expected": {"root": correct_root, "leaves": correct_leaves},
                            "got": {"root": potential_root, "leaves": potential_leaves},
                            "message": "Răspunsul corect identificat, dar există numere suplimentare în text"
                        }
                    }
            
            return {
                "is_correct": False,
                "score": 0.0,
                "details": {
                    "match_type": "minimax_too_many_numbers",
                    "expected": {"root": correct_root, "leaves": correct_leaves},
                    "got": [int(n) for n in user_nums]
                }
            }

    if question_type == "CSP_PROBLEM":
        correct_raw = correct_answer_json.get("answer", "").lower().replace(" ", "")
        
        # Extrage valorile din răspunsul corect (elimină acolade și spații)
        correct_clean = correct_raw.replace("{", "").replace("}", "").replace(" ", "")
        
        # Normalizează răspunsul utilizatorului (elimină acolade și spații)
        user_clean = user_answer_norm.replace("{", "").replace("}", "")
        
        # Verifică dacă răspunsul utilizatorului conține exact aceleași valori
        # Acceptă atât "{1,3}" cât și "1,3" sau "1, 3"
        if correct_clean and (correct_clean in user_clean or correct_raw in user_answer_norm):
            return {
                "is_correct": True,
                "score": 100.0,
                "details": {"match_type": "csp_flexible", "expected": correct_raw, "user_provided": user_clean}
            }
        
        # Verificare inversă pentru ordine diferită (ex: "3,1" vs "1,3")
        if correct_clean and len(correct_clean) > 0:
            correct_values = sorted(correct_clean.split(","))
            user_values = sorted([v.strip() for v in user_clean.split(",") if v.strip()])
            
            if correct_values == user_values:
                return {
                    "is_correct": True,
                    "score": 100.0,
                    "details": {"match_type": "csp_unordered", "expected": correct_raw, "user_provided": user_clean}
                }
        
        return {
            "is_correct": False,
            "score": 0.0,
            "details": {"match_type": "csp_mismatch", "expected": correct_raw, "user_provided": user_clean}
        }

    if question_type == "GAME_MATRIX":
        has_nash = correct_answer_json.get("has_nash", True)
        correct_text = correct_answer_json.get("answer", "") or correct_answer_json.get("answer_text", "")
        correct_text_norm = normalize_text(correct_text).replace(" ", "")
        
        no_nash_keywords = ["nuexista", "nuare", "noexiste", "fara", "nimic"]
        user_says_no_nash = any(kw in user_answer_norm for kw in no_nash_keywords)
        
        if not has_nash and user_says_no_nash:
            return {
                "is_correct": True,
                "score": 100.0,
                "details": {"match_type": "nash_no_equilibrium_correct"}
            }
        
        if has_nash and user_says_no_nash:
            return {
                "is_correct": False,
                "score": 0.0,
                "details": {"match_type": "nash_wrong_no_equilibrium", "expected": correct_text}
            }
        
        if not has_nash and not user_says_no_nash:
            return {
                "is_correct": False,
                "score": 0.0,
                "details": {"match_type": "nash_wrong_cell_given", "expected": "Nu există echilibru Nash pur"}
            }
        
        if correct_text_norm and correct_text_norm in user_answer_norm:
            return {
                "is_correct": True,
                "score": 100.0,
                "details": {"match_type": "nash_exact_match", "expected": correct_text}
            }
        
        # Verificare partiala prin strategii
        nash_equilibria = correct_answer_json.get("nash_equilibria", [])
        row_names = ["sus", "jos", "mijloc"]
        col_names = ["stanga", "dreapta", "centru"]
        
        for eq in nash_equilibria:
            if eq[0] < len(row_names) and eq[1] < len(col_names):
                row_name = row_names[eq[0]]
                col_name = col_names[eq[1]]
                if row_name in user_answer_norm and col_name in user_answer_norm:
                    return {
                        "is_correct": True,
                        "score": 100.0,
                        "details": {"match_type": "nash_strategy_match", "expected": correct_text}
                    }
        
        return {
            "is_correct": False,
            "score": 0.0,
            "details": {"match_type": "nash_no_match", "expected": correct_text}
        }

    if "answer" in correct_answer_json and "reference_text" not in correct_answer_json:
        correct_answer_text = correct_answer_json["answer"].lower().strip()
        is_correct = user_answer_norm == correct_answer_text.replace(" ", "")
        return {
            "is_correct": is_correct,
            "score": 100.0 if is_correct else 0.0,
            "details": {"match_type": "exact_multiple_choice"}
        }


    #evaluare semantica pentru raspunsuri text
    if "reference_text" in correct_answer_json:
        reference_text = correct_answer_json["reference_text"]
        user_doc = nlp(user_answer)
        ref_doc = nlp(reference_text)

        # Similaritate semantică
        semantic_score = 0.0
        if user_doc.has_vector and ref_doc.has_vector:
            semantic_score = user_doc.similarity(ref_doc)

        # Evaluare pe bază de keywords dacă există
        keyword_score = 0.0
        if "keywords" in correct_answer_json:
            keywords = correct_answer_json["keywords"]
            if keywords:
                user_answer_normalized = normalize_text(user_answer)
                matched_keywords = 0
                
                for keyword in keywords:
                    keyword_norm = normalize_text(keyword)
                    # Match exact sau ca parte din cuvânt
                    if keyword_norm in user_answer_normalized:
                        matched_keywords += 1
                
                # Scor bazat pe procentul de keywords găsite
                keyword_score = matched_keywords / len(keywords) if len(keywords) > 0 else 0.0
        
        # Combinăm scorurile: 60% semantic + 40% keywords (dacă există)
        if keyword_score > 0:
            combined_score = (semantic_score * 0.6) + (keyword_score * 0.4)
        else:
            combined_score = semantic_score
        
        # Scalare la 100
        final_score = max(0, min(100, combined_score * 100))
        
        return {
            "is_correct": final_score >= 60,  # Pragul pentru corect
            "score": final_score,
            "details": {
                "match_type": "text_evaluation",
                "semantic_similarity_score": round(semantic_score, 4),
                "keyword_match_score": round(keyword_score, 4) if keyword_score > 0 else None,
                "combined_score": round(combined_score, 4)
            }
        }

    return {"is_correct": False, "score": 0.0, "details": {"error": "invalid_format"}}

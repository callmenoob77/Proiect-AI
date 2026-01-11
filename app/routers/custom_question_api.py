from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from ..database import get_db
from .. import models, schemas
from ..question_patterns import QUESTION_PATTERNS

try:
    from ..core.minimax_generator import genereaza_intrebare_minimax
except ImportError:
    genereaza_intrebare_minimax = None

try:
    from ..core.nash_generator import genereaza_intrebare_nash
except ImportError:
    genereaza_intrebare_nash = None

# Baza de cunoștințe despre strategii
STRATEGY_KNOWLEDGE = {
    "A* Search": {
        "description": "algoritm de căutare informată care folosește euristica",
        "characteristics": "Utilizează funcția de evaluare f(n) = g(n) + h(n)",
        "usage": "Când avem o euristică bună pentru estimarea costului",
        "complexity": "O(b^d) timp și spațiu în cel mai rău caz"
    },
    "Backtracking": {
        "description": "tehnică recursivă de explorare sistematică a soluțiilor",
        "characteristics": "Explorează spațiul soluțiilor și revine când găsește o stare invalidă",
        "usage": "Când trebuie să găsim toate soluțiile sau să verificăm constrângeri",
        "complexity": "O(k^n) în cel mai rău caz, unde k este numărul de opțiuni"
    },
    "BFS": {
        "description": "algoritm de căutare nevizată care explorează în lățime",
        "characteristics": "Explorează nodurile nivel cu nivel folosind o coadă",
        "usage": "Când căutăm calea cea mai scurtă în grafuri neponderate",
        "complexity": "O(b^d) timp și spațiu"
    },
    "DFS": {
        "description": "algoritm de căutare nevizată care explorează în adâncime",
        "characteristics": "Explorează pe o ramură cât mai adânc posibil înainte de backtrack",
        "usage": "Când spațiul soluțiilor este adânc și soluțiile sunt frecvente",
        "complexity": "O(b^m) timp și O(bm) spațiu"
    },
    "Programare Dinamica": {
        "description": "metodă de rezolvare prin descompunere în subprobleme suprapuse",
        "characteristics": "Memorează soluțiile subproblemelor pentru a evita recalcularea",
        "usage": "Când problema are subprobleme suprapuse și substructură optimă",
        "complexity": "Depinde de problema specifică, de obicei O(n^2) sau O(n*m)"
    },
    "Greedy": {
        "description": "algoritm care face alegeri local optime la fiecare pas",
        "characteristics": "Ia decizia cea mai bună în momentul curent fără să privească înainte",
        "usage": "Când alegerea locală optimă conduce la soluția globală optimă",
        "complexity": "Variază, de obicei O(n log n) sau O(n^2)"
    },
    "Divide et Impera": {
        "description": "metodă care împarte problema în subprobleme mai mici",
        "characteristics": "Divide problema, rezolvă subproblemele și combină rezultatele",
        "usage": "Când problema poate fi împărțită în subprobleme independente",
        "complexity": "De obicei O(n log n)"
    }
}

router = APIRouter()

CHAPTER_BY_PATTERN = {
    "CSP": "Satisfacerea Constrangerilor (CSP)",
    "MINIMAX": "Algoritmi de cautare",
    "STRATEGY": "Algoritmi de cautare",
    "THEORY": "Algoritmi de cautare",
}
QUESTION_TYPE_BY_PATTERN = {
    "CSP": "CSP_PROBLEM",
    "MINIMAX": "MINIMAX_TREE",
    "STRATEGY": "A_STAR_DESCRIPTION",
    "THEORY": "A_STAR_DESCRIPTION",
}


#a
@router.post("/custom-question/ask")
def handle_custom_question(
    request: schemas.PatternQuestionRequest,
    db: Session = Depends(get_db)
):
    pattern_type = request.pattern_type
    pattern_id = request.pattern_id
    inputs = request.inputs
    answer_type = request.answer_type

    # Pentru MINIMAX, folosim generatorul dedicat
    if pattern_type == "MINIMAX":
        if not genereaza_intrebare_minimax:
            raise HTTPException(status_code=500, detail="Generator Minimax indisponibil")
        
        question_data = genereaza_intrebare_minimax(answer_type=answer_type)
        
        # Extragem chapter_name și options
        chapter_name = question_data.pop("chapter_name")
        options = question_data.pop("options", None)
        answer_type_from_gen = question_data.pop("answer_type", answer_type)
        
        # Găsim sau creăm capitolul
        chapter_db = db.query(models.Chapter).filter(models.Chapter.name == chapter_name).first()
        if not chapter_db:
            chapter_db = models.Chapter(name=chapter_name)
            db.add(chapter_db)
            db.commit()
            db.refresh(chapter_db)
        
        # Creăm întrebarea
        new_question = models.Question(**question_data)
        new_question.chapters.append(chapter_db)
        
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        # Returnăm răspunsul
        return {
            "id": new_question.id,
            "title": new_question.title,
            "prompt": new_question.prompt,
            "question_type": new_question.question_type.value if hasattr(new_question.question_type, 'value') else new_question.question_type,
            "difficulty": new_question.difficulty,
            "problem_instance": new_question.problem_instance,
            "reference_solution": new_question.reference_solution,
            "answer_type": answer_type_from_gen,
            "protected": new_question.protected,
            "options": options if options else []
        }

    # Pentru NASH, folosim generatorul dedicat
    if pattern_type == "NASH":
        if not genereaza_intrebare_nash:
            raise HTTPException(status_code=500, detail="Generator Nash indisponibil")
        
        question_data = genereaza_intrebare_nash(answer_type=answer_type)
        
        # Extragem chapter_name și options
        chapter_name = question_data.pop("chapter_name")
        options = question_data.pop("options", None)
        answer_type_from_gen = question_data.pop("answer_type", answer_type)
        
        # Găsim sau creăm capitolul
        chapter_db = db.query(models.Chapter).filter(models.Chapter.name == chapter_name).first()
        if not chapter_db:
            chapter_db = models.Chapter(name=chapter_name)
            db.add(chapter_db)
            db.commit()
            db.refresh(chapter_db)
        
        # Creăm întrebarea
        new_question = models.Question(**question_data)
        new_question.chapters.append(chapter_db)
        
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        # Returnăm răspunsul
        return {
            "id": new_question.id,
            "title": new_question.title,
            "prompt": new_question.prompt,
            "question_type": new_question.question_type.value if hasattr(new_question.question_type, 'value') else new_question.question_type,
            "difficulty": new_question.difficulty,
            "problem_instance": new_question.problem_instance,
            "reference_solution": new_question.reference_solution,
            "answer_type": answer_type_from_gen,
            "protected": new_question.protected,
            "options": options if options else []
        }

    # Pentru celelalte pattern-uri, continuăm cu logica existentă
    if pattern_type not in QUESTION_PATTERNS:
        raise HTTPException(status_code=400, detail="Categorie invalida")

    patterns_for_type = QUESTION_PATTERNS[pattern_type]

    # Pentru THEORY, selectăm aleatoriu un pattern pentru variație
    if not pattern_id or pattern_type == "THEORY":
        pattern_id = random.choice(list(patterns_for_type.keys()))

    if pattern_id not in patterns_for_type:
        raise HTTPException(status_code=400, detail="Pattern invalid")

    pattern = patterns_for_type[pattern_id]

    expected_inputs = pattern.get("inputs", [])
    missing = [field for field in expected_inputs if field not in inputs]

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Lipsesc campurile: {', '.join(missing)}"
        )

    try:
        prompt = pattern["template"].format(**inputs)
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Input invalid: {e.args[0]}"
        )

    # Generează opțiuni și răspuns corect pentru întrebările multiple
    options = None
    correct_answer = {}
    
    if answer_type == "multiple":
        if pattern_type == "CSP" and pattern_id == "FC":
            # Pentru Forward Checking, răspunsul depinde de valorile din domeniu
            domains_str = inputs.get("domains", "{}")
            var2 = inputs.get("var2", "Y")
            assigned_value = inputs.get("assigned_value", "")
            
            # Generăm opțiuni bazate pe domeniu
            try:
                # Extragem valorile din domeniu
                domain_vals = domains_str.strip("{}").split(",")
                domain_vals = [v.strip() for v in domain_vals if v.strip()]
                
                # Răspunsul corect: domeniul fără valoarea asignată
                correct_vals = [v for v in domain_vals if v != assigned_value]
                correct_str = "{" + ", ".join(correct_vals) + "}"
                correct_answer = {"answer": correct_str}
                
                # Generăm opțiuni distractor
                options = [correct_str]
                # Opțiune 1: domeniul complet
                options.append("{" + ", ".join(domain_vals) + "}")
                # Opțiune 2: doar valoarea asignată
                if assigned_value in domain_vals:
                    options.append("{" + assigned_value + "}")
                # Opțiune 3: subset random
                if len(domain_vals) > 1:
                    subset = random.sample(domain_vals, max(1, len(domain_vals) // 2))
                    options.append("{" + ", ".join(subset) + "}")
                    
                options = list(set(options))[:4]
                random.shuffle(options)
                
            except Exception:
                # Fallback simplu
                correct_answer = {"answer": domains_str}
                options = [domains_str, "{}", "{1,2}", "{1,2,3}"]
                
        elif pattern_type == "STRATEGY":
            # Pentru întrebări de strategie, generăm opțiuni cu strategii
            problem_name = inputs.get("problem_name", "N-Queens")
            instance = inputs.get("instance", "instanță generică")
            
            strategies = [
                "A* Search",
                "Backtracking",
                "BFS (Breadth-First Search)",
                "DFS (Depth-First Search)",
                "Programare Dinamică",
                "Algoritm Greedy"
            ]
            
            # Selectăm o strategie ca răspuns corect (bazat pe problema dată)
            correct_strategy = random.choice(strategies)
            correct_answer = {"answer": correct_strategy}
            
            # Generăm 3 distractori
            distractors = [s for s in strategies if s != correct_strategy]
            selected_distractors = random.sample(distractors, min(3, len(distractors)))
            
            options = [correct_strategy] + selected_distractors
            random.shuffle(options)
            
        elif pattern_type == "THEORY":
            # Pentru întrebări de teorie despre strategii
            strategy_name = inputs.get("strategy_name", "A* Search")
            
            # Caută strategia în baza de cunoștințe
            strategy_info = None
            for key in STRATEGY_KNOWLEDGE.keys():
                if key.lower() in strategy_name.lower() or strategy_name.lower() in key.lower():
                    strategy_info = STRATEGY_KNOWLEDGE[key]
                    break
            
            # Generăm opțiuni diferite în funcție de pattern_id
            if pattern_id == "DESCRIPTION":
                if strategy_info:
                    correct_desc = f"{strategy_name} este un {strategy_info['description']}"
                else:
                    correct_desc = f"{strategy_name} este un algoritm de rezolvare de probleme"
                
                # Distractori generici
                distractors = [
                    f"{strategy_name} este o tehnică de optimizare globală bazată pe evoluție",
                    f"{strategy_name} este un algoritm de sortare eficient",
                    f"{strategy_name} este o metodă de calcul probabilistic"
                ]
                descriptions = [correct_desc] + distractors[:3]
                
            elif pattern_id == "CHARACTERISTICS":
                if strategy_info:
                    correct_desc = strategy_info['characteristics']
                else:
                    correct_desc = f"Rezolvă problema prin explorare sistematică"
                
                distractors = [
                    "Folosește numere aleatoare pentru a găsi soluția",
                    "Garantează soluția optimă în timp constant",
                    "Necesită o bază de date pentru stocare"
                ]
                descriptions = [correct_desc] + distractors[:3]
                
            elif pattern_id == "USAGE":
                if strategy_info:
                    correct_desc = strategy_info['usage']
                else:
                    correct_desc = f"Când problema necesită o abordare sistematică"
                
                distractors = [
                    "Când avem memorie nelimitată și timp infinit",
                    "Doar pentru probleme cu exact 10 elemente",
                    "Când nu cunoaștem deloc structura problemei"
                ]
                descriptions = [correct_desc] + distractors[:3]
                
            elif pattern_id == "COMPLEXITY":
                if strategy_info:
                    correct_desc = strategy_info['complexity']
                else:
                    correct_desc = f"Depinde de problema specifică"
                
                distractors = [
                    "O(1) timp și spațiu constant",
                    "O(n!) factorial, foarte ineficient",
                    "O(log log n) dublu logaritmic"
                ]
                descriptions = [correct_desc] + distractors[:3]
            else:
                descriptions = [
                    f"{strategy_name} este un algoritm eficient",
                    f"{strategy_name} rezolvă probleme complexe",
                    f"{strategy_name} este o metodă optimă",
                    f"{strategy_name} funcționează în timp polinomial"
                ]
            
            correct_answer = {"answer": descriptions[0]}
            options = descriptions[:4]
            random.shuffle(options)
            
        else:
            # Pentru alte pattern-uri, setăm răspuns generic cu opțiuni
            correct_answer = {"answer": "Opțiunea corectă"}
            options = ["Opțiunea corectă", "Opțiune 1", "Opțiune 2", "Opțiune 3"]
            random.shuffle(options)
    else:
        # Pentru răspunsuri text
        if pattern_type == "THEORY":
            strategy_name = inputs.get("strategy_name", "A* Search")
            
            # Caută strategia în baza de cunoștințe
            strategy_info = None
            for key in STRATEGY_KNOWLEDGE.keys():
                if key.lower() in strategy_name.lower() or strategy_name.lower() in key.lower():
                    strategy_info = STRATEGY_KNOWLEDGE[key]
                    break
            
            # Generează cuvinte cheie și text de referință specific strategiei
            if strategy_info:
                keywords = [
                    strategy_name.lower(),
                    "algoritm", "strategie", "metoda",
                    "complexitate", "eficient", "optim"
                ]
                # Extrage cuvinte cheie din descriere
                desc_words = strategy_info['description'].lower().split()
                keywords.extend([w for w in desc_words if len(w) > 4])
                
                reference_text = (
                    f"{strategy_name} este un {strategy_info['description']}. "
                    f"{strategy_info['characteristics']}. "
                    f"Se folosește {strategy_info['usage']}. "
                    f"Complexitatea este {strategy_info['complexity']}."
                )
            else:
                keywords = [strategy_name.lower(), "algoritm", "strategie", "rezolvare", "problema"]
                reference_text = f"{strategy_name} este o strategie de rezolvare a problemelor care necesită o abordare sistematică."
            
            correct_answer = {
                "keywords": list(set(keywords)),
                "reference_text": reference_text
            }
            
        elif pattern_type == "STRATEGY":
            problem_name = inputs.get("problem_name", "Problema")
            instance = inputs.get("instance", "instanță")
            strategy_name = inputs.get("strategy_name", "")
            
            # Caută strategia sugerată în baza de cunoștințe pentru keywords
            strategy_info = None
            for key in STRATEGY_KNOWLEDGE.keys():
                if key.lower() in strategy_name.lower() or strategy_name.lower() in key.lower():
                    strategy_info = STRATEGY_KNOWLEDGE[key]
                    break
            
            # Construim keywords din problema și strategia sugerată
            keywords = [
                problem_name.lower(),
                "strategie", "algoritm", "rezolvare",
                "eficient", "optim", "solutie", "abordare"
            ]
            
            # Adaugă keywords specifice strategiei sugerate
            if strategy_info and strategy_name:
                keywords.extend([
                    strategy_name.lower(),
                    "selectare", "alegere", "potrivit"
                ])
                # Extrage cuvinte cheie din caracteristici
                char_words = strategy_info['characteristics'].lower().split()
                keywords.extend([w for w in char_words if len(w) > 5])
            
            reference_text = (
                f"Pentru {problem_name} cu instanța: {instance}, "
                f"trebuie analizate caracteristicile problemei (dimensiune, constrângeri, "
                f"optimizare necesară) pentru a selecta strategia potrivită. "
                f"Strategiile comune includ: Backtracking pentru explorare exhaustivă, "
                f"Greedy pentru soluții rapide, Programare Dinamică pentru subprobleme "
                f"suprapuse, A* pentru căi optime cu euristică."
            )
            
            correct_answer = {
                "keywords": list(set(keywords)),
                "reference_text": reference_text
            }
            
        elif pattern_type == "CSP":
            # Identifică tipul de CSP bazat pe pattern_id
            if pattern_id == "FC":
                # Forward Checking
                var1 = inputs.get("var1", "X")
                var2 = inputs.get("var2", "Y")
                domains = inputs.get("domains", "{}")
                assigned_value = inputs.get("assigned_value", "")
                
                # Parse domains: "{1,2,3}" -> [1,2,3]
                domain_values = []
                try:
                    domain_str = domains.strip().replace("{", "").replace("}", "")
                    domain_values = [v.strip() for v in domain_str.split(",") if v.strip()]
                except:
                    domain_values = ["1", "2", "3"]
                
                # Elimină valoarea asignată din domeniu
                remaining_values = [v for v in domain_values if v != str(assigned_value)]
                
                try:
                    remaining_values.sort()
                except:
                    pass
                
                correct_answer_set = "{" + ", ".join(remaining_values) + "}"
                correct_answer = {"answer": correct_answer_set}
                reference_solution = f"Răspunsul corect: {correct_answer_set}"
                
            elif pattern_id == "MRV":
                # Minimum Remaining Values
                variables_str = inputs.get("variables", "X, Y")
                domains_str = inputs.get("domains", "D(X)={1,2}, D(Y)={3}")
                
                # Parse domains pentru fiecare variabilă
                # Format așteptat: "D(X)={1,2}, D(Y)={3}" sau similar
                import re
                domain_pattern = r'D\((\w+)\)\s*=\s*\{([^}]+)\}'
                matches = re.findall(domain_pattern, domains_str)
                
                if matches:
                    # Găsește variabila cu domeniul cel mai mic
                    min_var = None
                    min_size = float('inf')
                    
                    for var_name, domain_vals in matches:
                        vals = [v.strip() for v in domain_vals.split(",") if v.strip()]
                        if len(vals) < min_size:
                            min_size = len(vals)
                            min_var = var_name
                    
                    correct_answer_set = min_var if min_var else "X"
                else:
                    # Fallback: prima variabilă
                    vars_list = [v.strip() for v in variables_str.split(",") if v.strip()]
                    correct_answer_set = vars_list[0] if vars_list else "X"
                
                correct_answer = {"answer": correct_answer_set}
                reference_solution = f"Răspunsul corect: {correct_answer_set}"
                
            elif pattern_id == "AC3":
                # Arc Consistency
                var1 = inputs.get("var1", "X")
                var2 = inputs.get("var2", "Y")
                domain1 = inputs.get("domain1", "{1,2,3}")
                domain2 = inputs.get("domain2", "{2,3,4}")
                constraint = inputs.get("constraint", "!=")
                
                # Parse domain1
                domain1_values = []
                try:
                    d1_str = domain1.strip().replace("{", "").replace("}", "")
                    domain1_values = [v.strip() for v in d1_str.split(",") if v.strip()]
                except:
                    domain1_values = ["1", "2", "3"]
                
                # Parse domain2
                domain2_values = []
                try:
                    d2_str = domain2.strip().replace("{", "").replace("}", "")
                    domain2_values = [v.strip() for v in d2_str.split(",") if v.strip()]
                except:
                    domain2_values = ["2", "3", "4"]
                
                # Aplică AC3: elimină din domain1 valorile care nu au suport în domain2
                remaining_values = []
                for val1 in domain1_values:
                    has_support = False
                    for val2 in domain2_values:
                        # Verifică constrângerea
                        if constraint == "!=":
                            if val1 != val2:
                                has_support = True
                                break
                        elif constraint == "<":
                            try:
                                if float(val1) < float(val2):
                                    has_support = True
                                    break
                            except:
                                pass
                        elif constraint == ">":
                            try:
                                if float(val1) > float(val2):
                                    has_support = True
                                    break
                            except:
                                pass
                        elif constraint == "==":
                            if val1 == val2:
                                has_support = True
                                break
                    
                    if has_support:
                        remaining_values.append(val1)
                
                try:
                    remaining_values.sort()
                except:
                    pass
                
                if remaining_values:
                    correct_answer_set = "{" + ", ".join(remaining_values) + "}"
                else:
                    correct_answer_set = "Mulțimea vidă"
                
                correct_answer = {"answer": correct_answer_set}
                reference_solution = f"Răspunsul corect: {correct_answer_set}"
            
            else:
                # Fallback pentru pattern_id necunoscut
                correct_answer = {"answer": "Necunoscut"}
                reference_solution = "Pattern CSP necunoscut"
            
        elif pattern_type == "MINIMAX":
            # Pentru MINIMAX, keywords despre algoritm
            keywords = [
                "minimax", "alpha", "beta", "alpha-beta", "taiere", "pruning",
                "max", "min", "radacina", "frunze", "arbore", "joc",
                "valoare", "optim", "adversar", "vizitat", "propagare"
            ]
            
            reference_text = (
                f"Algoritmul MinMax cu Alpha-Beta pruning evaluează arborele de joc "
                f"alternând între niveluri MAX (jucător) și MIN (adversar). "
                f"Alpha reprezintă cea mai bună valoare garantată pentru MAX, "
                f"iar Beta cea mai bună pentru MIN. Când Alpha >= Beta, restul ramurii "
                f"este tăiată (pruning) deoarece nu va influența decizia finală. "
                f"Valoarea se propagă de la frunze către rădăcină."
            )
            
            correct_answer = {
                "keywords": list(set(keywords)),
                "reference_text": reference_text
            }
        else:
            correct_answer = {"keywords": ["relevant", "algoritm"], "reference_text": "Răspuns text așteptat"}

    # Generează soluția de referință bazată pe răspunsul corect
    if "answer" in correct_answer:
        reference_solution = f"Răspunsul corect este: {correct_answer['answer']}"
    elif "reference_text" in correct_answer:
        reference_solution = correct_answer["reference_text"]
    else:
        reference_solution = "Evaluare bazată pe cuvinte cheie și context."

    qdata = {
        "title": f"{pattern_type} – {pattern_id}",
        "prompt": prompt,
        "question_type": QUESTION_TYPE_BY_PATTERN[pattern_type],
        "difficulty": 3,
        "problem_instance": inputs,
        "correct_answer": correct_answer,
        "reference_solution": reference_solution,
        "chapter_name": CHAPTER_BY_PATTERN[pattern_type],
    }


    chapter_name = qdata.pop("chapter_name")

    chapter_db = (
        db.query(models.Chapter)
        .filter(models.Chapter.name == chapter_name)
        .first()
    )
    if not chapter_db:
        chapter_db = models.Chapter(name=chapter_name)
        db.add(chapter_db)
        db.commit()
        db.refresh(chapter_db)

    new_question = models.Question(**qdata)
    new_question.chapters.append(chapter_db)

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "id": new_question.id,
        "title": new_question.title,
        "prompt": new_question.prompt,
        "question_type": new_question.question_type.value if hasattr(new_question.question_type, 'value') else new_question.question_type,
        "difficulty": new_question.difficulty,
        "problem_instance": new_question.problem_instance,
        "reference_solution": new_question.reference_solution,
        "answer_type": answer_type,   # DOAR pt UI
        "protected": new_question.protected,
        "options": options if options else []
    }

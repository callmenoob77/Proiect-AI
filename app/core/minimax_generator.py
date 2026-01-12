import random
from typing import Dict, Any
from .minimax_solver import MinMaxSolver


def count_leaves(node: Dict[str, Any]) -> int:
    """Numara frunzele din arbore
        Un nod e considerat frunza daca are campul "value"
    """
    if "value" in node: #este frunza
        return 1
    children = node.get("children", [])
    return sum(count_leaves(child) for child in children)


def _gen_random_tree(max_depth: int, difficulty: int, current_depth: int = 0) -> Dict[str, Any]:
    """
    Genereaza recursiv un arbore MIN/MAX
    - Frunzele apar la adancime maxima sau aleator
    - Nodurile altereaza intre MAX(nivel par) si MIN(impar)
    - Nr copii:
        - radacina poate avea 3 copii
        - toate celelalte noduri 2 copii
    - frunzele primesc valori radnom intre 1 si 20
    """

    #daca am atins adancimea max-> generez frunza
    if current_depth >= max_depth:
        return {
            "id": f"leaf_{random.randint(1000, 9999)}",
            "value": random.randint(1, 20)
        }

    #previn generarea arborilor mari
    early_stop_chance = (0.4 if difficulty == 1 else 0.1) * current_depth
    if current_depth >= 1 and random.random() < early_stop_chance:
        return {
            "id": f"leaf_{random.randint(1000, 9999)}",
            "value": random.randint(1, 20)
        }
    
    #doar 2 copii pe nod (poate 3 la radacina)
    if current_depth == 0:
        # La Easy/Medium radacina are 2 copii, la Hard poate avea 3
        num_children = 3 if (difficulty == 3 and random.random() < 0.6) else 2
    else:
        # La Hard permitem ocazional 3 copii și în noduri intermediare
        num_children = 3 if (difficulty == 3 and random.random() < 0.3) else 2

    #determin tipul nodului in functie de nivel
    node_type = "MAX" if current_depth % 2 == 0 else "MIN"

    return {
        "id": f"node_{current_depth}_{random.randint(1000, 9999)}",
        "type": node_type,
        "children": [
            _gen_random_tree(max_depth, difficulty, current_depth + 1)
            for _ in range(num_children)
        ]
    }


def genereaza_intrebare_minimax(answer_type: str = "multiple", difficulty: int = 2) -> Dict[str, Any]:
    """
    Generează o întrebare minimax cu arbori MICI (4-10 frunze).
    """

    if difficulty == 1:  # Easy
        max_depth = 2
        min_leaves, max_leaves = 3, 4
    elif difficulty == 2:  # Medium
        max_depth = random.choice([2, 3])
        min_leaves, max_leaves = 5, 7
    else:  # Hard (3)
        max_depth = 3
        min_leaves, max_leaves = 8, 12

    max_attempts = 20
    tree = None
    leaf_count = 0

    for attempt in range(max_attempts):
        tree = _gen_random_tree(max_depth, difficulty)
        leaf_count = count_leaves(tree)

        if min_leaves <= leaf_count <= max_leaves:
            break

        # Dacă eșuează repetat, forțăm o structură minimă
        if attempt == max_attempts - 1:
            max_depth = 2 if difficulty < 3 else 3
    
    # Solver MinMax cu Alpha-Beta
    solver = MinMaxSolver(tree)
    root_value, visited_leaves = solver.solve()
    
    root_type = tree.get("type", "MAX")

    #Solutia de referinta
    reference_solution = (
        f"Aplicand MinMax cu optimizarea Alpha-Beta pe arborele dat, cu rădăcina de tip {root_type}, "
        f"se obține valoarea {root_value} în radacina. "
        f"In timpul parcurgerii, au fost vizitate {visited_leaves} noduri frunza, "
        f"restul fiind eliminate prin taieri Alpha-Beta."
    )
    
    prompt = (
        "Pentru arborele de joc dat (nodurile alternează între MAX și MIN), "
        "determina valoarea din radacina și numarul de noduri frunza vizitate "
        "de algoritmul MinMax cu optimizarea Alpha-Beta. "
        "Arborele este reprezentat vizual în interfața."
    )
    
    # VARIANTA TEXT
    if answer_type == "text":
        return {
            "title": "MinMax cu Alpha-Beta pe arbore de joc",
            "prompt": prompt,
            "question_type": "MINIMAX_TREE",
            "difficulty": 3,
            "problem_instance": {
                "tree": tree,
                "root_type": root_type,
                "total_leaves": leaf_count,
                "tree_depth": max_depth
            },
            "correct_answer": {
                "reference_text": reference_solution,
                "root_value":root_value,
                "visited_leaves":visited_leaves,
                "keywords": [
                    "minmax", "alpha", "beta", "taiere", "pruning",
                    "MAX", "MIN", "radacina", "frunze",
                    str(root_value), str(visited_leaves),
                ],
            
            },
            "reference_solution": reference_solution,
            "chapter_name": "Algoritmi de cautare si CSP",
            "answer_type": "text",
            "options": []
        }
    
    # VARIANTA MULTIPLE CHOICE
    correct_str = f"Valoare radacina = {root_value}, frunze vizitate = {visited_leaves}"
    
    options = [correct_str]
    used_pairs = {(root_value, visited_leaves)}

    #generare variante gresite dar plauzibile
    def add_distractor(dv: int, dl: int):
        v = root_value + dv
        l = max(1, visited_leaves + dl) #nr frunze nu poate fi 0
        pair = (v, l)
        if pair not in used_pairs:
            used_pairs.add(pair)
            options.append(f"Valoare radacina = {v}, frunze vizitate = {l}")
    
    add_distractor(1, 0)
    add_distractor(-1, 1)
    add_distractor(0, 2)

    #completam pana avem 4 optuni
    while len(options) < 4:
        dv = random.randint(-3, 3)
        dl = random.randint(-2, 3)
        add_distractor(dv, dl)
    
    random.shuffle(options)
    
    return {
        "title": "MinMax cu Alpha-Beta pe arbore de joc",
        "prompt": prompt,
        "question_type": "MINIMAX_TREE",
        "difficulty": difficulty,
        "problem_instance": {
            "tree": tree,
            "root_type": root_type,
            "total_leaves": leaf_count,
            "tree_depth": max_depth
        },
        "correct_answer": {
            "answer": correct_str,
            "root_value":root_value,
            "visited_leaves":visited_leaves
        },
        "reference_solution": reference_solution,
        "chapter_name": "Algoritmi de cautare si CSP",
        "answer_type": "multiple",
        "options": options
    }
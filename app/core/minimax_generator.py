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


def _gen_random_tree(max_depth: int, current_depth: int = 0) -> Dict[str, Any]:
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
    early_stop_chance = 0.3 * current_depth
    if current_depth >= 1 and random.random() < early_stop_chance:
        return {
            "id": f"leaf_{random.randint(1000, 9999)}",
            "value": random.randint(1, 20)
        }
    
    #doar 2 copii pe nod (poate 3 la radacina)
    if current_depth == 0 and random.random() < 0.3:
        num_children = 3
    else:
        num_children = 2  #Toate celelalte noduri: doar 2 copii

    #determin tipul nodului in functie de nivel
    node_type = "MAX" if current_depth % 2 == 0 else "MIN"
    
    return {
        "id": f"node_{current_depth}_{random.randint(1000, 9999)}",
        "type": node_type,
        "children": [
            _gen_random_tree(max_depth, current_depth + 1)
            for _ in range(num_children)
        ]
    }


def genereaza_intrebare_minimax(answer_type: str = "multiple") -> Dict[str, Any]:
    """
    Generează o întrebare minimax cu arbori MICI (4-10 frunze).
    """
    
    # RESTRICȚIE PRINCIPALĂ: adâncime doar 2-3, preferabil 2
    max_depth = random.choices([2, 3], weights=[70, 30])[0]  # 70% șansă pentru adâncime 2
    
    # Încercăm să generăm un arbore mic
    max_attempts = 15
    tree = None
    leaf_count = 0
    
    for attempt in range(max_attempts):
        tree = _gen_random_tree(max_depth)
        leaf_count = count_leaves(tree)

        #accept doar arbori cu frunze intre 4 si 10
        if 4 <= leaf_count <= 10:
            break

        #daca arborele e prea mare, scad adancimea
        if leaf_count > 10:
            max_depth = 2

        if attempt == max_attempts - 1:
            tree = {
                "id": "root",
                "type": "MAX",
                "children": [
                    {
                        "id": "node_1",
                        "type": "MIN",
                        "children": [
                            {"id": "leaf_1", "value": random.randint(1, 20)},
                            {"id": "leaf_2", "value": random.randint(1, 20)}
                        ]
                    },
                    {
                        "id": "node_2",
                        "type": "MIN",
                        "children": [
                            {"id": "leaf_3", "value": random.randint(1, 20)},
                            {"id": "leaf_4", "value": random.randint(1, 20)}
                        ]
                    }
                ]
            }
            leaf_count = 4
    
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
        "difficulty": 3,
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
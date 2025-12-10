import random
from typing import Dict, Any
from .minimax_solver import MinMaxSolver


def count_leaves(node: Dict[str, Any]) -> int:
    """Numără frunzele din arbore"""
    if "value" in node:
        return 1
    children = node.get("children", [])
    return sum(count_leaves(child) for child in children)


def _gen_random_tree(max_depth: int, current_depth: int = 0) -> Dict[str, Any]:
    """
    Generează recursiv un arbore de joc MIN/MAX MIC și compact.
    """
    
    # Adâncime maximă absolută
    if current_depth >= max_depth:
        return {
            "id": f"leaf_{random.randint(1000, 9999)}",
            "value": random.randint(1, 20)
        }
    
    # Șansă MARE de oprire anticipată pentru arbori mici
    early_stop_chance = 0.3 * current_depth  # 0%, 30%, 60%
    if current_depth >= 1 and random.random() < early_stop_chance:
        return {
            "id": f"leaf_{random.randint(1000, 9999)}",
            "value": random.randint(1, 20)
        }
    
    # RESTRICȚIE STRICTĂ: doar 2 copii pe nod (ocazional 3 la rădăcină)
    if current_depth == 0 and random.random() < 0.3:  # 30% șansă pentru 3 copii la rădăcină
        num_children = 3
    else:
        num_children = 2  # Toate celelalte noduri: doar 2 copii
    
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
    
    # RESTRICȚIE PRINCIPALĂ: adâncime doar 2-3, preferabil 2
    max_depth = random.choices([2, 3], weights=[70, 30])[0]  # 70% șansă pentru adâncime 2
    
    # Încercăm să generăm un arbore mic
    max_attempts = 15
    tree = None
    leaf_count = 0
    
    for attempt in range(max_attempts):
        tree = _gen_random_tree(max_depth)
        leaf_count = count_leaves(tree)
        
        # ACCEPTĂM doar arbori cu 4-10 frunze (IDEAL pentru vizualizare)
        if 4 <= leaf_count <= 10:
            break
        
        # Dacă arborele e prea mare, scădem adâncimea
        if leaf_count > 10:
            max_depth = 2
        
        # La ultima încercare, forțăm un arbore simplu
        if attempt == max_attempts - 1:
            # Arbore minimalist: adâncime 2, doar 2 copii
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
    
    reference_solution = (
        f"Aplicând MinMax cu optimizarea Alpha-Beta pe arborele dat, cu rădăcina de tip {root_type}, "
        f"se obține valoarea {root_value} în rădăcină. "
        f"În timpul parcurgerii, au fost vizitate {visited_leaves} noduri frunză, "
        f"restul fiind eliminate prin tăieri Alpha-Beta."
    )
    
    prompt = (
        "Pentru arborele de joc dat (nodurile alternează între MAX și MIN), "
        "determină valoarea din rădăcină și numărul de noduri frunză vizitate "
        "de algoritmul MinMax cu optimizarea Alpha-Beta. "
        "Arborele este reprezentat vizual în interfață."
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
    correct_str = f"Valoare rădăcină = {root_value}, frunze vizitate = {visited_leaves}"
    
    options = [correct_str]
    used_pairs = {(root_value, visited_leaves)}
    
    def add_distractor(dv: int, dl: int):
        v = root_value + dv
        l = max(1, visited_leaves + dl)
        pair = (v, l)
        if pair not in used_pairs:
            used_pairs.add(pair)
            options.append(f"Valoare rădăcină = {v}, frunze vizitate = {l}")
    
    add_distractor(1, 0)
    add_distractor(-1, 1)
    add_distractor(0, 2)
    
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
import random
from typing import Dict, Any
from .minimax_solver import MinMaxSolver

def _gen_random_tree(max_depth: int, current_depth: int = 0) -> Dict[str, Any]:

    # Condiția de frunză
    if current_depth >= max_depth or (current_depth >= 1 and random.random() < 0.25):
        return {
            "id": f"leaf_{random.randint(1000, 9999)}",
            "value": random.randint(1, 20)
        }

    num_children = random.randint(2, 3)
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

    max_depth = random.randint(2, 4)
    tree = _gen_random_tree(max_depth)

    # Solver extern — LA FEL ca CSP!
    solver = MinMaxSolver(tree)
    root_value, visited_leaves = solver.solve()

    correct_str = f"Valoare rădăcină = {root_value}, frunze vizitate = {visited_leaves}"

    prompt = (
        "Pentru arborele de joc dat, determină valoarea din rădăcină și numărul "
        "de noduri frunze vizitate de algoritmul MinMax cu Alpha-Beta."
    )

    reference_solution = (
        f"Aplicând MinMax cu Alpha-Beta se obține valoarea {root_value} în rădăcină. "
        f"Au fost vizitate {visited_leaves} frunze."
    )

    # Distractori
    options = [correct_str]
    used = {(root_value, visited_leaves)}

    def add(v, l):
        if (v, l) not in used:
            used.add((v, l))
            options.append(f"Valoare rădăcină = {v}, frunze vizitate = {l}")

    add(root_value + 1, visited_leaves)
    add(root_value - 1, visited_leaves + 1)
    add(root_value, visited_leaves + 2)

    while len(options) < 4:
        dv = random.randint(-3, 3)
        dl = random.randint(-2, 3)
        add(root_value + dv, max(1, visited_leaves + dl))

    random.shuffle(options)

    return {
        "title": "MinMax cu Alpha-Beta",
        "prompt": prompt,
        "question_type": "MINIMAX_TREE",
        "difficulty": 3,
        "problem_instance": {"tree": tree},
        "correct_answer": {"answer": correct_str},
        "reference_solution": reference_solution,
        "chapter_name": "Algoritmi de cautare si CSP",
        "answer_type": "multiple",
        "options": options
    }

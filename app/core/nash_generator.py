import random
from typing import Dict, Any, List, Tuple


def find_pure_nash(matrix: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    """Gaseste echilibrele Nash pure - returneaza lista de (row, col)."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    nash_equilibria = []
    
    for i in range(rows):
        for j in range(cols):
            p1, p2 = matrix[i][j]
            is_best_for_p1 = all(matrix[k][j][0] <= p1 for k in range(rows))
            is_best_for_p2 = all(matrix[i][k][1] <= p2 for k in range(cols))
            
            if is_best_for_p1 and is_best_for_p2:
                nash_equilibria.append((i, j))
    
    return nash_equilibria


def _generate_random_matrix(rows: int, cols: int) -> List[List[Tuple[int, int]]]:
    """Matrice de payoff aleatoare."""
    return [
        [(random.randint(-5, 10), random.randint(-5, 10)) for _ in range(cols)]
        for _ in range(rows)
    ]


def _generate_matrix_with_nash() -> Tuple[List[List[Tuple[int, int]]], int, int]:
    """Matrice cu echilibru Nash garantat (jocuri clasice cu zgomot)."""
    classic_games = [
        [[(3, 3), (0, 5)], [(5, 0), (1, 1)]],  # Prisoner's Dilemma
        [[(3, 2), (0, 0)], [(0, 0), (2, 3)]],  # Battle of Sexes
        [[(2, 2), (0, 0)], [(0, 0), (1, 1)]],  # Coordination
        [[(1, 1), (0, 0)], [(0, 0), (1, 1)]],  # Pure coordination
    ]
    
    matrix = random.choice(classic_games)
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            p1, p2 = matrix[i][j]
            matrix[i][j] = (p1 + random.randint(-1, 1), p2 + random.randint(-1, 1))
    
    return matrix, len(matrix), len(matrix[0])


def genereaza_intrebare_nash(answer_type: str = "multiple", difficulty: int = 2) -> Dict[str, Any]:
    """Genereaza intrebare Nash Equilibrium pentru joc in forma normala."""

    if difficulty == 1:
        rows, cols = 2, 2
    elif difficulty == 2:
        rows, cols = random.choice([(2, 2), (2, 3), (3, 2)])
    else:  # Hard
        rows, cols = 3, 3

        # 2. Generăm matricea
        # La Easy/Medium preferăm jocuri cu echilibru garantat pentru a fi mai clar
    chance_for_classic = 0.8 if difficulty == 1 else 0.5

    if random.random() < chance_for_classic and rows == 2 and cols == 2:
        matrix, rows, cols = _generate_matrix_with_nash()
    else:
        matrix = _generate_random_matrix(rows, cols)
        # Pentru Hard, putem crește plaja valorilor
        if difficulty == 3:
            matrix = [[(random.randint(-10, 20), random.randint(-10, 20)) for _ in range(cols)] for _ in range(rows)]
    
    nash_list = find_pure_nash(matrix)
    
    row_strategies = ["Sus", "Jos", "Mijloc"][:rows]
    col_strategies = ["Stânga", "Dreapta", "Centru"][:cols]
    
    if len(nash_list) == 0:
        correct_answer = "Nu există echilibru Nash pur"
        has_nash = False
    elif len(nash_list) == 1:
        r, c = nash_list[0]
        correct_answer = f"({row_strategies[r]}, {col_strategies[c]})"
        has_nash = True
    else:
        equilibria_str = ", ".join(
            f"({row_strategies[r]}, {col_strategies[c]})" for r, c in nash_list
        )
        correct_answer = equilibria_str
        has_nash = True
    
    if has_nash:
        reference_solution = (
            f"Echilibrul Nash pur se gaseste verificand fiecare celula: "
            f"o celula (i, j) este echilibru Nash daca payoff-ul jucatorului 1 "
            f"este cel mai mare pe coloana j SI payoff-ul jucatorului 2 este "
            f"cel mai mare pe randul i. "
            f"Pentru aceasta matrice, echilibrul Nash pur este: {correct_answer}."
        )
    else:
        reference_solution = (
            f"Pentru a gasi echilibrul Nash pur, verificam fiecare celula: "
            f"trebuie ca payoff-ul fiecarui jucator sa fie cel mai bun raspuns "
            f"la strategia celuilalt. In aceasta matrice, nicio celula nu "
            f"satisface ambele conditii, deci nu exista echilibru Nash pur."
        )
    
    prompt = (
        f"Pentru jocul cu doi jucatori dat in forma normala (matricea atasata), "
        f"unde Jucatorul 1 alege randul iar Jucatorul 2 alege coloana, "
        f"exista echilibru Nash pur? Daca da, care este acesta?"
    )
    
    matrix_data = {
        "rows": rows,
        "cols": cols,
        "row_strategies": row_strategies,
        "col_strategies": col_strategies,
        "payoffs": matrix
    }
    
    if answer_type == "text":
        return {
            "title": "Echilibru Nash - Joc în formă normală",
            "prompt": prompt,
            "question_type": "GAME_MATRIX",
            "difficulty": difficulty,
            "problem_instance": {"matrix": matrix_data},
            "correct_answer": {
                "reference_text": reference_solution,
                "nash_equilibria": nash_list,
                "has_nash": has_nash,
                "answer_text": correct_answer,
                "keywords": ["nash", "echilibru", "best response", "strategie"]
            },
            "reference_solution": reference_solution,
            "chapter_name": "Teoria Jocurilor",
            "answer_type": "text",
            "options": []
        }
    
    # Multiple choice
    options = [correct_answer]
    used_options = {correct_answer}
    
    possible_cells = [
        f"({row_strategies[r]}, {col_strategies[c]})"
        for r in range(rows) for c in range(cols)
    ]
    
    for cell in possible_cells:
        if cell not in used_options and len(options) < 4:
            options.append(cell)
            used_options.add(cell)
    
    if "Nu există echilibru Nash pur" not in used_options and len(options) < 4:
        options.append("Nu există echilibru Nash pur")
    
    while len(options) < 4:
        r, c = random.randint(0, rows-1), random.randint(0, cols-1)
        fake = f"({row_strategies[r]}, {col_strategies[c]})"
        if fake not in used_options:
            options.append(fake)
            used_options.add(fake)
    
    random.shuffle(options)
    
    return {
        "title": "Echilibru Nash - Joc în formă normală",
        "prompt": prompt,
        "question_type": "GAME_MATRIX",
        "difficulty": difficulty,
        "problem_instance": {"matrix": matrix_data},
        "correct_answer": {
            "answer": correct_answer,
            "nash_equilibria": nash_list,
            "has_nash": has_nash
        },
        "reference_solution": reference_solution,
        "chapter_name": "Teoria Jocurilor",
        "answer_type": "multiple",
        "options": options
    }

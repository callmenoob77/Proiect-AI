import random
import json

PROBLEM_KNOWLEDGE = [

    {
        "problem_name": "Generalized Hanoi Towers",
        "correct_strategy": "DFS (Depth-First Search)",
        "example_instances": [
            "3 discuri si 4 tije",
            "5 discuri si 5 tije",
            "4 discuri si 4 tije"
        ],
        "chapter_name": "Strategii algoritmice",
        "enum_type": "HANOI"
    },

    {
        "problem_name": "Sliding puzzle problem",
        "correct_strategy": "A* Search",
        "example_instances": [
            "puzzle 3x3 cu o piesa lipsa",
            "puzzle 4x4 pornind de la o stare amestecata"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "SLIDING_PUZZLE"
    },

    {
        "problem_name": "X&O",
        "correct_strategy": "Backtracking (DFS in spatiul starilor)",
        "example_instances": [
            "tabla 3x3 clasica",
            "varianta 4x4 pentru un AI mai complex"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "X_O"
    },

    {
        "problem_name": "River crossing problem",
        "correct_strategy": "BFS (Breadth-First Search)",
        "example_instances": [
            "problema taranului, lupului, caprei si verzei",
            "transportarea a 3 persoane peste un rau cu o barca de 2 locuri"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "RIVER_CROSSING"
    },

    {
        "problem_name": "Water jug problem",
        "correct_strategy": "Uniform Cost Search (sau BFS)",
        "example_instances": [
            "doua vase de 3L si 5L pentru obtinerea a 4L de apa",
            "doua vase de 4L si 9L pentru obtinerea a 6L"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "WATER_JUG"
    },

    {
        "problem_name": "n-queens",
        "correct_strategy": "Backtracking",
        "example_instances": [
            "tabla de 4x4",
            "tabla de 8x8",
            "tabla de 6x6"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "N_QUEENS"
    },

    {
        "problem_name": "Graph coloring",
        "correct_strategy": "Backtracking (CSP)",
        "example_instances": [
            "colorarea hartii Australiei cu 3 culori",
            "colorarea unui graf cu 5 noduri si 4 muchii"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "GRAPH_COLORING"
    },

    {
        "problem_name": "Knight's tour",
        "correct_strategy": "DFS sau Hillclimbing",
        "example_instances": [
            "tabla de 5x5 pornind din colt",
            "tur complet pe o tabla de 6x6"
        ],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "KNIGHT_TOUR"
    }

]



MASTER_STRATEGIES = [
    "Backtracking", "Divide et Impera", "CSP (Constraint Satisfaction)",
    "Backtracking cu euristica Warnsdorff", "Programare Dinamică", "Algoritm Greedy",
    "Rețele Neuronale", "Algoritmi Genetici"
]


def genereaza_intrebare_strategie():
    problem_data = random.choice(PROBLEM_KNOWLEDGE)

    problem = problem_data["problem_name"]
    correct_answer = problem_data["correct_strategy"]
    chapter_name = problem_data["chapter_name"]

    enum_type_for_db = problem_data["enum_type"]

    instance = random.choice(problem_data["example_instances"])
    possible_distractors = [s for s in MASTER_STRATEGIES if s != correct_answer]
    distractors = random.sample(possible_distractors, 3)

    options = [correct_answer] + distractors
    random.shuffle(options)
    options_string = ", ".join(options)

    prompt_text = (
        f"Pentru problema {problem} (instanța: {instance}), "
        f"care este cea mai potrivită strategie de rezolvare, "
        f"dintre cele menţionate: {options_string}?"
    )

    title_text = f"Selectare strategie: {problem.replace('_', ' ').title()}"

    return {
        "title": title_text,
        "prompt": prompt_text,
        "question_type": enum_type_for_db,
        "difficulty": 2,
        "problem_instance": {"problem": problem, "instance": instance},
        "correct_answer": {"answer": correct_answer},
        "reference_solution": f"Răspunsul corect este '{correct_answer}'. Problema {problem} este un exemplu clasic care se rezolvă optim folosind {correct_answer}.",
        "chapter_name": chapter_name
    }
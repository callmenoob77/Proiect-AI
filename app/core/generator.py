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

TEXT_KNOWLEDGE = [
    {
        "strategy_name": "A* Search",
        "chapter_name": "Algoritmi de căutare și CSP",
        "keywords": ["euristica", "cost", "optim", "cale", "g(n)", "h(n)", "f(n)"],
        "description": "Algoritmul A* este un algoritm de căutare informată care utilizează o funcție de evaluare f(n) = g(n) + h(n), unde g(n) este costul de la start la nodul curent și h(n) este euristica (estimarea costului până la destinație)."
    },
    {
        "strategy_name": "Backtracking",
        "chapter_name": "Algoritmi de căutare și CSP",
        "keywords": ["recursiv", "solutie", "stare", "valid", "cautare", "adancime", "backtrack"],
        "description": "Backtracking este o tehnică de rezolvare sistematică care explorează recursiv spațiul soluțiilor, revenind (backtracking) când întâlnește o stare invalidă."
    },
    {
        "strategy_name": "CSP (Constraint Satisfaction)",
        "chapter_name": "Algoritmi de căutare și CSP",
        "keywords": ["variabile", "domenii", "constrangeri", "atribuire", "consistent"],
        "description": "CSP se ocupă cu probleme definite prin variabile, domenii de valori și constrângeri între variabile, căutând atribuiri consistente."
    },
    {
        "strategy_name": "Programare Dinamică",
        "chapter_name": "Strategii algoritmice",
        "keywords": ["subprobleme", "optim", "suprapunere", "memoizare", "tabel"],
        "description": "Programarea dinamică rezolvă probleme prin descompunere în subprobleme suprapuse, memorând soluțiile pentru a evita recalcularea."
    }
]

MASTER_STRATEGIES = [
    "Backtracking", "Divide et Impera", "CSP (Constraint Satisfaction)",
    "Backtracking cu euristica Warnsdorff", "Programare Dinamică", "Algoritm Greedy",
    "Rețele Neuronale", "Algoritmi Genetici", "A* Search", "BFS (Breadth-First Search)",
    "DFS (Depth-First Search)", "Uniform Cost Search (sau BFS)", "DFS sau Hillclimbing"
]


def genereaza_intrebare_strategie(answer_type="multiple"):
    """
    Generează o întrebare despre strategii de rezolvare.

    Args:
        answer_type: "multiple" pentru alegere multiplă, "text" pentru răspuns liber
    """
    problem_data = random.choice(PROBLEM_KNOWLEDGE)

    problem = problem_data["problem_name"]
    correct_answer = problem_data["correct_strategy"]
    chapter_name = problem_data["chapter_name"]
    enum_type_for_db = problem_data["enum_type"]
    instance = random.choice(problem_data["example_instances"])

    if answer_type == "multiple":
        # Generare întrebare cu opțiuni multiple
        possible_distractors = [s for s in MASTER_STRATEGIES if s != correct_answer]
        distractors = random.sample(possible_distractors, min(3, len(possible_distractors)))

        options = [correct_answer] + distractors
        random.shuffle(options)
        options_string = ", ".join(options)

        prompt_text = (
            f"Pentru problema {problem} (instanța: {instance}), "
            f"care este cea mai potrivită strategie de rezolvare, "
            f"dintre cele menționate: {options_string}?"
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
            "chapter_name": chapter_name,
            "answer_type": "multiple",
            "options": options
        }

    elif answer_type == "text":
        # Generare întrebare cu răspuns text (descriere strategie)
        strategy_data = random.choice(TEXT_KNOWLEDGE)
        strategy_name = strategy_data["strategy_name"]
        keywords = strategy_data["keywords"]
        description = strategy_data["description"]
        chapter_name = strategy_data["chapter_name"]

        prompt_text = f"Descrie pe scurt strategia '{strategy_name}' și menționează principalele caracteristici ale acesteia."
        title_text = f"Descriere strategie: {strategy_name}"

        return {
            "title": title_text,
            "prompt": prompt_text,
            "question_type": "A_STAR_DESCRIPTION",
            "difficulty": 3,
            "problem_instance": {"strategy": strategy_name},
            "correct_answer": {"keywords": keywords},
            "reference_solution": description,
            "chapter_name": chapter_name,
            "answer_type": "text"
        }

    else:
        raise ValueError(f"Tip de răspuns necunoscut: {answer_type}")
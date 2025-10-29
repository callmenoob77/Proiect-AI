import random
import json

PROBLEM_KNOWLEDGE = [
    {
        "problem_name": "n-queens",
        "correct_strategy": "Backtracking",
        "example_instances": ["o tablă de 4x4", "găsirea unei soluții pe o tablă de 8x8", "o tablă de 6x6"],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "N_QUEENS"
    },
    {
        "problem_name": "generalised Hanoi",
        "correct_strategy": "Divide et Impera",
        "example_instances": ["3 discuri și 4 tije", "5 discuri și 5 tije", "4 discuri și 4 tije"],
        "chapter_name": "Strategii algoritmice",
        "enum_type": "HANOI"
    },
    {
        "problem_name": "graph coloring",
        "correct_strategy": "CSP (Constraint Satisfaction)",
        "example_instances": ["colorarea hărții Australiei cu 3 culori", "colorarea unui graf cu 5 noduri și 4 muchii"],
        "chapter_name": "Algoritmi de căutare și CSP",
        "enum_type": "GRAPH_COLORING"
    },
    {
        "problem_name": "knight's tour",
        "correct_strategy": "Backtracking cu euristica Warnsdorff",
        "example_instances": ["o tablă de 5x5 pornind din colț", "găsirea unui tur complet pe o tablă de 6x6"],
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
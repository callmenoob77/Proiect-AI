import random
import json

try:
    from .csp_generator import genereaza_problema_csp
except ImportError:
    genereaza_problema_csp = None
    print("ATENTIE: Nu am gasit fisierul csp_generator.py!")

try:
    from .minimax_generator import genereaza_intrebare_minimax
except ImportError:
    genereaza_intrebare_minimax = None
    print("ATENTIE:Nu am gasit fisierul minimax_generator.py!")

try:
    from .nash_generator import genereaza_intrebare_nash
except ImportError:
    genereaza_intrebare_nash = None
    print("ATENTIE: Nu am gasit fisierul nash_generator.py!")



PROBLEM_KNOWLEDGE = [
    {"problem_name": "Generalized Hanoi Towers", "base_strategy": "DFS (Depth-First Search)", "chapter_name": "Strategii algoritmice", "enum_type": "HANOI"},
    {"problem_name": "Sliding Puzzle Problem", "base_strategy": "A* Search", "chapter_name": "Algoritmi de cautare si CSP", "enum_type": "SLIDING_PUZZLE"},
    {"problem_name": "River Crossing Problem", "base_strategy": "BFS (Breadth-First Search)", "chapter_name": "Algoritmi de cautare si CSP", "enum_type": "RIVER_CROSSING"},
    {"problem_name": "Water Jug Problem", "base_strategy": "Uniform Cost Search (sau BFS)", "chapter_name": "Algoritmi de cautare si CSP", "enum_type": "WATER_JUG"},
    {"problem_name": "N-Queens", "base_strategy": "Backtracking", "chapter_name": "Algoritmi de cautare si CSP", "enum_type": "N_QUEENS"},
    {"problem_name": "Graph Coloring", "base_strategy": "Backtracking (CSP)", "chapter_name": "Algoritmi de cautare si CSP", "enum_type": "GRAPH_COLORING"},
    {"problem_name": "Knight's Tour", "base_strategy": "DFS sau Hillclimbing", "chapter_name": "Algoritmi de cautare si CSP", "enum_type": "KNIGHT_TOUR"}
]

TEXT_KNOWLEDGE = [
    {
        "strategy_name": "A* Search",
        "chapter_name": "Algoritmi de cautare si CSP",
        "keywords": ["euristica", "cost", "optim", "cale", "g(n)", "h(n)", "f(n)"],
        "description": "Algoritmul A* este un algoritm de cautare informata care utilizeaza o functie de evaluare f(n) = g(n) + h(n), unde g(n) este costul de la start la nodul curent si h(n) este euristica (estimarea costului pana la destinatie)."
    },
    {
        "strategy_name": "Backtracking",
        "chapter_name": "Algoritmi de cautare si CSP",
        "keywords": ["recursiv", "solutie", "stare", "valid", "cautare", "adancime", "backtrack"],
        "description": "Backtracking este o tehnica de rezolvare sistematica care exploreaza recursiv spatiul solutiilor, revenind (backtracking) cand intalneste o stare invalida."
    },
    {
        "strategy_name": "CSP (Constraint Satisfaction)",
        "chapter_name": "Algoritmi de cautare si CSP",
        "keywords": ["variabile", "domenii", "constrangeri", "atribuire", "consistent"],
        "description": "CSP se ocupa cu probleme definite prin variabile, domenii de valori si constrangeri intre variabile, cautand atribuiri consistente."
    },
    {
        "strategy_name": "Programare Dinamica",
        "chapter_name": "Strategii algoritmice",
        "keywords": ["subprobleme", "optim", "suprapunere", "memoizare", "tabel"],
        "description": "Programarea dinamica rezolva probleme prin descompunere in subprobleme suprapuse, memorand solutiile pentru a evita recalcularea."
    }
]

MASTER_STRATEGIES = [
    "Backtracking", "Divide et Impera", "CSP (Constraint Satisfaction)",
    "Backtracking cu euristica Warnsdorff", "Programare Dinamica", "Algoritm Greedy",
    "Retele Neuronale", "Algoritmi Genetici", "A* Search", "BFS (Breadth-First Search)",
    "DFS (Depth-First Search)", "Uniform Cost Search (sau BFS)", "DFS sau Hillclimbing",
    "Uniform Cost Search"
]

PROMPT_INTROS = [
    "Pentru problema {problem} (instanta: {instance}),",
    "Analizand problema {problem} cu instanta {instance},",
    "Dat fiind scenariul {problem} ({instance}),",
    "Avand urmatoarea problema: {problem}, cu specificatia: {instance},"
]

PROMPT_QUESTIONS = [
    "care este cea mai potrivita strategie de rezolvare, dintre cele mentionate: {options_string}?",
    "ce strategie ai alege din lista de mai jos pentru a o rezolva eficient: {options_string}?",
    "selecteaza algoritmul optim din: {options_string}.",
    "identifica strategia de baza pentru aceasta problema din optiunile: {options_string}."
]

def genereaza_intrebare_strategie(answer_type="multiple", chapter_filter=None, difficulty=2):
    
    if answer_type == "multiple":
        
        # Selectie uniforma intre tipurile disponibile
        available_types = ["strategy"]  # mereu disponibil
        
        # Filtrare în funcție de capitol
        if chapter_filter:
            if chapter_filter == "Teoria Jocurilor":
                # Doar Nash pentru Teoria Jocurilor
                if genereaza_intrebare_nash:
                    return genereaza_intrebare_nash(answer_type="multiple", difficulty=difficulty)
            elif chapter_filter == "Algoritmi de cautare si CSP":
                # CSP și Minimax pentru acest capitol
                if genereaza_problema_csp:
                    available_types.append("csp")
                if genereaza_intrebare_minimax:
                    available_types.append("minimax")
            # Pentru "Strategii algoritmice" rămâne doar "strategy"
        else:
            # Fără filtru - toate tipurile
            if genereaza_problema_csp:
                available_types.append("csp")
            if genereaza_intrebare_minimax:
                available_types.append("minimax")
            if genereaza_intrebare_nash:
                available_types.append("nash")
        
        selected_type = random.choice(available_types)

        if selected_type == "csp":
            return genereaza_problema_csp(difficulty=difficulty)
        elif selected_type == "minimax":
            return genereaza_intrebare_minimax(answer_type="multiple", difficulty=difficulty)
        elif selected_type == "nash":
            return genereaza_intrebare_nash(answer_type="multiple", difficulty=difficulty)
             
        # Pentru strategy, filtrăm problemele după capitol dacă e necesar
        problems = PROBLEM_KNOWLEDGE
        if chapter_filter and chapter_filter != "Teoria Jocurilor":
            problems = [p for p in PROBLEM_KNOWLEDGE if p["chapter_name"] == chapter_filter]
            if not problems:
                problems = PROBLEM_KNOWLEDGE  # fallback dacă nu găsim probleme
        
        problem_data = random.choice(problems)
        problem_name = problem_data["problem_name"]
        enum_type = problem_data["enum_type"]
        chapter_name = problem_data["chapter_name"]
        
        instance = ""
        correct_answer = problem_data["base_strategy"]
        
        if enum_type == "WATER_JUG":
            vas1 = random.randint(3, 5)
            vas2 = random.randint(vas1 + 1, 10)
            target = random.randint(1, vas2 - 1)
            
            if random.choice([True, False]):
                instance = f"doua vase de {vas1}L si {vas2}L pentru a obtine {target}L (cost 1 per actiune)"
                correct_answer = "Uniform Cost Search (sau BFS)"
            else:
                cost1 = random.randint(2, 4)
                cost2 = random.randint(1, cost1 - 1)
                instance = f"doua vase de {vas1}L (cost umplere {cost1}p) si {vas2}L (cost umplere {cost2}p) pentru a obtine {target}L"
                correct_answer = "Uniform Cost Search" 

        elif enum_type == "KNIGHT_TOUR":
            if difficulty == 1:
                instance = "tabla de 5x5 (instanta mica)"
                correct_answer = "DFS sau Hillclimbing"
            else:
                instance = f"tabla de {8 if difficulty == 2 else 12}x{8 if difficulty == 2 else 12}"
                correct_answer = "Backtracking cu euristica Warnsdorff"

        elif enum_type == "N_QUEENS":
            if difficulty == 1:
                size = 4  # Cea mai simplă tablă
            elif difficulty == 2:
                size = random.randint(5, 8)
            else:
                size = random.randint(10, 14)  # Hard
            instance = f"tabla de {size}x{size}"
            correct_answer = "Backtracking"

        elif enum_type == "HANOI":
            # Dificultatea crește numărul de discuri
            if difficulty == 1:
                discuri = 3
                tije = 3
            elif difficulty == 2:
                discuri = random.randint(4, 5)
                tije = 3
            else:
                discuri = random.randint(6, 8)
                tije = random.randint(3, 4)

            instance = f"{discuri} discuri si {tije} tije"
            correct_answer = "DFS (Depth-First Search)"

        elif enum_type == "GRAPH_COLORING":
            # Dificultatea crește numărul de noduri și scade numărul de culori (face problema mai grea)
            if difficulty == 1:
                noduri = 4
                culori = 4
            elif difficulty == 2:
                noduri = random.randint(5, 7)
                culori = 3
            else:
                noduri = random.randint(8, 12)
                culori = 3

            instance = f"colorarea unui graf cu {noduri} noduri folosind {culori} culori"
            correct_answer = "Backtracking (CSP)"

        elif enum_type == "SLIDING_PUZZLE":
            # Dificultatea determină mărimea grilei
            if difficulty == 1:
                size = "2x2 (format redus)"
            elif difficulty == 2:
                size = "3x3"
            else:
                size = "4x4"

            instance = f"puzzle {size} cu o piesa lipsa"
            correct_answer = "A* Search"

        else:
            instance = "o instanta generica"
            correct_answer = problem_data["base_strategy"]
        
        exclude_list = [correct_answer]
        if "Backtracking" in correct_answer and correct_answer != "Backtracking":
            exclude_list.append("Backtracking")
        if correct_answer == "Uniform Cost Search":
            exclude_list.append("Uniform Cost Search (sau BFS)")
        elif correct_answer == "Uniform Cost Search (sau BFS)":
            exclude_list.append("Uniform Cost Search")
        if correct_answer == "Backtracking cu euristica Warnsdorff":
            exclude_list.append("DFS sau Hillclimbing")
        elif correct_answer == "DFS sau Hillclimbing":
             exclude_list.append("Backtracking cu euristica Warnsdorff")

        possible_distractors = [s for s in MASTER_STRATEGIES if s not in exclude_list]
        num_distractors = min(3, len(possible_distractors))
        if num_distractors < 3:
            additional_options = [s for s in MASTER_STRATEGIES if s != correct_answer]
            distractors = random.sample(additional_options, 3)
        else:
            distractors = random.sample(possible_distractors, 3)

        options = [correct_answer] + distractors
        options = list(set(options)) 
        random.shuffle(options)
        
        while len(options) < 4:
            extra = random.choice(MASTER_STRATEGIES)
            if extra not in options:
                options.append(extra)

        intro = random.choice(PROMPT_INTROS).format(problem=problem_name, instance=instance)
        question_part = random.choice(PROMPT_QUESTIONS)
        prompt_text = f"{intro} {question_part}"
        title_text = f"Selectare strategie: {problem_name.replace('_', ' ').title()}"

        return {
            "title": title_text,
            "prompt": prompt_text,
            "question_type": enum_type,
            "difficulty": difficulty,
            "problem_instance": {"problem": problem_name, "instance": instance},
            "correct_answer": {"answer": correct_answer},
            "reference_solution": f"Raspunsul corect este {correct_answer}. Pentru instanta {instance}, aceasta este strategia generala/optima.",
            "chapter_name": chapter_name,
            "answer_type": "multiple",
            "options": options
        }


    elif answer_type == "text":

        # Selectie uniforma intre tipurile disponibile
        available_types = ["strategy"]  # mereu disponibil
        
        # Filtrare în funcție de capitol
        if chapter_filter:
            if chapter_filter == "Teoria Jocurilor":
                # Doar Nash pentru Teoria Jocurilor
                if genereaza_intrebare_nash:
                    return genereaza_intrebare_nash(answer_type="text", difficulty=difficulty)
            elif chapter_filter == "Algoritmi de cautare si CSP":
                # CSP și Minimax pentru acest capitol
                if genereaza_intrebare_minimax:
                    available_types.append("minimax")
                if genereaza_problema_csp:
                    available_types.append("csp")
            # Pentru "Strategii algoritmice" rămâne doar "strategy"
        else:
            # Fără filtru - toate tipurile
            if genereaza_intrebare_minimax:
                available_types.append("minimax")
            if genereaza_intrebare_nash:
                available_types.append("nash")
            if genereaza_problema_csp:
                available_types.append("csp")
        
        selected_type = random.choice(available_types)

        if selected_type == "minimax":
            return genereaza_intrebare_minimax(answer_type="text", difficulty=difficulty)
        elif selected_type == "nash":
            return genereaza_intrebare_nash(answer_type="text", difficulty=difficulty)
        elif selected_type == "csp":
            # Atenție aici: genereaza_problema_csp returnează de obicei un obiect complet
            csp_question = genereaza_problema_csp(difficulty=difficulty)
            csp_question["answer_type"] = "text"
            return csp_question
        # else: fallback la strategy (continua mai jos)

        # Pentru strategy, filtrăm după capitol dacă e necesar
        strategies = TEXT_KNOWLEDGE
        if chapter_filter and chapter_filter != "Teoria Jocurilor":
            strategies = [s for s in TEXT_KNOWLEDGE if s["chapter_name"] == chapter_filter]
            if not strategies:
                strategies = TEXT_KNOWLEDGE  # fallback
        
        strategy_data = random.choice(strategies)
        strategy_name = strategy_data["strategy_name"]
        keywords = strategy_data["keywords"]
        description = strategy_data["description"]
        chapter_name = strategy_data["chapter_name"]

        prompt_text = (

            f"Descrie pe scurt strategia {strategy_name} si mentioneaza "
            f"principalele caracteristici ale acesteia."

        )
        title_text = f"Descriere strategie: {strategy_name}"

        return {
            "title": title_text,
            "prompt": prompt_text,
            "question_type": "A_STAR_DESCRIPTION",
            "difficulty": difficulty,
            "problem_instance": {"strategy": strategy_name},
            "correct_answer": {"keywords": keywords, "reference_text": description},
            "reference_solution": description,
            "chapter_name": chapter_name,
            "answer_type": "text"
        }


    else:
        raise ValueError(f"Tip de raspuns necunoscut: {answer_type}")
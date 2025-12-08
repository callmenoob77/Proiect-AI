import random
try:
    from .csp_solver import CSP 
except ImportError:
    CSP = None

def genereaza_problema_csp():
    subtype = random.choice(["MRV", "FC", "AC3"])
    
    problem_data = {
        "problem_category": "CSP",
        "subtype": subtype,
        "variables": [],
        "domains": {},
        "constraints": [],
        "assignment": {}, 
        "target": None    
    }
    
    prompt = ""
    correct_answer_str = "Eroare Generare"
    correct_raw = None
    
    # Lista globala de valori posibile (pentru generarea de distractori la final)
    all_possible_values = set()

    # =========================================================================
    # 1. LOGICA DE GENERARE AVANSATA
    # =========================================================================

    # -------------------------------------------------------------------------
    # A. MRV (Minimum Remaining Values) - Varietate Maxima
    # -------------------------------------------------------------------------
    if subtype == "MRV":
        # Pool variabil pentru nume
        if random.random() < 0.33:
            vars_pool = ["X", "Y", "Z", "W"]
        elif random.random() < 0.66:
            vars_pool = ["Tara_A", "Tara_B", "Tara_C", "Tara_D"]
        else:
            vars_pool = ["C1", "C2", "C3", "C4"] # Sudoku style
            
        problem_data["variables"] = random.sample(vars_pool, 3)
        
        # Generam marimi intre 2 si 6 (variat)
        sizes = [random.randint(1, 6) for _ in range(3)]
        
        # Asiguram un minim unic
        min_val = min(sizes)
        while sizes.count(min_val) > 1:
            sizes = [random.randint(1, 6) for _ in range(3)]
            sizes[random.randint(0, 2)] = 1 # Fortam un domeniu mic
            min_val = 1
            
        for i, var in enumerate(problem_data["variables"]):
            # Generam valori dummy doar ca sa populam JSON-ul corect
            problem_data["domains"][var] = [k for k in range(sizes[i])] 

        vars_str = ", ".join(problem_data["variables"])
        doms_str = ", ".join([f"|D({v})|={sizes[i]}" for i, v in enumerate(problem_data["variables"])])
        
        prompt = (
            f"Analizam un pas din algoritmul CSP pentru variabilele: {vars_str}.\n"
            f"Marimile domeniilor curente sunt: {doms_str}.\n"
            f"Conform euristicii MRV (Minimum Remaining Values), ce variabila va fi selectata?"
        )

    # -------------------------------------------------------------------------
    # B. FC (Forward Checking) - Scenarii Bogate
    # -------------------------------------------------------------------------
    elif subtype == "FC":
        scenario = random.choice(["harta", "orar", "sudoku"])
        var1, var2 = "", ""
        vals_pool = []
        intro = ""

        if scenario == "harta":
            v1_name, v2_name = random.sample(["Nord", "Sud", "Est", "Vest", "A", "B", "C"], 2)
            var1, var2 = f"Regiunea_{v1_name}", f"Regiunea_{v2_name}"
            vals_pool = ["Rosu", "Verde", "Albastru", "Galben", "Mov", "Gri", "Indigo"]
            intro = f"Regiunile {var1} si {var2} sunt vecine pe o harta (nu pot avea aceeasi culoare)."

        elif scenario == "orar":
            s1, s2 = random.sample(["Mate", "Info", "Fizica", "Chimie", "Bio", "Istorie"], 2)
            var1, var2 = f"Curs_{s1}", f"Curs_{s2}"
            vals_pool = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
            intro = f"Cursurile de {s1} si {s2} sunt tinute de acelasi profesor (nu se pot suprapune)."

        else: # Sudoku
            c1, c2 = random.sample(["A1", "A2", "B1", "B2", "C1", "C2", "X9", "Y9"], 2)
            var1, var2 = f"Celula_{c1}", f"Celula_{c2}"
            vals_pool = [str(i) for i in range(1, 10)]
            intro = f"{var1} si {var2} sunt doua casute de Sudoku pe aceeasi linie (trebuie sa aiba valori diferite)."

        problem_data["variables"] = [var1, var2]
        
        # Alegem un domeniu comun de dimensiune variabila (3-6)
        domain_size = random.randint(3, 6)
        common_domain = random.sample(vals_pool, min(len(vals_pool), domain_size))
        try: common_domain.sort()
        except: pass

        problem_data["domains"][var1] = list(common_domain)
        problem_data["domains"][var2] = list(common_domain)
        problem_data["constraints"].append({"var1": var1, "var2": var2, "op": "!="})
        
        # Asignam o valoare
        chosen = random.choice(common_domain)
        problem_data["assignment"] = {var1: chosen}
        problem_data["target"] = var2
        
        # Populam lista globala pt distractori
        for v in common_domain: all_possible_values.add(v)

        dom_str = "{" + ", ".join(map(str, common_domain)) + "}"
        prompt = (
            f"{intro}\n"
            f"Domeniile initiale sunt: D({var1}) = D({var2}) = {dom_str}.\n"
            f"Algoritmul asigneaza {var1} = {chosen}.\n"
            f"Ce valori raman in domeniul lui {var2} dupa aplicarea Forward Checking?"
        )

    # -------------------------------------------------------------------------
    # C. AC-3 (Arc Consistency) - CONFLICT FORCED + SCENARII NON-NUMERICE
    # -------------------------------------------------------------------------
    elif subtype == "AC3":
        # 50% sanse Numere, 50% sanse Harta/Sudoku
        if random.random() < 0.5:
            # --- NUMERIC (Conflict Forcat) ---
            problem_data["variables"] = ["X", "Y"]
            
            # Generam domenii de marime variabila (3-6)
            size_x = random.randint(3, 6)
            size_y = random.randint(3, 6)
            
            # Alegem intervale care se suprapun partial ca sa fie interesant
            start = random.randint(1, 30)
            
            op = random.choice(["<", ">"])
            
            # Generam valori astfel incat sa existe "victime"
            # Ex: X < Y. Daca X are numere mari si Y doar numere mici, se sterg valori din X.
            base_vals = range(start, start + 15)
            dom_x = sorted(random.sample(base_vals, size_x))
            dom_y = sorted(random.sample(base_vals, size_y))
            
            problem_data["domains"]["X"] = dom_x
            problem_data["domains"]["Y"] = dom_y
            problem_data["constraints"].append({"var1": "X", "var2": "Y", "op": op})
            problem_data["target"] = "X"
            
            # Populam lista globala
            for v in dom_x + dom_y: all_possible_values.add(v)

            d1_str = ", ".join(map(str, dom_x))
            d2_str = ", ".join(map(str, dom_y))
            prompt = (
                f"Avem variabilele X si Y cu domeniile:\n"
                f"D(X) = {{{d1_str}}}\n"
                f"D(Y) = {{{d2_str}}}\n"
                f"Exista constrangerea de arc: X {op} Y.\n"
                f"Ce valori raman in domeniul lui X dupa aplicarea algoritmului AC-3?"
            )
            
        else:
            # --- HARTA / SUDOKU PE AC-3 (Cu domeniu mic forcat) ---
            # AC-3 e interesant doar daca un domeniu e deja redus (singleton)
            is_map = random.choice([True, False])
            
            if is_map:
                v1, v2 = "Tara_A", "Tara_B"
                pool = ["Rosu", "Verde", "Albastru", "Galben"]
                intro = "Avem doua tari vecine, A si B."
            else:
                v1, v2 = "C1", "C2"
                pool = ["1", "2", "3", "4", "5"]
                intro = "Avem doua casute Sudoku vecine."
                
            problem_data["variables"] = [v1, v2]
            
            # Generam un domeniu mare pentru tinta (3-5 elemente)
            dom_target = random.sample(pool, random.randint(3, len(pool)))
            # Generam un domeniu MIC pentru vecin (1 singur element care e si in tinta)
            # Astfel, AC-3 va fi obligat sa stearga acel element din tinta
            val_conflict = random.choice(dom_target)
            dom_neighbor = [val_conflict] 
            
            try: dom_target.sort()
            except: pass

            problem_data["domains"][v1] = dom_target
            problem_data["domains"][v2] = dom_neighbor
            problem_data["constraints"].append({"var1": v1, "var2": v2, "op": "!="})
            problem_data["target"] = v1
            
            # Populam lista globala
            for v in dom_target: all_possible_values.add(v)

            d1_str = "{" + ", ".join(map(str, dom_target)) + "}"
            d2_str = "{" + str(val_conflict) + "}"
            prompt = (
                f"{intro}\n"
                f"Domeniile curente sunt:\n"
                f"D({v1}) = {d1_str}\n"
                f"D({v2}) = {d2_str}\n"
                f"Aplicam algoritmul AC-3 pentru constrangerea {v1} != {v2}.\n"
                f"Ce valori raman in domeniul lui {v1}?"
            )

    # =========================================================================
    # 2. REZOLVARE (SOLVER)
    # =========================================================================
    try:
        if CSP:
            csp_solver_instance = CSP(
                problem_data["variables"],
                problem_data["domains"],
                problem_data["constraints"]
            )
            
            if subtype == "MRV":
                correct_raw = csp_solver_instance.select_variable_mrv({})
                correct_answer_str = str(correct_raw)
                
            elif subtype == "FC":
                var_assigned = list(problem_data["assignment"].keys())[0]
                val_assigned = problem_data["assignment"][var_assigned]
                csp_solver_instance.forward_check(var_assigned, val_assigned, {})
                
                target_var = problem_data["target"]
                remaining_vals = csp_solver_instance.domains[target_var]
                try: remaining_vals.sort() 
                except: pass
                
                correct_raw = remaining_vals
                correct_answer_str = "{" + ", ".join(map(str, remaining_vals)) + "}"
                
            elif subtype == "AC3":
                csp_solver_instance.ac3()
                target_var = problem_data["target"]
                remaining_vals = csp_solver_instance.domains[target_var]
                try: remaining_vals.sort()
                except: pass
                
                correct_raw = remaining_vals
                if not remaining_vals:
                     correct_answer_str = "Multimea vida"
                else:
                     correct_answer_str = "{" + ", ".join(map(str, remaining_vals)) + "}"
        else:
            correct_answer_str = "Eroare: Solver indisponibil"

    except Exception as e:
        print(f"Eroare CSP Solver: {e}")
        correct_answer_str = "Eroare Solver"

    # =========================================================================
    # 3. GENERARE OPTIUNI (SAFE FALLBACK)
    # =========================================================================
    options = [correct_answer_str]
    distractors = []

    # A. Distractori Logici (Smart)
    if subtype in ["FC", "AC3"] and isinstance(correct_raw, list):
        target_var = problem_data["target"]
        original_domain = problem_data["domains"][target_var]
        
        # 1. Domeniul complet
        try: original_domain.sort()
        except: pass
        opt_full = "{" + ", ".join(map(str, original_domain)) + "}"
        if opt_full != correct_answer_str:
            distractors.append(opt_full)

        # 2. Wrong Removal
        removed = [x for x in original_domain if x not in correct_raw]
        if removed and correct_raw:
            fake_rem = correct_raw[0]
            fake_list = [x for x in original_domain if x != fake_rem]
            try: fake_list.sort()
            except: pass
            opt_fake = "{" + ", ".join(map(str, fake_list)) + "}"
            if opt_fake != correct_answer_str:
                distractors.append(opt_fake)

    elif subtype == "MRV":
        for v in problem_data["variables"]:
            if v != str(correct_raw):
                distractors.append(v)
        distractors.append("Oricare")

    # Adaugam distractorii gasiti
    for d in distractors:
        if d not in options:
            options.append(d)
            
    # B. Distractori de Umplere (SAFE - Subseturi din valori reale)
    # Daca inca nu avem 4 optiuni, generam subseturi random din `all_possible_values`
    # dar NU inventam numere gen "27" daca ele nu sunt in problema.
    
    attempts = 0
    all_vals_list = list(all_possible_values)
    
    while len(options) < 4 and attempts < 20:
        attempts += 1
        if subtype == "MRV": 
            break # La MRV nu prea ai ce subseturi sa faci, ramanem cu ce avem
            
        if not all_vals_list: break
        
        # Generam un subset random
        k = random.randint(1, min(4, len(all_vals_list)))
        fake_subset = random.sample(all_vals_list, k)
        try: fake_subset.sort()
        except: pass
        
        fake_opt = "{" + ", ".join(map(str, fake_subset)) + "}"
        
        if fake_opt not in options:
            options.append(fake_opt)

    # Daca tot nu avem 4 (foarte rar), adaugam Multimea Vida daca nu e deja
    if len(options) < 4 and "Multimea vida" not in options:
        options.append("Multimea vida")

    random.shuffle(options)

    return {
        "title": f"CSP: Optimizare {subtype}",
        "prompt": prompt,
        "question_type": "CSP_PROBLEM",
        "problem_instance": problem_data, 
        "correct_answer": {"answer": str(correct_answer_str)},
        "reference_solution": f"Raspunsul corect: {correct_answer_str}.",
        "chapter_name": "Satisfacerea Constrangerilor (CSP)",
        "answer_type": "multiple",
        "options": options
    }
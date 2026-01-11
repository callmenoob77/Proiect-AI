QUESTION_PATTERNS = {

    "THEORY": {
        "DESCRIPTION": {
            "template": (
                "Descrie pe scurt strategia {strategy_name} "
                "si mentioneaza principalele caracteristici ale acesteia."
            ),
            "inputs": ["strategy_name"]
        },
        "CHARACTERISTICS": {
            "template": (
                "Care dintre urmatoarele afirmatii descrie cel mai bine strategia {strategy_name}?"
            ),
            "inputs": ["strategy_name"]
        },
        "USAGE": {
            "template": (
                "In ce situatii este recomandat sa folosesti {strategy_name}?"
            ),
            "inputs": ["strategy_name"]
        },
        "COMPLEXITY": {
            "template": (
                "Care este complexitatea temporala/spatiala a strategiei {strategy_name}?"
            ),
            "inputs": ["strategy_name"]
        }
    },

    "STRATEGY": {
        "GENERIC": {
            "template": (
                "Pentru problema {problem_name} (instanta: {instance}), "
                "care este cea mai potrivita strategie de rezolvare?"
            ),
            "inputs": ["problem_name", "instance"]
        }
    },

    "MINIMAX": {
        "BASIC": {
            "template": (
                "Pentru arborele de joc dat, determina valoarea din radacina "
                "folosind algoritmul MinMax cu Alpha-Beta."
            ),
            "inputs": []
        }
    },

    "CSP": {
        "FC": {
            "template": (
                "Domeniile initiale sunt: D({var1}) = D({var2}) = {domains}.\n"
                "Algoritmul asigneaza {var1} = {assigned_value}.\n"
                "Ce valori raman in domeniul lui {var2} dupa aplicarea Forward Checking?"
            ),
            "inputs": ["var1", "var2", "domains", "assigned_value"]
        },

        "MRV": {
            "template": (
                "Avem variabilele {variables} cu domeniile {domains}.\n"
                "Conform euristicii MRV, ce variabila va fi selectata?"
            ),
            "inputs": ["variables", "domains"]
        },

        "AC3": {
            "template": (
                "Pentru variabilele {var1} si {var2} cu domeniile "
                "D({var1})={domain1} si D({var2})={domain2},\n"
                "si constrangerea {var1} {constraint} {var2},\n"
                "ce valori raman in domeniul lui {var1} dupa AC-3?"
            ),
            "inputs": ["var1", "var2", "domain1", "domain2", "constraint"]
        }
    },

    "NASH": {
        "BASIC": {
            "template": (
                "Pentru jocul cu doi jucatori dat in forma normala, "
                "unde Jucatorul 1 alege randul iar Jucatorul 2 alege coloana, "
                "exista echilibru Nash pur? Daca da, care este acesta?"
            ),
            "inputs": []
        }
    }
}

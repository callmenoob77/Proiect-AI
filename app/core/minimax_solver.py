import math
from typing import Dict, Any, List, Tuple


class MinMaxSolver:
    """
    Solver pentru MinMax cu optimizarea Alpha-Beta
    Primesc arborele in format JSON si calculez:
        - valoarea din radacina arborelui
        - nr de frunze vizitate
    """

    def __init__(self, tree: Dict[str, Any]):
        """
        tree = arborele JSON generat în generator.
        Format:
          - nod intern: {"type": "MAX"/"MIN", "children": [...]}
          - frunza:     {"value": int}
        """
        self.tree = tree
        self.visited_leaves = 0 #contor pt cate frunze am evaluat efectiv

    # ---------------------------------------------------------
    # ALPHA-BETA
    # ---------------------------------------------------------
    def alphabeta(self, node: Dict[str, Any],
                  alpha: float,
                  beta: float,
                  maximizing: bool) -> int:
        """
        Alg recursiv minmax cu alpha-beta
        :param node: nodul curent din arbore
        :param alpha: cea mai buna valoare gasita ptr MAX pana acum
        :param beta: cea mai buna valoare gasita ptr MIN pana acum
        :param maximizing: True daca nodul curent e MAX, False daca e MIN
        :return: valoarea minmax a nodului curent
        """

        # Nod frunza -> returnez valoarea
        if "value" in node:
            self.visited_leaves += 1
            return node["value"]

        #pt nodurile interne, extrag copiii
        children = node.get("children", [])

        # nodul MAX
        if maximizing:
            value = -math.inf
            for child in children:
                #apel recursiv: urmatorul nivel e min
                child_val = self.alphabeta(child, alpha, beta, False)

                value = max(value, child_val) #MAX alege valoarea maxima
                alpha = max(alpha, value) #actualizez alpha

                #conditie taiere beta
                if alpha >= beta:
                    break
            return value

        #nodul MIN
        else:
            value = math.inf
            for child in children:
                #apel recursiv: urmatorul nivel e MAX
                child_val = self.alphabeta(child, alpha, beta, True)

                value = min(value, child_val) #MIN alege valoarea minima
                beta = min(beta, value) #actualizez beta

                #conditie taiere alfa
                if alpha >= beta:
                    break
            return value


    def solve(self) -> Tuple[int, int]:
        """
        Ruleaza MINMAX cu alpha beta pe arbore

        Returneaza:
            (valoare_radacina, frunze_vizitate)
        """
        #identific daca radacina e MAX sau MIN
        root_type = self.tree.get("type", "MAX")
        maximizing = (root_type == "MAX")

        #apelez algoritmul de la radacina
        value = self.alphabeta(
            self.tree,
            alpha=-math.inf, #alfa initial
            beta=math.inf, #beta initial
            maximizing=maximizing
        )
        #valoarea calculata in radacina + nr total de frunze vizitate
        return value, self.visited_leaves

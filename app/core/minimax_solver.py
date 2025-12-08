import math
from typing import Dict, Any, List, Tuple


class MinMaxSolver:
    """
    Solver pentru MinMax cu optimizarea Alpha-Beta.
    Poate fi folosit atât în generator, cât și în evaluator.
    """

    def __init__(self, tree: Dict[str, Any]):
        """
        tree = arborele JSON generat în generator.
        Format:
          - nod intern: {"type": "MAX"/"MIN", "children": [...]}
          - frunză:     {"value": int}
        """
        self.tree = tree
        self.visited_leaves = 0

    # ---------------------------------------------------------
    # ALPHA-BETA
    # ---------------------------------------------------------
    def alphabeta(self, node: Dict[str, Any],
                  alpha: float,
                  beta: float,
                  maximizing: bool) -> int:

        # Nod frunză
        if "value" in node:
            self.visited_leaves += 1
            return node["value"]

        children = node.get("children", [])

        # MAX
        if maximizing:
            value = -math.inf
            for child in children:
                child_val = self.alphabeta(child, alpha, beta, False)
                value = max(value, child_val)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Tăiere beta
            return value

        # MIN
        else:
            value = math.inf
            for child in children:
                child_val = self.alphabeta(child, alpha, beta, True)
                value = min(value, child_val)
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Tăiere alfa
            return value

    # ---------------------------------------------------------
    # API PRINCIPAL
    # ---------------------------------------------------------
    def solve(self) -> Tuple[int, int]:
        """
        Returnează:
            (valoare_radacina, frunze_vizitate)
        """
        root_type = self.tree.get("type", "MAX")
        maximizing = (root_type == "MAX")

        value = self.alphabeta(
            self.tree,
            alpha=-math.inf,
            beta=math.inf,
            maximizing=maximizing
        )

        return value, self.visited_leaves

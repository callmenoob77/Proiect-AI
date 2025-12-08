from copy import deepcopy
from collections import deque
import operator

OPS = {
    "!=": operator.ne,
    "==": operator.eq,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le
}

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = deepcopy(domains)

        # constraints: list of {var1, var2, op}
        self.constraints = constraints

        # Build neighbors map
        self.neighbors = {v: [] for v in variables}
        for c in constraints:
            self.neighbors[c["var1"]].append(c["var2"])
            self.neighbors[c["var2"]].append(c["var1"])

    def check_constraint(self, var1, val1, var2, val2):
        #Checks constraint var1 op var2"
        for c in self.constraints:
            if (c["var1"] == var1 and c["var2"] == var2) or \
               (c["var1"] == var2 and c["var2"] == var1):

                op = OPS[c["op"]]
                if c["var1"] == var1:
                    return op(val1, val2)
                else:
                    return op(val2, val1)
        return True

    # =========================================================================
    # AC-3
    # =========================================================================
    def ac3(self):
        queue = deque()
        for c in self.constraints:
            queue.append((c["var1"], c["var2"]))
            queue.append((c["var2"], c["var1"]))

        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        #Remove values from domain[xi] that have no supporting value in xj
        revised = False
        new_domain = []

        for x in self.domains[xi]:
            ok = False
            for y in self.domains[xj]:
                if self.check_constraint(xi, x, xj, y):
                    ok = True
                    break
            if ok:
                new_domain.append(x)

        if len(new_domain) != len(self.domains[xi]):
            revised = True

        self.domains[xi] = new_domain
        return revised

    # =========================================================================
    # MRV heuristic
    # =========================================================================
    def select_variable_mrv(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda v: len(self.domains[v]))

    # =========================================================================
    # Forward Checking
    # =========================================================================
    def forward_check(self, var, value, assignment):
        #Prune neighbors' domains based on assignment
        saved = deepcopy(self.domains)

        for nb in self.neighbors[var]:
            if nb not in assignment:
                new_domain = []
                for v in self.domains[nb]:
                    if self.check_constraint(var, value, nb, v):
                        new_domain.append(v)
                self.domains[nb] = new_domain

                if len(new_domain) == 0:
                    self.domains = saved
                    return False

        return True

    # =========================================================================
    # Backtracking solver (FC or plain or MRV)
    # =========================================================================
    def backtrack(self, assignment, subtype):
        # Complete solution
        if len(assignment) == len(self.variables):
            return assignment

        # Choose variable
        if subtype == "MRV":
            var = self.select_variable_mrv(assignment)
        else:
            var = next(v for v in self.variables if v not in assignment)

        for value in self.domains[var]:
            # Check consistency with assigned neighbors
            ok = True
            for nb in self.neighbors[var]:
                if nb in assignment and not self.check_constraint(var, value, nb, assignment[nb]):
                    ok = False
                    break
            if not ok:
                continue

            # Apply Forward Checking if needed
            saved_domains = deepcopy(self.domains)
            if subtype == "FC":
                if not self.forward_check(var, value, assignment):
                    self.domains = saved_domains
                    continue

            new_assignment = deepcopy(assignment)
            new_assignment[var] = value

            result = self.backtrack(new_assignment, subtype)
            if result:
                return result

            self.domains = saved_domains  # restore domains

        return None

def solve_csp_from_json(data):
    subtype = data["subtype"]     # FC, MRV, AC-3
    variables = data["variables"]
    domains = data["domains"]
    constraints = data["constraints"]
    assignment = data["assignment"]
    target = data["target"]

    csp = CSP(variables, domains, constraints)

    # Apply AC-3 preprocessing if requested
    if subtype == "AC-3":
        ok = csp.ac3()
        if not ok:
            return {"status": "inconsistent"}

    # Backtracking continues from partial assignment
    solution = csp.backtrack(assignment, subtype)

    if solution is None:
        return {"status": "no_solution"}

    if target:
        return {
            "status": "solved",
            "target": target,
            "value": solution.get(target),
            "solution": solution
        }

    return {"status": "solved", "solution": solution}

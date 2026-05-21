import subprocess
import re
import os
from pathlib import Path
from typing import Generator, Any, Dict, List, Optional, Union

# Try importing pyswip
try:
    import pyswip
    PYSWIP_AVAILABLE = True
except ImportError:
    PYSWIP_AVAILABLE = False


# ─────────────────────────────────────────────────────────────
# 🧠 PURE PYTHON PROLOG INTERPRETER (SLD Resolution)
# ─────────────────────────────────────────────────────────────

class Variable:
    """Represents a logical variable in our pure Python engine."""
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Term:
    """Represents a Prolog term (e.g. parent(john, mary))."""
    def __init__(self, op: str, *args: Any):
        self.op = op
        self.args = list(args)

    def __repr__(self) -> str:
        if not self.args:
            return self.op
        return f"{self.op}({', '.join(map(str, self.args))})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Term) and 
                self.op == other.op and 
                self.args == other.args)


class Rule:
    """Represents a Prolog rule Head :- Body."""
    def __init__(self, head: Term, body: Optional[List[Term]] = None):
        self.head = head
        self.body = body or []

    def __repr__(self) -> str:
        if not self.body:
            return f"{self.head}."
        return f"{self.head} :- {', '.join(map(str, self.body))}."


def is_variable(x: Any) -> bool:
    if isinstance(x, Variable):
        return True
    if isinstance(x, str) and x:
        return (x[0].isupper() or x.startswith("_")) and re.match(r"^[A-Z_][a-zA-Z0-9_]*$", x) is not None
    return False


_ANON_COUNTER = 0


def to_term(x: Any) -> Any:
    global _ANON_COUNTER
    if is_variable(x):
        name = x if isinstance(x, str) else x.name
        if name.startswith("_"):
            _ANON_COUNTER += 1
            name = f"{name}_{_ANON_COUNTER}"
        return Variable(name)
    if isinstance(x, str):
        x = x.strip()
        if x.startswith("\\+"):
            inner_str = x[2:].strip()
            return Term("\\+", to_term(inner_str))
        if "\\=" in x:
            left, right = x.split("\\=", 1)
            return Term("\\=", to_term(left.strip()), to_term(right.strip()))
            
        # Check if it has structure like f(x,y)
        m = re.match(r"^([a-z_][a-zA-Z0-9_]*)\((.*)\)$", x)
        if m:
            op = m.group(1)
            args_str = m.group(2)
            args = [to_term(a.strip()) for a in _split_body_terms(args_str) if a.strip()]
            return Term(op, *args)
        if x.startswith("'") and x.endswith("'") and len(x) >= 2:
            x = x[1:-1].replace("\\'", "'")
        return Term(x)
    return x


def _split_body_terms(body_str: str) -> List[str]:
    terms = []
    current = []
    depth = 0
    in_quote = False
    quote_char = None
    
    for char in body_str:
        if char in ("'", '"'):
            if not in_quote:
                in_quote = True
                quote_char = char
            elif quote_char == char:
                in_quote = False
        
        if not in_quote:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 0:
                terms.append("".join(current).strip())
                current = []
                continue
                
        current.append(char)
        
    if current:
        terms.append("".join(current).strip())
    return [t for t in terms if t]


class PythonPrologDB:
    """In-memory Prolog database for pure Python execution."""
    def __init__(self):
        self.rules: List[Rule] = []

    def add_fact(self, op: str, *args: Any):
        self.rules.append(Rule(Term(op, *[to_term(a) for a in args])))

    def add_rule(self, head: Term, body: List[Term]):
        self.rules.append(Rule(head, body))

    def parse_and_load(self, prolog_text: str):
        """Parses a simple Prolog file into rules/facts."""
        # Clean comments
        prolog_text = re.sub(r"%.*$", "", prolog_text, flags=re.MULTILINE)
        prolog_text = re.sub(r"/\*.*?\*/", "", prolog_text, flags=re.DOTALL)
        
        # Split into clauses by dot ending (checking for dot followed by whitespace or EOF)
        clauses = [c.strip() for c in re.split(r"\.(?:\s+|$)", prolog_text) if c.strip()]
        for c in clauses:
            if ":-" in c:
                head_str, body_str = c.split(":-")
                head = to_term(head_str.strip())
                # Parse comma separated body terms
                body = []
                for b_str in _split_body_terms(body_str.strip()):
                    body.append(to_term(b_str))
                self.add_rule(head, body)
            else:
                self.rules.append(Rule(to_term(c)))


def unify(x: Any, y: Any, subst: Dict[Variable, Any]) -> Optional[Dict[Variable, Any]]:
    """Logical unification of x and y under substitution subst."""
    x = resolve_val(x, subst)
    y = resolve_val(y, subst)

    if x == y:
        return subst
    if isinstance(x, Variable):
        return extend_subst(x, y, subst)
    if isinstance(y, Variable):
        return extend_subst(y, x, subst)
    if isinstance(x, Term) and isinstance(y, Term):
        if x.op != y.op or len(x.args) != len(y.args):
            return None
        new_subst = subst.copy()
        for ax, ay in zip(x.args, y.args):
            res = unify(ax, ay, new_subst)
            if res is None:
                return None
            new_subst = res
        return new_subst
    return None


def resolve_val(x: Any, subst: Dict[Variable, Any]) -> Any:
    while isinstance(x, Variable) and x in subst:
        x = subst[x]
    return x


def deep_resolve(x: Any, subst: Dict[Variable, Any]) -> Any:
    x = resolve_val(x, subst)
    if isinstance(x, Term):
        return Term(x.op, *[deep_resolve(arg, subst) for arg in x.args])
    return x


def extend_subst(v: Variable, val: Any, subst: Dict[Variable, Any]) -> Optional[Dict[Variable, Any]]:
    if occurs_check(v, val, subst):
        return None
    new_subst = subst.copy()
    new_subst[v] = val
    return new_subst


def occurs_check(v: Variable, val: Any, subst: Dict[Variable, Any]) -> bool:
    val = resolve_val(val, subst)
    if v == val:
        return True
    if isinstance(val, Term):
        return any(occurs_check(v, arg, subst) for arg in val.args)
    return False


def rename_variables(rule: Rule, suffix: int) -> Rule:
    """Rename variables in rule to avoid collisions in resolution."""
    var_map: Dict[Variable, Variable] = {}

    def rename(x: Any) -> Any:
        if isinstance(x, Variable):
            if x not in var_map:
                var_map[x] = Variable(f"{x.name}_{suffix}")
            return var_map[x]
        if isinstance(x, Term):
            return Term(x.op, *[rename(arg) for arg in x.args])
        return x

    new_head = rename(rule.head)
    new_body = [rename(b) for b in rule.body]
    return Rule(new_head, new_body)


class PythonPrologEngine:
    """SLD Resolution Logic Interpreter."""
    def __init__(self, db: PythonPrologDB):
        self.db = db
        self._var_counter = 0

    def query(self, goal_str: str) -> List[Dict[str, Any]]:
        goal = to_term(goal_str)
        results = []
        
        # We find all variables in the goal
        goal_vars = self._find_vars(goal)
        
        for subst in self._resolve([goal], {}):
            # Extract values for variables in query
            res = {}
            for gv in goal_vars:
                val = deep_resolve(gv, subst)
                # Helper formatting
                if isinstance(val, Term):
                    res[gv.name] = str(val)
                elif isinstance(val, Variable):
                    res[gv.name] = val.name
                else:
                    res[gv.name] = val
            results.append(res)
            
        return results

    def _find_vars(self, term: Any) -> List[Variable]:
        vars_set = set()
        def collect(t):
            if isinstance(t, Variable):
                vars_set.add(t)
            elif isinstance(t, Term):
                for arg in t.args:
                    collect(arg)
        collect(term)
        return list(vars_set)

    def _resolve(self, goals: List[Any], subst: Dict[Variable, Any]) -> Generator[Dict[Variable, Any], None, None]:
        if not goals:
            # Check if all goals are empty
            yield subst
            return

        first, rest = goals[0], goals[1:]
        
        # Built-in negation: \+ or not
        if isinstance(first, Term) and first.op in ("\\+", "not"):
            inner_goal = first.args[0]
            # Try to resolve inner_goal under current subst
            inner_results = list(self._resolve([inner_goal], subst))
            if not inner_results:
                # If inner goal fails, negation succeeds! Continue with rest
                yield from self._resolve(rest, subst)
            return

        # Built-in inequality: \= or \\=
        if isinstance(first, Term) and first.op in ("\\=", "\\\\="):
            left = resolve_val(first.args[0], subst)
            right = resolve_val(first.args[1], subst)
            left_str = str(left) if not isinstance(left, Variable) else left
            right_str = str(right) if not isinstance(right, Variable) else right
            if left_str != right_str:
                yield from self._resolve(rest, subst)
            return

        self._var_counter += 1
        
        for rule in self.db.rules:
            # Rename variables in rule to avoid collision
            renamed_rule = rename_variables(rule, self._var_counter)
            
            # Try to unify first goal with rule head
            new_subst = unify(first, renamed_rule.head, subst)
            if new_subst is not None:
                # Resolve rule body + remaining goals
                new_goals = renamed_rule.body + rest
                yield from self._resolve(new_goals, new_subst)


# ─────────────────────────────────────────────────────────────
# 🛡️ THE HYBRID PROLOG ENGINE
# ─────────────────────────────────────────────────────────────

class HybridPrologEngine:
    """Hybrid Logic Engine delegating queries based on backend availability."""
    def __init__(self, prolog_file_path: Union[str, Path]):
        self.path = Path(prolog_file_path).resolve()
        if not self.path.exists():
            raise FileNotFoundError(f"Prolog source file not found at: {self.path}")

        # Pre-load database for Python fallback
        self.py_db = PythonPrologDB()
        self.py_db.parse_and_load(self.path.read_text(encoding="utf-8"))
        self.py_engine = PythonPrologEngine(self.py_db)

    def query(self, query_str: str) -> List[Dict[str, Any]]:
        """Runs query against the best available Prolog backend."""
        # Trim ending dot if present
        query_str = query_str.strip().rstrip(".")

        # Try 1: PySwip Direct Bindings
        if PYSWIP_AVAILABLE:
            try:
                return self._query_pyswip(query_str)
            except Exception:
                # Fallback to next backend
                pass

        # Try 2: SWI-Prolog Subprocess (invokes swipl directly)
        if self._swipl_executable_exists():
            try:
                return self._query_subprocess(query_str)
            except Exception:
                pass

        # Try 3: Pure Python Fallback
        return self._query_python(query_str)

    def _query_pyswip(self, query_str: str) -> List[Dict[str, Any]]:
        """Executes query using the PySwip wrapper."""
        pyswip.Prolog.consult(str(self.path))
        results = list(pyswip.Prolog.query(query_str))
        
        # Clean results (convert PySwip atoms to strings)
        cleaned = []
        for r in results:
            clean_r = {}
            for k, v in r.items():
                if isinstance(v, bytes):
                    clean_r[k] = v.decode("utf-8")
                else:
                    clean_r[k] = str(v)
            cleaned.append(clean_r)
        return cleaned

    def _query_subprocess(self, query_str: str) -> List[Dict[str, Any]]:
        """Executes query by spawning a swipl process."""
        # Extract variables from query_str
        vars_found = list(set(re.findall(r"\b([A-Z][a-zA-Z0-9_]*)\b", query_str)))
        
        if not vars_found:
            # Boolean query
            cmd = [
                "swipl", "-q", "-f", str(self.path),
                "-g", f"({query_str} -> write('true') ; write('false')), halt."
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.stdout.strip() == "true":
                return [{}]
            return []
        
        # Query containing variables: print as KV pairs
        print_goals = []
        for v in vars_found:
            print_goals.append(f"format('~w:~w~n', ['{v}', {v}])")
            
        goal_exec = f"forall({query_str}, ( {' , '.join(print_goals)} , format('---~n') )), halt."
        
        cmd = ["swipl", "-q", "-f", str(self.path), "-g", goal_exec]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        solutions = []
        current_sol = {}
        for line in res.stdout.splitlines():
            line = line.strip()
            if line == "---":
                if current_sol:
                    solutions.append(current_sol)
                    current_sol = {}
            elif ":" in line:
                k, v = line.split(":", 1)
                current_sol[k] = v
                
        if current_sol:
            solutions.append(current_sol)
            
        return solutions

    def _query_python(self, query_str: str) -> List[Dict[str, Any]]:
        """Pure Python fallback logic query."""
        return self.py_engine.query(query_str)

    def _swipl_executable_exists(self) -> bool:
        try:
            subprocess.run(["swipl", "--version"], capture_output=True)
            return True
        except FileNotFoundError:
            return False

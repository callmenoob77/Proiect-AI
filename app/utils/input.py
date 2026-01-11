# python
import ast
import unicodedata
import re
from typing import Any
import math

    _ZERO_WIDTH_RE = re.compile(r"[\u200B-\u200F\uFEFF]")
_WHITESPACE_RE = re.compile(r"\s+")

def normalize_text(s: str) -> str:
s = (s or "").strip()
s = unicodedata.normalize("NFKC", s)
s = _ZERO_WIDTH_RE.sub("", s)
s = _WHITESPACE_RE.sub(" ", s)
return s

def safe_parse(s: str) -> Any:
s = normalize_text(s)
if not s:
return s
# try safe literal (numbers, lists, dicts, strings)
try:
return ast.literal_eval(s)
except (ValueError, SyntaxError):
pass
# try numeric with comma decimal
try:
return float(s.replace(",", "."))
except Exception:
return s

def score_numeric(correct: float, given: float, rel_tol: float = 1e-3) -> float:
if math.isclose(correct, given, rel_tol=rel_tol, abs_tol=rel_tol):
return 100.0
diff = abs(correct - given)
denom = max(abs(correct), 1.0)
score = max(0.0, 100.0 * (1.0 - diff / denom))
return score

def token_overlap_score(a: str, b: str) -> float:
ta = set(normalize_text(a).lower().split())
tb = set(normalize_text(b).lower().split())
if not ta and not tb:
return 100.0
inter = ta & tb
denom = len(ta) + len(tb)
if denom == 0:
return 0.0
return 100.0 * (2 * len(inter) / denom)

def compare_answers(correct_raw: Any, given_raw: Any) -> float:
correct = correct_raw
given = given_raw
# try to parse if strings
if isinstance(correct_raw, str):
correct = safe_parse(correct_raw)
if isinstance(given_raw, str):
given = safe_parse(given_raw)

# numeric vs numeric
if isinstance(correct, (int, float)) and isinstance(given, (int, float)):
return score_numeric(float(correct), float(given))

# string comparison (token overlap)
return token_overlap_score(str(correct), str(given))
"""Closed check registry. Statements are labels; only typed parameters are checked.

No eval, network access, floating-point tolerance, or caller-supplied PASS labels.
Finite computations establish only their explicitly reported scope.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from math import comb
from fractions import Fraction
from pathlib import Path

PASS, FAIL, UNRESOLVED = "PASS", "FAIL", "UNRESOLVED"
ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def result(verdict, reason, evidence=None):
    return {
        "verdict": verdict,
        "evidence_status": {PASS: "demonstrated", FAIL: "rejected", UNRESOLVED: "unresolved"}[verdict],
        "reason": reason,
        "evidence": {} if evidence is None else evidence,
    }


def integer(x, name, minimum=0, maximum=None):
    if type(x) is not int or x < minimum or (maximum is not None and x > maximum):
        raise ValueError(f"{name}: expected integer in [{minimum}, {maximum}]")
    return x


def rational(x):
    if type(x) not in (int, str):
        raise ValueError("Use integer or rational string; floats and booleans are not accepted")
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid exact rational") from exc


def coefficients(values):
    if not isinstance(values, list) or not values or len(values) > 65:
        raise ValueError("Polynomial needs 1..65 coefficients in ascending degree order")
    out = [rational(v) for v in values]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def evaluate(poly, x):
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * x + coefficient
    return value


def polynomial_identity(p):
    left, right = coefficients(p["left"]), coefficients(p["right"])
    same = left == right
    return result(PASS if same else FAIL, "Exact coefficient comparison over Q[n].",
                  {"left": list(map(str, left)), "right": list(map(str, right))})


def affine_power_identity(p):
    """Compare a supplied polynomial to (a*n+b)^k + offset by binomial expansion."""
    power = integer(p["power"], "power", 0, 64)
    a, b, offset = rational(p["slope"]), rational(p["intercept"]), rational(p["offset"])
    expanded = [comb(power, i) * a**i * b**(power-i) for i in range(power+1)]
    expanded[0] += offset
    return polynomial_identity({"left": p["polynomial"], "right": list(map(str, expanded))})


def integer_volume(p):
    poly, scale = coefficients(p["polynomial"]), rational(p["scale"])
    start = integer(p["start"], "start")
    stop = integer(p["stop"], "stop", start, start + 10000)
    for n in range(start, stop + 1):
        value = scale * evaluate(poly, n)
        if value.denominator != 1:
            return result(FAIL, "Counterexample to integer count of whole, non-overlapping unit cubes.",
                          {"n": n, "volume": str(value), "interpretation": "literal cube count"})
    return result(PASS, "Integral at every integer in the stated finite interval only.",
                  {"interval": [start, stop], "universal_claim": False})


def determinant(m):
    return (m[0][0] * (m[1][1]*m[2][2]-m[1][2]*m[2][1])
            - m[0][1] * (m[1][0]*m[2][2]-m[1][2]*m[2][0])
            + m[0][2] * (m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def act(m, v):
    return tuple(sum(m[i][j]*v[j] for j in range(3)) for i in range(3))


def cube_rotations(p):
    expected = integer(p["expected_count"], "expected_count")
    vertices = set(itertools.product((-1, 1), repeat=3))
    matrices = []
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            m = tuple(tuple(signs[i] if j == permutation[i] else 0 for j in range(3)) for i in range(3))
            if determinant(m) == 1 and {act(m, v) for v in vertices} == vertices:
                matrices.append(m)
    return result(PASS if len(matrices) == expected else FAIL,
                  "Enumerated orientation-preserving signed permutation matrices of an undecorated cube.",
                  {"count": len(matrices), "expected": expected, "determinants": [1],
                   "scope": "Euclidean cube; not a junction model or a proof about glued complexes"})


def fano_automorphisms(p):
    expected = integer(p["expected_count"], "expected_count")
    # Nonzero vectors in F_2^3 encoded by 1..7; lines are {a,b,a XOR b}.
    lines = {frozenset((a, b, a ^ b)) for a in range(1, 8) for b in range(a + 1, 8)}
    count = 0
    for perm in itertools.permutations(range(1, 8)):
        if {frozenset(perm[x-1] for x in line) for line in lines} == lines:
            count += 1
    return result(PASS if count == expected else FAIL, "Exhaustive incidence-preserving permutations of the Fano plane.",
                  {"points": 7, "lines": len(lines), "permutations_tested": 5040, "count": count,
                   "expected": expected, "M11_identification": "not established by this check"})


def order_divides(p):
    child = integer(p["child_order"], "child_order", 1)
    parent = integer(p["parent_order"], "parent_order", 1)
    divides = parent % child == 0
    return result(PASS if divides else FAIL,
                  "Necessary order-divisibility check only; PASS supplies no subgroup, quotient, or action.",
                  {"child_order": child, "parent_order": parent, "remainder": parent % child,
                   "embedding_proven": False})


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def permutation_group(p):
    degree = integer(p["degree"], "degree", 1, 16)
    limit = integer(p.get("max_elements", 256), "max_elements", 1, 256)
    expected = integer(p["expected_order"], "expected_order", 1)
    generators = p["generators"]
    if not isinstance(generators, list) or not 1 <= len(generators) <= 16:
        raise ValueError("Need 1..16 generators")
    for g in generators:
        if (not isinstance(g, list) or any(type(x) is not int for x in g)
                or sorted(g) != list(range(degree))):
            raise ValueError("Generators must be bijections of 0..degree-1")
    generators = list(map(tuple, generators))
    identity = tuple(range(degree))
    seen, queue = {identity}, [identity]
    while queue:
        a = queue.pop()
        for b in generators:
            c = compose(a, b)
            if c not in seen:
                if len(seen) >= limit:
                    return result(UNRESOLVED, "Enumeration budget exhausted; no order conclusion.",
                                  {"at_least": len(seen) + 1, "limit": limit})
                seen.add(c)
                queue.append(c)
    elements = sorted(seen)
    closed = all(compose(a, b) in seen for a in elements for b in elements)
    inverse_witnesses = {str(i): elements.index(tuple(a.index(j) for j in range(degree)))
                         for i, a in enumerate(elements)}
    return result(PASS if closed and len(seen) == expected else FAIL,
                  "Finite group realized by explicit permutations; associativity is inherited from function composition.",
                  {"order": len(seen), "expected_order": expected, "closed": closed,
                   "abelian": all(compose(a, b) == compose(b, a) for a in elements for b in elements),
                   "elements": elements, "inverse_indices": inverse_witnesses,
                   "scope": "This finite action only; no Leech, anyon, or Monster bridge certified"})


def obligation(p):
    needed = p.get("needed")
    if not isinstance(needed, list) or not needed or any(not isinstance(v, str) or not v.strip() for v in needed):
        raise ValueError("obligation needs a nonempty list of missing definitions or evidence")
    return result(UNRESOLVED, "No executable witness checker for this obligation in v0.1.",
                  {"needed": needed, "supplied_notes": p.get("notes", ""),
                   "notes_are_proof": False})


CHECKS = {
    "polynomial_identity": polynomial_identity,
    "affine_power_identity": affine_power_identity,
    "integer_volume": integer_volume,
    "cube_rotations": cube_rotations,
    "fano_automorphisms": fano_automorphisms,
    "order_divides": order_divides,
    "permutation_group": permutation_group,
    "obligation": obligation,
}


def aggregate(verdicts):
    if FAIL in verdicts:
        return FAIL
    if not verdicts or UNRESOLVED in verdicts:
        return UNRESOLVED
    return PASS


def audit(data):
    if not isinstance(data, dict) or data.get("schema_version") != "pegasus-claims/1":
        raise ValueError("Expected schema_version pegasus-claims/1")
    claims = data.get("claims")
    required = data.get("required_claims")
    if not isinstance(claims, list) or not claims or len(claims) > 256:
        raise ValueError("Need 1..256 claims")
    if not isinstance(required, list) or not required or any(not isinstance(x, str) for x in required):
        raise ValueError("Need nonempty required_claims list of IDs")
    ids = {}
    for c in claims:
        if not isinstance(c, dict):
            raise ValueError("Claims must be objects")
        for key in ("id", "statement", "check"):
            if not isinstance(c.get(key), str) or not c[key].strip():
                raise ValueError(f"Each claim needs a nonempty {key}")
        if c["id"] in ids:
            raise ValueError("Duplicate claim ID")
        if not isinstance(c.get("params"), dict):
            raise ValueError("params must be an object")
        deps = c.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps):
            raise ValueError("depends_on must be a list of IDs")
        ids[c["id"]] = c
    for c in claims:
        if any(d not in ids for d in c.get("depends_on", [])):
            raise ValueError("Unknown dependency")
    if any(d not in ids for d in required):
        raise ValueError("Unknown required claim")

    # Detect every cycle before running checks; cycles cannot certify themselves.
    state, cyclic, path = {}, set(), []
    def visit(key):
        if state.get(key) == 1:
            cyclic.update(path[path.index(key):])
            return
        if state.get(key) == 2:
            return
        state[key] = 1
        path.append(key)
        for dep in ids[key].get("depends_on", []):
            visit(dep)
        path.pop()
        state[key] = 2
    for key in ids:
        visit(key)

    outputs = {}
    def run(key):
        if key in outputs:
            return outputs[key]
        c = ids[key]
        if key in cyclic:
            out = result(FAIL, "Circular dependency: claim cannot establish its own premises.")
        else:
            dependencies = {dep: run(dep)["verdict"] for dep in c.get("depends_on", [])}
            checker = CHECKS.get(c["check"])
            try:
                own = checker(c["params"]) if checker else result(UNRESOLVED, "Unknown checker; no automatic promotion.")
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"{key}: invalid parameters: {exc}") from exc
            out = dict(own)
            verdict = aggregate([own["verdict"], *dependencies.values()])
            if verdict != own["verdict"]:
                out = result(verdict, "A required premise failed or remains unresolved.", {"local_result": own})
            out["dependencies"] = dependencies
        out.update({"id": key, "statement": c["statement"], "check": c["check"]})
        outputs[key] = out
        return out
    rows = [run(c["id"]) for c in claims]
    return {
        "schema_version": "pegasus-report/1", "animal": "PEGASUS", "version": "0.1.0",
        "target": data.get("target", "unnamed"), "required_claims": required,
        "verdict": aggregate([outputs[k]["verdict"] for k in required]),
        "counts": {v: sum(row["verdict"] == v for row in rows) for v in (PASS, FAIL, UNRESOLVED)},
        "scope": "Only typed parameters and declared dependencies are checked; prose is not machine-parsed.",
        "independent_replication": "not performed", "results": rows,
    }


def audit_file(path):
    path = Path(path)
    report = audit(json.loads(path.read_text(encoding="utf-8")))
    report["input_sha256"] = digest(path)
    report["checker_sha256"] = digest(__file__)
    return report


def verify_freeze(path=ROOT / "freeze.json"):
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("Freeze must contain file hashes")
    rows = []
    for name, expected in sorted(files.items()):
        candidate = (ROOT / name).resolve()
        if not candidate.is_relative_to(ROOT) or not candidate.is_file():
            rows.append({"path": name, "verdict": FAIL, "reason": "missing or outside project"})
            continue
        actual = digest(candidate)
        rows.append({"path": name, "verdict": PASS if actual == expected else FAIL,
                     "expected": expected, "actual": actual})
    return {"verdict": aggregate([r["verdict"] for r in rows]), "files": rows,
            "scope": "Local consistency with the recorded freeze; not an independent timestamp or authorship proof"}

"""analyze2.py -- discovery pass, window-correct.

Fix over analyze.py: a relation can look "not forced" purely because the board is too
small for the value the PROOF needs.  So the window requirement [Kmin,Kmax] is part of
the rule: "if p+Kmin*s >= 1 and p+Kmax*s <= N then pos(p+k1*s) < pos(p+k2*s)".
For each (hypothesis, conclusion) we report the WEAKEST window requirement that makes
the relation forced, i.e. the smallest [Kmin,Kmax] containing {k1,k2}.
"""
import sys
from collections import defaultdict
from analyze import load, TYPES, ORDS, RATS, CONSS, trivial_closure

TNAME = {'ANY': 'ANY', 'R': 'R', 'G': 'G', 'RG': 'RG'}


def mine(B):
    res = []
    for m in (1, 2, 3):
        for pt in TYPES:
            for qt in TYPES:
                for on in ORDS:
                    for rn in RATS:
                        for cn in CONSS:
                            base = [b for b in B if b['m'] == m and b['tp'] in TYPES[pt]
                                    and b['tq'] in TYPES[qt] and b['ord'] in ORDS[on]
                                    and b['rat'] in RATS[rn] and b['cons'] in CONSS[cn]]
                            if not base:
                                continue
                            for k1 in range(-2, m + 3):
                                for k2 in range(-2, m + 3):
                                    if k1 == k2:
                                        continue
                                    best = None
                                    for Kmin in range(min(k1, k2), -3, -1):
                                        for Kmax in range(max(k1, k2), m + 3):
                                            sel = [b for b in base
                                                   if b['kmin'] <= Kmin and b['kmax'] >= Kmax]
                                            if not sel:
                                                continue
                                            fwd = sum(b['cnt'] for b in sel if (k1, k2) in b['rels'])
                                            bwd = any((k2, k1) in b['rels'] for b in sel)
                                            if not bwd and fwd > 0:
                                                if best is None or (Kmax - Kmin) < (best[1] - best[0]):
                                                    best = (Kmin, Kmax, fwd)
                                    if best is None:
                                        continue
                                    Kmin, Kmax, fwd = best
                                    triv = trivial_closure(pt, qt, on, m, min(Kmin, -2), max(Kmax, m + 2))
                                    if (k1, k2) in triv:
                                        continue
                                    res.append(dict(m=m, pt=pt, qt=qt, ord=on, rat=rn, cons=cn,
                                                    k1=k1, k2=k2, Kmin=Kmin, Kmax=Kmax, fires=fwd))
    return res


def hypset(r):
    return (TYPES[r['pt']], TYPES[r['qt']], ORDS[r['ord']], RATS[r['rat']], CONSS[r['cons']])


def keep_weakest(rules):
    by = defaultdict(list)
    for r in rules:
        by[(r['m'], r['k1'], r['k2'])].append(r)
    out = []
    for k, rs in by.items():
        for r in rs:
            hr = hypset(r)
            dom = False
            for s in rs:
                if s is r:
                    continue
                hs = hypset(s)
                # s has weaker-or-equal hypothesis AND weaker-or-equal window requirement
                if (all(a <= b for a, b in zip(hr, hs)) and s['Kmin'] >= r['Kmin']
                        and s['Kmax'] <= r['Kmax'] and (hr != hs or s['Kmin'] != r['Kmin']
                                                        or s['Kmax'] != r['Kmax'])):
                    dom = True
                    break
            if not dom:
                out.append(r)
    return out


if __name__ == '__main__':
    B = load(sys.argv[1])
    rules = keep_weakest(mine(B))
    rules.sort(key=lambda r: -r['fires'])
    print(f"# {sys.argv[1]}: {len(rules)} weakest-hypothesis forced non-trivial relations")
    print("# slot k means value p + k*s, s=(q-p)/m; p=slot 0, q=slot m")
    print("# window req: values p+Kmin*s .. p+Kmax*s must all lie in [1..N]")
    for r in rules:
        print(f"m={r['m']} p:{r['pt']:3} q:{r['qt']:3} ord:{r['ord']:4} rat:{r['rat']:9} "
              f"{r['cons']:4} win[{r['Kmin']:2},{r['Kmax']:2}] | slot {r['k1']:2} < slot {r['k2']:2} "
              f" (fires {r['fires']})")

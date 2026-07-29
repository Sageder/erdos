"""analyze.py -- aggregate the raw bucket dump of mine.c into candidate two-point rules.

Input: raw_N<k>.txt produced by mine.c (one line per nonempty exact bucket, listing every
ordered slot pair (k1,k2) for which pos(p+k1 s) < pos(p+k2 s) was OBSERVED on some board).

A coarse hypothesis H is a predicate on (type(p), type(q), order, ratio, cons) together with
a fixed step count m.  Relation (k1 < k2) is FORCED under H iff, over all exact buckets
matching H whose window contains both slots, the pair (k2,k1) was never observed and
(k1,k2) was observed at least once (non-vacuity).

Trivially forced relations (record/grounded/assumed-order plus their transitive closure)
are filtered out; what remains are candidate two-point supply rules.
"""
import sys, itertools
from collections import defaultdict

def load(path):
    buckets = []
    for line in open(path):
        if line.startswith('#'):
            continue
        f = line.split()
        tp, tq, ordr, rat, cons, m, kmin, kmax = map(int, f[1:9])
        cnt = int(f[9])
        rels = set()
        if len(f) > 10:
            for tok in f[10].split(';'):
                if tok:
                    a, b = tok.split(',')
                    rels.add((int(a), int(b)))
        buckets.append(dict(tp=tp, tq=tq, ord=ordr, rat=rat, cons=cons, m=m,
                            kmin=kmin, kmax=kmax, cnt=cnt, rels=rels))
    return buckets

# type predicates: name -> set of exact types allowed (type = 2*grounded + record)
TYPES = {'ANY': {0, 1, 2, 3}, 'R': {1, 3}, 'G': {2, 3}, 'RG': {3}}
ORDS = {'ANY': {0, 1}, 'q<p': {0}, 'p<q': {1}}          # ord=1 means pos(p)<pos(q)
RATS = {'ANY': {0, 1, 2}, 'q<2p': {0}, '2p<=q<3p': {1}, 'q>=3p': {2},
        'q<3p': {0, 1}, 'q>=2p': {1, 2}}
CONSS = {'ANY': {0, 1}, 'cons': {1}}


def trivial_closure(ptype, qtype, ordname, m, kmin, kmax):
    """Relations forced for free by recordness / groundedness / the assumed order."""
    slots = list(range(kmin, kmax + 1))
    base = set()
    prec = TYPES[ptype]
    qrec = TYPES[qtype]
    p_is_record = prec <= {1, 3}
    p_is_gnd = prec <= {2, 3}
    q_is_record = qrec <= {1, 3}
    q_is_gnd = qrec <= {2, 3}
    for k in slots:
        if p_is_record and k > 0:
            base.add((0, k))
        if p_is_gnd and k < 0:
            base.add((k, 0))
        if q_is_record and k > m:
            base.add((m, k))
        if q_is_gnd and k < m:
            base.add((k, m))
    if ORDS[ordname] == {1}:
        base.add((0, m))
    if ORDS[ordname] == {0}:
        base.add((m, 0))
    # transitive closure
    changed = True
    while changed:
        changed = False
        for (a, b) in list(base):
            for (c, d) in list(base):
                if b == c and (a, d) not in base and a != d:
                    base.add((a, d))
                    changed = True
    return base


def mine(buckets, verbose=True):
    out = []
    for m in (1, 2, 3):
        for pt in TYPES:
            for qt in TYPES:
                for on in ORDS:
                    for rn in RATS:
                        for cn in CONSS:
                            sel = [b for b in buckets
                                   if b['m'] == m and b['tp'] in TYPES[pt] and b['tq'] in TYPES[qt]
                                   and b['ord'] in ORDS[on] and b['rat'] in RATS[rn]
                                   and b['cons'] in CONSS[cn]]
                            if not sel:
                                continue
                            tot = sum(b['cnt'] for b in sel)
                            # candidate slot pairs
                            lo = min(b['kmin'] for b in sel)
                            hi = max(b['kmax'] for b in sel)
                            for k1 in range(lo, hi + 1):
                                for k2 in range(lo, hi + 1):
                                    if k1 == k2:
                                        continue
                                    seen_fwd = 0
                                    seen_bwd = False
                                    for b in sel:
                                        if b['kmin'] <= min(k1, k2) and max(k1, k2) <= b['kmax']:
                                            if (k1, k2) in b['rels']:
                                                seen_fwd += b['cnt']
                                            if (k2, k1) in b['rels']:
                                                seen_bwd = True
                                                break
                                    if seen_bwd or seen_fwd == 0:
                                        continue
                                    triv = trivial_closure(pt, qt, on, m, min(lo, k1, k2), max(hi, k1, k2))
                                    if (k1, k2) in triv:
                                        continue
                                    out.append(dict(m=m, pt=pt, qt=qt, ord=on, rat=rn, cons=cn,
                                                    k1=k1, k2=k2, tot=tot))
    return out


def key(r):
    return (r['m'], r['k1'], r['k2'])


def minimal_hypotheses(rules):
    """Keep only rules whose hypothesis is not strictly weaker-implied by another
    rule with the same conclusion (i.e. drop rules whose hypothesis is a strict
    specialisation of another rule already listed)."""
    bykey = defaultdict(list)
    for r in rules:
        bykey[key(r)].append(r)
    kept = []
    for k, rs in bykey.items():
        def hypset(r):
            return (TYPES[r['pt']], TYPES[r['qt']], ORDS[r['ord']], RATS[r['rat']], CONSS[r['cons']])
        for r in rs:
            hr = hypset(r)
            dominated = False
            for s in rs:
                if s is r:
                    continue
                hs = hypset(s)
                if all(a <= b for a, b in zip(hr, hs)) and hr != hs:
                    dominated = True
                    break
            if not dominated:
                kept.append(r)
    return kept


if __name__ == '__main__':
    path = sys.argv[1]
    buckets = load(path)
    rules = mine(buckets)
    kept = minimal_hypotheses(rules)
    kept.sort(key=lambda r: (-r['tot'], r['m'], r['k1'], r['k2']))
    print(f"# {path}: {len(buckets)} exact buckets, {len(rules)} forced non-trivial "
          f"relations, {len(kept)} with maximal (weakest) hypothesis")
    for r in kept:
        print(f"m={r['m']} p:{r['pt']:3} q:{r['qt']:3} ord:{r['ord']:4} rat:{r['rat']:9} "
              f"{r['cons']:4} | slot {r['k1']} < slot {r['k2']}   (fires {r['tot']})")

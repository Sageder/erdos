"""query.py -- targeted queries on the raw bucket dump.

(1) forced ORDER between the two named points: for which (type(p), type(q), ratio)
    is one of the two position-orders never realised?
(2) all forced hypotheses for a named conclusion (m, k1, k2).
"""
import sys
from collections import defaultdict
from analyze import load, TYPES, ORDS, RATS, CONSS, trivial_closure

path = sys.argv[1]
B = load(path)

print("=== (1) forced order between the two named points ===")
print("    (bucket key = tp,tq,rat with tp/tq = 2*grounded+record; ")
print("     'p<q only' means pos(q)<pos(p) never occurred)")
agg = defaultdict(lambda: [0, 0])           # (tp,tq,rat) -> [count ord=0, count ord=1]
for b in B:
    agg[(b['tp'], b['tq'], b['rat'])][b['ord']] += b['cnt']
TNAME = {0: '-', 1: 'R', 2: 'G', 3: 'RG'}
RNAME = {0: 'q<2p', 1: '2p<=q<3p', 2: 'q>=3p'}
for k in sorted(agg):
    c0, c1 = agg[k]
    if c0 == 0 or c1 == 0:
        tp, tq, rat = k
        forced = 'p<q' if c0 == 0 else 'q<p'
        print(f"  p:{TNAME[tp]:2} q:{TNAME[tq]:2} {RNAME[rat]:9} -> pos order FORCED {forced}"
              f"   (fires {max(c0,c1)})")

print()
print("=== (2) forced hypotheses for selected conclusions ===")


def forced(m, k1, k2, pt, qt, on, rn, cn):
    sel = [b for b in B if b['m'] == m and b['tp'] in TYPES[pt] and b['tq'] in TYPES[qt]
           and b['ord'] in ORDS[on] and b['rat'] in RATS[rn] and b['cons'] in CONSS[cn]
           and b['kmin'] <= min(k1, k2) and max(k1, k2) <= b['kmax']]
    if not sel:
        return None
    fwd = sum(b['cnt'] for b in sel if (k1, k2) in b['rels'])
    bwd = sum(b['cnt'] for b in sel if (k2, k1) in b['rels'])
    tot = sum(b['cnt'] for b in sel)
    return fwd, bwd, tot


QUERIES = [
    ("W1  rec-grounded trisection:  w+2s < w+s", 3, 2, 1, 'R', 'G', 'ANY', 'ANY', 'ANY'),
    ("W2a rec-grounded bisection L1: g+s < g",   2, 3, 2, 'R', 'G', 'ANY', 'ANY', 'ANY'),
    ("W2b rec-grounded bisection L2: w < w-s",   2, 0, -1, 'R', 'G', 'ANY', 'ANY', 'ANY'),
    ("W3  gnd-gnd bisection:        g+s < g",    2, 1, 0, 'G', 'G', 'ANY', 'q<3p', 'ANY'),
    ("W4  rec-rec bisection:        w' < w+s",   2, 2, 1, 'R', 'R', 'ANY', 'ANY', 'ANY'),
    ("W5  gnd-gnd m=1 L1:           2g'-g < g'", 1, 2, 1, 'G', 'G', 'ANY', 'q<2p', 'ANY'),
    ("W6  rec-rec m=1 L1:        3w'-2w < 2w'-w",1, 3, 2, 'R', 'R', 'ANY', 'ANY', 'ANY'),
    ("W6b rec-rec m=1 L2:           w < 2w-w'",  1, 0, -1, 'R', 'R', 'ANY', 'q<2p', 'ANY'),
    ("W8  gnd-gnd trisection m=3:  g+2s < g+s",  3, 2, 1, 'G', 'G', 'ANY', 'ANY', 'ANY'),
    ("W9  rec-rec trisection m=3:  w+2s < w+s",  3, 2, 1, 'R', 'R', 'ANY', 'ANY', 'ANY'),
    ("W10 gnd-rec (g<w) m=2:      ?",            2, 1, 0, 'G', 'R', 'ANY', 'ANY', 'ANY'),
    ("W11 rec-gnd m=3 slot3<slot? ",             3, 4, 3, 'R', 'G', 'ANY', 'ANY', 'ANY'),
]
for name, m, k1, k2, pt, qt, on, rn, cn in QUERIES:
    r = forced(m, k1, k2, pt, qt, on, rn, cn)
    if r is None:
        print(f"  {name:44} : NO MATCHING BUCKETS")
        continue
    fwd, bwd, tot = r
    verdict = "FORCED" if (bwd == 0 and fwd > 0) else ("VACUOUS" if fwd == 0 and bwd == 0 else "REFUTED")
    print(f"  {name:44} : {verdict:8} fwd={fwd} bwd={bwd} buckets_tot={tot}")

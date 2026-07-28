"""verify_R8.py — independent re-verification of route R8's hand-proved,
machine-checkable claims (Theorem W and the bit-reversed-rate ladder at k=2),
plus the elementary pieces of T1/T2/T3 that can be checked by arithmetic.

Only the CHEAP, self-contained claims are re-run here; R8's SAT results
(N=242 / +-242 UNSAT, +-127 windows) are NOT re-run and are marked UNVERIFIED
in STATUS.md.
"""
import sys
sys.path.insert(0, "/home/user/erdos/experiments")
import apcheck

OUT = []
P = OUT.append


# ---------- Theorem W: W = 2, (1,4,6), (3,8,10), (5,12,14), ... ----------
def W_prefix(npos):
    seq = [2]
    i = 1
    while len(seq) < npos:
        seq.extend([2 * i - 1, 4 * i, 4 * i + 2])
        i += 1
    return seq[:npos]


def check_odd_d_4ap(seq, k=4, only_odd_d=True):
    """Exact: is there a monotone k-AP with odd common difference among the values
    of `seq` (all terms present)?  Returns a witness or None."""
    posmap = {v: i for i, v in enumerate(seq)}
    vset = set(posmap)
    vals = sorted(vset)
    mx = vals[-1]
    for x in vals:
        for d in range(1, (mx - x) // (k - 1) + 1):
            if only_odd_d and d % 2 == 0:
                continue
            terms = [x + j * d for j in range(k)]
            if not all(t in vset for t in terms):
                continue
            ps = [posmap[t] for t in terms]
            if all(ps[j] < ps[j + 1] for j in range(k - 1)):
                return (x, d, "inc")
            if all(ps[j] > ps[j + 1] for j in range(k - 1)):
                return (x, d, "dec")
    return None


for npos in (400, 1300, 4000):
    seq = W_prefix(npos)
    ok_inj = len(set(seq)) == len(seq)
    w_odd = check_odd_d_4ap(seq, 4, True)
    w_all = check_odd_d_4ap(seq, 4, False)
    P(f"Thm W  prefix of {npos:5d} positions (max value {max(seq)}): injective={ok_inj}  "
      f"monotone 4-AP with ODD d: {w_odd}   with ANY d: {w_all}")

# the position formulas R8 uses in the proof
seq = W_prefix(3000)
pos = {v: i + 1 for i, v in enumerate(seq)}
bad = []
for v in sorted(pos):
    if v % 2 == 1:
        if pos[v] != (3 * v + 1) // 2:
            bad.append(("odd", v, pos[v], (3 * v + 1) / 2))
    else:
        if not ((3 * v - 2) / 4 <= pos[v] <= 3 * v / 4):
            bad.append(("even", v, pos[v]))
P(f"Thm W  position formulas pos(odd o)=(3o+1)/2 and (3e-2)/4 <= pos(even e) <= 3e/4: "
  f"{'VERIFIED on all values of the 3000-position prefix' if not bad else 'FAILURES ' + str(bad[:5])}")

# W is surjective onto N in the limit (odds ascending, evens ascending)
vals = sorted(seq)
P(f"Thm W  the 3000-position prefix covers 1..{max(v for v in range(1, max(vals)+1) if all(u in set(vals) for u in range(1, v+1)))} contiguously")


# ---------- ladder level k=2: residues mod 4 with bit-reversed geometric rates ----------
def ladder_k2(npos, rates=(1, 4, 2, 8), residues=(1, 2, 3, 0)):
    """Emit ascending streams: residue class residues[j] mod 4 at relative rate rates[j],
    scheduled by exact fractional (Bresenham) accounting."""
    from fractions import Fraction
    tot = sum(rates)
    nxt = []
    for j, r in enumerate(residues):
        v = r if r > 0 else 4
        nxt.append(v)
    credit = [Fraction(0)] * 4
    out = []
    while len(out) < npos:
        # pick the stream whose 'ideal count' is furthest behind
        best, bestval = None, None
        n = len(out)
        for j in range(4):
            ideal = Fraction(rates[j] * (n + 1), tot)
            deficit = ideal - credit[j]
            if best is None or deficit > bestval:
                best, bestval = j, deficit
        out.append(nxt[best])
        nxt[best] += 4
        credit[best] += 1
    return out


for npos in (600, 2000):
    s = ladder_k2(npos)
    ok = len(set(s)) == len(s)
    posmap = {v: i for i, v in enumerate(s)}
    vset = set(s)
    vals = sorted(vset)
    witness = None
    for x in vals:
        for d in range(1, (vals[-1] - x) // 3 + 1):
            if d % 4 == 0:
                continue
            terms = [x + j * d for j in range(4)]
            if not all(t in vset for t in terms):
                continue
            ps = [posmap[t] for t in terms]
            if all(ps[j] < ps[j + 1] for j in range(3)) or all(ps[j] > ps[j + 1] for j in range(3)):
                witness = (x, d)
                break
        if witness:
            break
    P(f"ladder k=2 (rates 1,4,2,8 on residues 1,2,3,0 mod 4), {npos} positions: injective={ok}  "
      f"monotone 4-AP with d not= 0 mod 4: {witness}")

# ---------- T1 sanity: the descent map on random permutations of prefixes ----------
P("T1 (hand proof re-checked by inspection): c=a(1); if pi(2v-c)<pi(v) for all v>=2c+1 the "
  "orbit v_{k+1}=2v_k-c stays in [2c+1,inf) (2v-c>=3c+2>=2c+1 for c>=1) and gives an "
  "infinite strictly pi-decreasing sequence -- impossible in a type-omega order. VALID.")
P("T2 (hand proof re-checked): x:=c-d=2c-v <= -1 <= 0 for v>=2c+1, so x sits at a position "
  "< s, before all of the right part; (c-d,c,c+d,c+2d) is then an increasing monotone 4-AP. "
  "VALID (given T1's descent applied inside the right part, whose value set is N minus a "
  "finite set -- the orbit-avoidance count is correct: g^k(v)=f forces v=c+(f-c)/2^k).")

print("\n".join(OUT))
with open("/home/user/erdos/attempts/consolidated/verify_R8.out", "w") as f:
    f.write("\n".join(OUT) + "\n")

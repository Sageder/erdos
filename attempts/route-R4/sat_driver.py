"""sat_driver.py — SAT-based frontier pusher (CaDiCaL via pysat_check.solve).

For a stream (cls, C, rounding): walks N upward by `step`, solving each instance with a
wall timeout (via subprocess so timeouts are clean).
  SAT     -> witness verified by apcheck inside pysat_check, saved to avoiders/, logged;
  UNSAT   -> refine: binary-search the exact threshold in (last_SAT, first_UNSAT],
             log EXTINCT records, then stop;
  timeout -> shrink step / stop when step==1.
Appends records to results/frontier.jsonl with phase "sat".
usage: python3 sat_driver.py cls C n_start n_max step timeout_s [round]
"""

import json
import os
import subprocess
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results", "frontier.jsonl")
AVD = os.path.join(HERE, "avoiders")


def log(rec):
    with open(RES, "a") as f:
        f.write(json.dumps(rec) + "\n")


def solve(N, cls, C, rnd, timeout):
    cmd = ["python3", os.path.join(HERE, "pysat_check.py"), str(N), cls,
           str(C.numerator), str(C.denominator)]
    if rnd != "f":
        cmd.append(rnd)
    t0 = time.time()
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT", None, time.time() - t0
    line = [l for l in out.splitlines() if l.startswith("PYSAT")]
    if not line:
        return "ERROR", out, time.time() - t0
    d = dict(kv.split("=", 1) for kv in line[0].split()[1:])
    perm = [int(x) for x in d["example"].split(",")] if "example" in d else None
    return d["status"], perm, time.time() - t0


def save(cls, C, rnd, N, perm):
    suf = "_ceil" if rnd == "c" else ""
    fn = os.path.join(AVD, f"{cls}_{C.numerator}_{C.denominator}{suf}.txt")
    with open(fn, "a") as f:
        f.write(f"N={N} how=pysat perm=" + ",".join(map(str, perm)) + "\n")


def main():
    cls = sys.argv[1]
    C = Fraction(sys.argv[2])
    n, n_max = int(sys.argv[3]), int(sys.argv[4])
    step = int(sys.argv[5])
    timeout = float(sys.argv[6])
    rnd = sys.argv[7] if len(sys.argv) > 7 else "f"
    Cs = f"{C.numerator}/{C.denominator}"
    last_sat = None
    first_unsat = None
    while n <= n_max:
        st, perm, secs = solve(n, cls, C, rnd, timeout)
        rec = {"cls": cls, "C": Cs, "N": n, "phase": "sat", "secs": round(secs, 1)}
        if rnd != "f":
            rec["round"] = rnd
        if st == "SAT":
            log({**rec, "verdict": "EXISTS"})
            save(cls, C, rnd, n, perm)
            print(f"[{cls} C={Cs}{rnd if rnd != 'f' else ''}] N={n}: SAT ({secs:.0f}s)",
                  flush=True)
            last_sat = n
            n += step
        elif st == "UNSAT":
            log({**rec, "verdict": "EXTINCT"})
            print(f"[{cls} C={Cs}] N={n}: UNSAT ({secs:.0f}s)", flush=True)
            first_unsat = n
            # binary search exact threshold above last_sat
            lo = last_sat if last_sat is not None else 3
            hi = n
            while hi - lo > 1:
                mid = (lo + hi) // 2
                st2, perm2, s2 = solve(mid, cls, C, rnd, timeout)
                rec2 = {"cls": cls, "C": Cs, "N": mid, "phase": "sat",
                        "secs": round(s2, 1)}
                if rnd != "f":
                    rec2["round"] = rnd
                if st2 == "SAT":
                    log({**rec2, "verdict": "EXISTS"})
                    save(cls, C, rnd, mid, perm2)
                    lo = mid
                elif st2 == "UNSAT":
                    log({**rec2, "verdict": "EXTINCT"})
                    hi = mid
                else:
                    print(f"[{cls} C={Cs}] N={mid}: {st2} during refine — stop",
                          flush=True)
                    return
                print(f"[{cls} C={Cs}] refine: max SAT so far {lo}, min UNSAT {hi}",
                      flush=True)
            print(f"[{cls} C={Cs}] THRESHOLD: max SAT N={lo}, min UNSAT N={hi}",
                  flush=True)
            return
        elif st == "TIMEOUT":
            print(f"[{cls} C={Cs}] N={n}: SAT-timeout after {secs:.0f}s "
                  f"(step {step})", flush=True)
            if step > 1:
                step = max(1, step // 2)
                continue
            log({**rec, "verdict": "UNKNOWN"})
            return
        else:
            print(f"[{cls} C={Cs}] N={n}: ERROR {perm}", flush=True)
            return
    print(f"[{cls} C={Cs}] reached n_max={n_max}, still SAT at {last_sat}", flush=True)


if __name__ == "__main__":
    main()

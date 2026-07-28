"""d7probe.py -- can the verified depth-6 chain 1,2,4,10,46,136 be extended?
Uses the TOP-WINDOW relaxation (free variables restricted to a window of the top
block; every clause with a same-block link outside the window is DROPPED).  Dropping
clauses only weakens the system, so UNSAT of the relaxation is SOUND for the full
system, hence a genuine impossibility theorem for that cut set.
"""
import sys, time
sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import solve_window

W, U = 46, 136
for V in [406, 407, 408, 410, 420, 450, 500, 550, 600, 626, 680, 700, 750, 800]:
    for width in (120, 170, 230):
        lo = max(U + 1, V - width)
        t = time.time()
        r, info = solve_window([W, U, V], lo, V)
        print(f"[46,136,{V}] window [{lo},{V}] -> {r} [{time.time()-t:.0f}s]", flush=True)
        if r == 'UNSAT':
            break

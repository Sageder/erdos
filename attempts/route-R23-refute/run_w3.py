import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from classorder import classes_of, check
from halfblock import W3

Ns = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else
                       ["40", "60", "90", "130", "180", "250", "350"])]
for b in (3, 4, 5, 7):
    for hn, h in [("h=2", lambda M: 2), ("h=M+2", lambda M: M + 2)]:
        for N in Ns:
            c = classes_of(W3(N, b, h), N, b)
            res, _ = check(f"W3 b={b} {hn} N={N}", c, N)
            if res != "SAT":
                break

import sys
from reduce import reduce_universe
lo, N = int(sys.argv[1]), int(sys.argv[2])
A, _ = reduce_universe(N, lo=lo)
print(N, len(A))
print(" ".join(map(str, A)))

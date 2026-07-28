"""gen_universe.py N  -- emit "N K a1 a2 ... aK" (reduced universe) for bsearch."""
import sys
from reduce import reduce_universe

N = int(sys.argv[1])
A, _ = reduce_universe(N)
print(N, len(A))
print(" ".join(map(str, A)))

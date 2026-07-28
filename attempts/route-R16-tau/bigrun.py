import sys
sys.path.insert(0,'/home/user/erdos/attempts/route-R16-tau')
from level0_blocks import run
for N in (150,200,243,250,300):
    run(N, True, lambda d: d%3!=0, 'level0+contig blocks')

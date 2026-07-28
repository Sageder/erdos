#!/bin/bash
cd /home/user/erdos/attempts/route-F
D=17599117536000
python3 pool2.py 500   1000  $D 60 R1b.txt 1 200000 900000000000 0 1 > lr1b.txt 2>&1 &
python3 pool2.py 1002  2000  $D 60 R2b.txt 1 80000  900000000000 0 1 > lr2b.txt 2>&1 &
python3 pool2.py 2002  2400  $D 60 S1.txt 1 20000 400000000000 0 1 > ls1.txt 2>&1 &
python3 pool2.py 2402  2800  $D 60 S2.txt 1 20000 400000000000 0 1 > ls2.txt 2>&1 &
wait
python3 pool2.py 2802  3400  $D 60 S3.txt 1 20000 400000000000 0 1 > ls3.txt 2>&1 &
python3 pool2.py 3402  4000  $D 60 S4.txt 1 20000 400000000000 0 1 > ls4.txt 2>&1 &
python3 pool2.py 4002  4800  $D 60 S5.txt 1 20000 400000000000 0 1 > ls5.txt 2>&1 &
python3 pool2.py 4802  6460  $D 60 S6.txt 1 20000 400000000000 0 1 > ls6.txt 2>&1 &
wait

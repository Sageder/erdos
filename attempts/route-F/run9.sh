#!/bin/bash
cd /home/user/erdos/attempts/route-F
D=17599117536000
python3 pool2.py 500   1000  $D 0  R1.txt 1 120000 400000000000 0 1 > lr1.txt 2>&1 &
python3 pool2.py 1002  2000  $D 60 R2.txt 1 60000  400000000000 0 1 > lr2.txt 2>&1 &
python3 pool2.py 2002  2800  $D 60 R3.txt 1 20000  400000000000 0 1 > lr3.txt 2>&1 &
python3 pool2.py 2802  4000  $D 60 R4.txt 1 20000  400000000000 0 1 > lr4.txt 2>&1 &
wait
python3 pool2.py 4002  5600  $D 60 R5.txt 1 20000 400000000000 0 1 > lr5.txt 2>&1 &
python3 pool2.py 5602  8000  $D 60 R6.txt 1 20000 400000000000 0 1 > lr6.txt 2>&1 &
wait

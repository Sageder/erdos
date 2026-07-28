#!/bin/bash
cd /home/user/erdos/attempts/route-F
D=17599117536000
cp R1b.txt R1c.txt
python3 pool2.py 500  1000 $D 60 R1c.txt 1 150000 900000000000 0 1 768      > lr1c.txt 2>&1 &
cp R2.txt R2c.txt
python3 pool2.py 1002 2000 $D 60 R2c.txt 1 40000 900000000000 0 1 1024     > lr2c.txt 2>&1 &
python3 pool2.py 2002 2800 $D 60 R3c.txt 1 20000 400000000000 0 1          > lr3c.txt 2>&1 &
python3 pool2.py 2802 4000 $D 60 R4c.txt 1 20000 400000000000 0 1          > lr4c.txt 2>&1 &
wait

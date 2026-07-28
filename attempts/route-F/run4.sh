#!/bin/bash
cd /home/user/erdos/attempts/route-F
D=17599117536000
python3 pool2.py 806   1612  $D 60 P3.txt 1 30000 200000000000 0 1 > lp3.txt 2>&1 &
python3 pool2.py 1614  3228  $D 60 P4.txt 1 30000 200000000000 0 1 > lp4.txt 2>&1 &
python3 pool2.py 3230  6460  $D 60 P5.txt 1 30000 200000000000 0 1 > lp5.txt 2>&1 &
python3 pool2.py 6462  12924 $D 60 P6.txt 1 30000 200000000000 0 1 > lp6.txt 2>&1 &
wait

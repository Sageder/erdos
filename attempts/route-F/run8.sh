#!/bin/bash
cd /home/user/erdos/attempts/route-F
D=17599117536000
python3 pool2.py 1614  2400 $D 60 Q1.txt 1 20000 200000000000 0 1 > lq1.txt 2>&1
python3 pool2.py 2402  3228 $D 60 Q2.txt 1 20000 200000000000 0 1 > lq2.txt 2>&1
python3 pool2.py 3230  4800 $D 60 Q3.txt 1 20000 200000000000 0 1 > lq3.txt 2>&1
python3 pool2.py 4802  6460 $D 60 Q4.txt 1 20000 200000000000 0 1 > lq4.txt 2>&1
python3 pool2.py 9602 12924 $D 60 Q6.txt 1 20000 200000000000 0 1 > lq6.txt 2>&1

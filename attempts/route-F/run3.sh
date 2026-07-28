#!/bin/bash
cd /home/user/erdos/attempts/route-F
D=17599117536000
python3 pool2.py 806   1612  $D 60 P3.txt 10 3000 6000000000 0.45 0.90 > lp3.txt 2>&1 &
python3 pool2.py 1614  3228  $D 60 P4.txt 10 3000 6000000000 0.55 0.95 > lp4.txt 2>&1 &
python3 pool2.py 3230  6460  $D 60 P5.txt 10 3000 6000000000 0.50 0.95 > lp5.txt 2>&1 &
python3 pool2.py 6462  12924 $D 60 P6.txt 10 3000 6000000000 0.55 0.95 > lp6.txt 2>&1 &
wait
python3 pool2.py 12926 25852 $D 60 P7.txt 10 3000 6000000000 0.45 0.95 > lp7.txt 2>&1 &
python3 pool2.py 25854 51708 $D 60 P8.txt 10 3000 6000000000 0.40 0.95 > lp8.txt 2>&1 &
wait

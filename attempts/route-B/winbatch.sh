#!/bin/bash
cd /home/user/erdos/attempts/route-B
for w in "22 220" "24 240" "26 260" "30 330" "33 330" "35 350" "38 380" "40 400" "42 420" "45 450" "30 400" "40 500" "35 450" "25 300" "20 250" "28 350"; do
  set -- $w
  u=u_w$1_$2.txt
  [ -s $u ] || python3 gen_window.py $1 $2 > $u
  timeout 900 ./bsearch 300 < $u 2>/dev/null | grep '^SOL' > pool/w$1_$2.txt
  echo "lo=$1 N=$2 -> $(grep -c SOL pool/w$1_$2.txt)"
done

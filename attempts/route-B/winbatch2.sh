#!/bin/bash
cd /home/user/erdos/attempts/route-B
for w in "30 255" "35 265" "35 280" "40 320" "45 340" "45 360" "50 370" "50 400" "50 425" "55 400" "60 426" "60 450" "65 480" "70 500" "70 574" "80 584" "25 230" "28 250" "32 260" "38 290" "42 330" "48 380" "58 440" "75 560"; do
  set -- $w
  u=u_w$1_$2.txt
  [ -s $u ] || python3 gen_window.py $1 $2 > $u
  timeout 400 ./bsearch 200 < $u 2>/dev/null | grep '^SOL' > pool/w$1_$2.txt
  echo "lo=$1 N=$2 -> $(grep -c SOL pool/w$1_$2.txt)"
done
echo DONE

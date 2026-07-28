#!/bin/bash
cd /home/user/erdos/attempts/route-B
for w in "55 420" "56 430" "54 410" "57 430"; do
  set -- $w
  u=u_w$1_$2.txt
  [ -s "$u" ] || python3 gen_window.py "$1" "$2" > "$u"
  for b in 91 92 93 95; do
    for sd in 5 13 29 61 97; do
      timeout 60 ./hunt $((sd*100+b)) 200000 $b 10 < "$u" 2>/dev/null | grep '^SOL' >> "pool/f$1_$2.txt"
    done
  done
  echo "lo=$1 N=$2 -> $(grep -c SOL "pool/f$1_$2.txt" 2>/dev/null)"
done
echo KFOCUSDONE

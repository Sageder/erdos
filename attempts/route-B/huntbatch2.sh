#!/bin/bash
# Randomised certificate hunt on large windows, to push the realisable k upwards.
cd /home/user/erdos/attempts/route-B
for w in "50 370" "55 400" "60 426" "60 450" "65 480" "70 500" "70 574" "45 360" "48 380" "52 400"; do
  set -- $w
  u=u_w$1_$2.txt
  [ -s "$u" ] || python3 gen_window.py "$1" "$2" > "$u"
  for b in 90 92 94; do
    for sd in 3 17; do
      timeout 100 ./hunt $((b * 31 + sd)) 300000 $b 15 < "$u" 2>/dev/null | grep '^SOL' >> "pool/h$1_$2.txt"
    done
  done
  echo "lo=$1 N=$2 -> $(grep -c SOL "pool/h$1_$2.txt" 2>/dev/null)"
done
echo HUNTDONE

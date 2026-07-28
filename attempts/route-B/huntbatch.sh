#!/bin/bash
cd /home/user/erdos/attempts/route-B
for w in "45 340" "50 370" "55 400" "60 426" "60 450" "65 480" "70 500" "70 574" "80 584" "90 650"; do
  set -- $w
  u=u_w$1_$2.txt
  [ -s $u ] || python3 gen_window.py $1 $2 > $u
  # skip windows whose lcm would overflow 128 bits (bsearch prints the bit length)
  bits=$(head -1 <(echo "" | ./bsearch 0 < $u 2>/dev/null) | grep -o '([0-9]* bits)' | grep -o '[0-9]*')
  for b in 90 92 94; do
    timeout 120 ./hunt $((b*7+1)) 400000 $b 25 < $u 2>/dev/null | grep '^SOL' >> pool/h$1_$2.txt
  done
  echo "lo=$1 N=$2 Lbits=$bits -> $(grep -c SOL pool/h$1_$2.txt 2>/dev/null)"
done
echo HUNTDONE

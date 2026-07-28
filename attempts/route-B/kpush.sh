#!/bin/bash
# Push the realisable block count k upwards: randomised hunt (bias ~92, which is the
# setting that works on dense windows) over windows [lo,N] with N/lo ~ 7.5, i.e.
# reduced total reciprocal sum ~1.2-1.4.  One process only.
cd /home/user/erdos/attempts/route-B
for w in "55 420" "60 460" "65 500" "70 540" "48 380" "52 400" "58 440" "62 470" "75 570" "80 600"; do
  set -- $w
  u=u_w$1_$2.txt
  [ -s "$u" ] || python3 gen_window.py "$1" "$2" > "$u"
  for sd in 11 23 47 91; do
    timeout 90 ./hunt $sd 250000 92 12 < "$u" 2>/dev/null | grep '^SOL' >> "pool/k$1_$2.txt"
  done
  echo "lo=$1 N=$2 -> $(grep -c SOL "pool/k$1_$2.txt" 2>/dev/null)"
done
echo KPUSHDONE

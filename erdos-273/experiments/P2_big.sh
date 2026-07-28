#!/bin/sh
# P2_big.sh -- targeted exact/certificate search for THE PIVOT on large highly-composite lattices.
# Each L is decided by P2_exact2 (exhaustive, with node cap); SAT would be a pivot certificate.
D=/home/user/erdos/erdos-273/experiments
for L in 720720 1081080 1441440 2162160 4324320 6486480 12972960; do
  echo "########## L = $L"
  timeout 2400 $D/P2_exact2 $L $L --nodes 3000000000 --work 2000000 2>&1 | grep -vE "^# (P2_exact2|minm|coverings)" 
done

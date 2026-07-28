#!/bin/sh
# route-D Q3 sweep: is 1/N in B(T) with all elements <= X ?
D=/home/user/erdos/attempts/route-D
X=$1
for T in 2 5 10 20 40; do
  for N in 2 3 4 5 6 7 8 9 10 12 14 15 16 18 20 21 24 28 30 35 36 40 42 45 48 56 60 70 84 90 100 120 210 2520; do
    R=$($D/btarget $T $X 1 $N 1 2>/dev/null | tail -2 | tr '\n' ' ')
    case "$R" in
      *SOLUTION*) echo "T=$T X=$X  1/$N : YES  $R";;
      *"does not divide"*) echo "T=$T X=$X  1/$N : no (den does not divide lcm)";;
      *) echo "T=$T X=$X  1/$N : NO   $R";;
    esac
  done
done

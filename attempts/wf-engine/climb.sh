#!/bin/bash
# climb.sh T Nstart Nstop Nstep SECS  -- from just above the exhaustive
# threshold Nmin(T), walk N upwards; the tightest feasible window (maxsum only
# just above the target) has the smallest search tree, so the first N that
# admits a solution is usually found fastest this way.
cd "$(dirname "$0")"
T=$1; A=$2; B=$3; S=$4; SECS=${5:-90}; K=${K:-30}
for ((N=A; N<=B; N+=S)); do
  P="w_${T}_${N}.prob"
  [ -f "$P" ] || python3 prune.py "$T" "$N" 1 1 -o "$P" >/dev/null
  OUT=$(timeout $((SECS + 30)) ./esearch "$P" -k "$K" -m 1 -t "$SECS" 2>&1)
  SOL=$(echo "$OUT" | grep -m1 '^SOL')
  if [ -n "$SOL" ]; then
    echo "FOUND T=$T N=$N | $(echo "$OUT" | head -1)"
    echo "$SOL" >> found.txt
    exit 0
  fi
  echo "none  T=$T N=$N | $(echo "$OUT" | head -1) | $(echo "$OUT" | tail -1)"
done
echo "exhausted range for T=$T"

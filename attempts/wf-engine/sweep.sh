#!/bin/bash
# sweep.sh -- for each (T,N) pair on stdin ("T N"), prune the range and run the
# exact target-1 search for $SECS seconds, logging the outcome.
# usage: echo "45 345" | SECS=120 MODE=det ./sweep.sh   (MODE=det|rand)
cd "$(dirname "$0")"
SECS=${SECS:-120}
MODE=${MODE:-det}
K=${K:-30}
while read -r T N; do
  [ -z "$T" ] && continue
  P="w_${T}_${N}.prob"
  [ -f "$P" ] || python3 prune.py "$T" "$N" 1 1 -o "$P" >/dev/null
  if [ "$MODE" = rand ]; then
    OUT=$(timeout $((SECS + 20)) ./esearch "$P" -k "$K" -m 1 -R "${SEED:-1}" -B "${BUD:-20000000}" -t "$SECS" 2>&1)
  else
    OUT=$(timeout $((SECS + 20)) ./esearch "$P" -k "$K" -m 1 -t "$SECS" 2>&1)
  fi
  SOL=$(echo "$OUT" | grep -m1 '^SOL')
  HEAD=$(echo "$OUT" | head -1)
  if [ -n "$SOL" ]; then
    echo "FOUND T=$T N=$N | $HEAD"
    echo "$SOL" >> found.txt
  else
    echo "none  T=$T N=$N | $HEAD | $(echo "$OUT" | tail -1)"
  fi
done

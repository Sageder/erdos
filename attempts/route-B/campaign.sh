#!/bin/bash
# campaign.sh -- certificate-collection campaign.
# For a list of windows [lo,N] it builds the reduced universe of the class
# {U legal, sum 1/n = 1, lo <= min(U), max(U) <= N} and runs the exhaustive DFS
# with a solution cap and a wall-clock cap, appending every certificate to pool/.
# Windows are a RESTRICTED class (min(U) >= lo); certificates found are of course
# unconditionally valid, only the absence of them would be class-relative.
cd "$(dirname "$0")"
mkdir -p pool
run() {  # lo N timeout cap
  lo=$1; N=$2; TO=$3; CAP=$4
  f=pool/w${lo}_${N}.txt
  [ -f u_w${lo}_${N}.txt ] || python3 gen_window.py $lo $N > u_w${lo}_${N}.txt
  timeout $TO ./bsearch $CAP < u_w${lo}_${N}.txt 2>/dev/null | grep '^SOL' >> $f
  echo "window lo=$lo N=$N -> $(grep -c SOL $f 2>/dev/null || echo 0) certificates"
}
export -f run
"$@"

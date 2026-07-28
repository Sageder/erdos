#!/bin/bash
cd /home/user/erdos/attempts/route-B
lo=$1; N=$2; TO=$3; CAP=$4
u=u_w${lo}_${N}.txt
[ -s $u ] || python3 gen_window.py $lo $N > $u
timeout $TO ./bsearch $CAP < $u 2>/dev/null | grep '^SOL' > pool/w${lo}_${N}.txt
echo "lo=$lo N=$N : $(grep -c SOL pool/w${lo}_${N}.txt 2>/dev/null)"

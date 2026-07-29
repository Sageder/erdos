import re
s = open('mine.c').read()
s = s.replace('''        if(!bcount[bi]) continue;
        int k1,k2;
        for(k1=kmin;k1<=kmax;k1++)for(k2=kmin;k2<=kmax;k2++){
            if(k1==k2) continue;
            int i1=k1+2,i2=k2+2;
            if(seenLT[bi][i1][i2] && !seenLT[bi][i2][i1]){
                printf("F tp=%d tq=%d ord=%d rat=%d cons=%d m=%d kmin=%d kmax=%d cnt=%lld : %d < %d\\n",
                       tp,tq,ord,rat,cons,m,kmin,kmax,bcount[bi],k1,k2);
            }
        }''','''        if(!bcount[bi]) continue;
        printf("B %d %d %d %d %d %d %d %d %lld ",tp,tq,ord,rat,cons,m,kmin,kmax,bcount[bi]);
        int k1,k2;
        for(k1=kmin;k1<=kmax;k1++)for(k2=kmin;k2<=kmax;k2++){
            if(k1==k2) continue;
            int i1=k1+2,i2=k2+2;
            if(seenLT[bi][i1][i2]) printf("%d,%d;",k1,k2);
        }
        printf("\\n");''')
open('mine.c','w').write(s)

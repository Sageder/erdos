/* P2_front.c -- the HONEST FRONTIER of local (fiber) elimination for THE PIVOT.
 *
 * For a lattice L let S(L) = {m | L : m >= MINM, 2m+1 prime}.  For a finite set Q of primes put
 *        B_Q(L) = sum over m in S(L) with gcd(m, prod Q) = 1 of 1/m .
 * PROVED (one line): every such m has nu_q(m) = 0 for all q in Q, hence contributes 1/m to EVERY
 * Q-fiber whatever the residue assignment; therefore  Phi_Q(S(L)) >= B_Q(L).  So if B_Q(L) >= 1
 * the necessary condition "Phi_Q >= 1" is VACUOUS -- the Q-local test can never eliminate L.
 *
 * Route D's barrier says sum_{m in H, (m, prod Q)=1} 1/m diverges for every fixed finite Q, so as
 * L becomes divisible by more and more primes every fixed-Q test must eventually go vacuous.
 * This program measures WHERE, honestly:
 *   for every L <= LMAX with budget(S(L)) > 1 it reports min over single primes q | L of B_q(L),
 *   min over pairs, min over triples, and the running fraction of candidates that still have
 *   SOME non-vacuous local test of each size.
 *
 * usage: ./P2_front LMAX [--minm M]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    setbuf(stdout, NULL);
    long LMAX = 300000, MINM = 3;
    if (argc > 1) LMAX = atol(argv[1]);
    for (int i = 2; i < argc; i++) if (!strcmp(argv[i],"--minm") && i+1<argc) MINM = atol(argv[++i]);
    long lim = 2*LMAX+2;
    unsigned char *isp = malloc(lim+1); memset(isp,1,lim+1); isp[0]=isp[1]=0;
    for (long i=2;i*i<=lim;i++) if (isp[i]) for (long j=i*i;j<=lim;j+=i) isp[j]=0;
    unsigned char *inH = malloc(LMAX+1);
    for (long m=0;m<=LMAX;m++) inH[m] = (m>=MINM && isp[2*m+1]);
    double *bud = calloc(LMAX+1,sizeof(double));
    for (long m=MINM;m<=LMAX;m++) if (inH[m]) { double r=1.0/m; for (long t=m;t<=LMAX;t+=m) bud[t]+=r; }

    printf("# P2_front  LMAX = %ld  minm = %ld\n", LMAX, MINM);
    printf("# B_Q(L) = sum of 1/m over m in S(L) coprime to Q ;  Phi_Q >= B_Q, so B_Q >= 1 == test dead\n");
    long ncand=0, alive1=0, alive2=0, alive3=0;
    long first_dead1=0, first_dead2=0, first_dead3=0;
    long ck[8] = {1000,3000,10000,30000,100000,300000,1000000,0};
    int ckn = 0;
    long S[8192];
    for (long L = 6; L <= LMAX; L++) {
        if (bud[L] <= 1.0) goto checkpoint;
        {
        int ns=0; double b=0;
        for (long d=1; d*d<=L; d++) if (L%d==0) { long e=L/d;
            if (inH[d]) { S[ns++]=d; b += 1.0/d; }
            if (e!=d && inH[e]) { S[ns++]=e; b += 1.0/e; } }
        if (!ns || b <= 1.0) goto checkpoint;
        ncand++;
        long P[32]; int np=0; long t=L;
        for (long q=2;q*q<=t;q++) if (t%q==0) { P[np++]=q; while(t%q==0) t/=q; }
        if (t>1) P[np++]=t;
        double m1=1e9, m2=1e9, m3=1e9;
        for (int a=0;a<np;a++) { double s=0;
            for (int i=0;i<ns;i++) if (S[i]%P[a]) s += 1.0/S[i];
            if (s<m1) m1=s;
            for (int c=a+1;c<np;c++) { double s2=0;
                for (int i=0;i<ns;i++) if (S[i]%P[a] && S[i]%P[c]) s2 += 1.0/S[i];
                if (s2<m2) m2=s2;
                for (int d2=c+1;d2<np;d2++) { double s3=0;
                    for (int i=0;i<ns;i++) if (S[i]%P[a] && S[i]%P[c] && S[i]%P[d2]) s3 += 1.0/S[i];
                    if (s3<m3) m3=s3; } } }
        if (m1 < 1.0) alive1++; else if (!first_dead1) first_dead1 = L;
        if (np>=2) { if (m2 < 1.0) alive2++; else if (!first_dead2) first_dead2 = L; }
        else alive2++;
        if (np>=3) { if (m3 < 1.0) alive3++; else if (!first_dead3) first_dead3 = L; }
        else alive3++;
        }
      checkpoint:
        if (ckn < 7 && ck[ckn] && L == ck[ckn]) {
            printf("  L <= %8ld : candidates %6ld ; single-prime test alive %6ld (%5.1f%%) ; "
                   "pair alive %6ld (%5.1f%%) ; triple alive %6ld (%5.1f%%)\n",
                   L, ncand, alive1, 100.0*alive1/(ncand?ncand:1),
                   alive2, 100.0*alive2/(ncand?ncand:1), alive3, 100.0*alive3/(ncand?ncand:1));
            ckn++;
        }
    }
    printf("\n# TOTAL candidates (budget>1) up to %ld : %ld\n", LMAX, ncand);
    printf("# single-prime local test non-vacuous for %ld of them; first L where EVERY single-prime\n"
           "#   test is vacuous: %ld\n", alive1, first_dead1);
    printf("# pair   test first vacuous at L = %ld ;  triple test first vacuous at L = %ld\n",
           first_dead2, first_dead3);
    return 0;
}

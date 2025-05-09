#!/usr/bin/env python3
import sys, time, resource, re

delta = 30
alpha = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}
}

def parse_input(path):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    s1 = lines[0]
    for i in range(1, len(lines)):
        if re.fullmatch(r"[ACGT]+", lines[i]):
            s2_idx = i
            break
    indices1 = list(map(int, lines[1:s2_idx]))
    s2 = lines[s2_idx]
    indices2 = list(map(int, lines[s2_idx+1:]))
    return s1, indices1, s2, indices2


def generate(base, indices):
    s = base
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s


def nw_score(A, B):
    # Needleman-Wunsch score vector (last row) in linear space
    prev = [j * delta for j in range(len(B) + 1)]
    for i in range(1, len(A) + 1):
        curr = [i * delta] + [0] * len(B)
        for j in range(1, len(B) + 1):
            cost = alpha[A[i-1]][B[j-1]]
            curr[j] = min(prev[j-1] + cost, prev[j] + delta, curr[j-1] + delta)
        prev = curr
    return prev


def hirschberg(A, B):
    m, n = len(A), len(B)
    if m == 0:
        return '-'*n, B
    if n == 0:
        return A, '-'*m
    if m == 1 or n == 1:
        # fallback to basic DP for small cases
        # reuse basic_align on single-character edge-case
        from itertools import product
        best = (float('inf'), '', '')
        # brute-force all possible alignments for one-length
        # but simpler: call full DP
        # build full DP table
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1): dp[i][0] = i*delta
        for j in range(1, n+1): dp[0][j] = j*delta
        for i in range(1, m+1):
            for j in range(1, n+1):
                cost = alpha[A[i-1]][B[j-1]]
                dp[i][j] = min(dp[i-1][j-1]+cost, dp[i-1][j]+delta, dp[i][j-1]+delta)
        # backtrack as in basic
        i, j = m, n
        X1, X2 = [], []
        while i>0 and j>0:
            if dp[i][j] == dp[i-1][j-1] + alpha[A[i-1]][B[j-1]]:
                X1.append(A[i-1]); X2.append(B[j-1]); i-=1; j-=1
            elif dp[i][j] == dp[i-1][j] + delta:
                X1.append(A[i-1]); X2.append('-'); i-=1
            else:
                X1.append('-'); X2.append(B[j-1]); j-=1
        while i>0:
            X1.append(A[i-1]); X2.append('-'); i-=1
        while j>0:
            X1.append('-'); X2.append(B[j-1]); j-=1
        return ''.join(reversed(X1)), ''.join(reversed(X2))
    else:
        i_mid = m // 2
        scoreL = nw_score(A[:i_mid], B)
        scoreR = nw_score(A[i_mid:][::-1], B[::-1])
        # find partition point
        j_mid = min(range(len(B)+1), key=lambda j: scoreL[j] + scoreR[len(B)-j])
        A_left, B_left = hirschberg(A[:i_mid], B[:j_mid])
        A_right, B_right = hirschberg(A[i_mid:], B[j_mid:])
        return A_left + A_right, B_left + B_right


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <input.txt> <output.txt>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    s1, idx1, s2, idx2 = parse_input(inp)
    X = generate(s1, idx1)
    Y = generate(s2, idx2)
    start = time.time()
    A1, A2 = hirschberg(X, Y)
    end = time.time()
    # compute cost
    cost = 0
    for a, b in zip(A1, A2):
        if a == '-' or b == '-': cost += delta
        else: cost += alpha[a][b]
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t_ms = (end - start) * 1000
    with open(outp, 'w') as f:
        f.write(f"{cost}\n{A1}\n{A2}\n{t_ms:.3f}\n{mem}\n")

if __name__ == '__main__':
    main()
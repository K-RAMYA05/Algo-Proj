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
    # find the start of second base string (first pure-letters after the initial)
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
        # insert full copy of current s after position idx (0-based)
        s = s[:idx+1] + s + s[idx+1:]
    return s


def basic_align(X, Y):
    m, n = len(X), len(Y)
    dp = [[0]*(n+1) for _ in range(m+1)]
    # initialize
    for i in range(1, m+1): dp[i][0] = i * delta
    for j in range(1, n+1): dp[0][j] = j * delta
    # fill
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = alpha[X[i-1]][Y[j-1]]
            dp[i][j] = min(
                dp[i-1][j-1] + cost,
                dp[i-1][j]   + delta,
                dp[i][j-1]   + delta
            )
    # backtrack
    i, j = m, n
    A1, A2 = [], []
    while i > 0 and j > 0:
        if dp[i][j] == dp[i-1][j-1] + alpha[X[i-1]][Y[j-1]]:
            A1.append(X[i-1]); A2.append(Y[j-1]); i -= 1; j -= 1
        elif dp[i][j] == dp[i-1][j] + delta:
            A1.append(X[i-1]); A2.append('-');       i -= 1
        else:
            A1.append('-');       A2.append(Y[j-1]); j -= 1
    while i > 0:
        A1.append(X[i-1]); A2.append('-'); i -= 1
    while j > 0:
        A1.append('-'); A2.append(Y[j-1]); j -= 1
    return dp[m][n], ''.join(reversed(A1)), ''.join(reversed(A2))


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <input.txt> <output.txt>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    s1, idx1, s2, idx2 = parse_input(inp)
    X = generate(s1, idx1)
    Y = generate(s2, idx2)
    start = time.time()
    cost, A1, A2 = basic_align(X, Y)
    end = time.time()
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t_ms = (end - start) * 1000
    with open(outp, 'w') as f:
        f.write(f"{cost}\n{A1}\n{A2}\n{t_ms:.3f}\n{mem}\n")

if __name__ == '__main__':
    main()
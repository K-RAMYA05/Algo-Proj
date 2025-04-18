import sys
import time
import psutil

def process_memory():
    process = psutil.Process()
    mem_info = process.memory_info()
    return float(mem_info.rss) / 1024  # Convert bytes to KB

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines[0], lines[1]

def write_output(file_path, cost, aligned_s1, aligned_s2, time_ms, memory_kb):
    with open(file_path, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{aligned_s1}\n")
        f.write(f"{aligned_s2}\n")
        f.write(f"{time_ms:.3f}\n")
        f.write(f"{memory_kb:.3f}\n")

def mismatch_cost_fn(a, b):
    cost_table = {
        'AA': 0, 'CC': 0, 'GG': 0, 'TT': 0,
        'AC': 110, 'AG': 48, 'AT': 94,
        'CA': 110, 'CG': 118, 'CT': 48,
        'GA': 48, 'GC': 118, 'GT': 110,
        'TA': 94, 'TC': 48, 'TG': 110
    }
    if a == '-' or b == '-':
        return 30
    return cost_table.get(a + b, cost_table.get(b + a, 0))

def compute_cost(X, Y):
    prev = [i * 30 for i in range(len(Y) + 1)]
    for i in range(1, len(X) + 1):
        curr = [i * 30]
        for j in range(1, len(Y) + 1):
            match = prev[j - 1] + mismatch_cost_fn(X[i - 1], Y[j - 1])
            delete = prev[j] + 30
            insert = curr[j - 1] + 30
            curr.append(min(match, delete, insert))
        prev = curr
    return prev

def hirschberg(X, Y):
    if len(X) == 0:
        return '-' * len(Y), Y
    if len(Y) == 0:
        return X, '-' * len(X)
    if len(X) == 1 or len(Y) == 1:
        return basic_alignment(X, Y)

    xmid = len(X) // 2

    scoreL = compute_cost(X[:xmid], Y)
    scoreR = compute_cost(X[xmid:][::-1], Y[::-1])
    total = [l + r for l, r in zip(scoreL, scoreR[::-1])]
    ymid = total.index(min(total))

    left_X, left_Y = hirschberg(X[:xmid], Y[:ymid])
    right_X, right_Y = hirschberg(X[xmid:], Y[ymid:])

    return left_X + right_X, left_Y + right_Y

def basic_alignment(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * 30
    for j in range(n + 1):
        dp[0][j] = j * 30

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = mismatch_cost_fn(X[i - 1], Y[j - 1])
            dp[i][j] = min(dp[i - 1][j - 1] + cost,
                           dp[i - 1][j] + 30,
                           dp[i][j - 1] + 30)

    aligned_X, aligned_Y = '', ''
    i, j = m, n
    while i > 0 and j > 0:
        cost = mismatch_cost_fn(X[i - 1], Y[j - 1])
        if dp[i][j] == dp[i - 1][j - 1] + cost:
            aligned_X = X[i - 1] + aligned_X
            aligned_Y = Y[j - 1] + aligned_Y
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + 30:
            aligned_X = X[i - 1] + aligned_X
            aligned_Y = '-' + aligned_Y
            i -= 1
        else:
            aligned_X = '-' + aligned_X
            aligned_Y = Y[j - 1] + aligned_Y
            j -= 1

    while i > 0:
        aligned_X = X[i - 1] + aligned_X
        aligned_Y = '-' + aligned_Y
        i -= 1
    while j > 0:
        aligned_X = '-' + aligned_X
        aligned_Y = Y[j - 1] + aligned_Y
        j -= 1

    return aligned_X, aligned_Y

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    s1, s2 = read_input(input_file)

    start_time = time.time()
    aligned_s1, aligned_s2 = hirschberg(s1, s2)
    cost = sum(mismatch_cost_fn(a, b) for a, b in zip(aligned_s1, aligned_s2))
    end_time = time.time()
    time_ms = (end_time - start_time) * 1000
    memory_kb = process_memory()

    write_output(output_file, cost, aligned_s1, aligned_s2, time_ms, memory_kb)

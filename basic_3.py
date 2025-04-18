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

def min_cost_alignment(s1, s2, gap_cost=30, mismatch_cost= {'AA': 0, 'CC': 0, 'GG': 0, 'TT': 0,
                                                              'AC': 110, 'AG': 48, 'AT': 94,
                                                              'CA': 110, 'CG': 118, 'CT': 48,
                                                              'GA': 48, 'GC': 118, 'GT': 110,
                                                              'TA': 94, 'TC': 48, 'TG': 110}):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i * gap_cost
    for j in range(n+1):
        dp[0][j] = j * gap_cost

    for i in range(1, m+1):
        for j in range(1, n+1):
            char1 = s1[i-1]
            char2 = s2[j-1]
            cost_match = mismatch_cost.get(char1+char2, mismatch_cost.get(char2+char1, 0))
            dp[i][j] = min(
                dp[i-1][j-1] + cost_match,
                dp[i-1][j] + gap_cost,
                dp[i][j-1] + gap_cost
            )

    aligned_s1 = ''
    aligned_s2 = ''
    i, j = m, n

    while i > 0 and j > 0:
        char1 = s1[i-1]
        char2 = s2[j-1]
        cost_match = mismatch_cost.get(char1+char2, mismatch_cost.get(char2+char1, 0))
        if dp[i][j] == dp[i-1][j-1] + cost_match:
            aligned_s1 = char1 + aligned_s1
            aligned_s2 = char2 + aligned_s2
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j] + gap_cost:
            aligned_s1 = char1 + aligned_s1
            aligned_s2 = '-' + aligned_s2
            i -= 1
        else:
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = char2 + aligned_s2
            j -= 1

    while i > 0:
        aligned_s1 = s1[i-1] + aligned_s1
        aligned_s2 = '-' + aligned_s2
        i -= 1
    while j > 0:
        aligned_s1 = '-' + aligned_s1
        aligned_s2 = s2[j-1] + aligned_s2
        j -= 1

    return dp[m][n], aligned_s1, aligned_s2

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    s1, s2 = read_input(input_file)

    start_time = time.time()
    cost, aligned_s1, aligned_s2 = min_cost_alignment(s1, s2)
    end_time = time.time()
    time_ms = (end_time - start_time) * 1000
    memory_kb = process_memory()

    write_output(output_file, cost, aligned_s1, aligned_s2, time_ms, memory_kb)

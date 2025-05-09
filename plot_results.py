#!/usr/bin/env python3
import glob, subprocess, re, matplotlib.pyplot as plt

# Parse input file to compute total sequence length
def parse_input(path):
    import re
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    s1 = lines[0]
    # locate where second base string starts
    for i in range(1, len(lines)):
        if re.fullmatch(r"[ACGT]+", lines[i]):
            s2_idx = i
            break
    indices1 = list(map(int, lines[1:s2_idx]))
    s2 = lines[s2_idx]
    indices2 = list(map(int, lines[s2_idx+1:]))
    # generate full sequences
    s = s1
    for idx in indices1:
        s = s[:idx+1] + s + s[idx+1:]
    t = s2
    for idx in indices2:
        t = t[:idx+1] + t + t[idx+1:]
    return len(s) + len(t)

# Collect inputs
inputs = sorted(glob.glob('datapoints/in*.txt'), key=lambda x: int(re.search(r'in(\d+)', x).group(1)))
sizes = []
t_basic, t_efficient = [], []
m_basic, m_efficient = [], []

for inp in inputs:
    size = parse_input(inp)
    sizes.append(size)
    # Basic: call the Python alignment script directly
    outb = 'temp_basic.txt'
    subprocess.run(['python3', 'basic_3.py', inp, outb], check=True)
    with open(outb) as f:
        lines = f.read().splitlines()
    t_basic.append(float(lines[3]))
    m_basic.append(float(lines[4]))
    # Efficient: call the Python alignment script directly
    oute = 'temp_efficient.txt'
    subprocess.run(['python3', 'efficient_3.py', inp, oute], check=True)
    with open(oute) as f:
        lines = f.read().splitlines()
    t_efficient.append(float(lines[3]))
    m_efficient.append(float(lines[4]))

# Plot CPU time comparison
plt.figure()
plt.plot(sizes, t_basic, label='Basic', marker='o')
plt.plot(sizes, t_efficient, label='Efficient', marker='o')
plt.xlabel('Problem size (m+n)')
plt.ylabel('CPU time (ms)')
plt.title('CPU time vs Problem Size')
plt.legend()
plt.savefig('time_plot.png')

# Plot Memory usage comparison
plt.figure()
plt.plot(sizes, m_basic, label='Basic', marker='o')
plt.plot(sizes, m_efficient, label='Efficient', marker='o')
plt.xlabel('Problem size (m+n)')
plt.ylabel('Memory usage (KB)')
plt.title('Memory usage vs Problem Size')
plt.legend()
plt.savefig('memory_plot.png')

print('Plots saved as time_plot.png and memory_plot.png')
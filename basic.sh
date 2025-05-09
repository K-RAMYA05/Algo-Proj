#!/bin/bash

# Create output directory
mkdir -p outputs_basic

# Process all input files
for i in {1..15}; do
  input="datapoints/in${i}.txt"
  output="outputs_basic/out_basic_${i}.txt"
  echo "Processing ${input} -> ${output}"
  python3 basic_3.py "${input}" "${output}"
done

echo "Basic processing completed. Outputs in outputs_basic/"
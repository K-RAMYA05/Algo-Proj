#!/bin/bash

# Create output directory
mkdir -p outputs_efficient

# Process all input files
for i in {1..15}; do
  input="datapoints/in${i}.txt"
  output="outputs_efficient/out_efficient_${i}.txt"
  echo "Processing ${input} -> ${output}"
  python3 efficient_3.py "${input}" "${output}"
done

echo "Efficient processing completed. Outputs in outputs_efficient/"
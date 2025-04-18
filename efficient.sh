# efficient.sh
#!/bin/bash
outdir=$(dirname "$2")
mkdir -p "$outdir"
python3 efficient_3.py "$1" "$2"

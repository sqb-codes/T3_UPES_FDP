# Count Frequency of Each Character

import sys

for line in sys.stdin:
    # strip() - remove leading and trailing white spaces
    for char in line.strip():
        if char.isalnum():
            print(f"{char}\t1")
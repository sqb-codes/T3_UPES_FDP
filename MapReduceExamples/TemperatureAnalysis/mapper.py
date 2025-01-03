# Find max temperature for each year
'''
Input
2021,45
2021,42
2022,39
2022,40
2023,47
2023,41

Output
2021 45
2022 40
2023 47
'''

import sys

for line in sys.stdin:
    year, temp = line.strip().split(",")
    print(f"{year}\t{temp}")
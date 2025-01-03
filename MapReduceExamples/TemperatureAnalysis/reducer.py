import sys
from itertools import groupby
from operator import itemgetter

def read_mapper_output(file):
    for line in file:
        yield line.strip().split("\t",1)

data = read_mapper_output(sys.stdin)

for year, group in groupby(data, itemgetter(0)):
    temps = [int(temp) for i, temp in group]
    print(f"{year}\t{max(temps)}")
import sys
from itertools import groupby
from operator import itemgetter

def read_mapper_output(file):
    for line in file:
        yield line.strip().split("\t",1)

data = read_mapper_output(sys.stdin)
for char, group in groupby(data, itemgetter(0)):
    try:
        total = sum(int(count) for i, count in group)
        print(f"{char}\t{total}")
    except BaseException as ex:
        print(ex)
        continue

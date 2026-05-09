#!/usr/bin/python3
# Item le plus vendu selon CA
import sys

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        try:
            float(cost)
            print("{0}\t{1}".format(item, cost))
        except ValueError:
            continue
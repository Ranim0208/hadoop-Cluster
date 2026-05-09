#!/usr/bin/python3
# Moyenne de vente par store
import sys

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        try:
            float(cost)
            print("{0}\t{1}".format(store, cost))
        except ValueError:
            continue
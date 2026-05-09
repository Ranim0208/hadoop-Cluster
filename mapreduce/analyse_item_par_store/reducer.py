#!/usr/bin/python3
# Moyenne de vente par store
import sys

oldKey = None
total = 0
count = 0

for line in sys.stdin:
    try:
        data = line.strip().split("\t")
        if len(data) != 2:
            continue
        thisKey, thisSale = data
        thisSale = float(thisSale)
        if oldKey and oldKey != thisKey:
            print("{0}\t{1:.2f}".format(oldKey, total/count))
            oldKey = thisKey
            total = 0
            count = 0
        oldKey = thisKey
        total += thisSale
        count += 1
    except ValueError:
        continue

if oldKey:
    print("{0}\t{1:.2f}".format(oldKey, total/count))
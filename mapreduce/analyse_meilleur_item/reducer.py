#!/usr/bin/python3
# Item le plus vendu selon CA
import sys

oldKey = None
salesTotal = 0
best_item = None
best_total = 0

for line in sys.stdin:
    try:
        data = line.strip().split("\t")
        if len(data) != 2:
            continue
        thisKey, thisSale = data
        thisSale = float(thisSale)
        if oldKey and oldKey != thisKey:
            if salesTotal > best_total:
                best_total = salesTotal
                best_item = oldKey
            oldKey = thisKey
            salesTotal = 0
        oldKey = thisKey
        salesTotal += thisSale
    except ValueError:
        continue

if oldKey:
    if salesTotal > best_total:
        best_total = salesTotal
        best_item = oldKey

print("{0}\t{1:.2f}".format(best_item, best_total))
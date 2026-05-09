#!/usr/bin/python3
# Calcule le chiffre d'affaires total par item

import sys

oldKey = None
salesTotal = 0

for line in sys.stdin:
    try:
        line = line.strip()
        data = line.split("\t")
        if len(data) != 2:
            continue
        thisKey, thisSale = data
        thisSale = float(thisSale)
        if oldKey and oldKey != thisKey:
            print("{0}\t{1:.2f}".format(oldKey, salesTotal))
            oldKey = thisKey
            salesTotal = 0
        oldKey = thisKey
        salesTotal += thisSale
    except ValueError:
        continue

if oldKey:
    print("{0}\t{1:.2f}".format(oldKey, salesTotal))
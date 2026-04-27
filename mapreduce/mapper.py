#!/usr/bin/python3
# Format: date\ttime\tstore\titem\tcost\tpayment
# On extrait : item\tcost

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
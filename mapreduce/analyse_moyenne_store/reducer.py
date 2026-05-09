#!/usr/bin/python3
# Item le plus vendu par store
import sys

oldStore = None
item_counts = {}

for line in sys.stdin:
    try:
        data = line.strip().split("\t")
        if len(data) != 2:
            continue
        store, item = data
        if oldStore and oldStore != store:
            best_item = max(item_counts, key=item_counts.get)
            print("{0}\t{1}\t{2}".format(oldStore, best_item, item_counts[best_item]))
            item_counts = {}
        oldStore = store
        item_counts[item] = item_counts.get(item, 0) + 1
    except Exception:
        continue

if oldStore:
    best_item = max(item_counts, key=item_counts.get)
    print("{0}\t{1}\t{2}".format(oldStore, best_item, item_counts[best_item]))
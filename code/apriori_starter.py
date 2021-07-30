from collections import defaultdict
import numpy as np
import pandas as pd
from itertools import combinations as subset
import time

# Kindly add datasets to this list if you wish to run the program on more dataset
datasets = ['BMS1_spmf.txt']
min_support = 0.01 

def all_except_last(item_1, item_2):
    if item_1[:-1] == item_2[:-1] and item_1[-1] < item_2[-1]: return True
    return False

def has_infrequent_subset(item, L_prev):
    subsets = [sorted(list(s)) for s in (subset(item, len(item) - 1))]
    for s in subsets: 
        if s not in L_prev: return True
    return False

def apriori_gen(L_prev):
    C_ret = []
    for item_1 in L_prev:
        for item_2 in L_prev:
            if all_except_last(item_1,item_2):
                item = item_1 + [item_2[-1]]
                if not has_infrequent_subset(item, L_prev):
                    C_ret.append(item)
    return C_ret

def _find_frequent_1_itemsets(transactions, min_sup):
    count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            count[item]+=1
    items = [ [item] for item, val in count.items() if val >= min_sup]
    return items , ""


def generate_frequent_itemsets(transactions, min_sup = 0.1):
    FI = []
    # Implement the Apriori algorithm here
    return FI


def process(data):
    data = data.split("\n")
    if not data[-1]: data = data[:-1]
    data= [set([int(item.strip()) for item in line.split("-2")[0].strip().split("-1")[:-1]]) for line in data]
    return data

for dataset in datasets:
    with open(dataset) as f:
        data = f.read()
    transactions = process(data)
    print("Dataset:", transactions)

    start_time = time.time()
    print("Running basic apriori")
    apriori_result = generate_frequent_itemsets(transactions, min_support)
    print("Time taken:", time.time() - start_time)

    print("Frequent itemsets formed for", dataset, "at min_support", min_support*100, "%:")
    print(apriori_result)
from collections import defaultdict
import itertools
from typing import Tuple
import numpy as np
import pandas as pd
from itertools import combinations as subset
import time

# Kindly add datasets to this list if you wish to run the program on more dataset
datasets = ['code/BMS1_spmf.txt']
min_support = 0.01
level = 1


def get_level1_items(transactions):
    ## identify the transacitons for the first level
    search_items = set()
    for transaction in transactions:
        for item in transaction:
            search_items.add(item)
    items =  [[item] for item in search_items]
    return items

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

## This method not only identifies the transactions which  
## have mininum support and also keeps only throse transactions 
## so that further processing will be easy
def _find_frequent_1_itemsets(transactions, min_sup):
    trimmed_trans = []
    items_set = set()
    result_items_map =defaultdict(list)
    
    ## First all items into set.
    for transaction in transactions:
        for item in transaction:
            items_set.add(item)
    
    for item in items_set:
        tran_array_indexs = []
        tran_counter = -1
        for transaction in transactions:
            tran_counter = tran_counter + 1
            if item in transaction:
                tran_array_indexs.append(tran_counter)

            
        if(len(tran_array_indexs)>=min_sup):
            result_items_map[item] = tran_array_indexs
    
    
            
    final_items = [[item] for item in result_items_map.keys()]
    
    final_tran_array_indexs = set(itertools.chain(*result_items_map.values()))
    
    
    for i in final_tran_array_indexs:
        trimmed_trans.append(transactions[i])
    
    return (final_items , trimmed_trans)


def _find_frequentitemsets2(transactions, items_to_search, min_sup,curr_level):
    trimmed_trans = []
    
    result_items_map =defaultdict(list)
    
    for item in items_to_search:
        tran_array_indexs = []
        tran_counter = -1
        for transaction in transactions:
            tran_counter = tran_counter + 1
            isFound = set(item).issubset(set(transaction))
            if isFound:
                tran_array_indexs.append(tran_counter)
        cnt_transacitons = len(tran_array_indexs)
        #print(f" searching for {item} in all trans and found in  transactions {cnt_transacitons}") 
            
        if(cnt_transacitons>=min_sup):
            result_items_map[tuple(item)] = tran_array_indexs
    
    
            
    if(curr_level>1):
        final_items = [list(item) for item in result_items_map.keys()]
    else:
        final_items = [[item[0]] for item in result_items_map.keys()]
    
    final_tran_array_indexs = set(itertools.chain(*result_items_map.values()))
    
    
    for i in final_tran_array_indexs:
        trimmed_trans.append(transactions[i])
    
    return (final_items , trimmed_trans)

def generate_frequent_itemsets_2(transactions, freq_items, min_sup):
	## level maintains the level
    global level
    min_sup_count	=	min_sup * len(transactions)
    print(f" For Level = {level} total transacitons = {len(transactions)}, input min_sup={min_sup}, min_sup% = {min_sup*100} and min_sup_count = {min_sup_count}")
	
    fi_trans    		= _find_frequentitemsets2(transactions,freq_items, min_sup_count,level)
    freq_items    	    = fi_trans[0]
    transactions 		= fi_trans[1]
    transactions 		= list(filter(lambda x: len(x)>=level, transactions))
    prev_freq_items 	= freq_items
    while len(freq_items) > 0:
        prev_freq_items =  freq_items
        freq_items 	    =  apriori_gen(freq_items)
        ##print(f"freq_items={freq_items[0]}")
        min_sup_count = len(transactions) * min_sup
        level = level + 1
        fi_trans = _find_frequentitemsets2(transactions,freq_items, min_sup_count,level)
        freq_items    	= fi_trans[0]
        transactions    = fi_trans[1]
        transactions    = list(filter(lambda x: len(x)>=level, transactions))
        
        print(f"level={level-1} and FI length={len(freq_items)} and freq_items = {prev_freq_items}")
    return prev_freq_items


def process(data):
    data = data.split("\n")
    if not data[-1]: data = data[:-1]
    data= [set([int(item.strip()) for item in line.split("-2")[0].strip().split("-1")[:-1]]) for line in data]
    
    return data

for dataset in datasets:
    with open(dataset) as f:
        data = f.read()
    transactions = process(data)
    items = get_level1_items(transactions)
    #print("Dataset:", transactions)
    start_time = time.time()
    apriori_result = generate_frequent_itemsets_2(transactions,items,min_support)
    print("Time taken:", time.time() - start_time)

    print("At level " , level-1, " Frequent itemsets formed for", dataset, "at min_support", min_support*100, "%:")
    print(apriori_result)
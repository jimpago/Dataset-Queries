import csv
import sys
import time

def read_transactions(file):
    transactions = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            int_row = [int(value.strip().replace('[','').replace(']','')) for value in row]
            transactions.append(int_row)
    return transactions

def read_queries(file):
    queries = []
    with open(file, 'r') as f:
        for line in f:
            query = [int(value.strip().replace('[','').replace(']','')) for value in line.split(',')]
            queries.append(query)
    return queries

def create_inverted_occ(transactions):
    inverted = {}
    for tid, transaction in enumerate(transactions):
        for obj in transaction:
            if obj not in inverted:
                inverted[obj] = {}
            if tid not in inverted[obj]:
                inverted[obj][tid] = 0
            inverted[obj][tid] += 1
    return inverted

def compute_rarity_factors(inverted, num_transactions):
    rarity = {}
    for obj, tid_dict in inverted.items():
        trf = len(tid_dict)
        rarity[obj] = num_transactions / trf if trf > 0 else 0
    return rarity

def write_inverted_occ(inverted, rarity, filename='invfileocc.txt'):
    with open(filename, 'w') as f:
        for obj in sorted(inverted):
            pairs = [[tid, occ] for tid, occ in sorted(inverted[obj].items())]
            f.write(f"{obj}: {rarity[obj]}, {pairs}\n")

def merge_union(lists):
    # lists: dict {obj: [[tid, occ], ...]}
    # Επιστρέφει dict {tid: {obj: occ}}
    union = {}
    for obj, lst in lists.items():
        for tid, occ in lst:
            if tid not in union:
                union[tid] = {}
            union[tid][obj] = occ
    return union

def relevance_query_evaluation(queries, inverted, rarity, num_transactions, k=None):
    results = []
    for query in queries:
        obj_lists = {obj: [[tid, occ] for tid, occ in inverted.get(obj, {}).items()] for obj in query}
        union = merge_union(obj_lists)
        rels = []
        for tid, obj_occ in union.items():
            rel = 0
            for obj in query:
                occ = obj_occ.get(obj, 0)
                rel += occ * rarity.get(obj, 0)
            if rel > 0:
                rels.append([rel, tid])
        rels.sort(reverse=True)
        if k is not None:
            rels = rels[:k]
        results.append(rels)
    return results

def naive_relevance_query_evaluation(queries, transactions, rarity, k=None):
    results = []
    num_transactions = len(transactions)
    for query in queries:
        rels = []
        for tid, transaction in enumerate(transactions):
            rel = 0
            for obj in query:
                occ = transaction.count(obj)
                rel += occ * rarity.get(obj, 0)
            if rel > 0:
                rels.append([rel, tid])
        rels.sort(reverse=True)
        if k is not None:
            rels = rels[:k]
        results.append(rels)
    return results


if len(sys.argv) != 6:
    print("Usage: python relevance.py <transactions file> <queries file> <qnum> <method> <k>")
    print("method: 0 = naive, 1 = inverted, -1 = both")
    sys.exit(1)

transactions_file = sys.argv[1]
queries_file = sys.argv[2]
qnum = int(sys.argv[3])
method = int(sys.argv[4])
k = int(sys.argv[5])

transactions = read_transactions(transactions_file)
inverted = create_inverted_occ(transactions)
rarity = compute_rarity_factors(inverted, len(transactions))
write_inverted_occ(inverted, rarity)

queries = read_queries(queries_file)


if qnum != -1:
    queries = [queries[qnum]]

if method in (-1, 0):
    start = time.time()
    naive_results = naive_relevance_query_evaluation(queries, transactions, rarity, k)
    end = time.time()
    if qnum != -1:
        print("Naive Method result:")
        print(naive_results[0])
    print(f"Naive Method computation time = {end - start:.4f} seconds")

if method in (-1, 1):
    start = time.time()
    inv_results = relevance_query_evaluation(queries, inverted, rarity, len(transactions), k)
    end = time.time()
    if qnum != -1:
        print("Inverted File result:")
        print(inv_results[0])
    print(f"Inverted File computation time = {end - start:.4f} seconds")
import csv
import time
import sys

def read_and_process(file):
    transactions = []
    
    with open(file, 'r') as f_transactions:
        reader = csv.reader(f_transactions)
        for row in reader:
            # Remove unwanted characters and convert to int
            int_row = sorted(set(int(value.strip().replace('[','').replace(']','')) for value in row))
            transactions.append(int_row)
            
    return transactions

def naive(queries, transactions):
    results = []
    for query in queries:
        result = []
        for idx, transaction in enumerate(transactions):
            i, j = 0, 0
            while i < len(query) and j < len(transaction):
                if query[i] < transaction[j]:
                    break
                elif query[i] > transaction[j]:
                    j += 1
                else:
                    i += 1
                    j += 1
            if i == len(query):
                result.append(idx)
        results.append(result)
    return results
                
            
    
def signature(output_file,transactions):
    
    sigfile = []
    with open(output_file, 'w') as f_sigfile:
    
        for transaction in transactions:
            
            bitmap = 0
            for object in transaction:
                
                mask = 1 << object
                bitmap |= mask
                
            sigfile.append(bitmap)
            f_sigfile.write(f"{bitmap}\n")
    #bitmap = 0
    return sigfile

def signature_query_evaluation(queries, sigfile, transactions):
    results = []
    for query in queries:
        result = []
        for idx, transaction in enumerate(transactions):
            bitmap = sigfile[idx]
            match = True
            for obj in query:
                if not (bitmap & (1 << obj)):
                    match = False
                    break
            if match:
                result.append(idx)
        results.append(result)
    return results

def create_bitslices(transactions):
    
    unique_objects = set(obj for transaction in transactions for obj in transaction)
    bitslices = {obj: 0 for obj in unique_objects}

    
    for idx, transaction in enumerate(transactions):
        for obj in transaction:
            bitslices[obj] |= (1 << idx)
    return bitslices

def write_bitslices(bitslices, filename='bitslice.txt'):
    with open(filename, 'w') as f:
        for obj in sorted(bitslices):
            f.write(f"{obj}: {bitslices[obj]}\n")
    
def bitslice_query_evaluation(queries, bitslices, num_transactions):
    results = []
    for query in queries:
        
        if not query:
            results.append([])
            continue
        
        bitmap = bitslices.get(query[0], 0)
        for obj in query[1:]:
            bitmap &= bitslices.get(obj, 0)
        
        matches = [i for i in range(num_transactions) if (bitmap >> i) & 1]
        results.append(matches)
        
    return results


def create_inverted_file(transactions):
    inverted = {}
    for idx, transaction in enumerate(transactions):
        for obj in transaction:
            if obj not in inverted:
                inverted[obj] = []
            inverted[obj].append(idx)
    # Ταξινόμηση των λιστών για κάθε αντικείμενο
    for obj in inverted:
        inverted[obj].sort()
    return inverted

def write_inverted_file(inverted, filename='invfile.txt'):
    with open(filename, 'w') as f:
        for obj in sorted(inverted):
            f.write(f"{obj}: {inverted[obj]}\n")

def merge_intersection(lists):
    if not lists:
        return []
    # Ξεκινάμε με την πρώτη λίστα
    result = lists[0]
    for lst in lists[1:]:
        i = j = 0
        temp = []
        while i < len(result) and j < len(lst):
            if result[i] < lst[j]:
                i += 1
            elif result[i] > lst[j]:
                j += 1
            else:
                temp.append(result[i])
                i += 1
                j += 1
        result = temp
        if not result:
            break
    return result

def inverted_query_evaluation(queries, inverted):
    results = []
    for query in queries:
        lists = [inverted.get(obj, []) for obj in query]
        intersection = merge_intersection(lists)
        results.append(intersection)
    return results
    
def read_queries(file):
    queries = []
    with open(file, 'r') as f_queries:
        for line in f_queries:
            query = sorted([int(value.strip().replace('[','').replace(']','')) for value in line.split(',')])
            queries.append(query)
    return queries


if len(sys.argv) != 5:
     print("Usage: python containment_queries.py <transactions file> <queries file> <qnum> <method>")
     sys.exit(1)
    

trasnsactions_file = sys.argv[1]
queries_file = sys.argv[2]
qnum = int(sys.argv[3])
method = int(sys.argv[4])

transactions = read_and_process(trasnsactions_file)
queries = read_queries(queries_file)

if qnum != -1:
    queries = [queries[qnum]]

# 0 = naive, 1 = signature, 2 = bitslice, 3 = inverted, -1 = όλες
if method in (-1, 0):
        start = time.time()
        naive_results = naive(queries, transactions)
        end = time.time()
        
        print("Naive Method result:\n")

        if qnum != -1:
            print(naive_results[0])
        
        print(f"Naive Method computation time: {end - start:.4f} seconds\n")

if method in (-1, 1):
        start = time.time()
        sigfile = signature('sigfile.txt', transactions)
        sig_results = signature_query_evaluation(queries, sigfile, transactions)
        end = time.time()
        
        print("Signature File result:\n")
        
        if qnum != -1:
            print(sig_results[0])
            
        print(f"Signature Method computation time: {end - start:.4f} seconds\n")

if method in (-1, 2):
        start = time.time()
        bitslices = create_bitslices(transactions)
        write_bitslices(bitslices)
        bitslice_results = bitslice_query_evaluation(queries, bitslices, len(transactions))
        end = time.time()
        
        print("Bitslice Method result:\n")
        
        if qnum != -1:
            print(bitslice_results[0])
        
        print(f"Bitslice Method computation time: {end - start:.4f} seconds\n")

if method in (-1, 3):
        start = time.time()
        inverted = create_inverted_file(transactions)
        write_inverted_file(inverted)
        inv_results = inverted_query_evaluation(queries, inverted)
        end = time.time()
        
        print("Inverted File Method result:\n")
        
        if qnum != -1:
            print(inv_results[0])
            
        print(f"Inverted File Method computation time: {end - start:.4f} seconds")
    


# Dataset Containment & Relevance Queries

Implementation of algorithms for evaluating **containment** and **relevance** queries on transaction datasets.

This project was developed as part of the *Complex Data Management* course assignment.

## 📂 Repository Structure

src/ # Source code (containment.py, relevance.py)
data/ # Input files (transactions.txt, queries.txt)
output/ # Generated outputs (sigfile.txt, bitslice.txt, invfile.txt, invfileocc.txt)
docs/ # Report or assignment description (Report.pdf)

### Part 1 — Containment Queries
Run with:

python src/containment.py data/transactions.txt data/queries.txt <qnum> <method>

<transactions.txt>: dataset file with transactions

<transactions.txt>: dataset file with transactions

<queries.txt>: query file in the same format

<qnum>: query id (line number in queries file, starting from 0; use -1 to run all queries)

<method>: which method to run

-1: all methods

0: Naïve

1: Exact Signature File

2: Bitslice Signature File

3: Inverted File

### Part 2 — Relevance Queries

Run with:

python src/relevance.py data/transactions.txt data/queries.txt <qnum> <method> <k>

<qnum>: query id (or -1 for all queries)

<method>: -1 = all, 0 = Naïve, 1 = Inverted File

<k>: number of top results to return

📜 Methods Implemented

Containment

Naïve: scans all transactions linearly.

Exact Signature File: transaction bitmaps using bitwise operations.

Bitslice Signature File: per-item bitmaps across transactions.

Inverted File: per-item sorted transaction lists.

Relevance

Naïve: directly computes rel(τ,q) for all transactions.

Inverted File: computes rel(τ,q) using inverted lists with occurrence counts and rarity weights.

📄 Report

For full assignment details and explanations see: docs/Report.pdf

# Frequent Itemsets and Association Rules

This is our solution to Homework 2 in ID2222 Data Mining at KTH. It finds frequent itemsets in a set of shopping baskets using the A-Priori algorithm, then builds association rules from them (the optional bonus task).

Everything is plain Python. There's no Spark and no third-party library in the main program.

## What you need

- Python 3.8 or newer
- `pytest`, but only if you want to run the tests

## Getting the dataset

The dataset isn't in the submission, so download it first. We used `T10I4D100K.dat`, which has 100,000 baskets of hashed item IDs. You can get it from the link on the assignment page or from the FIMI repository:

http://fimi.uantwerpen.be/data/T10I4D100K.dat

Save it as `data/T10I4D100K.dat` inside this folder. The program always reads that path.

## Running it

From the project folder:

```bash
python3 main.py
```

That runs both tasks with the default thresholds: a minimum support of 1000 baskets (1% of the data) and a minimum confidence of 0.7.

To pick your own values:

```bash
python3 main.py --support 500 --confidence 0.8
python3 main.py -s 500 -c 0.8      # same thing, shorter
```

| Option | Default | What it does |
|---|---|---|
| `-s`, `--support` | 1000 | Minimum support, as a number of baskets |
| `-c`, `--confidence` | 0.7 | Minimum confidence, between 0 and 1 |
| `-h`, `--help` | | Shows the options and exits |

If support isn't a positive whole number, or confidence isn't between 0 and 1, the program stops and tells you why.

### With make

There's also a Makefile, if you'd rather not type the full command:

```bash
make run                                  # defaults: support 1000, confidence 0.7
make run SUPPORT=500 CONFIDENCE=0.8       # your own values
make test                                 # run the unit tests
make clean                                # delete Python cache files
```

## What you'll see

While A-Priori runs, it prints how many candidates it built at each level, how many turned out to be frequent and how long that level took. After that you get a summary of each task and the rules, sorted by confidence. A default run looks like this:

```
===== TASK 1: APRIORI =====
Total transactions: 100000
Minimum support: 1000
Frequent itemsets: 385
Execution time: 3.2096s

===== TASK 2: ASSOCIATION RULES =====
Minimum confidence: 70%
Total valid rules: 3
Execution time: 0.0001s
[704, 825] -> [39] | Support: 1035 | Confidence: 93.92%
[39, 704] -> [825] | Support: 1035 | Confidence: 93.50%
[39, 825] -> [704] | Support: 1035 | Confidence: 87.19%
```

Times depend on your machine. On an Apple M4 the default run takes around 3 to 5 seconds. Lower support values take longer, and `-s 500` needs about a minute.

## Running the tests

```bash
pip install -r requirements.txt
python3 -m pytest
```

There are 13 tests covering the data loader, the A-Priori steps and rule generation. Most use small hand-made baskets. The data loader tests use `data/sample.dat`, the first 15 baskets of the real dataset.

## How the code is laid out

```
main.py                    reads the options, runs both tasks, prints results
Makefile                   shortcuts for running, testing and cleaning up
src/data_loader.py         turns the .dat file into a list of sets
src/apriori.py             Task 1: A-Priori
src/association_rules.py   Task 2: rule generation
tests/                     unit tests
data/sample.dat            small sample used by the tests
finding.txt                console logs from our earlier runs
report.tex                 the report (LaTeX source)
images/                    screenshots used in the report
```

## How it works, briefly

A-Priori finds frequent itemsets one size at a time. It counts single items, keeps the ones that appear in at least `s` baskets, and builds candidate pairs only from those. Then it does the same for triples and so on. A candidate is thrown out early if any of its smaller subsets wasn't frequent, because it can't be frequent either.

Counting is done from the basket side. For each basket we list the item combinations it actually contains and look them up in the candidate set. Our first version checked every candidate against every basket instead, and that took 421 seconds at the default support. The current version gives exactly the same itemsets in a few seconds.

Rule generation reuses the support counts from A-Priori, so it never reads the data again. It starts with rules that have one item on the right-hand side and only grows the ones that pass the confidence threshold. That's safe because moving more items to the right can't raise confidence.

The report covers the details, the timing tables and what we'd improve next.

## Authors

- Md Ahsanul Karim (makari@kth.se)
- Md Sakibul Islam (msis3@kth.se)

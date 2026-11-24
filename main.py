
import argparse
import time

from src.association_rules import generate_association_rules
from src.data_loader import load_transactions
from src.apriori import apriori


# def main():
#     transactions = load_transactions("data/sample.dat")

#     min_support = 2

#     frequent_itemsets = apriori(transactions, min_support)

#     for itemset, support in sorted(
#         frequent_itemsets.items(),
#         key=lambda x: (len(x[0]), sorted(x[0]))
#     ):
#         print(sorted(itemset), "Support:", support)

# def main():
#     transactions = load_transactions("data/T10I4D100K.dat")

#     min_support = 1000  # 1% of 100,000 transactions

#     start_time = time.perf_counter()

#     frequent_itemsets = apriori(transactions, min_support)

#     execution_time = time.perf_counter() - start_time

#     print(f"Total transactions: {len(transactions)}")
#     print(f"Minimum support: {min_support}")
#     print(f"Execution time: {execution_time:.4f} seconds")
#     print(f"Total frequent itemsets: {len(frequent_itemsets)}")


# Minimum support: 1000 (1% of 100,000 transactions)

# Minimum confidence: 0.7 (70%)

# Optimized support-counting implementation


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find frequent itemsets with A-Priori and "
                    "generate association rules."
    )
    parser.add_argument(
        "-s", "--support",
        type=int,
        default=1000,
        help="minimum support as a basket count (default: 1000)"
    )
    parser.add_argument(
        "-c", "--confidence",
        type=float,
        default=0.7,
        help="minimum confidence between 0 and 1 (default: 0.7)"
    )
    args = parser.parse_args()

    if args.support < 1:
        parser.error("--support must be a positive integer")
    if not 0 < args.confidence <= 1:
        parser.error("--confidence must be in the range (0, 1]")

    return args


def main():
    args = parse_args()

    transactions = load_transactions("data/T10I4D100K.dat")

    # Thresholds from the command line
    min_support = args.support
    min_confidence = args.confidence

    # Task 1: Find frequent itemsets
    start_time = time.perf_counter()

    frequent_itemsets = apriori(transactions, min_support)

    apriori_time = time.perf_counter() - start_time

    print("\n===== TASK 1: APRIORI =====")
    print(f"Total transactions: {len(transactions)}")
    print(f"Minimum support: {min_support}")
    print(f"Frequent itemsets: {len(frequent_itemsets)}")
    print(f"Execution time: {apriori_time:.4f}s")

    # Task 2: Generate association rules
    start_time = time.perf_counter()

    rules = generate_association_rules(
        frequent_itemsets,
        min_confidence
    )

    rules_time = time.perf_counter() - start_time

    print("\n===== TASK 2: ASSOCIATION RULES =====")
    print(f"Minimum confidence: {min_confidence:.0%}")
    print(f"Total valid rules: {len(rules)}")
    print(f"Execution time: {rules_time:.4f}s")

    for (antecedent, consequent), data in sorted(
        rules.items(),
        key=lambda x: (
            -x[1]["confidence"],
            sorted(x[0][0]),
            sorted(x[0][1])
        )
    ):
        print(
            f"{sorted(antecedent)} -> {sorted(consequent)} "
            f"| Support: {data['support']} "
            f"| Confidence: {data['confidence']:.2%}"
        )



if __name__ == "__main__":
    main()

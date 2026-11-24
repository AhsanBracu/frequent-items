
import time

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

def main():
    transactions = load_transactions("data/T10I4D100K.dat")

    min_support = 1000  # 1% of 100,000 transactions

    start_time = time.perf_counter()

    frequent_itemsets = apriori(transactions, min_support)

    execution_time = time.perf_counter() - start_time

    print(f"Total transactions: {len(transactions)}")
    print(f"Minimum support: {min_support}")
    print(f"Execution time: {execution_time:.4f} seconds")
    print(f"Total frequent itemsets: {len(frequent_itemsets)}")


if __name__ == "__main__":
    main()

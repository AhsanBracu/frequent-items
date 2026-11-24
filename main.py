
from src.data_loader import load_transactions
from src.apriori import apriori


def main():
    transactions = load_transactions("data/sample.dat")

    min_support = 2

    frequent_itemsets = apriori(transactions, min_support)

    for itemset, support in sorted(
        frequent_itemsets.items(),
        key=lambda x: (len(x[0]), sorted(x[0]))
    ):
        print(sorted(itemset), "Support:", support)


if __name__ == "__main__":
    main()

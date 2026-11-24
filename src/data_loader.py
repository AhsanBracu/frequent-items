
def load_transactions(file_path):
    transactions = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            items = set(map(int, line.split()))
            transactions.append(items)

    return transactions

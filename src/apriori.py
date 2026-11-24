
from collections import Counter
from itertools import combinations


def find_frequent_singletons(transactions, min_support):
    item_counts = Counter()

    # Count occurrences of every item
    for basket in transactions:
        for item in basket:
            item_counts[item] += 1

    # Keep items meeting the support threshold
    frequent = {
        frozenset([item]): count
        for item, count in item_counts.items()
        if count >= min_support
    }

    return frequent



def generate_candidates(previous_frequent, k):
    itemsets = list(previous_frequent.keys())
    previous_set = set(itemsets)

    candidates = set()

    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            # Combine two frequent itemsets
            candidate = itemsets[i] | itemsets[j]

            # Candidate must contain exactly k items
            if len(candidate) != k:
                continue

            # Every (k-1)-subset must be frequent
            if all(
                frozenset(subset) in previous_set
                for subset in combinations(candidate, k - 1)
            ):
                candidates.add(candidate)

    return candidates


def count_candidate_support(transactions, candidates):
    counts = Counter()

    for basket in transactions:
        for candidate in candidates:
            if candidate.issubset(basket):
                counts[candidate] += 1

    return counts



def filter_frequent(counts, min_support):
    frequent = {
        itemset: count
        for itemset, count in counts.items()
        if count >= min_support
    }

    return frequent


def apriori(transactions, min_support):
    # Step 1: Find frequent singletons
    frequent = find_frequent_singletons(
        transactions, min_support
    )

    all_frequent = dict(frequent)
    k = 2

    while frequent:
        # Generate candidates of size k
        candidates = generate_candidates(frequent, k)

        if not candidates:
            break

        # Count support
        counts = count_candidate_support(
            transactions, candidates
        )

        # Keep only frequent itemsets
        frequent = filter_frequent(counts, min_support)

        # Store discovered frequent itemsets
        all_frequent.update(frequent)

        k += 1

    return all_frequent


from collections import Counter
from itertools import combinations
import time

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


# def count_candidate_support(transactions, candidates):
#     counts = Counter()

#     for basket in transactions:
#         for candidate in candidates:
#             if candidate.issubset(basket):
#                 counts[candidate] += 1

#     return counts



def filter_frequent(counts, min_support):
    frequent = {
        itemset: count
        for itemset, count in counts.items()
        if count >= min_support
    }

    return frequent


def apriori(transactions, min_support):
    start = time.perf_counter()

    print(f"Starting Apriori with {len(transactions)} transactions",
          flush=True)

    # Pass 1: Frequent singletons
    frequent = find_frequent_singletons(
        transactions, min_support
    )

    print(f"L1: {len(frequent)} frequent singletons", flush=True)

    all_frequent = dict(frequent)
    k = 2

    while frequent:
        iteration_start = time.perf_counter()

        print(f"\nGenerating C{k} candidates...", flush=True)

        candidates = generate_candidates(frequent, k)

        print(f"C{k}: {len(candidates)} candidates", flush=True)

        if not candidates:
            break

        print(f"Counting support for C{k}...", flush=True)

        counts = count_candidate_support(
            transactions, candidates
        )

        frequent = filter_frequent(counts, min_support)

        elapsed = time.perf_counter() - iteration_start

        print(
            f"L{k}: {len(frequent)} frequent itemsets "
            f"| Time: {elapsed:.2f}s",
            flush=True
        )

        all_frequent.update(frequent)
        k += 1

    total_time = time.perf_counter() - start

    print(f"\nApriori completed in {total_time:.2f}s", flush=True)

    return all_frequent


def count_candidate_support(transactions, candidates):
    counts = Counter()

    if not candidates:
        return counts

    # Get candidate size (2 for pairs, 3 for triples, etc.)
    k = len(next(iter(candidates)))

    for basket in transactions:
        if len(basket) < k:
            continue

        # Generate combinations from the basket
        for combination in combinations(basket, k):
            candidate = frozenset(combination)

            # Check candidate using hash-set lookup
            if candidate in candidates:
                counts[candidate] += 1

    return counts

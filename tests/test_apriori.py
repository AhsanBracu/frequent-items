
from src.data_loader import load_transactions
from src.apriori import apriori, count_candidate_support, filter_frequent, find_frequent_singletons


def test_frequent_singletons():
    transactions = load_transactions("data/sample.dat")

    frequent = find_frequent_singletons(
        transactions,
        min_support=2
    )

    assert frequent[frozenset({39})] == 2
    assert frequent[frozenset({825})] == 3
    assert frequent[frozenset({834})] == 2

    # Item 240 appears only once
    assert frozenset({240}) not in frequent


from src.apriori import generate_candidates


def test_generate_candidates():
    frequent_singletons = {
        frozenset({1}): 4,
        frozenset({2}): 3,
        frozenset({3}): 3
    }

    candidates = generate_candidates(
        frequent_singletons,
        k=2
    )

    expected = {
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3})
    }

    assert candidates == expected
    assert len(candidates) == 3


def test_count_candidate_support():
    transactions = [
        {1, 2, 3},
        {1, 2},
        {2, 3},
        {1, 3},
        {1, 2, 3}
    ]

    candidates = {
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
        frozenset({1, 4})
    }

    counts = count_candidate_support(
        transactions,
        candidates
    )

    assert counts[frozenset({1, 2})] == 3
    assert counts[frozenset({1, 3})] == 3
    assert counts[frozenset({2, 3})] == 3

    # Candidate {1,4} does not occur
    assert counts[frozenset({1, 4})] == 0


def test_filter_frequent():
    counts = {
        frozenset({1, 2}): 4,
        frozenset({1, 3}): 3,
        frozenset({2, 3}): 1
    }

    result = filter_frequent(counts, min_support=2)

    expected = {
        frozenset({1, 2}): 4,
        frozenset({1, 3}): 3
    }

    assert result == expected
    assert len(result) == 2

def test_apriori():
    transactions = [
        {1, 2, 3},
        {1, 2},
        {2, 3},
        {1, 3},
        {1, 2, 3}
    ]

    result = apriori(transactions, min_support=2)

    assert result[frozenset({1})] == 4
    assert result[frozenset({2})] == 4
    assert result[frozenset({3})] == 4

    assert result[frozenset({1, 2})] == 3
    assert result[frozenset({1, 3})] == 3
    assert result[frozenset({2, 3})] == 3

    assert result[frozenset({1, 2, 3})] == 2

    # No larger itemsets
    assert len(result) == 7

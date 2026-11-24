
from src.association_rules import filter_rules_by_confidence, generate_association_rules, generate_initial_rules, generate_next_rule_candidates
from src.apriori import apriori

def test_generate_initial_rules():
    itemset = frozenset({"A", "B", "C"})

    rules = generate_initial_rules(itemset)

    expected = {
        (frozenset({"A", "B"}), frozenset({"C"})),
        (frozenset({"A", "C"}), frozenset({"B"})),
        (frozenset({"B", "C"}), frozenset({"A"}))
    }

    assert rules == expected
    assert len(rules) == 3


def test_singleton_generates_no_rules():
    itemset = frozenset({"A"})

    rules = generate_initial_rules(itemset)

    assert rules == set()


def test_filter_rules_by_confidence():
    frequent_itemsets = {
        frozenset({"A"}): 5,
        frozenset({"B"}): 4,
        frozenset({"C"}): 3,
        frozenset({"A", "B"}): 4,
        frozenset({"A", "C"}): 3,
        frozenset({"B", "C"}): 2,
        frozenset({"A", "B", "C"}): 2,
    }

    rules = {
        (
            frozenset({"A", "B"}),
            frozenset({"C"})
        ),
        (
            frozenset({"A", "C"}),
            frozenset({"B"})
        ),
        (
            frozenset({"B", "C"}),
            frozenset({"A"})
        ),
    }

    valid_rules = filter_rules_by_confidence(
        rules,
        frequent_itemsets,
        min_confidence=0.7
    )

    expected = {
        (
            frozenset({"B", "C"}),
            frozenset({"A"})
        ): 1.0
    }

    assert valid_rules == expected
    assert len(valid_rules) == 1


def test_generate_next_rule_candidates():
    itemset = frozenset({"A", "B", "C"})

    # Rules that passed confidence filtering
    valid_rules = {
        (
            frozenset({"A", "B"}),
            frozenset({"C"})
        ): 0.8,
        (
            frozenset({"A", "C"}),
            frozenset({"B"})
        ): 0.9
    }

    candidates = generate_next_rule_candidates(
        itemset,
        valid_rules,
        k=2
    )

    assert candidates == {
        (
            frozenset({"A"}),
            frozenset({"B", "C"})
        )
    }


def test_generate_association_rules():
    frequent_itemsets = {
        frozenset({"A"}): 5,
        frozenset({"B"}): 4,
        frozenset({"C"}): 3,
        frozenset({"A", "B"}): 4,
        frozenset({"A", "C"}): 3,
        frozenset({"B", "C"}): 2,
        frozenset({"A", "B", "C"}): 2
    }

    rules = generate_association_rules(
        frequent_itemsets,
        min_confidence=0.7
    )

    # A -> B: 4/5 = 0.8
    assert rules[
        (frozenset({"A"}), frozenset({"B"}))
    ]["confidence"] == 0.8

    # B -> A: 4/4 = 1.0
    assert rules[
        (frozenset({"B"}), frozenset({"A"}))
    ]["confidence"] == 1.0

    # BC -> A: 2/2 = 1.0
    assert rules[
        (frozenset({"B", "C"}), frozenset({"A"}))
    ]["confidence"] == 1.0

    # AB -> C: 2/4 = 0.5, should be pruned
    assert (
        frozenset({"A", "B"}),
        frozenset({"C"})
    ) not in rules

    # Every returned rule must pass confidence
    assert all(
        data["confidence"] >= 0.7
        for data in rules.values()
    )

    # Support is the count of baskets containing X union Y
    assert rules[
        (frozenset({"B", "C"}), frozenset({"A"}))
    ]["support"] == 2



def test_rules_with_two_item_consequents():
    frequent_itemsets = {
        frozenset({"A"}): 4,
        frozenset({"B"}): 4,
        frozenset({"C"}): 4,
        frozenset({"A", "B"}): 3,
        frozenset({"A", "C"}): 3,
        frozenset({"B", "C"}): 3,
        frozenset({"A", "B", "C"}): 3
    }

    rules = generate_association_rules(
        frequent_itemsets,
        min_confidence=0.7
    )

    # A -> BC: Support(ABC) / Support(A) = 3/4
    assert rules[
        (frozenset({"A"}), frozenset({"B", "C"}))
    ]["confidence"] == 0.75

    assert rules[
        (frozenset({"A"}), frozenset({"B", "C"}))
    ]["support"] == 3


def test_apriori_with_association_rules():
    transactions = [
        {1, 2, 3},
        {1, 2},
        {2, 3},
        {1, 3},
        {1, 2, 3}
    ]

    frequent_itemsets = apriori(
        transactions,
        min_support=2
    )

    rules = generate_association_rules(
        frequent_itemsets,
        min_confidence=0.7
    )

    # 1 -> 2: Support(1,2) / Support(1) = 3/4
    rule = (frozenset({1}), frozenset({2}))

    assert rule in rules
    assert rules[rule]["support"] == 3
    assert rules[rule]["confidence"] == 0.75

    # 1 -> {2,3}: Support(1,2,3) / Support(1) = 2/4
    pruned_rule = (
        frozenset({1}),
        frozenset({2, 3})
    )

    assert pruned_rule not in rules

    # Every returned rule meets both thresholds
    assert all(
        data["support"] >= 2
        and data["confidence"] >= 0.7
        for data in rules.values()
    )

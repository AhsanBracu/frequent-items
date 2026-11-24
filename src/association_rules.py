
from itertools import combinations


def generate_initial_rules(itemset):
    rules = set()

    if len(itemset) < 2:
        return rules

    for item in itemset:
        consequent = frozenset({item})
        antecedent = itemset - consequent

        rules.add((antecedent, consequent))

    return rules



def filter_rules_by_confidence(rules, frequent_itemsets, min_confidence):
    valid_rules = {}

    for antecedent, consequent in rules:
        # X ∪ Y
        itemset = antecedent | consequent

        # Support counts from Task 1
        support_xy = frequent_itemsets[itemset]
        support_x = frequent_itemsets[antecedent]

        # Calculate confidence
        confidence = support_xy / support_x

        if confidence >= min_confidence:
            valid_rules[(antecedent, consequent)] = confidence

    return valid_rules

def generate_next_rule_candidates(itemset, valid_rules, k):
    # Extract the consequents of rules that passed
    consequents = {
        consequent
        for antecedent, consequent in valid_rules
        if antecedent | consequent == itemset
    }

    candidates = set()

    for h1, h2 in combinations(consequents, 2):
        # Combine consequents
        new_consequent = h1 | h2

        if len(new_consequent) != k:
            continue

        # All smaller consequents must have passed
        if not all(
            frozenset(subset) in consequents
            for subset in combinations(new_consequent, k - 1)
        ):
            continue

        # Left side must not be empty
        antecedent = itemset - new_consequent

        if antecedent:
            candidates.add((antecedent, new_consequent))

    return candidates



def generate_association_rules(frequent_itemsets, min_confidence):
    all_rules = {}

    # Process every frequent itemset from Task 1
    for itemset, support in frequent_itemsets.items():

        # Singletons cannot produce association rules
        if len(itemset) < 2:
            continue

        # Generate rules with one item on the right
        candidates = generate_initial_rules(itemset)

        # Number of items in the consequent
        k = 1

        while candidates:
            # Calculate confidence and keep passing rules
            valid_rules = filter_rules_by_confidence(
                candidates,
                frequent_itemsets,
                min_confidence
            )

            # Store support and confidence
            for rule, confidence in valid_rules.items():
                all_rules[rule] = {
                    "support": support,
                    "confidence": confidence
                }

            # Increase consequent size
            k += 1

            # Generate next rules using confidence pruning
            candidates = generate_next_rule_candidates(
                itemset,
                valid_rules,
                k
            )

    return all_rules

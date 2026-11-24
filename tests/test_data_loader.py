
from src.data_loader import load_transactions


def test_load_transactions():
    transactions = load_transactions("data/sample.dat")

    # We have 15 baskets
    assert len(transactions) == 15

    # First basket
    assert transactions[0] == {
        25, 52, 164, 240, 274, 328, 368, 448,
        538, 561, 630, 687, 730, 775, 825, 834
    }

    # Second basket
    assert transactions[1] == {
        39, 120, 124, 205, 401,
        581, 704, 814, 825, 834
    }

    # Eighth basket
    assert transactions[7] == {227, 390}

    # Last basket
    assert transactions[14] == {
        101, 147, 229, 350, 411,
        461, 572, 579, 657, 675,
        778, 803, 842, 903
    }

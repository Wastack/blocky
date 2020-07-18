from game.utils.position import Position


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Position) and isinstance(right, Position) and op == "==":
        return [
            "Comparing Position instances:",
            "   {} != {}".format(left, right),
        ]

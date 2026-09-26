#!/usr/bin/env python3
"""Solve the included budget-constrained purchase scenarios with PuLP.

Run ``python solver.py`` for the original four-item scenario, or use
``python solver.py --scenario basic`` for the former ``solver2.py`` scenario.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

try:
    from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, PULP_CBC_CMD
except ImportError as error:  # Keep importing this module useful without PuLP.
    PULP_IMPORT_ERROR = error
else:
    PULP_IMPORT_ERROR = None


@dataclass(frozen=True)
class Item:
    """An item that may be purchased in a budget optimization."""

    name: str
    price: float
    minimum_quantity: int
    objective_weight: float

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Item prices cannot be negative.")
        if self.minimum_quantity < 0:
            raise ValueError("Minimum quantities cannot be negative.")


@dataclass(frozen=True)
class PurchaseScenario:
    """The budget and items that define an integer linear program."""

    name: str
    budget: float
    items: tuple[Item, ...]

    def __post_init__(self) -> None:
        if self.budget < 0:
            raise ValueError("Budget cannot be negative.")
        if not self.items:
            raise ValueError("A scenario needs at least one item.")


@dataclass(frozen=True)
class SolverResult:
    """The status and quantities returned by the linear-programming solver."""

    status: str
    quantities: dict[str, int]
    total_cost: float
    remaining_budget: float

    @property
    def total_items(self) -> int:
        return sum(self.quantities.values())


SCENARIOS = {
    "full": PurchaseScenario(
        name="full",
        budget=75,
        items=(
            Item("Coffee", 1.08, 12, 0.2),
            Item("Breakfast", 3.26, 4, 1.1),
            Item("Sports Betting", 5.00, 1, -1.0),
            Item("Mello Yello Zero", 3.27, 4, 1.5),
        ),
    ),
    "basic": PurchaseScenario(
        name="basic",
        budget=7.35,
        items=(
            Item("Coffee", 1.08, 2, 0.2),
            Item("Mello Yello Zero", 3.27, 1, 1.1),
        ),
    ),
}


def solve_purchase_scenario(scenario: PurchaseScenario) -> SolverResult:
    """Maximize a weighted integer purchase plan without exceeding its budget."""
    if PULP_IMPORT_ERROR is not None:
        raise RuntimeError("PuLP is required; install it with: python3 -m pip install pulp")

    problem = LpProblem(f"Maximize_{scenario.name.title()}_Items", LpMaximize)
    variables = {
        item.name: LpVariable(item.name.replace(" ", "_"), lowBound=0, cat="Integer")
        for item in scenario.items
    }

    problem += (
        sum(item.price * variables[item.name] for item in scenario.items)
        <= scenario.budget,
        "Budget_Constraint",
    )
    for item in scenario.items:
        problem += variables[item.name] >= item.minimum_quantity, f"Minimum_{item.name}"
    problem += sum(
        item.objective_weight * variables[item.name] for item in scenario.items
    )

    problem.solve(PULP_CBC_CMD(msg=False))
    quantities = {
        item.name: int(variables[item.name].value() or 0) for item in scenario.items
    }
    total_cost = sum(item.price * quantities[item.name] for item in scenario.items)
    return SolverResult(
        status=LpStatus[problem.status],
        quantities=quantities,
        total_cost=total_cost,
        remaining_budget=scenario.budget - total_cost,
    )


def print_result(result: SolverResult) -> None:
    """Print a compact summary of a solved scenario."""
    print(f"Status: {result.status}")
    for item, quantity in result.quantities.items():
        print(f"{item}: {quantity}")
    print(f"Total items: {result.total_items}")
    print(f"Total cost: ${result.total_cost:.2f}")
    print(f"Remaining budget: ${result.remaining_budget:.2f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=SCENARIOS,
        default="full",
        help="built-in purchase scenario to solve (default: full)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        print_result(solve_purchase_scenario(SCENARIOS[args.scenario]))
    except RuntimeError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

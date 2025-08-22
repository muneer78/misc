#!/usr/bin/env python3
"""
Enhanced Portfolio Rebalancing Calculator
Calculates optimal asset allocation adjustments and new investment distribution
"""

from typing import Tuple, NamedTuple
from dataclasses import dataclass


class Portfolio(NamedTuple):
    """Current portfolio holdings"""

    domestic_stocks: float
    international_stocks: float
    bonds: float

    @property
    def total_stocks(self) -> float:
        return self.domestic_stocks + self.international_stocks

    @property
    def total_value(self) -> float:
        return self.domestic_stocks + self.international_stocks + self.bonds


@dataclass
class TargetAllocation:
    """Target allocation percentages"""

    stocks_pct: float
    bonds_pct: float
    domestic_stock_ratio: float = 0.8  # 80% domestic, 20% international within stocks

    def __post_init__(self):
        if abs(self.stocks_pct + self.bonds_pct - 100) > 0.01:
            raise ValueError("Stock and bond percentages must sum to 100%")
        if not (0 <= self.domestic_stock_ratio <= 1):
            raise ValueError("Domestic stock ratio must be between 0 and 1")


@dataclass
class RebalanceResult:
    """Results of rebalancing calculation"""

    current_total: float
    new_total: float
    current_stock_pct: float
    current_bond_pct: float

    # Adjustments needed to existing portfolio
    sell_domestic_stocks: float = 0
    sell_international_stocks: float = 0
    sell_bonds: float = 0
    buy_domestic_stocks: float = 0
    buy_international_stocks: float = 0
    buy_bonds: float = 0

    # How to invest new money
    new_money_to_domestic: float = 0
    new_money_to_international: float = 0
    new_money_to_bonds: float = 0


def get_user_input() -> Tuple[Portfolio, float, TargetAllocation]:
    """Get user input with validation"""
    print("Portfolio Rebalancing Calculator")
    print("=" * 40)

    # Get current portfolio
    print("\n1. Current Portfolio Holdings:")
    while True:
        try:
            domestic = float(input("Domestic stocks amount: $"))
            international = float(input("International stocks amount: $"))
            bonds = float(input("Bonds amount: $"))

            if any(x < 0 for x in [domestic, international, bonds]):
                print("Error: Amounts cannot be negative. Please try again.\n")
                continue

            portfolio = Portfolio(domestic, international, bonds)
            if portfolio.total_value == 0:
                print("Error: Portfolio cannot be empty. Please try again.\n")
                continue
            break
        except ValueError:
            print("Error: Please enter valid numbers. Please try again.\n")

    # Get new investment
    print("\n2. New Investment:")
    while True:
        try:
            new_money = float(input("New money to invest: $"))
            if new_money < 0:
                print("Error: New investment cannot be negative. Please try again.\n")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number. Please try again.\n")

    # Get target allocation
    print("\n3. Target Allocation:")
    while True:
        try:
            stocks_pct = float(input("Target stocks percentage (0-100): "))
            bonds_pct = float(input("Target bonds percentage (0-100): "))

            if not (0 <= stocks_pct <= 100) or not (0 <= bonds_pct <= 100):
                print(
                    "Error: Percentages must be between 0 and 100. Please try again.\n"
                )
                continue

            target = TargetAllocation(stocks_pct, bonds_pct)
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.\n")

    # Optional: customize domestic/international split
    print("\n4. Stock Allocation (optional):")
    while True:
        try:
            response = input(
                "Domestic stock ratio within stocks (default 80%, press Enter to accept): "
            ).strip()
            if not response:
                domestic_ratio = 0.8
                break

            domestic_pct = float(response)
            if not (0 <= domestic_pct <= 100):
                print(
                    "Error: Percentage must be between 0 and 100. Please try again.\n"
                )
                continue
            domestic_ratio = domestic_pct / 100
            target.domestic_stock_ratio = domestic_ratio
            break
        except ValueError:
            print("Error: Please enter a valid percentage. Please try again.\n")

    return portfolio, new_money, target


def calculate_rebalancing(
    portfolio: Portfolio, new_money: float, target: TargetAllocation
) -> RebalanceResult:
    """Calculate optimal rebalancing strategy"""
    new_total = portfolio.total_value + new_money

    # Current allocation percentages
    current_stock_pct = (portfolio.total_stocks / portfolio.total_value) * 100
    current_bond_pct = (portfolio.bonds / portfolio.total_value) * 100

    # Target amounts after adding new money
    target_stock_amount = (target.stocks_pct / 100) * new_total
    target_bond_amount = (target.bonds_pct / 100) * new_total

    # Target domestic/international split
    target_domestic_amount = target_stock_amount * target.domestic_stock_ratio
    target_international_amount = target_stock_amount * (
        1 - target.domestic_stock_ratio
    )

    # Calculate differences
    domestic_diff = target_domestic_amount - portfolio.domestic_stocks
    international_diff = target_international_amount - portfolio.international_stocks
    bond_diff = target_bond_amount - portfolio.bonds

    result = RebalanceResult(
        current_total=portfolio.total_value,
        new_total=new_total,
        current_stock_pct=current_stock_pct,
        current_bond_pct=current_bond_pct,
    )

    # Strategy: First allocate new money optimally, then rebalance existing if needed
    remaining_new_money = new_money

    # Allocate new money to assets that are below target
    if domestic_diff > 0:
        allocation = min(domestic_diff, remaining_new_money)
        result.new_money_to_domestic = allocation
        remaining_new_money -= allocation
        domestic_diff -= allocation

    if international_diff > 0 and remaining_new_money > 0:
        allocation = min(international_diff, remaining_new_money)
        result.new_money_to_international = allocation
        remaining_new_money -= allocation
        international_diff -= allocation

    if bond_diff > 0 and remaining_new_money > 0:
        allocation = min(bond_diff, remaining_new_money)
        result.new_money_to_bonds = allocation
        remaining_new_money -= allocation
        bond_diff -= allocation

    # If there's remaining new money, allocate proportionally to target
    if remaining_new_money > 0:
        result.new_money_to_domestic += remaining_new_money * (
            target_domestic_amount / new_total
        )
        result.new_money_to_international += remaining_new_money * (
            target_international_amount / new_total
        )
        result.new_money_to_bonds += remaining_new_money * (
            target_bond_amount / new_total
        )

    # Handle remaining imbalances through rebalancing existing assets
    if domestic_diff > 0:
        result.buy_domestic_stocks = domestic_diff
    elif domestic_diff < 0:
        result.sell_domestic_stocks = -domestic_diff

    if international_diff > 0:
        result.buy_international_stocks = international_diff
    elif international_diff < 0:
        result.sell_international_stocks = -international_diff

    if bond_diff > 0:
        result.buy_bonds = bond_diff
    elif bond_diff < 0:
        result.sell_bonds = -bond_diff

    return result


def print_results(result: RebalanceResult, target: TargetAllocation):
    """Print formatted results"""
    print("\n" + "=" * 50)
    print("REBALANCING RESULTS")
    print("=" * 50)

    # Current state
    print(f"\nCurrent Portfolio: ${result.current_total:,.2f}")
    print(
        f"  Stocks: {result.current_stock_pct:.1f}% (Target: {target.stocks_pct:.1f}%)"
    )
    print(f"  Bonds:  {result.current_bond_pct:.1f}% (Target: {target.bonds_pct:.1f}%)")

    print(f"\nAfter New Investment: ${result.new_total:,.2f}")

    # New money allocation
    print("\nNEW MONEY ALLOCATION:")
    print(f"  Domestic Stocks:     ${result.new_money_to_domestic:,.2f}")
    print(f"  International Stocks: ${result.new_money_to_international:,.2f}")
    print(f"  Bonds:               ${result.new_money_to_bonds:,.2f}")
    print(
        f"  Total:               ${result.new_money_to_domestic + result.new_money_to_international + result.new_money_to_bonds:,.2f}"
    )

    # Rebalancing actions
    rebalancing_needed = any(
        [
            result.sell_domestic_stocks,
            result.sell_international_stocks,
            result.sell_bonds,
            result.buy_domestic_stocks,
            result.buy_international_stocks,
            result.buy_bonds,
        ]
    )

    if rebalancing_needed:
        print("\nEXISTING PORTFOLIO ADJUSTMENTS:")
        if result.sell_domestic_stocks > 0:
            print(f"  Sell Domestic Stocks:     ${result.sell_domestic_stocks:,.2f}")
        if result.sell_international_stocks > 0:
            print(
                f"  Sell International Stocks: ${result.sell_international_stocks:,.2f}"
            )
        if result.sell_bonds > 0:
            print(f"  Sell Bonds:               ${result.sell_bonds:,.2f}")

        if result.buy_domestic_stocks > 0:
            print(f"  Buy Domestic Stocks:      ${result.buy_domestic_stocks:,.2f}")
        if result.buy_international_stocks > 0:
            print(
                f"  Buy International Stocks:  ${result.buy_international_stocks:,.2f}"
            )
        if result.buy_bonds > 0:
            print(f"  Buy Bonds:                ${result.buy_bonds:,.2f}")
    else:
        print("\nEXISTING PORTFOLIO ADJUSTMENTS:")
        print("  No rebalancing of existing assets needed!")


def main():
    """Main program execution"""
    try:
        portfolio, new_money, target = get_user_input()
        result = calculate_rebalancing(portfolio, new_money, target)
        print_results(result, target)

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your inputs and try again.")


if __name__ == "__main__":
    main()

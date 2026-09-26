#!/usr/bin/env python3
"""Calculate how to invest new cash and rebalance a three-fund portfolio."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Portfolio:
    """Dollar amounts held in each asset class."""

    domestic_stocks: float
    international_stocks: float
    bonds: float

    def __post_init__(self) -> None:
        if any(amount < 0 for amount in self.amounts):
            raise ValueError("Portfolio amounts cannot be negative.")

    @property
    def amounts(self) -> tuple[float, float, float]:
        return self.domestic_stocks, self.international_stocks, self.bonds

    @property
    def total_stocks(self) -> float:
        return self.domestic_stocks + self.international_stocks

    @property
    def total_value(self) -> float:
        return sum(self.amounts)

    def add(self, other: "Portfolio") -> "Portfolio":
        return Portfolio(*(left + right for left, right in zip(self.amounts, other.amounts)))


@dataclass(frozen=True)
class TargetAllocation:
    """Target percentages, including the domestic portion of stocks."""

    stocks_pct: float
    bonds_pct: float
    domestic_stock_ratio: float = 0.8

    def __post_init__(self) -> None:
        if not 0 <= self.stocks_pct <= 100 or not 0 <= self.bonds_pct <= 100:
            raise ValueError("Target percentages must be between 0 and 100.")
        if abs(self.stocks_pct + self.bonds_pct - 100) > 0.01:
            raise ValueError("Stock and bond percentages must sum to 100%.")
        if not 0 <= self.domestic_stock_ratio <= 1:
            raise ValueError("Domestic stock ratio must be between 0 and 1.")

    def target_amounts(self, total: float) -> Portfolio:
        stock_amount = total * self.stocks_pct / 100
        return Portfolio(
            domestic_stocks=stock_amount * self.domestic_stock_ratio,
            international_stocks=stock_amount * (1 - self.domestic_stock_ratio),
            bonds=total * self.bonds_pct / 100,
        )


@dataclass(frozen=True)
class Trades:
    """Signed trades: positive amounts are buys and negative amounts are sells."""

    domestic_stocks: float
    international_stocks: float
    bonds: float

    @property
    def amounts(self) -> tuple[float, float, float]:
        return self.domestic_stocks, self.international_stocks, self.bonds


@dataclass(frozen=True)
class RebalanceResult:
    """Contribution allocation and trades needed to reach the target."""

    current_portfolio: Portfolio
    target_portfolio: Portfolio
    contribution: Portfolio
    trades: Trades

    @property
    def current_total(self) -> float:
        return self.current_portfolio.total_value

    @property
    def new_total(self) -> float:
        return self.target_portfolio.total_value

    @property
    def current_stock_pct(self) -> float:
        return self.current_portfolio.total_stocks / self.current_total * 100

    @property
    def current_bond_pct(self) -> float:
        return self.current_portfolio.bonds / self.current_total * 100


ASSET_LABELS = ("Domestic stocks", "International stocks", "Bonds")


def allocate_contribution(
    portfolio: Portfolio, contribution: float, target: Portfolio
) -> Portfolio:
    """Invest cash in underweight assets first, then according to target weights."""
    remaining = contribution
    allocations = [0.0, 0.0, 0.0]

    for index, (current, desired) in enumerate(zip(portfolio.amounts, target.amounts)):
        allocation = min(max(desired - current, 0), remaining)
        allocations[index] = allocation
        remaining -= allocation

    if remaining:
        for index, desired in enumerate(target.amounts):
            allocations[index] += remaining * desired / target.total_value

    return Portfolio(*allocations)


def calculate_rebalancing(
    portfolio: Portfolio, new_money: float, target: TargetAllocation
) -> RebalanceResult:
    """Return an exact, cash-balanced plan for the requested allocation."""
    if portfolio.total_value <= 0:
        raise ValueError("Portfolio cannot be empty.")
    if new_money < 0:
        raise ValueError("New investment cannot be negative.")

    target_portfolio = target.target_amounts(portfolio.total_value + new_money)
    contribution = allocate_contribution(portfolio, new_money, target_portfolio)
    after_contribution = portfolio.add(contribution)
    trades = Trades(
        *(desired - actual for desired, actual in zip(target_portfolio.amounts, after_contribution.amounts))
    )
    return RebalanceResult(portfolio, target_portfolio, contribution, trades)


def read_amount(prompt: str, *, allow_zero: bool = True) -> float:
    """Read one non-negative dollar amount."""
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0 or (not allow_zero and amount == 0):
                raise ValueError
            return amount
        except ValueError:
            qualifier = "positive" if not allow_zero else "non-negative"
            print(f"Please enter a valid {qualifier} number.")


def read_percentage(prompt: str, *, default: float | None = None) -> float:
    """Read a percentage from zero through 100."""
    while True:
        response = input(prompt).strip()
        if not response and default is not None:
            return default
        try:
            percentage = float(response)
            if 0 <= percentage <= 100:
                return percentage
        except ValueError:
            pass
        print("Please enter a percentage from 0 to 100.")


def get_user_input() -> tuple[Portfolio, float, TargetAllocation]:
    """Collect a portfolio and its desired allocation."""
    print("Portfolio Rebalancing Calculator\n" + "=" * 32)
    print("\nCurrent portfolio holdings")
    portfolio = Portfolio(
        read_amount("Domestic stocks: $"),
        read_amount("International stocks: $"),
        read_amount("Bonds: $"),
    )
    if portfolio.total_value == 0:
        raise ValueError("Portfolio cannot be empty.")

    print("\nNew investment")
    new_money = read_amount("New money to invest: $")

    print("\nTarget allocation")
    while True:
        stocks_pct = read_percentage("Stocks (0-100): ")
        bonds_pct = read_percentage("Bonds (0-100): ")
        try:
            allocation = TargetAllocation(stocks_pct, bonds_pct)
            break
        except ValueError as error:
            print(error)

    domestic_pct = read_percentage(
        "Domestic share of stocks (default 80%): ", default=80
    )
    target = TargetAllocation(
        allocation.stocks_pct, allocation.bonds_pct, domestic_pct / 100
    )
    return portfolio, new_money, target


def print_portfolio(title: str, portfolio: Portfolio) -> None:
    print(f"\n{title}: ${portfolio.total_value:,.2f}")
    for label, amount in zip(ASSET_LABELS, portfolio.amounts):
        print(f"  {label:<22} ${amount:>12,.2f}")


def print_results(result: RebalanceResult, target: TargetAllocation) -> None:
    """Print the stock/bond percentages and actionable transactions."""
    print("\n" + "=" * 50 + "\nREBALANCING RESULTS\n" + "=" * 50)
    print(
        f"\nCurrent stocks: {result.current_stock_pct:.2f}% "
        f"(target: {target.stocks_pct:.2f}%)"
    )
    print(
        f"Current bonds:  {result.current_bond_pct:.2f}% "
        f"(target: {target.bonds_pct:.2f}%)"
    )
    print_portfolio("Target portfolio after contribution", result.target_portfolio)
    print_portfolio("Invest new money as follows", result.contribution)

    transactions = [
        (label, amount)
        for label, amount in zip(ASSET_LABELS, result.trades.amounts)
        if abs(amount) >= 0.005
    ]
    print("\nRebalancing trades after the contribution:")
    if not transactions:
        print("  None needed.")
    for label, amount in transactions:
        action = "Buy" if amount > 0 else "Sell"
        print(f"  {action} {label:<21} ${abs(amount):>12,.2f}")


def main() -> None:
    try:
        portfolio, new_money, target = get_user_input()
        print_results(calculate_rebalancing(portfolio, new_money, target), target)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram interrupted.")
    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()

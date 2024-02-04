# Step 1: Input total amount invested
total_invested_amount = float(input("Enter the total amount invested: "))

# Step 2: Input amounts of money invested in stocks, international stocks, and bonds
stocks_amount = float(input("Enter the amount invested in stocks: "))
international_stocks_amount = float(input("Enter the amount invested in international stocks: "))
bonds_amount = float(input("Enter the amount invested in bonds: "))

# Step 3: Input target percentages to invest in stocks and bonds
target_stocks_percentage = int(input("Enter the target percentage for stocks: "))
target_bonds_percentage = int(input("Enter the target percentage for bonds: "))

# Step 4: Calculate target equity and bond amounts based on total invested amount
target_equity_amount = (target_stocks_percentage / 100) * total_invested_amount
target_bond_amount = (target_bonds_percentage / 100) * total_invested_amount

# Step 5: Add all 3 amounts together to get total invested amount
total_invested_amount = stocks_amount + international_stocks_amount + bonds_amount

# Step 6: Add stocks and international stock amounts and store as Total Stocks. Then divide Total Stocks by total invested amount and store that number as Equities %. Express output in percentage format.
total_stocks = stocks_amount + international_stocks_amount
equities_percentage = (total_stocks / total_invested_amount) * 100

# Step 7: Divide bond amount by total amount invested and store as Bond %. Express output in percentage format.
bond_percentage = (bonds_amount / total_invested_amount) * 100

# Step 8: Calculate difference between Target Equity Amount and Total Stocks
equity_difference = target_equity_amount - total_stocks

# Step 9: Calculate difference between Target Bond Amount and Bond Amount
bond_difference = target_bond_amount - bonds_amount

# Step 10: Calculate how much needs to be moved from Total Stocks to Total Bonds to achieve target percentages
move_from_stocks_to_bonds = min(equity_difference, total_stocks)

# Step 11: Calculate how much to move from stocks. This will be 80% of move_from_stocks_to_bonds.
move_from_stocks = 0.8 * move_from_stocks_to_bonds

# Step 12: Calculate how much to move from international stocks. This will be 20% of move_from_stocks_to_bonds.
move_from_international_stocks = 0.2 * move_from_stocks_to_bonds

# Output results
print(f"Equities Percentage: {equities_percentage:.2f}%")
print(f"Bond Percentage: {bond_percentage:.2f}%")
print(f"Difference between Target Equity Amount and Total Stocks: ${equity_difference:.2f}")
print(f"Difference between Target Bond Amount and Bond Amount: ${bond_difference:.2f}")
print(f"Move {move_from_stocks:.2f} from Total Stocks to achieve target percentages.")
print(f"Move {move_from_international_stocks:.2f} from International Stocks to achieve target percentages.")
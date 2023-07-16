amount = float(input("How much is at stake?\n"))
odds = int(input("What are the odds?\n"))

cleaned_odds = abs(odds)

winnings = round(
    ((cleaned_odds / 100) * amount) if odds > 0 else ((100 / cleaned_odds) * amount), 2
)

breakeven = round(
    (100 / (100 + cleaned_odds)) if odds > 0 else (cleaned_odds / (100 + cleaned_odds)),
    2,
)

ev = round((breakeven * winnings) - ((1 - breakeven) * amount), 2)

print(winnings)
print(breakeven * 100)
print(ev)

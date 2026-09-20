import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("draftsheet.csv")

row_colors = [
    "#FF9999" if value > 20 else "#99FF99" if value < -20 else "#FFFFFF"
    for value in df["RankDiff"]
]

fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))
ax.axis("off")

ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellColours=[[color] * len(df.columns) for color in row_colors],
    cellLoc="center",
    loc="center",
)

fig.savefig("draftsheet.pdf", bbox_inches="tight")
plt.close(fig)

"""Stage 1: simple returns and compounding using fictional teaching prices."""

import csv
from pathlib import Path


def main():
    # Resolve relative to this file so VS Code can run it from any folder.
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_prices.csv"
    initial_value = 100.0
    investment_value = initial_value
    previous_price = None

    print("FICTIONAL practice data — no dividends, splits, or trading costs")
    print(f"{'Date':<12} {'Close':>10} {'Daily return':>14} {'Value (£)':>12} {'Total return':>14}")

    with data_path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            price = float(row["close"])
            if previous_price is None:
                daily_label = "—"
            else:
                daily_return = price / previous_price - 1
                investment_value *= 1 + daily_return
                daily_label = f"{daily_return:.2%}"

            cumulative_return = investment_value / initial_value - 1
            print(
                f"{row['date']:<12} {price:>10.3f} {daily_label:>14} "
                f"{investment_value:>12.2f} {cumulative_return:>14.2%}"
            )
            previous_price = price


if __name__ == "__main__":
    main()

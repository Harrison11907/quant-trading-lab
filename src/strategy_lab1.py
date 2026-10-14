"""Compare Apple buy-and-hold strategy with a moving average strategy, including risk and trading costs."""

from pathlib import Path
import matplotlib.pyplot as plt
import yfinance as yf


def main():
    # Keep the library's cache inside this project.
    project_folder = Path(__file__).resolve().parents[1]
    yf.set_tz_cache_location(str(project_folder / ".cache" / "yfinance"))

    download_start = "2024-09-01"  # Start date is included: request 4 months of data before 2025.
    test_start = "2025-01-01"  # Start date is included: request 1 year of data for 2025.
    test_end = "2026-01-01"  # End date is excluded: request calendar year 2025.
    
    prices = yf.download(
        "AAPL",
        start=download_start,
        end=test_end,  # End date is excluded: request calendar year 2025.
        interval="1d",
        auto_adjust=False,  # Keep Close and Adj Close as separate columns.
        multi_level_index=False,
        progress=False,
    )

    if prices is None or prices.empty:
        raise SystemExit("No prices downloaded. Check your connection and try again later.")

    print("Apple (AAPL) daily prices from Yahoo Finance — USD")
    print("Close: split-adjusted; Adj Close: also adjusted for dividends.")
    prices["Daily Return"] = prices["Adj Close"].pct_change()
    
    output_folder = project_folder / "data" / "raw"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"AAPL_{download_start}_to_{test_end}_exclusive.csv"
    prices["MA20"] = prices["Adj Close"].rolling(window=20).mean()
    prices["MA50"] = prices["Adj Close"].rolling(window=50).mean()
    print("First date MA50 is available:", prices["MA50"].first_valid_index())
    prices["Signal"] = (prices["MA20"] > prices["MA50"]).astype(int)
    # Apply yesterday's closing signal at today's open.
    prices["Position"] = prices["Signal"].shift(1).fillna(0)
    prices["Overnight Position"] = prices["Position"].shift(1).fillna(0)

    # Put Open on the same adjustment basis as Adj Close.
    prices["Adjusted Open"] = prices["Open"] * prices["Adj Close"] / prices["Close"]
    prices["Overnight Return"] = (
        prices["Adjusted Open"] / prices["Adj Close"].shift(1) - 1
    )
    prices["Intraday Return"] = prices["Adj Close"] / prices["Adjusted Open"] - 1
    overnight_factor = (
        1 + prices["Overnight Position"] * prices["Overnight Return"].fillna(0)
    )
    intraday_factor = 1 + prices["Position"] * prices["Intraday Return"]
    prices["Trade"] = prices["Position"].diff().abs()
    prices.loc[prices.index[0], "Trade"] = prices["Position"].iloc[0]
    prices["Strategy Return"] = overnight_factor * intraday_factor - 1
    cost_rate = 0.001  # 0.1% per buy or sell
    prices["Trading Cost"] = prices["Trade"] * cost_rate
    # Costs are charged at the open, between the overnight and intraday moves.
    # Each entry/exit deducts 0.1% of portfolio value at that opening trade.
    prices["Net Strategy Return"] = (
        overnight_factor * (1 - prices["Trading Cost"]) * intraday_factor - 1
    )
    # Evaluate only test dates with averages available before the open.
    ready_at_open = prices["MA50"].shift(1).notna()
    in_test_period = (prices.index >= test_start) & (prices.index < test_end)
    comparison = prices.loc[ready_at_open & in_test_period].copy()
    if comparison.empty:
        raise SystemExit("Not enough observations for a next-open comparison.")
    comparison.loc[comparison.index[0], "Trade"] = comparison["Position"].iloc[0]
    print("Number of buys and sells:", int(comparison["Trade"].sum()))
    print("Percentage of days invested:",f"{comparison['Position'].mean():.1%}")
    comparison_returns = comparison[["Daily Return", "Strategy Return", "Net Strategy Return"]].copy()
    # Buy-and-hold enters at that first open: no preceding overnight return.
    comparison_returns.loc[comparison_returns.index[0], "Daily Return"] = (
        (1 - cost_rate) * (1 + comparison["Intraday Return"].iloc[0]) - 1)
    first_day = comparison.index[0]
    starting_position = comparison["Position"].iloc[0]
    first_strategy_factor = (1 + starting_position * comparison["Intraday Return"].iloc[0])
    comparison_returns.loc[first_day, "Strategy Return"] = (first_strategy_factor - 1)
    comparison_returns.loc[first_day, "Net Strategy Return"] = ((1 - starting_position * cost_rate)* first_strategy_factor- 1)
    comparison_values = (100 * (1 + comparison_returns).cumprod())
    comparison_values.columns = ["Buy and Hold After Costs", "MA Strategy", "MA Strategy After Costs"]
    comparison_total_returns = comparison_values.iloc[-1] / 100 - 1
    # Include the original $100 budget as a peak, including initial entry costs.
    comparison_peaks = comparison_values.cummax().clip(lower=100)
    comparison_drawdowns = comparison_values / comparison_peaks - 1
    # Every row now contains an earned return, including the first intraday period.
    daily_volatility = comparison_returns.std()
    daily_volatility.index = comparison_values.columns
    # One row per approach; align each metric using the approach names.
    results = comparison_values.iloc[-1].to_frame(name="Final Value ($)")
    results["Total Return"] = comparison_total_returns
    results["Max Drawdown"] = comparison_drawdowns.min()
    results["Daily Volatility"] = daily_volatility

    print("\nResults over the shared period:")
    print(results.to_string(formatters={
        "Final Value ($)": lambda value: f"{value:.2f}",
        "Total Return": lambda value: f"{value:.2%}",
        "Max Drawdown": lambda value: f"{value:.2%}",
        "Daily Volatility": lambda value: f"{value:.2%}",
    }))

    results_folder = project_folder / "results"
    results_folder.mkdir(exist_ok=True)
    results.to_csv(results_folder / "AAPL_2025_summary.csv", index_label="Approach")
    formatted_results = results.to_string(formatters={
    "Final Value ($)": lambda value: f"${value:.2f}",
    "Total Return": lambda value: f"{value:.2%}",
    "Max Drawdown": lambda value: f"{value:.2%}",
    "Daily Volatility": lambda value: f"{value:.2%}",})
    (results_folder / "AAPL_2025_summary.txt").write_text(formatted_results,encoding="utf-8",)
    print("Saved results table to:", results_folder / "AAPL_2025_summary.csv")
    print("Saved readable table to:", results_folder / "AAPL_2025_summary.txt")
    prices.to_csv(output_path, index_label="Date")
    print(f"Saved full table to: {output_path}")
    print("Execution: previous closing signal, next opening trade; adjusted-price model.")
    print("Cash earns zero; costs are 0.1% per entry/exit; no forced final sale.")
    print("Comparison starts at open:", comparison.index[0].date())

    
    comparison_values.plot(
    title=f"Apple: next-open comparison from {comparison.index[0].date()}",
    ylabel="Investment value (USD)",
    xlabel="Date",
    figsize=(10, 5),)

    plt.tight_layout()
    plt.show()
    
    
    prices[["Adj Close", "MA20", "MA50"]].plot(
    title="Apple: adjusted price and moving averages",
    ylabel="Adjusted price (USD)",
    xlabel="Date",
    figsize=(10, 5),)

    plt.tight_layout()
    plt.show()
    
    
    comparison_drawdowns.mul(100).plot(
    title="Apple: drawdowns over the shared period",
    ylabel="Below previous peak (%)",
    xlabel="Date",
    figsize=(10, 4),)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

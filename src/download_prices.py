"""Compare Apple buy-and-hold strategy with a moving average strategy, including risk and trading costs."""

from pathlib import Path
import matplotlib.pyplot as plt
import yfinance as yf


def main():
    # Keep the library's cache inside this project.
    project_folder = Path(__file__).resolve().parents[1]
    yf.set_tz_cache_location(str(project_folder / ".cache" / "yfinance"))

    prices = yf.download(
        "AAPL",
        start="2025-01-01",
        end="2026-01-01",  # End date is excluded: request calendar year 2025.
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
    prices["Investment Value"] = (
    100 * (1 + prices["Daily Return"].fillna(0)).cumprod())
    print(prices[["Close", "Adj Close", "Daily Return", "Investment Value"]].head())
    print(f"\nDownloaded {len(prices)} trading-day rows.")
    final_value = prices["Investment Value"].iloc[-1]
    total_return = final_value / 100 - 1
    print(f"Final investment value: ${final_value:.2f}")
    print(f"Total return: {total_return:.2%}")
    prices["Running Peak"] = prices["Investment Value"].cummax()
    prices["Drawdown"] = (prices["Investment Value"] / prices["Running Peak"] - 1)
    max_drawdown = prices["Drawdown"].min()
    print(f"Maximum drawdown: {max_drawdown:.2%}")
    
    output_folder = project_folder / "data" / "raw"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / "AAPL_2025.csv"
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
    # First evaluation day is the open AFTER the first valid MA50 signal.
    ready_at_open = prices["MA50"].shift(1).notna()
    comparison = prices.loc[ready_at_open].copy()
    if comparison.empty:
        raise SystemExit("Not enough observations for a next-open comparison.")
    print("Number of buys and sells:", int(comparison["Trade"].sum()))
    print("Percentage of days invested:",f"{comparison['Position'].mean():.1%}")
    comparison_returns = comparison[["Daily Return", "Strategy Return", "Net Strategy Return"]].copy()
    # Buy-and-hold enters at that first open: no preceding overnight return.
    comparison_returns.loc[comparison_returns.index[0], "Daily Return"] = (
        (1 - cost_rate) * (1 + comparison["Intraday Return"].iloc[0]) - 1)
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
    print("Saved results table to:", results_folder / "AAPL_2025_summary.csv")
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

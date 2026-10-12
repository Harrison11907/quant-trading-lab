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
    prices.to_csv(output_path, index_label="Date")
    prices["MA20"] = prices["Adj Close"].rolling(window=20).mean()
    prices["MA50"] = prices["Adj Close"].rolling(window=50).mean()
    print("First date MA50 is available:", prices["MA50"].first_valid_index())
    prices["Signal"] = (prices["MA20"] > prices["MA50"]).astype(int)
    prices["Position"] = prices["Signal"].shift(1).fillna(0)
    prices["Trade"] = prices["Position"].diff().abs()
    prices.loc[prices.index[0], "Trade"] = prices["Position"].iloc[0]
    prices["Strategy Return"] = (prices["Position"] * prices["Daily Return"])
    cost_rate = 0.001  # 0.1% per buy or sell
    prices["Trading Cost"] = prices["Trade"] * cost_rate
    prices["Net Strategy Return"] = (
    prices["Strategy Return"] - prices["Trading Cost"])
    comparison = prices.loc[prices["MA50"].notna()].copy()
    comparison_returns = comparison[["Daily Return", "Strategy Return", "Net Strategy Return"]].copy()
    comparison_returns.iloc[0] = 0
    comparison_returns.loc[
    comparison_returns.index[0], "Daily Return"] = -cost_rate
    comparison_values = (100 * (1 + comparison_returns).cumprod())
    comparison_values.columns = ["Buy and Hold After Costs", "MA Strategy", "MA Strategy After Costs"]
    comparison_total_returns = comparison_values.iloc[-1] / 100 - 1
    print("Total return over the shared period:")
    print(comparison_total_returns.map(lambda value: f"{value:.2%}"))
    comparison_peaks = comparison_values.cummax()
    comparison_drawdowns = comparison_values / comparison_peaks - 1
    print("Maximum drawdown over the shared period:")
    print(comparison_drawdowns.min().map(lambda value: f"{value:.2%}"))
    daily_volatility = comparison_returns.iloc[1:].std()
    daily_volatility.index = comparison_values.columns
    print("Daily volatility over the shared period:")
    print(daily_volatility.map(lambda value: f"{value:.2%}"))
    print(f"Saved full table to: {output_path}")

    
    comparison_values.plot(
    title="Apple: comparison from 17 March 2025",
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

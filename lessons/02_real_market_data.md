# Stage 1 continued — Apple historical data

We now download daily Apple prices for calendar year 2025. AAPL identifies Apple; prices are in US dollars. This is an inspection exercise, not a strategy.

## Understand the columns first

Yahoo's historical Close series already accounts for splits. Adj Close also incorporates dividend adjustments. An adjusted price is a historical calculation, not necessarily the price at which you could have traded that day. Using adjusted returns later approximates reinvested-dividend performance; do not also add those dividends again.

We explicitly set `auto_adjust=False` to retain both columns. Setting it to True would automatically adjust the price columns instead. We request daily observations; weekends and exchange holidays generally have no rows. The end date is exclusive, so 2026-01-01 means stop before that date.

## Setup and run

In VS Code, open a terminal in the quant-trading-lab folder. Use the same interpreter that successfully ran the first exercise:

```powershell
python -m pip install -r requirements.txt
python src/download_prices.py
```

If the default Python shortcut still fails, use the verified interpreter:

```powershell
& 'C:\Users\hmars\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pip install -r requirements.txt
& 'C:\Users\hmars\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/download_prices.py
```

The new script prints the first five rows and saves the full provider table to data/raw/AAPL_2025.csv. The fictional sample and first script remain available. Internet access is required. If installation fails or the service returns no data, keep the error message for troubleshooting.

## Read the new code a few lines at a time

`import yfinance as yf` loads an external library and gives it the short name `yf`. Unlike csv and pathlib, it needs installing.

`yf.download(...)` fetches the observations into a pandas DataFrame, a table with labelled rows and columns. `prices[["Close", "Adj Close"]]` selects two columns; `.head()` shows the first five rows. `to_csv(...)` saves that table as a file.

Before calculating returns, inspect the downloaded dates and both columns. Why might the adjusted price differ from Close? Why are weekends absent?

Sources:
- https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
- https://ranaroussi.github.io/yfinance/advanced/price_repair.html

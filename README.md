# Quant Trading Strategy & Backtesting Lab

Harrison's learning project: understand the finance, then implement it in Python.

## Start here

Open this folder in VS Code. Read `lessons/01_market_data_and_returns.md`, then open `src/market_returns.py`.

With a working Python 3 interpreter selected in VS Code, run from this folder:

```powershell
python src/market_returns.py
```

The first script uses no third-party dependencies. It reads a fictional CSV and prints daily returns and the value of an initial £100 investment. It makes no trades or network requests.

### Python setup on this computer

The default `python` command currently resolves to a Windows shortcut that could not run. This exercise was verified with the bundled interpreter below. In VS Code, use **Python: Select Interpreter → Enter interpreter path** and select:

```text
C:\Users\hmars\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Or run directly in the terminal:

```powershell
& 'C:\Users\hmars\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/market_returns.py
```

This bundled path may change with app updates; a dedicated project environment can come with the real-data lesson.

## Folder guide

- `lessons/`: finance explanations and exercises
- `src/`: Python code
- `data/sample_prices.csv`: fictional teaching data, not market history

## Roadmap

1. Market data and returns: practice prices → daily returns → compounding → real adjusted market data.
2. Moving-average signals and careful execution timing.
3. Backtesting with transaction costs and a buy-and-hold comparison.
4. Risk and performance measures.
5. Additional strategies and out-of-sample evaluation.
6. Charts and a small app.

Stage 1 now also includes `src/download_prices.py`, a separate Apple price download and inspection exercise. Read `lessons/02_real_market_data.md` for its setup and explanation. Install its external dependency using `python -m pip install -r requirements.txt` with your selected interpreter. Returns from real data are the next learning step.

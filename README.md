# Quant Trading Strategy & Backtesting Lab

A Python project exploring how rule-based trading strategies perform on historical market data, built step by step while learning the finance and programming behind each decision.

The central question is: can a simple trading strategy improve on buying and holding an asset after accounting for risk and trading costs?

The goal is to build a research tool that can:

- Load and inspect historical market data, including adjustments for stock splits and dividends.
- Generate trading signals from rules such as moving-average crossovers, momentum, and mean reversion.
- Backtest those rules with realistic trade timing and transaction costs.
- Compare strategy performance with a buy-and-hold benchmark.
- Measure returns, volatility, and drawdowns, and explain the results through charts.
- Evaluate strategies on data outside the period used to develop them, reducing the risk of overfitting.

The project currently explores Apple price data, investment returns, drawdowns, and moving-average signals. Backtesting and broader strategy comparisons are planned next.

The emphasis is on understanding why each calculation and trading rule works, and what its limitations are, before extending the code.

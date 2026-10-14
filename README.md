# Quant Trading Strategy & Backtesting Lab

I'm building this Python project to learn how to test trading strategies and understand the finance behind the results.

My main question is whether a simple trading rule can improve on buying and holding an asset once I account for risk and trading costs. I'm interested in the trade-off between returns and losses along the way, rather than just which approach finishes with the most money.

## What I've built so far

I started with fictional prices to understand daily returns and compounding, then moved on to Apple historical data for 2025. My first backtest compares a 20-day/50-day moving-average strategy with buy-and-hold.

The script uses closing-price signals to trade at the next open, includes a simple trading-cost assumption, and compares both approaches over the same evaluation period. I use charts and a results table to examine total return, daily volatility, and maximum drawdown.

I've written up what I found and the assumptions behind the test in [FINDINGS.md](FINDINGS.md).

## Where I want to take it

- Test the same rule on other periods and assets.
- Explore other rules, such as momentum and mean reversion.
- Improve the execution and cost assumptions.
- Evaluate strategies on separate data from the period used to develop them.
- Make the results easier to explore and compare.

I'm building this step by step so I can understand and explain each calculation before adding more complexity. Finding that a strategy doesn't outperform is still a useful result.

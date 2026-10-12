# Stage 1 — Market data and returns

## The finance first

A daily closing price is an observation at the end of a trading session. A daily simple return measures the proportional change between consecutive observations:

    daily_return = current_price / previous_price - 1

£100 to £105 gives 0.05, or 5%. £105 to £99.75 gives -0.05, or -5%.

These changes compound: £100 × 1.05 × 0.95 = £99.75. Adding the percentages would incorrectly suggest that you broke even.

    investment_value = previous_value × (1 + daily_return)
    cumulative_return = investment_value / initial_value - 1

The first price has no preceding observation, so its daily return is unavailable, not zero. We use it as the starting point for the £100 investment. A return between adjacent trading sessions can span a weekend or holiday.

Our fictional dataset has no dividends or splits. With real stocks, raw prices can mislead: a stock split changes price without necessarily changing your wealth, and dividends distribute cash. We will explain the data provider's adjustment rules before calculating returns from real data. This exercise assumes fractional holdings, no costs, and no interest; it is not yet a backtest.

## Predict before running

1. Calculate the return from 99.75 to 101.745.
2. Predict the final value of £100 after prices 100 → 105 → 99.75 → 101.745.
3. Why does the first row show a dash for daily return?

Now read and run `src/market_returns.py`. Trace one row through the loop and compare the output with your predictions.

Expected answers: 2%; £101.745 (displayed as £101.75); no earlier observation exists.

## Next lesson

Choose a real asset, understand adjusted prices, and load historical data. Later we will introduce log returns, which add across time, and explain when simple returns are more useful.

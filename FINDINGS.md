# Apple moving-average experiment

## What I wanted to test

I wanted to see how a strategy based on 20-day and 50-day moving averages compares with simply buying and holding Apple. I compared returns as well as volatility and drawdown, because a higher final return doesn't tell me how difficult the journey was.

## How I tested it

I downloaded daily Apple data from Yahoo Finance from September 2024 through December 2025 and calculated the moving averages from adjusted closing prices. My rule is to hold Apple when MA20 is above MA50 and stay in cash otherwise.

I calculate the signal at the close and model the trade at the next trading day's open. This avoids assuming I can act on a closing signal at the same closing price.

I evaluate calendar year 2025, starting both approaches with a $100 cash budget at the first trading open on 2 January and measuring performance through the final trading close of the year. September-to-December 2024 provides warm-up data, so the averages are ready before the test begins. If the strategy starts with a buy signal, it buys at the first test open and pays the entry cost; it does not earn returns from before that open.

I put opening prices on the same adjustment basis as closing prices using `Open * Adj Close / Close`. This models dividend-reinvested performance using adjusted prices; I don't separately track dividend cash or share quantities. The strategy earns overnight returns only if it already holds shares, and earns intraday returns if it holds shares after the opening trade.

## What I found

My saved full-year results were:

| Approach | Final value | Total return | Maximum drawdown | Daily volatility |
|---|---:|---:|---:|---:|
| Buy-and-hold after costs | $109.60 | 9.60% | -30.73% | 2.05% |
| MA strategy before costs | $105.81 | 5.81% | -21.40% | 1.17% |
| MA strategy after costs | $105.07 | 5.07% | -21.95% | 1.17% |

The MA strategy earned less than buy-and-hold, but had a smaller maximum drawdown and lower daily volatility. Trading costs reduced the strategy's total return by about 0.74 percentage points. Earlier trade-count and exposure observations came from the March-start test and aren't used to describe this full-year result.

My initial chart made the strategy look more successful. It stayed in cash while waiting for 50 observations, whereas buy-and-hold was invested from January. Once I compared them from a shared starting point, the result changed. This helped me understand why the data preparation period and evaluation period need to be separated.

My conclusion from this experiment is that the strategy reduced risk on the measures I checked, but gave up some return. It wasn't better on every measure. Spending time in cash reduced its exposure to Apple, although which days it held shares also mattered.

The script prints the current results table and saves it to `results/AAPL_2025_summary.csv` for numeric analysis and `results/AAPL_2025_summary.txt` for reading. The table contains final value, total return, maximum drawdown, and daily volatility. Percentage values are stored as decimals in the CSV. The downloaded dataset's filename includes the warm-up start and exclusive end date to distinguish it from the test-period summaries.

## Assumptions and limitations

- I assume the strategy is fully invested or fully in cash, with fractional holdings, no borrowing, and no short selling.
- I deduct 0.1% of portfolio value for each opening buy or sell. Buy-and-hold pays its initial entry cost. I also show the MA strategy before costs as a reference.
- I assume cash earns no interest. I don't include taxes, explicit dividend withholding, or a forced sale at the end.
- I assume trades fill at the adjusted opening price. Actual execution can differ, and the fixed cost is only an approximation.
- I measure drawdowns using daily closing values and the original $100 budget, so I don't capture the worst loss within each day.
- I measure daily volatility using the sample standard deviation of the observed returns. The first observation covers only the first open-to-close period.
- I've tested one asset over one period while developing the code. That isn't enough to conclude that the rule will work elsewhere or predict future returns. I haven't independently checked the provider's prices and adjustments.

## What I'd do next

Next I want to add a mean-reversion strategy and compare it using the same evaluation period, execution timing, and cost assumptions. I also want to test unchanged rules on a separate period to see whether the findings hold outside the data I've already explored.

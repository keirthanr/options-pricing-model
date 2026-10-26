# Options Pricing Model: Black–Scholes vs Monte Carlo

A beginner-friendly Python project comparing two methods for pricing **European call and put options**. It also calculates **Delta and Vega** and creates two sensitivity charts.

## What is an option?

A **call** gives the buyer the right to buy at an agreed strike price. A **put** gives the right to sell at that strike price. European options can only be exercised at expiry.

## What it does

1. Prices European calls and puts using the Black–Scholes formula.
2. Simulates 100,000 possible prices at expiry under the same model, then discounts average payoffs.
3. Compares Black–Scholes prices with Monte Carlo prices and standard errors.
4. Calculates call/put **Delta** (stock-price sensitivity) and **Vega** (volatility sensitivity).
5. Saves charts showing option prices against stock prices and a call price against volatility.

## Run

Install Python 3.10 or later, then run:

```bash
python -m pip install -r requirements.txt
python options_pricing.py
```

Check the core calculations using:

```bash
python -m unittest -v
```

The script creates two PNG charts in the `output/` directory.

## Example assumptions

| Parameter | Example value |
|---|---:|
| Current stock price | 100 |
| Strike price | 100 |
| Time to expiry | 1 year |
| Continuously compounded risk-free rate | 5% |
| Annual volatility | 20% |
| Monte Carlo simulations | 100,000 |

Inputs are illustrative, **not live market data**. Adjust the constants at the beginning of `options_pricing.py` to explore other scenarios.

## The basic mathematics

- **Call payoff at expiry:** `max(final stock price - strike, 0)`.
- **Put payoff at expiry:** `max(strike - final stock price, 0)`.
- **Monte Carlo price:** average simulated payoff multiplied by `exp(-rate * time)`.
- **Black–Scholes:** an analytical pricing formula based on the standard normal distribution.
- **Delta:** approximate change in option price for a 1-unit increase in current stock price.
- **Vega:** approximate change in option price for a 1.00 increase in volatility (divide by 100 for a one-percentage-point change).

Monte Carlo approximates the same risk-neutral model that Black–Scholes solves analytically, so the results should be close but not identical. Standard error measures simulation uncertainty; it does not measure real-world prediction accuracy.

## Questions to explain in an interview

1. Why does a call generally become more valuable when the underlying stock rises?
2. Why can higher volatility increase option prices?
3. Why are the simulated prices slightly different from the formula?
4. What is the difference between the option **payoff** and the option **price**?
5. What do Delta and Vega mean?

## Limitations

Educational project, not investment advice. It assumes European options, no dividends, constant interest rates and volatility, and no transaction costs. It does not capture volatility smiles, early exercise, market liquidity or changing economic conditions.

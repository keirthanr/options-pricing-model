"""European options: Black–Scholes prices, Monte Carlo estimates and Greeks."""
from math import erf, exp, log, sqrt, pi
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Illustrative inputs: edit these to explore different scenarios.
STOCK_PRICE = 100.0
STRIKE = 100.0
TIME_YEARS = 1.0
RATE = 0.05
VOLATILITY = 0.20
SIMULATIONS = 100_000


def cdf(x):
    """Standard normal cumulative probability."""
    return 0.5 * (1 + erf(x / sqrt(2)))


def pdf(x):
    return exp(-x * x / 2) / sqrt(2 * pi)


def black_scholes(stock, strike, time, rate, volatility, kind="call"):
    """Price a European call or put with no dividends."""
    if min(stock, strike, time, volatility) <= 0:
        raise ValueError("Stock, strike, time and volatility must be positive.")
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    d1 = (log(stock / strike) + (rate + volatility**2 / 2) * time) / (volatility * sqrt(time))
    d2 = d1 - volatility * sqrt(time)
    discounted_strike = strike * exp(-rate * time)
    if kind == "call":
        return stock * cdf(d1) - discounted_strike * cdf(d2)
    return discounted_strike * cdf(-d2) - stock * cdf(-d1)


def greeks(stock, strike, time, rate, volatility):
    """Delta for calls/puts and vega for a one-unit volatility change."""
    d1 = (log(stock / strike) + (rate + volatility**2 / 2) * time) / (volatility * sqrt(time))
    return {"Call delta": cdf(d1), "Put delta": cdf(d1) - 1,
            "Vega": stock * pdf(d1) * sqrt(time)}


def monte_carlo(stock, strike, time, rate, volatility, n=SIMULATIONS, seed=42):
    """Risk-neutral lognormal simulation of terminal prices and discounted payoffs."""
    if min(stock, strike, time, volatility) <= 0 or n < 2:
        raise ValueError("Positive inputs and at least two simulations required.")
    random = np.random.default_rng(seed).standard_normal(n)
    final_stock = stock * np.exp((rate - volatility**2 / 2) * time
                                + volatility * np.sqrt(time) * random)
    discount = np.exp(-rate * time)
    call = discount * np.maximum(final_stock - strike, 0)
    put = discount * np.maximum(strike - final_stock, 0)
    return {"call": (float(call.mean()), float(call.std(ddof=1) / np.sqrt(n))),
            "put": (float(put.mean()), float(put.std(ddof=1) / np.sqrt(n)))}


def main():
    out = Path("output")
    out.mkdir(exist_ok=True)
    simulation = monte_carlo(STOCK_PRICE, STRIKE, TIME_YEARS, RATE, VOLATILITY)
    print("Illustrative European option prices (not market quotes)")
    print(f"Stock {STOCK_PRICE}; strike {STRIKE}; time {TIME_YEARS} years; "
          f"rate {RATE:.0%}; volatility {VOLATILITY:.0%}")
    print(f"{'Option':<8}{'Black-Scholes':>16}{'Monte Carlo':>16}{'MC std. error':>16}")
    for kind in ("call", "put"):
        exact = black_scholes(STOCK_PRICE, STRIKE, TIME_YEARS, RATE, VOLATILITY, kind)
        estimate, standard_error = simulation[kind]
        print(f"{kind:<8}{exact:>16.4f}{estimate:>16.4f}{standard_error:>16.4f}")
    for name, value in greeks(STOCK_PRICE, STRIKE, TIME_YEARS, RATE, VOLATILITY).items():
        print(f"{name}: {value:.4f}")
    print("Vega is per 1.00 volatility change; divide by 100 for 1 percentage point.")

    prices = np.linspace(60, 140, 81)
    fig, ax = plt.subplots(figsize=(8, 5))
    for kind in ("call", "put"):
        ax.plot(prices, [black_scholes(p, STRIKE, TIME_YEARS, RATE, VOLATILITY, kind)
                         for p in prices], label=kind.title())
    ax.set(xlabel="Stock price", ylabel="Option value",
           title="Black-Scholes price sensitivity to stock price")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "price_vs_stock.png", dpi=150)
    plt.close(fig)

    vols = np.linspace(.05, .60, 56)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(vols * 100, [black_scholes(STOCK_PRICE, STRIKE, TIME_YEARS, RATE, v)
                         for v in vols])
    ax.set(xlabel="Volatility (%)", ylabel="Call option value",
           title="Call sensitivity to volatility")
    fig.tight_layout()
    fig.savefig(out / "price_vs_volatility.png", dpi=150)
    plt.close(fig)
    print("Charts saved to output/")


if __name__ == "__main__":
    main()

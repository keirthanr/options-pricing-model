"""Run with python -m unittest -v."""
import unittest
from math import exp
from options_pricing import black_scholes, greeks, monte_carlo


class PricingTests(unittest.TestCase):
    def test_known_call(self):
        self.assertAlmostEqual(black_scholes(100, 100, 1, .05, .2), 10.450583572, places=5)

    def test_put_call_parity(self):
        c = black_scholes(100, 100, 1, .05, .2)
        p = black_scholes(100, 100, 1, .05, .2, "put")
        self.assertAlmostEqual(c - p, 100 - 100 * exp(-.05), places=8)

    def test_delta_relation(self):
        g = greeks(100, 100, 1, .05, .2)
        self.assertAlmostEqual(g["Call delta"] - g["Put delta"], 1)

    def test_monte_carlo(self):
        estimates = monte_carlo(100, 100, 1, .05, .2, n=100_000, seed=42)
        for kind in ("call", "put"):
            price, stderr = estimates[kind]
            self.assertLess(abs(price - black_scholes(100, 100, 1, .05, .2, kind)), 4 * stderr)


if __name__ == "__main__":
    unittest.main()

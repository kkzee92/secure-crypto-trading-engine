"""Spot Momentum Strategy — simple SMA crossover example."""

from dataclasses import dataclass
from typing import List, Dict, Any
from src.risk.risk_engine import Signal


class SpotMomentumStrategy:
    """
    Basic momentum: buy when short SMA > long SMA, sell when reverse.
    Suitable for trending spot markets. Fails in ranges.
    """

    def __init__(self, symbol: str, short_window: int = 20, long_window: int = 50):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, current_price: float, history: List[float]) -> Signal:
        # Demo logic — in real system compute SMAs from history
        # Here we simulate a mild uptrend for illustration
        if current_price > 65000:
            return Signal(
                side="buy",
                size_hint=0.03,  # 3% of equity suggested
                confidence=0.7,
                reason=f"Momentum positive on {self.symbol} (demo SMA logic)",
                metadata={"price": current_price, "asset_class": "spot"},
            )
        return Signal(
            side="hold",
            size_hint=0.0,
            confidence=0.4,
            reason="No clear momentum",
            metadata={"price": current_price, "asset_class": "spot"},
        )

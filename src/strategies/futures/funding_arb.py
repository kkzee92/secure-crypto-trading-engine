"""Futures Funding Rate Arbitrage conceptual strategy."""

from src.risk.risk_engine import Signal


class FundingArbStrategy:
    """
    Delta-neutral: long spot + short perp when funding is highly positive (shorts pay longs).
    Or reverse when funding is deeply negative.
    Earns funding while remaining market-neutral.
    Risks: funding flip, basis risk, liquidation on the leveraged leg, execution slippage.
    """

    def __init__(self, symbol: str, funding_threshold: float = 0.0005):  # 0.05% per period
        self.symbol = symbol
        self.funding_threshold = funding_threshold

    def generate_signal(self, current_funding_rate: float, spot_price: float, perp_price: float) -> Signal:
        if current_funding_rate > self.funding_threshold:
            return Signal(
                side="buy",  # conceptually long spot / short perp
                size_hint=0.1,
                confidence=0.75,
                reason=f"Positive funding {current_funding_rate:.6f} > threshold — long spot / short perp",
                metadata={
                    "asset_class": "futures",
                    "funding_rate": current_funding_rate,
                    "basis": perp_price - spot_price,
                },
            )
        return Signal(
            side="hold",
            size_hint=0.0,
            confidence=0.3,
            reason="Funding not extreme enough for arb",
            metadata={"asset_class": "futures", "funding_rate": current_funding_rate},
        )

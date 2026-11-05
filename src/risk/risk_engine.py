"""Risk Engine — deterministic pre-trade gates. Always the final word."""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class Signal:
    side: str  # "buy", "sell", "hold"
    size_hint: float  # suggested fraction or absolute (context-dependent)
    confidence: float
    reason: str
    metadata: Dict[str, Any] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class RiskDecision:
    approved: bool
    reason: str
    adjusted_size: Optional[float] = None
    metadata: Dict[str, Any] = None

    def to_dict(self):
        return asdict(self)


class RiskEngine:
    def __init__(
        self,
        max_position_pct: float = 0.05,
        max_daily_loss_pct: float = 0.03,
        max_leverage: float = 2.0,
        max_total_exposure_pct: float = 0.20,
    ):
        self.max_position_pct = max_position_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_leverage = max_leverage
        self.max_total_exposure_pct = max_total_exposure_pct
        self.daily_pnl = 0.0  # track in production

    def evaluate(self, signal: Signal, current_equity: float, current_positions: Dict) -> RiskDecision:
        if signal.side == "hold" or signal.confidence < 0.5:
            return RiskDecision(approved=False, reason="Hold or low confidence")

        # Position size check
        proposed_size = signal.size_hint * current_equity
        max_allowed = self.max_position_pct * current_equity
        if proposed_size > max_allowed:
            adjusted = max_allowed
            return RiskDecision(
                approved=True,
                reason=f"Size capped from {proposed_size:.2f} to {adjusted:.2f}",
                adjusted_size=adjusted,
            )

        # Daily loss check (simplified)
        if self.daily_pnl < -self.max_daily_loss_pct * current_equity:
            return RiskDecision(approved=False, reason="Daily loss limit breached — circuit breaker")

        # Exposure check (simplified)
        current_exposure = sum(abs(v) for v in current_positions.values())
        if current_exposure + proposed_size > self.max_total_exposure_pct * current_equity:
            return RiskDecision(approved=False, reason="Total exposure limit would be exceeded")

        return RiskDecision(
            approved=True,
            reason="All risk checks passed",
            adjusted_size=proposed_size,
        )

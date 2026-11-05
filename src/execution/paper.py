"""Paper trading executor — never touches real funds."""

from typing import Dict, Any
from src.risk.risk_engine import RiskDecision


class PaperExecutor:
    def __init__(self, initial_equity: float):
        self.equity = initial_equity
        self.positions: Dict[str, float] = {}
        self.trades = []

    def execute(self, decision: RiskDecision) -> Dict[str, Any]:
        if not decision.approved:
            return {"status": "rejected", "reason": decision.reason}

        # Simulated fill
        size = decision.adjusted_size or 0
        self.equity -= size * 0.001  # tiny simulated fee
        self.trades.append({
            "size": size,
            "reason": decision.reason,
        })
        return {
            "status": "filled_paper",
            "size": size,
            "remaining_equity": round(self.equity, 2),
            "note": "This is a simulation. No real order was placed.",
        }

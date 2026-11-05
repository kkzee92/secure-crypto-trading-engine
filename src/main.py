"""Main entry point for the Secure Crypto Trading Engine."""

import argparse
import os
from datetime import datetime

from src.risk.risk_engine import RiskEngine
from src.security.audit import AuditLogger
from src.strategies.spot.momentum import SpotMomentumStrategy
from src.execution.paper import PaperExecutor


def main():
    parser = argparse.ArgumentParser(description="Secure Crypto Trading Engine")
    parser.add_argument("--mode", choices=["paper", "live"], default="paper",
                        help="paper (default) or live (requires extreme caution)")
    parser.add_argument("--strategy", default="spot_momentum")
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--equity", type=float, default=10000.0, help="Simulated equity for paper mode")
    args = parser.parse_args()

    if args.mode == "live":
        print("⚠️  LIVE MODE selected. Ensure you have thoroughly tested and reviewed risk settings.")
        confirm = input("Type 'I UNDERSTAND THE RISKS' to continue: ")
        if confirm != "I UNDERSTAND THE RISKS":
            print("Aborted.")
            return

    audit = AuditLogger(log_path="logs/audit.jsonl")
    risk = RiskEngine(
        max_position_pct=0.05,      # 5% of equity max per position
        max_daily_loss_pct=0.03,    # 3% daily loss limit
        max_leverage=2.0,
    )
    executor = PaperExecutor(initial_equity=args.equity) if args.mode == "paper" else None

    strategy = SpotMomentumStrategy(symbol=args.symbol)

    print(f"Starting {args.mode} mode | strategy={args.strategy} | symbol={args.symbol}")
    audit.log("system_start", {"mode": args.mode, "strategy": args.strategy, "symbol": args.symbol})

    # Demo loop (in real system this would be event-driven or scheduled)
    for i in range(3):
        # In production: fetch real data
        mock_price = 65000 + i * 100
        signal = strategy.generate_signal(current_price=mock_price, history=[])
        audit.log("signal", {"iteration": i, "signal": signal.to_dict()})

        decision = risk.evaluate(signal, current_equity=args.equity, current_positions={})
        audit.log("risk_decision", {"iteration": i, "decision": decision.to_dict()})

        if decision.approved and executor:
            result = executor.execute(decision)
            audit.log("execution", {"iteration": i, "result": result})
            print(f"[{i}] Signal: {signal.side} | Risk: {decision.reason} | Executed: {result.get('status')}")
        else:
            print(f"[{i}] Signal: {signal.side} | REJECTED: {decision.reason}")

    print("Demo complete. Check logs/audit.jsonl")
    audit.log("system_stop", {"timestamp": datetime.utcnow().isoformat()})


if __name__ == "__main__":
    main()

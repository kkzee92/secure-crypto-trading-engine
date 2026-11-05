# Secure Crypto Trading Engine

Automated cryptocurrency trading **information system** with modular strategies per asset class, strong cyber/data security architecture, and risk gates.

**⚠️ DISCLAIMER**: This is educational software for research and paper trading only. Cryptocurrency trading involves substantial risk of loss. Never trade with funds you cannot afford to lose. Always test thoroughly in sandbox/paper mode. API keys with withdrawal permissions are forbidden by design in this architecture.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Layer    │───▶│  Strategy Layer  │───▶│   Risk Engine   │
│ (OHLCV, funding,│    │ (per asset class)│    │ (pre-trade gates│
│ orderbook, news)│    │                  │    │  circuit breaker│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Audit / Logs   │◀───│ Execution Layer  │◀───│ Secure Secrets  │
│ (immutable JSONL│    │ (ccxt + safety)  │    │ (env / vault)   │
│  + alerts)      │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Asset Classes Supported (Strategy Modules)

| Asset Class | Typical Instruments | Key Strategies | Risk Notes |
|-------------|---------------------|----------------|------------|
| **Spot** | BTC/USDT, ETH/USDT, alts | Momentum, Mean-reversion, DCA, Grid | Custody, volatility |
| **Futures / Perpetuals** | BTC-PERP, ETH-PERP | Funding rate arb, Basis (cash-and-carry), Trend with leverage caps | Liquidation, funding flips |
| **Options** | BTC/ETH options (Deribit-style) | Protective puts, Covered calls, Vol (straddle conceptual) | Greeks, liquidity, complexity |
| **DeFi / On-chain** | AMMs, lending, yield | LP provision (hedged), yield farming with risk params | Smart contract, IL, MEV |

## Security Architecture Highlights

- **Least privilege**: API keys never have withdrawal or transfer rights. Trade + read only.
- **Secrets management**: Environment variables or external vault (HashiCorp Vault / AWS Secrets Manager). Never commit keys.
- **Pre-trade risk engine**: Deterministic gates (position size %, max drawdown, daily loss limit, exposure caps) that can always veto.
- **Circuit breakers**: Automatic halt on volatility spikes, consecutive losses, or stale data.
- **Audit trail**: Every decision, signal, and order logged in append-only JSONL with timestamps and hashes.
- **Rate limiting & retries**: Built-in via ccxt + custom backoff.
- **Data integrity**: Timestamp checks, gap detection, multi-source validation.
- **PDPA / Privacy alignment**: Inspired by Singapore PDPA practices from related agent harnesses — synthetic data for testing, no real user PII in logs.

See [SECURITY.md](SECURITY.md) and [docs/architecture.md](docs/architecture.md) for full details.

## Quick Start (Paper Trading)

```bash
# Clone and setup
git clone https://github.com/kkzee92/secure-crypto-trading-engine.git
cd secure-crypto-trading-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy and configure (use sandbox keys)
cp config/.env.example .env
# Edit .env with sandbox API keys (NO real funds)

# Run paper mode example
python -m src.main --mode paper --strategy spot_momentum --symbol BTC/USDT
```

## Project Structure

```
src/
  data/          # Ingestion, indicators, multi-source
  strategies/    # Per-asset-class strategy modules
  security/      # Secrets, encryption helpers, audit
  execution/     # Safe order placement via ccxt
  risk/          # Risk engine, position sizing, circuit breakers
  main.py        # Entry point
docs/            # Architecture, strategy details
config/          # Example configs
tests/           # Unit tests for risk & strategies
```

## Enhancing Strategies

Strategies are pure functions or classes that take market data → emit signals. The risk engine always sits between signal and execution.

Example enhancements per class:
- **Spot**: Add on-chain metrics (exchange inflows), sentiment.
- **Futures**: Dynamic funding rate thresholds, cross-exchange basis.
- **Options**: Greeks calculation, vol surface fitting.
- **DeFi**: Impermanent loss estimators, protocol risk scores.

## Contributing / AI Agent Harness

This project follows safe AI coding practices similar to agent harness demos: clear AGENTS.md rules, CI gates, human review for production changes, and disclosure of AI-assisted contributions.

## License

MIT

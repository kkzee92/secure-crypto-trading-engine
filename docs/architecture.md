# Secure Crypto Trading Engine Architecture

## Layers

### 1. Data Layer (`src/data`)
- Multi-exchange ingestion via ccxt (REST + optional WebSocket).
- Indicators (SMA, RSI, ATR, funding rates).
- Stale-data detection and gap handling.
- Optional on-chain / news feeds (pluggable).

### 2. Strategy Layer (`src/strategies`)
Modular per asset class:

- **spot/**: Momentum, MeanReversion, DCA, Grid
- **futures/**: FundingArb, BasisTrade, LeveragedTrend
- **options/**: ProtectivePut, CoveredCall (conceptual, venue-specific)
- **defi/**: HedgedLP, YieldRisk

Strategies emit `Signal` objects: `{side, size_hint, confidence, reason, metadata}`.

### 3. Risk Engine (`src/risk`)
Deterministic gates (always runs, cannot be skipped in live mode):

- Max position size (% equity)
- Max total exposure
- Daily loss limit
- Max leverage (futures)
- Volatility circuit breaker (ATR spikes)
- Stale data veto
- Consecutive loss counter

Returns `ApprovedOrder` or `Rejected` with reason.

### 4. Execution Layer (`src/execution`)
- ccxt wrapper with `enableRateLimit=True`.
- Client order IDs for idempotency.
- Sandbox / paper mode support.
- Partial fill handling.
- Balance reconciliation.

### 5. Security & Audit (`src/security`)
- Secrets loader (env only).
- Audit logger (JSONL append-only).
- Optional encryption helpers for local state.
- Configuration validation.

## Asset Class Strategy Enhancements

### Spot
- Combine technicals with volume profile and exchange inflow/outflow proxies.
- Regime detection (trend vs range) to switch strategies.

### Futures / Perpetuals
- Funding rate mean-reversion thresholds.
- Basis monitoring across venues.
- Liquidation price awareness and auto-deleverage rules.

### Options
- Delta-hedging loops.
- IV vs RV comparison for vol trades.
- Defined-risk structures preferred.

### DeFi
- Impermanent loss estimators.
- Protocol TVL and audit score filters.
- Hedge via perps or options.

## Data Flow

Market data → Strategy.generate_signal() → RiskEngine.evaluate() → (if approved) Execution.place() → Audit.log()

## Extensibility

New strategies implement a common `BaseStrategy` interface. New risk rules can be composed into the engine.

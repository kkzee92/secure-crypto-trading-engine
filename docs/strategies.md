# Trading Strategies by Asset Class

## Spot

### Momentum (SMA Crossover / Breakout)
- **Logic**: Buy strength, sell weakness.
- **Best regime**: Strong trends.
- **Enhancement ideas**: Volume confirmation, multi-timeframe, regime filter (ADX).

### Mean Reversion (RSI, Bollinger)
- **Logic**: Fade extremes.
- **Best regime**: Ranges.
- **Enhancement**: Combine with funding or on-chain metrics.

### DCA / Grid
- **Logic**: Systematic accumulation or range harvesting.
- **Risk**: Prolonged trends against the grid.

## Futures / Perpetuals

### Funding Rate Arbitrage
- Long spot + short perp (or vice versa) to capture funding.
- Delta-neutral income.
- **Enhancements**: Multi-venue, dynamic thresholds, auto-rebalance on basis drift.

### Cash-and-Carry / Basis Trade
- Exploit premium of dated futures over spot.
- Hold to expiry for locked-in yield (minus costs).

### Leveraged Trend Following
- Same as spot momentum but with strict leverage and liquidation distance rules.
- Circuit breakers critical.

## Options

### Protective Put
- Buy puts against spot holdings. Defined downside.

### Covered Call
- Sell calls against holdings for premium income. Caps upside.

### Volatility (Straddle / Strangle)
- Buy when IV is low relative to expected RV; sell when rich.
- Requires continuous delta hedging for pure vol exposure.

## DeFi

### Hedged Liquidity Provision
- Provide to AMM and hedge delta with perps or options.
- Monitor IL vs fee income.

### Yield Farming with Risk Scoring
- Filter protocols by audit status, TVL, and historical exploits.
- Position size by risk score.

All strategies must pass the Risk Engine before any execution.

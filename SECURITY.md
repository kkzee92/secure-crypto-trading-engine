# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Please open a private security advisory or email the maintainer. Do not open public issues for vulnerabilities.

## Core Security Principles

1. **Least Privilege**
   - API keys: Trade + Read only. Withdrawals permanently disabled.
   - Sub-accounts preferred when available.
   - IP allowlists strongly recommended.

2. **Secrets Handling**
   - Never hardcode API keys, private keys, or seed phrases.
   - Use environment variables or a secrets manager.
   - `.env` files are gitignored.
   - Rotate keys regularly.

3. **Pre-Trade Controls**
   - Every order passes through the Risk Engine.
   - Hard limits on position size (% of equity), total exposure, daily loss.
   - Circuit breakers for abnormal volatility or consecutive losses.

4. **Auditability**
   - Append-only JSONL logs of signals, risk decisions, and orders.
   - Include timestamps, decision reasons, and hashes where practical.

5. **Data Security**
   - Prefer encrypted storage for any persistent state.
   - No real personal data in test fixtures.
   - Validate all external data (prices, timestamps).

6. **Operational**
   - Run with minimal OS privileges.
   - Monitor for anomalies (unexpected orders, balance changes).
   - Kill switch available (manual or automated).

## Forbidden Practices

- Storing withdrawal-enabled keys in the system.
- Disabling risk checks in production.
- Logging full API secrets.
- Using real funds without extensive paper trading and review.

This system is designed so that even if the strategy layer is compromised or generates bad signals, the risk and execution layers limit damage.

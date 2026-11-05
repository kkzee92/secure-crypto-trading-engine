# AGENTS.md — Rules for AI Coding Agents

You are assisting with a **secure automated crypto trading information system**. Follow these rules strictly.

## Absolute Rules

1. **Never generate code that hardcodes secrets**, API keys, private keys, or seed phrases.
2. **Never suggest or implement withdrawal-enabled API permissions**.
3. **Always keep the Risk Engine as a hard gate** between any signal and order placement. Do not bypass it.
4. **Prefer paper/sandbox mode** in examples and tests. Clearly mark live trading paths.
5. **Add or update tests** for any change to risk logic, position sizing, or execution.
6. **Log decisions** with reasons. Prefer structured (JSON) logs.
7. **Cite data sources** and handle stale/missing data explicitly.
8. **Disclose AI assistance** in commits/PRs (e.g., trailer `AI-assisted: true`).

## Recommended Practices

- Use type hints and docstrings.
- Keep strategies pure and testable independently of exchange.
- Validate configuration at startup.
- Implement circuit breakers for extreme conditions.
- Document strategy assumptions and known failure modes.

## Definition of Done for Changes

- Unit tests pass.
- No secrets in code.
- Risk checks remain intact.
- Documentation updated if architecture or strategy behavior changes.
- Human review for any production-impacting change.

This harness is inspired by safe AI agent practices (CI gates + human accountability).

"""Append-only audit logger for decisions and executions."""

import json
import os
from datetime import datetime
from typing import Dict, Any


class AuditLogger:
    def __init__(self, log_path: str = "logs/audit.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log(self, event_type: str, data: Dict[str, Any]):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event_type,
            "data": data,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

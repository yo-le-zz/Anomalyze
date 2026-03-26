from __future__ import annotations

from .models import Alert


def format_alert(alert: Alert) -> str:
    reasons = "; ".join(alert.reasons)
    return (
        f"[{alert.severity.upper()}] {alert.process_name} (pid={alert.pid}) "
        f"score={alert.risk_score}/100 -> {reasons}"
    )

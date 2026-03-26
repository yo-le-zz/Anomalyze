from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ProcessSample:
    """Single observation for one process."""

    pid: int
    process_name: str
    cpu_percent: float
    memory_mb: float
    open_files: int
    connection_count: int
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class BaselineStats:
    """Simple running baseline with Welford variance."""

    count: int = 0
    cpu_mean: float = 0.0
    cpu_m2: float = 0.0
    memory_mean: float = 0.0
    memory_m2: float = 0.0
    files_mean: float = 0.0
    files_m2: float = 0.0
    conn_mean: float = 0.0
    conn_m2: float = 0.0


@dataclass(slots=True)
class Alert:
    """Detection output enriched with risk metadata."""

    process_name: str
    pid: int
    severity: str
    risk_score: int
    reasons: list[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)

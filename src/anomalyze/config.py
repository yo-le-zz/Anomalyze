from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AnomalyzeConfig:
    sample_interval_seconds: float = 1.5
    baseline_min_samples: int = 25
    z_threshold: float = 3.0
    rapid_spawn_threshold: int = 15
    sensitive_paths: tuple[str, ...] = (
        "/etc",
        "/home",
        "/Users",
        "C:\\Users",
    )
    data_dir: Path = Path(".anomalyze")

    @property
    def baseline_file(self) -> Path:
        return self.data_dir / "baseline.json"

    @property
    def alerts_file(self) -> Path:
        return self.data_dir / "alerts.log"

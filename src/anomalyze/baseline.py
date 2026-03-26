from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import BaselineStats, ProcessSample


class BaselineStore:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._stats: dict[str, BaselineStats] = {}

    @property
    def stats(self) -> dict[str, BaselineStats]:
        return self._stats

    def load(self) -> None:
        if not self.file_path.exists():
            self._stats = {}
            return
        payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        self._stats = {name: BaselineStats(**data) for name, data in payload.items()}

    def save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        serializable = {name: asdict(stats) for name, stats in self._stats.items()}
        self.file_path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    def update(self, sample: ProcessSample) -> BaselineStats:
        stats = self._stats.get(sample.process_name, BaselineStats())
        stats.count += 1

        _update_running_stats(stats, "cpu", sample.cpu_percent)
        _update_running_stats(stats, "memory", sample.memory_mb)
        _update_running_stats(stats, "files", sample.open_files)
        _update_running_stats(stats, "conn", sample.connection_count)

        self._stats[sample.process_name] = stats
        return stats


def _update_running_stats(stats: BaselineStats, prefix: str, value: float) -> None:
    mean_key = f"{prefix}_mean"
    m2_key = f"{prefix}_m2"

    current_mean = getattr(stats, mean_key)
    current_m2 = getattr(stats, m2_key)

    delta = value - current_mean
    next_mean = current_mean + (delta / stats.count)
    next_delta = value - next_mean
    next_m2 = current_m2 + (delta * next_delta)

    setattr(stats, mean_key, next_mean)
    setattr(stats, m2_key, next_m2)

from __future__ import annotations

import math
from collections import Counter

from .config import AnomalyzeConfig
from .models import Alert, BaselineStats, ProcessSample


class Detector:
    def __init__(self, config: AnomalyzeConfig) -> None:
        self.config = config

    def detect(
        self,
        sample: ProcessSample,
        baseline: BaselineStats,
        spawn_counter: Counter[str],
    ) -> Alert | None:
        if baseline.count < self.config.baseline_min_samples:
            return None

        reasons: list[str] = []
        score = 0

        metric_checks = [
            ("CPU", sample.cpu_percent, baseline.cpu_mean, _stddev(baseline.cpu_m2, baseline.count), 25),
            (
                "RAM",
                sample.memory_mb,
                baseline.memory_mean,
                _stddev(baseline.memory_m2, baseline.count),
                20,
            ),
            (
                "Fichiers",
                sample.open_files,
                baseline.files_mean,
                _stddev(baseline.files_m2, baseline.count),
                20,
            ),
            (
                "Réseau",
                sample.connection_count,
                baseline.conn_mean,
                _stddev(baseline.conn_m2, baseline.count),
                20,
            ),
        ]

        anomalies = 0
        for label, value, mean, stdev, weight in metric_checks:
            z_score = abs(value - mean) / stdev if stdev else 0.0
            if z_score >= self.config.z_threshold:
                anomalies += 1
                reasons.append(f"{label} hors baseline (z={z_score:.2f}, valeur={value:.2f})")
                score += weight

        if spawn_counter[sample.process_name] >= self.config.rapid_spawn_threshold:
            reasons.append(
                f"rafale de processus ({spawn_counter[sample.process_name]} instances observées)"
            )
            score += 20

        if anomalies >= 3:
            reasons.append("corrélation multi-signal suspecte (CPU + mémoire/fichiers/réseau)")
            score += 20

        if score == 0:
            return None

        risk = min(100, score)
        severity = _severity_from_score(risk)
        return Alert(
            process_name=sample.process_name,
            pid=sample.pid,
            severity=severity,
            risk_score=risk,
            reasons=reasons,
        )


def _stddev(m2: float, count: int) -> float:
    if count <= 1:
        return 0.0
    return math.sqrt(m2 / (count - 1))


def _severity_from_score(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 50:
        return "suspicious"
    return "light"

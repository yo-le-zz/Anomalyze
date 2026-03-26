from collections import Counter

from anomalyze.config import AnomalyzeConfig
from anomalyze.detector import Detector
from anomalyze.models import BaselineStats, ProcessSample


def _warm_baseline() -> BaselineStats:
    return BaselineStats(
        count=50,
        cpu_mean=5.0,
        cpu_m2=49.0,
        memory_mean=100.0,
        memory_m2=490.0,
        files_mean=2.0,
        files_m2=49.0,
        conn_mean=1.0,
        conn_m2=49.0,
    )


def test_detector_returns_none_when_no_anomaly() -> None:
    detector = Detector(AnomalyzeConfig())
    sample = ProcessSample(
        pid=123,
        process_name="safe_app",
        cpu_percent=5.0,
        memory_mb=100.0,
        open_files=2,
        connection_count=1,
    )

    result = detector.detect(sample, _warm_baseline(), Counter())
    assert result is None


def test_detector_flags_critical_when_correlated_anomaly() -> None:
    detector = Detector(AnomalyzeConfig(rapid_spawn_threshold=3))
    sample = ProcessSample(
        pid=123,
        process_name="weird_app",
        cpu_percent=99.0,
        memory_mb=900.0,
        open_files=60,
        connection_count=50,
    )

    result = detector.detect(sample, _warm_baseline(), Counter({"weird_app": 4}))

    assert result is not None
    assert result.severity == "critical"
    assert result.risk_score >= 80
    assert len(result.reasons) >= 3

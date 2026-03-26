from __future__ import annotations

import argparse

if __package__ in (None, ""):
    # Allow direct execution: `python src/anomalyze/cli.py`
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from anomalyze.config import AnomalyzeConfig
else:
    from .config import AnomalyzeConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="anomalyze",
        description="Behavior-based anomaly detection for local process activity.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.5,
        help="Sampling interval in seconds (default: 1.5)",
    )
    parser.add_argument(
        "--loops",
        type=int,
        default=3,
        help="Number of loops to execute. Use a large number for continuous mode.",
    )
    parser.add_argument(
        "--baseline-min-samples",
        type=int,
        default=25,
        help="Minimum samples per app before anomaly detection.",
    )
    parser.add_argument(
        "--z-threshold",
        type=float,
        default=3.0,
        help="Z-score threshold for adaptive outlier detection.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = AnomalyzeConfig(
        sample_interval_seconds=args.interval,
        baseline_min_samples=args.baseline_min_samples,
        z_threshold=args.z_threshold,
    )

    # Lazy import to keep CLI importable even if runtime deps are missing.
    if __package__ in (None, ""):
        from anomalyze.engine import AnomalyzeEngine
    else:
        from .engine import AnomalyzeEngine

    AnomalyzeEngine(config).run(loops=args.loops)


if __name__ == "__main__":
    main()

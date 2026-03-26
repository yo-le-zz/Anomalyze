from __future__ import annotations

import argparse

from .config import AnomalyzeConfig
from .engine import AnomalyzeEngine


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
    AnomalyzeEngine(config).run(loops=args.loops)


if __name__ == "__main__":
    main()

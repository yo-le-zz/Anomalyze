# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Fixed CLI execution from file path (`python src/anomalyze/cli.py`) by handling package-relative imports safely.
- Improved process burst detection to count **new PIDs between cycles** instead of static concurrent instances.
- Switched network connection collection to `proc.net_connections()`.
- Relaxed build-system requirement (`setuptools` without hard `>=69` pin) for better compatibility.

### Added
- Nuitka build support via optional dependency group `build` and helper script `scripts/build_nuitka.sh`.
- README section for binary compilation with Nuitka.

## [0.1.0] - 2026-03-26

### Added
- Initial Python package structure (`src/anomalyze`) with CLI entrypoint.
- Process telemetry collection (CPU, RAM, open files, network connections) using `psutil`.
- Baseline storage with running mean/variance per process name.
- Adaptive anomaly detection with z-score and rapid-spawn detection.
- Multi-signal correlation and risk scoring with alert severity levels.
- Persistent baseline and alert logging under `.anomalyze/`.
- Initial developer tooling (`pyproject.toml`, pytest/ruff settings).
- Basic unit tests for detector scoring behavior.

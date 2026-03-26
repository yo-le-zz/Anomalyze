# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

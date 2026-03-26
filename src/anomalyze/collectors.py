from __future__ import annotations

from collections import Counter

import psutil

from .models import ProcessSample


def collect_process_samples() -> tuple[list[ProcessSample], Counter[str]]:
    """Collect lightweight process telemetry and spawn-rate by process name."""
    samples: list[ProcessSample] = []
    spawn_counter: Counter[str] = Counter()

    for proc in psutil.process_iter(
        attrs=["pid", "name", "cpu_percent", "memory_info"], ad_value=None
    ):
        try:
            info = proc.info
            name = (info.get("name") or f"pid-{info['pid']}").lower()
            memory_mb = ((info.get("memory_info").rss if info.get("memory_info") else 0) / 1024**2)
            open_files = len(proc.open_files()) if proc.is_running() else 0
            conn_count = len(proc.connections(kind="inet")) if proc.is_running() else 0

            samples.append(
                ProcessSample(
                    pid=info["pid"],
                    process_name=name,
                    cpu_percent=float(info.get("cpu_percent") or 0.0),
                    memory_mb=float(memory_mb),
                    open_files=open_files,
                    connection_count=conn_count,
                )
            )
            spawn_counter[name] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return samples, spawn_counter

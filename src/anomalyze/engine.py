from __future__ import annotations

import time

from .alerts import format_alert
from .baseline import BaselineStore
from .collectors import collect_process_samples
from .config import AnomalyzeConfig
from .detector import Detector
from .logging_utils import configure_logging


class AnomalyzeEngine:
    def __init__(self, config: AnomalyzeConfig | None = None) -> None:
        self.config = config or AnomalyzeConfig()
        self.logger = configure_logging(self.config.alerts_file)
        self.baseline_store = BaselineStore(self.config.baseline_file)
        self.detector = Detector(self.config)

    def run(self, loops: int | None = None) -> None:
        self.baseline_store.load()
        loop_count = 0

        self.logger.info("Anomalyze démarré (intervalle=%.1fs)", self.config.sample_interval_seconds)
        while loops is None or loop_count < loops:
            samples, spawn_counter = collect_process_samples()
            for sample in samples:
                baseline = self.baseline_store.update(sample)
                alert = self.detector.detect(sample, baseline, spawn_counter)
                if alert:
                    self.logger.warning(format_alert(alert))

            self.baseline_store.save()
            loop_count += 1
            time.sleep(self.config.sample_interval_seconds)

        self.logger.info("Anomalyze arrêté après %s boucle(s)", loop_count)

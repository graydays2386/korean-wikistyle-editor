# -*- coding: utf-8 -*-
import time
from contextlib import contextmanager


@contextmanager
def measure_latency(metrics: dict, name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        metrics[name] = round(elapsed, 4)


def print_latency_report(metrics: dict) -> None:
    print("\n========== LATENCY REPORT ==========")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f} sec")
    print("====================================\n")
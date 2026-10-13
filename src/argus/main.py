
import os
import socket
import time

from fastapi import FastAPI, Query

app = FastAPI(
    title="Argus Backend",
    description="A workload for learning Kubernetes through observation.",
    version="0.1.0",
)

START_TIME = time.monotonic()


@app.get("/")
def root():
    return {"hostname": socket.gethostname()}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return{
        "hostname":socket.gethostname(),
        "pid":os.getpid(),
        "uptime_seconds":round(time.monotonic() - START_TIME , 2),
        "cpu_count":os.cpu_count()
    }


@app.get("/cpu")
def burn_cpu(
    seconds: int = Query(default=5, ge=1, le=30),
):
    start = time.perf_counter()
    deadline = start + seconds
    iterations = 0
    value = 1

    # Deliberately consume CPU for load-testing experiments.
    while time.perf_counter() < deadline:
        value = (value * 31 + 7) % 1_000_003
        iterations += 1

    elapsed = time.perf_counter() - start

    return {
        "hostname": socket.gethostname(),
        "requested_seconds": seconds,
        "elapsed_seconds": round(elapsed, 3),
        "iterations": iterations,
    }

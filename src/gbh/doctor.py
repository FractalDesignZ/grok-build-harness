"""Environment doctor. Never claims a scientific gate."""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any


def probe() -> dict[str, Any]:
    report: dict[str, Any] = {
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "cwd": str(Path.cwd()),
        "which": {
            "uv": shutil.which("uv"),
            "just": shutil.which("just"),
            "nvidia-smi": shutil.which("nvidia-smi"),
        },
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "gpus": [],
        "torch": None,
    }
    try:
        import torch  # type: ignore

        report["torch"] = {
            "version": torch.__version__,
            "cuda": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "bf16_gpu": bool(
                torch.cuda.is_available() and torch.cuda.is_bf16_supported()
            ),
        }
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                report["gpus"].append(
                    {
                        "index": i,
                        "name": props.name,
                        "total_memory_gb": round(props.total_memory / 1024**3, 2),
                        "major": props.major,
                        "minor": props.minor,
                    }
                )
    except Exception as exc:  # pragma: no cover
        report["torch"] = {"error": str(exc)}
    return report


def write_report(path: Path) -> dict[str, Any]:
    report = probe()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

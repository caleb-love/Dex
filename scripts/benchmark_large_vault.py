#!/usr/bin/env python3
"""Benchmark core file traversal operations on a synthetic large vault."""

from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path


PARA_DIRS = [
    "00-Inbox/Meetings",
    "00-Inbox/Ideas",
    "00-Inbox/Daily_Plans",
    "01-Quarter_Goals",
    "02-Week_Priorities",
    "03-Tasks",
    "04-Projects",
    "05-Areas/People/Internal",
    "05-Areas/People/External",
    "05-Areas/Companies",
    "05-Areas/Career/Evidence",
    "06-Resources/Intel/Meeting_Intel",
    "06-Resources/Learnings",
    "07-Archives",
    "System",
]


def create_synthetic_vault(root: Path, file_count: int) -> None:
    for d in PARA_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "03-Tasks/Tasks.md").write_text("# Tasks\n", encoding="utf-8")

    for idx in range(file_count):
        if idx % 5 == 0:
            path = root / "00-Inbox/Meetings" / f"meeting-{idx:05d}.md"
            payload = f"# Meeting {idx}\n- follow-up task task-{idx:05d}\n"
        elif idx % 5 == 1:
            path = root / "04-Projects" / f"project-{idx:05d}.md"
            payload = f"# Project {idx}\nReference: 03-Tasks/Tasks.md\n"
        elif idx % 5 == 2:
            path = root / "05-Areas/People/Internal" / f"person-{idx:05d}.md"
            payload = f"# Person {idx}\n- [ ] action item {idx}\n"
        elif idx % 5 == 3:
            path = root / "06-Resources/Learnings" / f"note-{idx:05d}.md"
            payload = f"# Learning {idx}\nkeywords: testing, automation\n"
        else:
            path = root / "07-Archives" / f"archive-{idx:05d}.md"
            payload = f"# Archived {idx}\n"
        path.write_text(payload, encoding="utf-8")


def benchmark_scan(root: Path) -> tuple[float, int]:
    start = time.perf_counter()
    files = list(root.rglob("*.md"))
    # Simulate lightweight parse work used by scripts/tools.
    _ = sum(1 for path in files if "task-" in path.read_text(encoding="utf-8", errors="ignore"))
    elapsed = time.perf_counter() - start
    return elapsed, len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark large-vault operations")
    parser.add_argument("--files", type=int, default=2000, help="Number of synthetic markdown files")
    parser.add_argument("--budget-seconds", type=float, default=5.0, help="Fail if elapsed > budget")
    parser.add_argument("--vault-root", default="", help="Optional existing directory for synthetic vault")
    args = parser.parse_args()

    if args.vault_root:
        vault_root = Path(args.vault_root).resolve()
        vault_root.mkdir(parents=True, exist_ok=True)
        create_synthetic_vault(vault_root, args.files)
        elapsed, scanned = benchmark_scan(vault_root)
    else:
        with tempfile.TemporaryDirectory(prefix="dex-large-vault-") as tmp:
            vault_root = Path(tmp)
            create_synthetic_vault(vault_root, args.files)
            elapsed, scanned = benchmark_scan(vault_root)

    print(f"large-vault benchmark: scanned={scanned} files elapsed={elapsed:.3f}s budget={args.budget_seconds:.3f}s")
    if elapsed > args.budget_seconds:
        print("Performance budget exceeded.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

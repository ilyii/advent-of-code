"""
Advent of Code Profiler
Tracks metrics for each day/year and generates reports.
"""

import json
import os
import statistics
import time
import tracemalloc
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

# Global metrics file path (relative to repo root)
METRICS_FILE = Path(__file__).parent / "metrics.json"


def load_metrics():
    """Load existing metrics from file"""
    if METRICS_FILE.exists():
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_metrics(metrics):
    """Save metrics to file"""
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, sort_keys=True)


def get_day_info():
    """Extract year and day from current working directory"""
    cwd = os.getcwd()
    parts = cwd.split(os.sep)
    
    # Find year (4-digit folder) and day (e.g., "05-12")
    year = None
    day = None
    
    for i, part in enumerate(parts):
        if part.isdigit() and len(part) == 4:
            year = part
            if i + 1 < len(parts):
                day = parts[i + 1]
            break
    
    return year, day


def _safe_int(value, default=None):
    try:
        return int(value)
    except Exception:
        return default


def _percentile(values, p: float):
    """Nearest-rank percentile for a non-empty list of floats."""
    if not values:
        return None
    if p <= 0:
        return min(values)
    if p >= 100:
        return max(values)
    values_sorted = sorted(values)
    # nearest-rank: k = ceil(p/100 * n)
    k = int((p / 100.0) * len(values_sorted) + 0.999999999)
    k = max(1, min(k, len(values_sorted)))
    return values_sorted[k - 1]


def get_input_stats(submission: bool):
    """Best-effort input stats for current folder.

    Returns (bytes, lines, filename) or (None, None, filename) if missing.
    """
    filename = "input.txt" if submission else "example_input.txt"
    try:
        p = Path(os.getcwd()) / filename
        if not p.exists():
            return None, None, filename
        data = p.read_text(encoding="utf-8")
        return len(data.encode("utf-8")), data.count("\n") + (1 if data else 0), filename
    except Exception:
        return None, None, filename


def record_run(
    runtime,
    part1=None,
    part2=None,
    submission=False,
    *,
    cpu_time=None,
    peak_kb=None,
    input_bytes=None,
    input_lines=None,
    input_file=None,
):
    """Record a single run's metrics"""
    year, day = get_day_info()
    if not year or not day:
        print("Warning: Could not determine year/day from path")
        return
    
    metrics = load_metrics()
    
    if year not in metrics:
        metrics[year] = {}
    
    if day not in metrics[year]:
        metrics[year][day] = {
            "runs": [],
            "best_time": None,
            "best_cpu_time": None,
            "part1": None,
            "part2": None,
        }
    
    run_data = {
        "timestamp": datetime.now().isoformat(),
        "runtime": runtime,
        "cpu_time": cpu_time,
        "peak_kb": peak_kb,
        "input_bytes": input_bytes,
        "input_lines": input_lines,
        "input_file": input_file,
        "submission": submission,
    }
    
    if part1 is not None:
        run_data["part1"] = str(part1)
        if submission:
            metrics[year][day]["part1"] = str(part1)
    
    if part2 is not None:
        run_data["part2"] = str(part2)
        if submission:
            metrics[year][day]["part2"] = str(part2)
    
    metrics[year][day]["runs"].append(run_data)
    
    # Update best time (only for submission runs)
    if submission:
        current_best = metrics[year][day]["best_time"]
        if current_best is None or runtime < current_best:
            metrics[year][day]["best_time"] = runtime

        current_best_cpu = metrics[year][day].get("best_cpu_time")
        if cpu_time is not None and (current_best_cpu is None or cpu_time < current_best_cpu):
            metrics[year][day]["best_cpu_time"] = cpu_time
    
    save_metrics(metrics)
    
    msg = f"[TIME] Runtime: {runtime:.4f}s"
    if cpu_time is not None:
        msg += f" | CPU: {cpu_time:.4f}s"
    if peak_kb is not None:
        msg += f" | PeakPyMem: {peak_kb:.0f} KB"
    if input_bytes is not None:
        msg += f" | Input: {input_bytes/1024.0:.1f} KB"
    print(msg)
    if submission and metrics[year][day]["best_time"] == runtime:
        print("[BEST] New best time!")


@contextmanager
def profile(submission=False):
    """Context manager for profiling solution execution"""
    start = time.perf_counter()
    start_cpu = time.process_time()
    input_bytes, input_lines, input_file = get_input_stats(submission)
    tracemalloc.start()
    results = {"part1": None, "part2": None}
    
    yield results
    
    elapsed = time.perf_counter() - start
    cpu_elapsed = time.process_time() - start_cpu
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak / 1024.0

    record_run(
        elapsed,
        results["part1"],
        results["part2"],
        submission,
        cpu_time=cpu_elapsed,
        peak_kb=peak_kb,
        input_bytes=input_bytes,
        input_lines=input_lines,
        input_file=input_file,
    )


def generate_report():
    """Generate a markdown report of all metrics"""
    metrics = load_metrics()
    
    if not metrics:
        print("No metrics recorded yet.")
        return
    
    report_lines = [
        "# Advent of Code - Performance Report",
        f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
    ]
    
    total_time = 0
    total_days = 0
    
    for year in sorted(metrics.keys(), reverse=True):
        year_time = 0
        report_lines.append(f"\n## {year}\n")
        report_lines.append("| Day | Best | Median | P95 | Std | PeakPyMem | Input | Part 1 | Part 2 | Runs |")
        report_lines.append("|-----|------|--------|-----|-----|-----------|-------|--------|--------|------|")
        
        for day in sorted(metrics[year].keys()):
            data = metrics[year][day]
            best = data.get("best_time")
            best_str = f"{best:.4f}s" if best else "-"
            p1 = data.get("part1", "-") or "-"
            p2 = data.get("part2", "-") or "-"
            runs = len(data.get("runs", []))

            run_list = data.get("runs", [])
            submission_runs = [r for r in run_list if r.get("submission")]
            stat_runs = submission_runs if submission_runs else run_list
            runtimes = [r.get("runtime") for r in stat_runs if isinstance(r.get("runtime"), (int, float))]
            # Peak memory is useful even for example-mode runs; include all runs.
            peaks = [r.get("peak_kb") for r in run_list if isinstance(r.get("peak_kb"), (int, float))]
            # Prefer the most recent run for input stats
            input_bytes = None
            input_lines = None
            for r in reversed(run_list):
                if r.get("input_bytes") is not None:
                    input_bytes = r.get("input_bytes")
                    input_lines = r.get("input_lines")
                    break

            median = statistics.median(runtimes) if runtimes else None
            p95 = _percentile(runtimes, 95) if runtimes else None
            std = statistics.pstdev(runtimes) if len(runtimes) >= 2 else None
            peak_str = f"{max(peaks):.0f} KB" if peaks else "-"
            input_str = "-"
            if input_bytes is not None:
                if input_lines is not None:
                    input_str = f"{input_bytes/1024.0:.1f} KB / {input_lines} lines"
                else:
                    input_str = f"{input_bytes/1024.0:.1f} KB"

            median_str = f"{median:.4f}s" if median is not None else "-"
            p95_str = f"{p95:.4f}s" if p95 is not None else "-"
            std_str = f"{std:.4f}s" if std is not None else "-"
            
            # Truncate long answers
            p1 = p1[:15] + "..." if len(str(p1)) > 15 else p1
            p2 = p2[:15] + "..." if len(str(p2)) > 15 else p2
            
            report_lines.append(
                f"| {day} | {best_str} | {median_str} | {p95_str} | {std_str} | {peak_str} | {input_str} | {p1} | {p2} | {runs} |"
            )
            
            if best:
                year_time += best
                total_days += 1
        
        report_lines.append(f"\n**Year Total: {year_time:.4f}s**")
        total_time += year_time
    
    report_lines.append(f"\n---\n**Grand Total: {total_time:.4f}s across {total_days} days**")
    
    # Calculate average
    if total_days > 0:
        report_lines.append(f"\n**Average: {total_time/total_days:.4f}s per day**")
    
    report = "\n".join(report_lines)
    
    # Save report
    report_path = Path(__file__).parent / "PERFORMANCE.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print(f"\nReport saved to: {report_path}")


def print_summary():
    """Print a quick summary of today's metrics"""
    year, day = get_day_info()
    metrics = load_metrics()
    
    if year in metrics and day in metrics[year]:
        data = metrics[year][day]
        run_list = data.get("runs", [])
        latest = run_list[-1] if run_list else None
        print(f"\n[STATS] {year}/{day}:")
        print(f"   Best time: {data.get('best_time', 'N/A'):.4f}s" if data.get('best_time') else "   Best time: N/A")
        if latest and isinstance(latest.get("runtime"), (int, float)):
            cpu = latest.get("cpu_time")
            peak = latest.get("peak_kb")
            ib = latest.get("input_bytes")
            il = latest.get("input_lines")
            extra = []
            if isinstance(cpu, (int, float)):
                extra.append(f"CPU {cpu:.4f}s")
            if isinstance(peak, (int, float)):
                extra.append(f"PeakPyMem {peak:.0f} KB")
            if isinstance(ib, (int, float)):
                if isinstance(il, int):
                    extra.append(f"Input {ib/1024.0:.1f} KB / {il} lines")
                else:
                    extra.append(f"Input {ib/1024.0:.1f} KB")
            if extra:
                print(f"   Latest: {latest['runtime']:.4f}s ({' | '.join(extra)})")
        print(f"   Total runs: {len(data.get('runs', []))}")
        if data.get('part1'):
            print(f"   Part 1: {data['part1']}")
        if data.get('part2'):
            print(f"   Part 2: {data['part2']}")


def run_all(year=None):
    """Run all solutions and generate a fresh report"""
    import subprocess
    import re

    # Import setup logic (so missing input can be fetched automatically)
    try:
        from setup import MissingSessionError, setup_day
    except Exception:
        MissingSessionError = Exception  # type: ignore
        setup_day = None  # type: ignore
    
    repo_root = Path(__file__).parent
    
    # Find all year folders
    year_folders = []
    for item in repo_root.iterdir():
        if item.is_dir() and item.name.isdigit() and len(item.name) == 4:
            if year is None or item.name == str(year):
                year_folders.append(item)
    
    year_folders.sort(reverse=True)
    
    if not year_folders:
        print(f"No year folders found{f' for {year}' if year else ''}.")
        return
    
    print("Running all solutions...\n")
    
    for year_folder in year_folders:
        print(f"{'='*40}")
        print(f"Year {year_folder.name}")
        print(f"{'='*40}")
        
        # Find all day folders
        day_folders = []
        for day in year_folder.iterdir():
            if day.is_dir():
                # Check for solution.py or code.py
                solution = day / "solution.py"
                code = day / "code.py"
                if solution.exists() or code.exists():
                    day_folders.append(day)
        
        day_folders.sort(key=lambda x: x.name)
        
        for day_folder in day_folders:
            solution_file = day_folder / "solution.py"
            if not solution_file.exists():
                solution_file = day_folder / "code.py"
            
            # Check if input.txt exists
            input_file = day_folder / "input.txt"
            if not input_file.exists():
                # Try to fetch it automatically via setup.py
                day_match = re.search(r"(\d+)", day_folder.name)
                day_num = int(day_match.group(1)) if day_match else None
                year_num = int(year_folder.name)

                if setup_day is not None and day_num is not None:
                    print(f"  [FETCH] {day_folder.name}: missing input.txt", flush=True)
                    try:
                        setup_day(year_num, day_num, force=False)
                    except MissingSessionError as e:
                        print(f"  [SKIP]  {day_folder.name}: {e}")
                        continue
                    except Exception as e:
                        print(f"  [SKIP]  {day_folder.name}: fetch failed ({e})")
                        continue

                if not input_file.exists():
                    print(f"  [SKIP]  {day_folder.name}: No input.txt")
                    continue
            
            print(f"  [RUN]  {day_folder.name}...", end=" ", flush=True)
            
            try:
                result = subprocess.run(
                    ["python", str(solution_file), "-s"],
                    cwd=str(day_folder),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    # Extract runtime from output
                    for line in result.stdout.split('\n'):
                        if '[TIME]' in line:
                            print(line.strip())
                            break
                    else:
                        print("OK")
                else:
                    print(f"ERROR: {result.stderr[:50]}")
            except subprocess.TimeoutExpired:
                print("TIMEOUT (>60s)")
            except Exception as e:
                print(f"ERROR: {e}")
    
    print(f"\n{'='*40}")
    print("Generating report...")
    print(f"{'='*40}\n")
    generate_report()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Advent of Code Profiler")
    parser.add_argument("-r", "--report", action="store_true", help="Generate performance report")
    parser.add_argument("-a", "--all", action="store_true", help="Run all solutions and generate report")
    parser.add_argument("-y", "--year", type=int, help="Specific year to run (use with -a)")
    parser.add_argument("-s", "--summary", action="store_true", help="Show today's summary")
    parser.add_argument("-c", "--clear", action="store_true", help="Clear all metrics")
    args = parser.parse_args()
    
    if args.all:
        run_all(args.year)
    elif args.report:
        generate_report()
    elif args.summary:
        print_summary()
    elif args.clear:
        if input("Clear all metrics? (y/N): ").lower() == "y":
            save_metrics({})
            print("Metrics cleared.")
    else:
        parser.print_help()

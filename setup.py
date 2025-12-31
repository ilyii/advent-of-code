#!/usr/bin/env python
"""
Simple setup script for Advent of Code.
Creates a new day folder with template and fetches input.

Usage:
    python setup.py              # Today's puzzle
    python setup.py -y 2024 -d 5 # Specific day
"""
import argparse
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from markdownify import markdownify

load_dotenv()

REPO_ROOT = Path(__file__).parent
TEMPLATE = REPO_ROOT / "template.py"
AOC_URL = "https://adventofcode.com"


class MissingSessionError(RuntimeError):
    pass


def get_session():
    """Get AOC session token from .env"""
    session = os.getenv("AOC_SESSION")
    if not session:
        raise MissingSessionError(
            "AOC_SESSION not found in .env. Add AOC_SESSION=your_session_cookie"
        )
    return session


def fetch_input(year: int, day: int) -> str:
    """Fetch puzzle input from AOC"""
    url = f"{AOC_URL}/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": get_session()}, timeout=10)
    response.raise_for_status()
    return response.text.strip()


def fetch_description(year: int, day: int) -> str:
    """Fetch puzzle description page (HTML)."""
    url = f"{AOC_URL}/{year}/day/{day}"
    response = requests.get(url, cookies={"session": get_session()}, timeout=10)
    response.raise_for_status()

    return response.text


def extract_example(description: str) -> str:
    """Try to extract example input from the description HTML."""
    matches = re.findall(r"<pre><code>(.*?)</code></pre>", description, re.DOTALL)
    for match in matches:
        # Heuristic: example inputs usually have multiple lines or numbers
        if "\n" in match or re.search(r"\d", match):
            # Basic HTML unescape for common cases
            text = (
                match.replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&amp;", "&")
            )
            return text.strip()
    return "# Paste example input here"


def setup_day(year: int, day: int, force: bool = False):
    """Set up a new day folder"""
    day_folder = REPO_ROOT / str(year) / f"{day:02d}-12"

    day_folder.mkdir(parents=True, exist_ok=True)

    if day_folder.exists() and not force:
        print(f"Using existing folder: {day_folder}")
    else:
        print(f"Created: {day_folder}")
    
    # Copy template
    solution_file = day_folder / "solution.py"
    if TEMPLATE.exists():
        if force or not solution_file.exists():
            shutil.copy(TEMPLATE, solution_file)
            print("  -> solution.py (from template)")
    else:
        print("  Warning: template.py not found")
    
    # Fetch description
    try:
        desc_path = day_folder / "description.md"
        example_path = day_folder / "example_input.txt"

        if force or (not desc_path.exists()) or (not example_path.exists()):
            print("  Fetching description...")
            page_html = fetch_description(year, day)
            match = re.search(
                r'<article class="day-desc">(.*?)</article>',
                page_html,
                re.DOTALL,
            )
            article_html = match.group(1) if match else ""

            if force or not desc_path.exists():
                desc_md = markdownify(article_html, heading_style="ATX") if article_html else ""
                desc_path.write_text(desc_md, encoding="utf-8")
                print("  -> description.md")

            if force or not example_path.exists():
                example = extract_example(page_html)
                example_path.write_text(example, encoding="utf-8")
                print("  -> example_input.txt")
    except Exception as e:
        print(f"  Warning: Could not fetch description: {e}")
    
    # Fetch input
    try:
        input_path = day_folder / "input.txt"
        if force or not input_path.exists():
            print("  Fetching input...")
            input_data = fetch_input(year, day)
            input_path.write_text(input_data, encoding="utf-8")
            print("  -> input.txt")
    except Exception as e:
        print(f"  Warning: Could not fetch input: {e}")
    
    print(f"\nReady! cd {day_folder}")


def main():
    parser = argparse.ArgumentParser(description="Set up Advent of Code day")
    parser.add_argument("-y", "--year", type=int, default=datetime.now().year)
    parser.add_argument("-d", "--day", type=int, default=datetime.now().day)
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()
    
    try:
        setup_day(args.year, args.day, args.force)
    except MissingSessionError as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

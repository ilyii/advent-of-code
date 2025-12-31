# Advent of Code

My solutions for [Advent of Code](https://adventofcode.com/).

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your AOC session token to `.env`:
```
AOC_SESSION=your_session_cookie_here
```

## Usage

### Create a new day
```bash
python setup.py              # Today's puzzle
python setup.py -y 2024 -d 5 # Specific day
```

This creates `YEAR/DAY/` with:
- `solution.py` - Template to write your solution
- `input.txt` - Your puzzle input
- `example_input.txt` - Example from description
- `description.md` - Puzzle description

### Run your solution
```bash
cd 2024/05-12
python solution.py      # Run with example input
python solution.py -s   # Run with real input (submission)
```

### View performance stats
```bash
python profiler.py -r   # Generate report
python profiler.py -a   # Run all solutions + report
```

## Structure

```
advent-of-code/
├── setup.py        # Create new day
├── template.py     # Solution template
├── profiler.py     # Performance tracking
├── 2024/
│   ├── 01-12/
│   │   ├── solution.py
│   │   ├── input.txt
│   │   └── example_input.txt
│   └── ...
└── metrics.json    # Saved performance data
```

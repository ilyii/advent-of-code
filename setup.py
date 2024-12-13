import os
import re
import shutil
import sys
from argparse import ArgumentParser
from datetime import datetime

import markdownify
import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv

init()
load_dotenv()
AOC_SESSION = os.getenv("AOC_SESSION")

def printc(message, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{message}{Style.RESET_ALL}")



def fetch(directory, day, year):
    url = f"https://adventofcode.com/{year}/day/{day}"
    printc(f"URL for day {day}, year {year}: {url}", Fore.CYAN)
    url += "/input"
    headers = {"Cookie": f"session={AOC_SESSION}"}
    response = requests.get(url, headers=headers)
    input_file_path = os.path.join(directory, "input.txt")
    example_input_file_path = os.path.join(directory, "example_input.txt")

    ret_code = 0
    if response.status_code == 200:
        input_data = response.text.strip()
        example_input_data = "Placeholder for example input..."
        printc("Input data fetched successfully.", Fore.GREEN)
    else:
        printc(
            f"Failed to fetch input data for Day {day}. Status Code: {response.status_code}",
            Fore.RED,
        )
        ret_code = response.status_code
        input_data = ""
        example_input_data = ""

    with open(input_file_path, "w", encoding="utf-8") as input_file:
        input_file.write(input_data)
    with open(example_input_file_path, "w", encoding="utf-8") as example_input_file:
        example_input_file.write(example_input_data)

    return ret_code, input_file_path, example_input_file_path


def find_example_input(md_path, example_input_file_path):
    assert os.path.exists(md_path), printc(f"Markdown file not found: {md_path}", Fore.RED)
    assert os.path.exists(example_input_file_path), printc(f"Example input file not found: {example_input_file_path}", Fore.RED)

    with open(md_path, "r") as md_file:
        md_content = md_file.read()
        code_blocks = re.findall(r"```(.*?)```", md_content, re.DOTALL)
        if len(code_blocks) > 0:
            example_input = code_blocks[0].strip()
            with open(example_input_file_path, "w") as example_input_file:
                example_input_file.write(example_input)
            printc("Example input fetched from markdown file.", Fore.GREEN)
        else:
            printc("No code blocks found in markdown file. Skipping...", Fore.YELLOW)


def get_description(day, year):
    url = f"https://adventofcode.com/{year}/day/{day}"
    headers = {"Cookie": f"session={AOC_SESSION}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        description = response.text
        description = description.split('<article class="day-desc">')[1]
        description = description.split("</article>")[0]
        description = description.replace("<p>", "").replace("</p>", "\n")
    
        return description
    else:
        printc(
            f"Failed to fetch description for Day {day}. Status Code: {response.status_code}",
            Fore.RED,
        )


def get_args():
    parser = ArgumentParser()
    parser.add_argument( "-d", "--day", dest="day", type=int, default=datetime.now().day)
    parser.add_argument("-y", "--year", dest="year",type=int, default=datetime.now().year)
    return parser.parse_args()


# -------- MAIN -------- #
if __name__ == "__main__":
    args = get_args()
    assert 1 <= args.day <= 25, printc(f"--day must be between 1 and 25! (Got {args.day})", Fore.RED)
    
    # INITIALIZATION
    printc(f"Creating files for {args.day}-12-{args.year}...", Fore.CYAN)
    year_path = os.path.join(os.getcwd(), str(args.year))
    day_path = os.path.join(year_path, f"{args.day:02d}-12")
    os.makedirs(day_path, exist_ok=True)

    # FETCH INPUT FROM adventofcode.com
    ret_code, _, example_input_file_path = fetch(day_path, args.day, args.year)

    # BUILD PY SCRIPT
    template_path = os.path.join(os.path.dirname(__file__), "template.py")
    script_path = os.path.join(day_path, "solution.py")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    if not os.path.exists(script_path):
        with open(script_path, "w+", encoding="utf-8") as f:
            f.write(template)
            printc("Template script created.", Fore.GREEN)
    else:
        printc("Template script already exists. Skipping...", Fore.YELLOW)

    # BUILD DESCRIPTION
    description = get_description(args.day, args.year)
    try:
        descpath = os.path.join(os.getcwd(), str(args.year), f"{args.day:02d}-12", "description.md")
        markdown_text = markdownify.markdownify(description)
        with open(descpath, "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except Exception as e:
        printc(f"Failed to create the markdown description: {e}", Fore.RED)
        printc("Saving the description as in raw format instead...", Fore.YELLOW)
        with open(os.path.join(day_path, "description.txt"), "w", encoding="utf-8") as f:
            f.write(description)

    # FETCH EXAMPLE INPUT FROM MARKDOWN
    find_example_input(descpath, example_input_file_path) 
       
    printc(f"Files created for {args.day}-12-{args.year}.", Fore.GREEN)
    printc("Done.", Fore.CYAN)
    

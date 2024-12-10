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


cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(cur_dir))



def create_day_folder(day):
    folder_path = f"{day:02d}-12"
    folder_path = os.path.join(cur_dir, folder_path)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def fetch_input(folder_path, day, year):
    url = f"https://adventofcode.com/{year}/day/{day}"
    printc(f"URL for day {day}, year {year}: {url}", Fore.CYAN)
    url += "/input"
    headers = {"Cookie": f"session={AOC_SESSION}"}
    response = requests.get(url, headers=headers)
    input_file_path = os.path.join(folder_path, "input.txt")
    example_input_file_path = os.path.join(folder_path, "example_input.txt")

    ret_code = 0
    if response.status_code == 200:
        input_data = response.text.strip()
        example_input_data = "Placeholder for example input..."
        printc(f"Input for Day {day} fetched successfully.", Fore.GREEN)
    else:
        printc(
            f"Failed to fetch input for Day {day}. Status Code: {response.status_code}",
            Fore.RED,
        )
        printc("Creating empty input file and example input file...", Fore.YELLOW)
        input_data = ""
        example_input_data = ""
        ret_code = -1

    with open(input_file_path, "w", encoding="utf-8") as input_file:
        input_file.write(input_data)
    with open(example_input_file_path, "w", encoding="utf-8") as example_input_file:
        example_input_file.write(example_input_data)

    return ret_code, input_file_path, example_input_file_path


def try_get_example_input(md_path, example_input_file_path):
    if not os.path.exists(example_input_file_path):
        printc("Example input file not found. Skipping...", Fore.YELLOW)
        return

    if not os.path.exists(md_path):
        printc("Markdown file not found. Skipping...", Fore.YELLOW)
        return

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


def get_exercise_description(current_day, year):
    url = f"https://adventofcode.com/{year}/day/{current_day}"
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
            f"Failed to fetch description for Day {current_day}. Status Code: {response.status_code}",
            Fore.RED,
        )


def create_python_script(day, template_path):
    script_path = f"{day:02d}-12/solution.py"
    script_path = os.path.join(cur_dir, script_path)

    with open(template_path, "r") as template_file:
        template = template_file.read()

    if not os.path.exists(script_path):
        with open(script_path, "w+") as script_file:
            script_file.write(template)
            printc(f"Python script for Day {day} created.", Fore.GREEN)
    else:
        printc(f"Python script for Day {day} already exists. Skipping...", Fore.YELLOW)


def create_markdown(day, description):
    markdown_path = f"{day:02d}-12/description.md"
    markdown_path = os.path.join(cur_dir, markdown_path)
    markdown_text = markdownify.markdownify(description)
    with open(markdown_path, "w") as markdown_file:
        markdown_file.write(markdown_text)
    printc(f"Markdown file for Day {day} created.", Fore.GREEN)

    return markdown_path


def main(current_day, year):
    if 1 <= current_day <= 25:
        printc(f"Creating files for Day {current_day}...", Fore.CYAN)
        folder_path = create_day_folder(current_day)
        ret_code, _, example_input_file_path = fetch_input(folder_path, current_day, year)

        template_path = "template.py"
        template_path = os.path.join(cur_dir, template_path)
        create_python_script(current_day, template_path)

        if ret_code != 0:
            printc(
                "Failed to fetch input data. Exiting before adding the markdown...",
                Fore.RED,
            )
            sys.exit(ret_code)

        exercise_description = get_exercise_description(current_day, year)
        md_path = create_markdown(current_day, exercise_description)
        try_get_example_input(md_path, example_input_file_path)
    else:
        printc(f"Day {current_day} is not valid for AOC {year}!", Fore.RED)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--day",
        dest="day",
        help="day to create. If not specified, today's day will be used",
        default=datetime.now().day,
    )

    parser.add_argument(
        "-y",
        "--year",
        dest="year",
        help="year to create. If not specified, the current year will be used",
        default=datetime.now().year,
    )
    args = parser.parse_args()
    main(int(args.day), int(args.year))
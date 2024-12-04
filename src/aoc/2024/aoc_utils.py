import os
import requests


def download_input_data(year: int, day: int) -> str:
    session_cookie = os.environ.get("AOC_SESSION_COOKIE")
    if not session_cookie:
        raise ValueError("AOC_SESSION_COOKIE environment variable not set")
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": session_cookie})
    response.raise_for_status()
    return response.text


def get_input_data(year: int, day: int) -> str:
    """Get inout data for the specified year/day (saving locally if not yet downloaded)"""
    root_dir = os.path.dirname(__file__)
    filename = f"{root_dir}/inputs/day{str(day).zfill(2)}_input.txt"
    try:
        with open(filename) as file:
            input_data = file.read()
    except FileNotFoundError:
        input_data = download_input_data(year, day)
        with open(filename, "w") as file:
            file.write(input_data)
    return input_data


def download_archive_inputs(start_year: int = 2015, end_year: int = 2023):
    """Download input data for for the specified years and store in the inputs folder"""
    for year in range(start_year, end_year):
        directory = f"{year}/inputs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for day in range(1, 26):
            get_input_data(year, day)


def generate_stub_files(year: int):
    """Generate stub files for the specified year"""
    year_directory = os.path.dirname(__file__)
    inputs_directory = os.path.join(year_directory, "inputs")
    if not os.path.exists(inputs_directory):
        os.makedirs(inputs_directory)
    with open(os.path.join(year_directory, "__init__.py"), "w") as f:
        pass
    for day in range(1, 26):
        with open(os.path.join(year_directory, f"day{day:02d}.py"), "w") as f:
            f.write(f'"""https://adventofcode.com/{year}/day/{day}"""\n\n')
            f.write("from aoc_utils import get_input_data\n\n")
            f.write(f"actual_input = get_input_data({year}, {day})\n\n\n")
            f.write('example_input = """xxx"""\n\n\n')
            f.write("def solve(inputs: str):\n")
            f.write("    values = tuple(map(int, inputs.splitlines()))\n\n")
            f.write('    print(f"Part 1: {False}")\n')
            f.write('    print(f"Part 2: {False}\\n")\n\n\n')
            f.write("solve(example_input)\n")
            f.write("# solve(actual_input)\n")

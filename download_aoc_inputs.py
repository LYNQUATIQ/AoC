import os
import requests

SESSION_COOKIE = "<PUT YOUR SESSION COOKIE HERE - DON'T COMMIT IT TO GIT!>"


def fetch_input_data(year, day):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": SESSION_COOKIE})
    response.raise_for_status()
    return response.text


for year in range(2015, 2024):
    directory = f"Archive/{year}/inputs"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for day in range(1, 26):
        data = fetch_input_data(year, day)
        filename = f"{directory}/day{str(day).zfill(2)}_input.txt"
        with open(filename, "w") as file:
            file.write(data)

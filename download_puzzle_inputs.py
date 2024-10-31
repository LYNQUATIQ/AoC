import os
import requests

SESSION_COOKIE = "53616c7465645f5f0a132f175f35083af2327bc61a534cc232e88b9ab5fb1c24f64a8ecd232481bb63613b680a11d252eb2e6d110cddf5ad1689a4e4e696bd53"


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

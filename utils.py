# supports the use of csv library
import csv

import re
from datetime import datetime
from special_character_map import CHARACTER_MAP

# this global variable will be set once the highest id value is found
next_ids = {}

# this is populated and used in runtime
athlete_edition_map = {}


# This function reads a csv file and return a list of lists
# each element of the returned list is a row in the csv file
# The first row is the header row
def read_csv_file(file_name):
    data_set = []
    with open(file_name, mode="r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_set.append(row)
    return data_set


# This function writes out a list of lists to a csv file.
# each element of the list is a row in the csv file
# The first row is the header row
def write_csv_file(file_name, data_set):
    with open(file_name, mode="w", newline="", encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        for row in data_set:
            csv_writer.writerow(row)


# creates a unique identifier (key) from each object type using specific row values
def create_unique_id(
    data: dict[str, str], column_names: list[str], is_paris_names: bool = False
) -> str:
    out = ""
    for i, name in enumerate(column_names):
        if i != 0:
            out += ","
        id_part = data[name]
        if is_paris_names and name == "name_tv":
            # special case for paris data - fallback using re-organized "name" if name_tv is empty
            if not bool(id_part):
                id_part = convert_paris_to_normal_name(data["name"])
        if not is_paris_names and name == "name":
            id_part = normalize_name(id_part)
        out += f"{id_part.lower()}"
    return out


# Normalizes the special accented characters for the athlete names
def normalize_name(name: str):
    out = ""
    for ch in name:
        try:
            ch = CHARACTER_MAP[ch]
        except KeyError:
            pass
        out += ch
    return out


def convert_paris_to_normal_name(name: str) -> str:
    non_tv_name = name.split(" ")
    return " ".join([non_tv_name[-1]] + non_tv_name[:-1])


def create_athlete_edition_id_map(
    event_data: list[list[str]], editions: list[list[str]]
):
    global athlete_edition_map

    edition_year_idx = 3
    edition_id_idx = 1
    edition_map = {}
    for row in editions[1:]:
        edition_map[row[edition_id_idx]] = row[edition_year_idx]

    athlete_id_idx = 7
    edition_id_idx = 1
    for row in event_data[1:]:
        if row[athlete_id_idx] not in athlete_edition_map:
            athlete_edition_map[row[athlete_id_idx]] = edition_map[row[edition_id_idx]]


# Normalizes the special dates
def normalize_date(date_str: str, athlete_id: int | None = None) -> str:
    global athlete_edition_map
    output_format = "%d-%b-%Y"
    date_str = date_str.strip()
    if not date_str:
        return ""

    def predict_prefix(day: str, mon: str, year: str, athlete_id: int) -> str:
        edition_year = athlete_edition_map[str(athlete_id)]
        prefix = 20
        while int(edition_year) <= int(f"{prefix}{year}"):
            prefix -= 1

        return datetime.strptime(f"{day}-{mon}-{prefix}{year}", "%d-%b-%Y").strftime(
            output_format
        )

    if date_str.isdigit() and len(date_str) == 4:
        return datetime(int(date_str), 1, 1).strftime(output_format)

    first_match_text = re.search(r"^(\d{1,2})-([A-Za-z]{3})-(\d{2})$", date_str)
    if first_match_text and athlete_id is not None:
        day, mon, year = first_match_text.groups()
        return predict_prefix(day, mon, year, athlete_id)

    second_match_text = re.search(r"^([A-Za-z]{3})-(\d{2})$", date_str)
    if second_match_text and athlete_id is not None:
        mon, year = second_match_text.groups()
        return predict_prefix("01", mon, year, athlete_id)

    formats = ["%d %B %Y", "%Y-%m-%d", "%d-%b-%Y", "%B %Y", "%b %d, %Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime(output_format)
        except ValueError:
            continue

    # final try if it still has not been parsed, but has a year in it, we use that (arbitrarily chose the largest)
    matches = re.findall(r"\d{4}", date_str)
    if len(matches) > 0:
        return datetime(max([int(match) for match in matches]), 1, 1).strftime(
            output_format
        )

    print("invalid date:", date_str)
    return ""


# finds the maximum athlete id and sets global id tracker
def find_next_id(data: list[list[str]], key: str, index: int) -> int:
    global next_ids
    maximum = 0
    for i in range(1, len(data)):
        id = int(data[i][index])
        if id > maximum:
            maximum = id

    next_ids[key] = maximum + 1
    return next_ids[key]


# gets a new athlete id and increments the global tracker
def get_next_id(key) -> int:
    global next_ids
    ret = next_ids[key]
    next_ids[key] += 1
    return ret


# this function was generated by ChatGPT, prompt is in prompts.md
# gets all the permutations of a list o all possible lengths, used in the get_name_permutations function
def permutations_all_lengths(lst):
    def permute(cur, remaining, result):
        if cur:
            result.append(cur[:])

        for i in range(len(remaining)):
            permute(cur + [remaining[i]], remaining[:i] + remaining[i + 1 :], result)

    result = []
    permute([], lst, result)
    return result


# this function returns a list of potential names of an athlete
# all the names have the same first name, but if there are multiple last names then all
# of the permutations of every possible length are considered
def get_name_permutations(name: list[str]) -> list[str]:
    new_name_list = []
    for word in name[1:]:
        if "-" in word:
            unhyphenated = word.split("-")
            new_name_list += unhyphenated
        else:
            new_name_list.append(word)

    # if there are multiple last names we have to check the olympic data
    # against all of them and all of the permutations of them
    if len(new_name_list) > 1:
        permutations = permutations_all_lengths(new_name_list)
        return [" ".join([name[0]] + permutation) for permutation in permutations]
    else:
        return [" ".join(name)]

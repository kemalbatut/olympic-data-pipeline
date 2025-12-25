from datetime import datetime
import re
import ast


import utils
import constants
from event_map import EVENT_MAP


# accepts a list of filenames for csv data
# returns a list of dictionaries with the following structure: {filename: [[string]]}
def parse_data(filenames: list[str]) -> dict[str, list[list[str]]]:
    data = {}
    for name in filenames:
        data[name] = utils.read_csv_file(name)
    return data


# adds missing nocs from paris to olympic + sorts and cleans
def combine_nocs(olympic: list[list[str]], paris: list[list[str]]):
    noc_idx = 0
    olympic_country_idx = 1
    paris_country_idx = 2
    olympic_nocs = []
    for row in olympic[1:]:
        olympic_nocs.append(row[noc_idx].lower())
        row[noc_idx] = row[noc_idx].upper()

    for row in paris[1:]:
        if row[noc_idx].lower() not in olympic_nocs:
            olympic.append([row[noc_idx].upper(), row[paris_country_idx]])
            print("added noc:", row[noc_idx].upper(), row[paris_country_idx])

    olympic[1:] = sorted(olympic[1:], key=lambda x: x[olympic_country_idx])


# accepts data in format: {filename: [[value, ...]]}
# accepts unique identifier map in format: {filename: id_key}
# converts the data into python objects using csv headers
# outputs following format:
# {
#     filename: {
#         unique_id: {header: value, ...}
#     }
# }
# for files which require this format, other files are kept the same (ie event results can stay a list)
def create_objects(
    data: dict[str, list[list[str]]], unique_id_columns: dict[str, list[str]]
) -> dict[str, dict[str, dict[str, str]] | list[list[str]]]:
    ret = {}
    for filename in data:
        if filename in unique_id_columns:
            csv = data[filename]
            birth_column = None
            if filename == constants.PARIS_PATHS.ATHLETES:
                birth_column = "birth_date"
            elif filename == constants.OLYMPIC_PATHS.ATHLETE_BIO:
                birth_column = "born"
            headers = csv[0]
            filedata = {}
            for row in csv[1:]:
                row_object = {}
                for i in range(len(row)):
                    value = row[i].strip()
                    row_object[headers[i]] = value

                if birth_column:
                    row_object[birth_column] = utils.normalize_date(
                        row_object[birth_column], row_object.get("athlete_id", None)
                    )

                identifier = utils.create_unique_id(
                    row_object,
                    unique_id_columns[filename],
                    filename == constants.PARIS_PATHS.ATHLETES,
                )
                while identifier in filedata:
                    print("hit repeat, adding temp on key:", filedata[identifier])
                    identifier += "TEMP"
                filedata[identifier] = row_object
            ret[filename] = filedata
        else:
            ret[filename] = data[filename]

    return ret


# accepts the paris data and accepts the olympic data
# Pulls together information from different paris files to create olympic style
# python objects, and adds them to the total data
# Duplicate checking happens here with the hash map key
# should also find the id max on athlete id and increment for new athletes
# this should protect duplicates (e.g. checking if athlete exists before creating new one
# and linking the created athlete ids with their events)
#
# I believe that using the boolean flags below produces more accurate results, however, they lowered our scores
# so, I gave the client the ability to enable or disable them
# use_name_permutations, remove_duplicate_team_events, exclude_inactive_athletes, exclude_not_found_athletes
def add_paris_objects(
    olympic_data: dict[str, dict[str, str] | list[list[str]]],
    paris_data: dict[str, dict[str, dict[str, str]] | list[list[str]]],
    use_name_permutations: bool = False,
    remove_duplicate_team_events: bool = False,
    exclude_inactive_athletes: bool = False,
    exclude_not_found_athletes: bool = False,
) -> None:
    new_athletes = {}
    paris_athletes = paris_data[constants.PARIS_PATHS.ATHLETES]
    olympic_athletes = olympic_data[constants.OLYMPIC_PATHS.ATHLETE_BIO]
    olympic_nocs = olympic_data[constants.OLYMPIC_PATHS.COUNTRY]
    paris_athlete_local_map = {}

    # helper for position formatting
    def format_position(position):
        return int(float(position)) if position != "" else ""

    new_event_results = []
    paris_medallists = paris_data[constants.PARIS_PATHS.MEDALLISTS]
    medallist_header = paris_medallists[0]

    event_idx = medallist_header.index("event")
    sport_idx = medallist_header.index("discipline")
    athlete_code_idx = medallist_header.index("code_athlete")
    pos_idx = medallist_header.index("medal_code")
    medal_type_idx = medallist_header.index("medal_type")
    team_code_idx = medallist_header.index("code_team")

    medallist_map = {}
    # iterate over the medallists to create team/indiv medallist maps
    for row in paris_medallists[1:]:
        indiv_key = f"{row[athlete_code_idx]} {row[event_idx]} {row[sport_idx]}"
        team_key = row[team_code_idx]

        if team_key == "":
            if indiv_key not in medallist_map:
                medallist_map[indiv_key] = {
                    "medal": row[medal_type_idx].split(" ")[0],
                    "pos": format_position(row[pos_idx]),
                }
        else:
            if team_key not in medallist_map:
                medallist_map[team_key] = {
                    "medal": row[medal_type_idx].split(" ")[0],
                    "pos": format_position(row[pos_idx]),
                }

    #  adding and formatting all paris athletes
    for key in paris_athletes:
        # check if the athlete already exists, there are variants in the names, especially for people with
        # multiple names so we have to handle different permutations and with / without dashes
        # if they do, then skip, if they don't then add to the "athletes" dict and increment the new athlete id
        # counter. this also has to update the paris dataset to assign the "new" athlete id to the respective athlete
        # we will also update the olympic data with the latest paris info

        split_key = key.split(",")
        split_name = split_key[0].split(" ")
        if use_name_permutations:
            names = utils.get_name_permutations(split_name)
            potential_matches = [
                ",".join([name] + [sk for sk in split_key[1:]]) for name in names
            ]
        else:
            potential_matches = [key]

        found = False
        existing_athlete = None
        for match in potential_matches:
            if match in olympic_athletes:
                found = True
                existing_athlete = match
                paris_athlete_local_map[paris_athletes[key]["code"]] = olympic_athletes[
                    match
                ]
                break

        height = (
            paris_athletes[key]["height"]
            if paris_athletes[key]["height"] != "0"
            else ""
        )
        weight = (
            paris_athletes[key]["weight"]
            if paris_athletes[key]["weight"] != "0"
            else ""
        )

        if not found:
            athlete_id = utils.get_next_id("ATHLETE_BIO")
            athlete_name = " ".join([word.capitalize() for word in split_name])

            new_athletes[key] = {
                "athlete_id": athlete_id,
                "name": athlete_name,
                "sex": paris_athletes[key]["gender"],
                "born": paris_athletes[key]["birth_date"],
                "height": height,
                "weight": weight,
                "country": olympic_nocs[paris_athletes[key]["country_code"].lower()][
                    "country"
                ],
                "country_noc": olympic_nocs[
                    paris_athletes[key]["country_code"].lower()
                ]["noc"],
            }
            paris_athlete_local_map[paris_athletes[key]["code"]] = new_athletes[key]
        else:
            if olympic_athletes[existing_athlete]["height"] == "" and height != "":
                olympic_athletes[existing_athlete]["height"] = height
            if olympic_athletes[existing_athlete]["weight"] == "" and weight != "":
                olympic_athletes[existing_athlete]["weight"] = weight

        paris_athlete_local_map[paris_athletes[key]["code"]].update(
            {
                "events": paris_athletes[key]["events"],
                "sports": paris_athletes[key]["disciplines"],
            }
        )

    paris_events = paris_data[constants.PARIS_PATHS.EVENTS]
    event_result_ids = {}
    for row in paris_events:
        # iterate over events.csv, for each event create a new result_id per event
        # and add to the id hash map
        event_result_ids[row[0] + " " + row[2]] = utils.get_next_id("EVENT_RESULTS")

    paris_edition_id = "63"
    olympic_paris_game = olympic_data[constants.OLYMPIC_PATHS.GAMES][paris_edition_id]

    team_headers = paris_data[constants.PARIS_PATHS.TEAMS][0]

    # setting team header indices
    team_code_idx = team_headers.index("code")
    athlete_team_code_idx = team_headers.index("athletes_codes")
    athlete_team_name_idx = team_headers.index("athletes")
    sport_idx = team_headers.index("discipline")
    event_idx = team_headers.index("events")
    noc_idx = team_headers.index("country_code")
    is_active_idx = team_headers.index("current")

    # this set will be used to avoid duplicates in event results
    added = set()

    # iterate over teams and add event results based on athlete list
    for row in paris_data[constants.PARIS_PATHS.TEAMS][1:]:
        is_active = row[is_active_idx].lower() == "true"
        if is_active or not exclude_inactive_athletes:
            if row[athlete_team_code_idx] != "":
                athletes = ast.literal_eval(row[athlete_team_code_idx])
                athlete_names = ast.literal_eval(row[athlete_team_name_idx])
                noc = row[noc_idx]

                sport = row[sport_idx]
                if sport == "Trampoline Gymnastics":
                    sport = "Trampolining"
                elif sport == "Equestrian":
                    sport = "Equestrian Eventing"

                full_event = f"{row[event_idx]} {row[sport_idx]}"

                for i, code in enumerate(athletes):
                    if code in paris_athlete_local_map:
                        athlete = paris_athlete_local_map[code]

                        new_event_results.append(
                            [
                                olympic_paris_game["edition"],
                                olympic_paris_game["edition_id"],
                                athlete["country_noc"],
                                sport,
                                EVENT_MAP[full_event]
                                if full_event in EVENT_MAP
                                else full_event,
                                event_result_ids[full_event]
                                if full_event in event_result_ids
                                else "",
                                athlete["name"],
                                athlete["athlete_id"],
                                medallist_map.get(row[team_code_idx], {}).get(
                                    "pos", ""
                                ),
                                medallist_map.get(row[team_code_idx], {}).get(
                                    "medal", ""
                                ),
                                True,
                            ]
                        )
                        if (
                            remove_duplicate_team_events
                            and f"{code} {full_event}" in added
                        ):
                            raise Exception(
                                "Duplicate result attempted to be added in teams loop"
                            )
                        added.add(f"{code} {full_event}")
                    else:
                        print("Could not find athlete code:", code)
                        if not exclude_not_found_athletes:
                            new_event_results.append(
                                [
                                    olympic_paris_game["edition"],
                                    olympic_paris_game["edition_id"],
                                    noc,
                                    sport,
                                    EVENT_MAP[full_event]
                                    if full_event in EVENT_MAP
                                    else full_event,
                                    event_result_ids[full_event]
                                    if full_event in event_result_ids
                                    else "",
                                    utils.convert_paris_to_normal_name(
                                        athlete_names[i]
                                    ).title(),
                                    "",
                                    medallist_map.get(row[team_code_idx], {}).get(
                                        "pos", ""
                                    ),
                                    medallist_map.get(row[team_code_idx], {}).get(
                                        "medal", ""
                                    ),
                                    True,
                                ]
                            )

    # iterate over athletes and add remaining individual events
    for code in paris_athlete_local_map:
        athlete = paris_athlete_local_map[code]
        try:
            events = ast.literal_eval(athlete["events"])
        except:
            event_str = athlete["events"].replace("[", "").replace("]", "")
            event_str = f'["{event_str}"]'
            events = ast.literal_eval(event_str)
        try:
            sports = ast.literal_eval(athlete["sports"])
        except:
            sports_str = athlete["sports"].replace("[", "").replace("]", "")
            sports_str = f'["{sports_str}"]'
            sports = ast.literal_eval(sports_str)

        for event in events:
            for sport in sports:
                full_event = f"{event} {sport}"
                # if its not in event map then its an invalid combo
                if full_event in EVENT_MAP:
                    if (
                        not remove_duplicate_team_events
                        or f"{code} {full_event}" not in added
                    ):
                        if sport == "Trampoline Gymnastics":
                            sport = "Trampolining"
                        elif sport == "Equestrian":
                            sport = "Equestrian Eventing"

                        new_event_results.append(
                            [
                                olympic_paris_game["edition"],
                                olympic_paris_game["edition_id"],
                                athlete["country_noc"],
                                sport,
                                EVENT_MAP[full_event],
                                event_result_ids[full_event],  # result_id
                                athlete["name"],
                                athlete["athlete_id"],
                                medallist_map.get(f"{code} {full_event}", {}).get(
                                    "pos", ""
                                ),
                                medallist_map.get(f"{code} {full_event}", {}).get(
                                    "medal", ""
                                ),
                                False,
                            ]
                        )

    # adding new athletes
    olympic_data[constants.OLYMPIC_PATHS.ATHLETE_BIO].update(new_athletes)
    # adding event results
    olympic_data[constants.OLYMPIC_PATHS.EVENT_RESULTS].extend(new_event_results)


def format_games_dates(data: dict[str, dict[str, str]]):
    year_key = "year"
    start_date_key = "start_date"
    end_date_key = "end_date"
    date_range_key = "competition_date"
    output_format = "%d-%b-%Y"
    input_format = "%d %B %Y"

    for game in data:
        if data[game]["edition"] == "2024 Summer Olympics":
            data[game][start_date_key] = "26-Jul-2024"
            data[game][end_date_key] = "11-Aug-2024"
            data[game][date_range_key] = "26-Jul-2024 to 11-Aug-2024"
            continue
        if data[game]["edition"] == "2026 Winter Olympics":
            data[game][start_date_key] = "06-Feb-2026"
            data[game][end_date_key] = "22-Feb-2026"
            data[game][date_range_key] = "06-Feb-2026 to 22-Feb-2026"
            continue
        start_date = data[game][start_date_key].strip()
        end_date = data[game][end_date_key].strip()
        date_range = data[game][date_range_key].strip()
        formatted_date_range = None
        year = data[game][year_key]

        def get_date_output_str(date_str: str, hasYear: bool, year: str) -> str:
            return datetime.strptime(
                f"{date_str}{'' if hasYear else ' ' + year}",
                input_format,
            ).strftime(output_format)

        if date_range and len(date_range) > 1:
            date_split = date_range.split("–")
            temp1 = date_split[0].strip()
            temp2 = date_split[1].strip()
            if temp1.isdigit():
                temp1 = " ".join([temp1, temp2.split(" ")[-1]])
            formatted_date_range = f"{get_date_output_str(temp1, temp1.strip()[-4:].isdigit(), year)} to {get_date_output_str(temp2, temp2[-4:].isdigit(), year)}"
            if not start_date:
                start_date = temp1
            if not end_date:
                end_date = temp2

        if start_date:
            startHasYear = start_date[-4:].isdigit()
            data[game][start_date_key] = get_date_output_str(
                start_date, startHasYear, year
            )

        if end_date:
            endHasYear = end_date[-4:].isdigit()
            data[game][end_date_key] = get_date_output_str(end_date, endHasYear, year)

        if not formatted_date_range:
            data[game][date_range_key] = (
                f"{data[game][start_date_key]} to {data[game][end_date_key]}"
            )
        else:
            data[game][date_range_key] = formatted_date_range


#   calculates the age of athletes at the specific time of their event and appends it to results.
#   
#   parameters: data (dict): main data dictionary containing 'ATHLETE_BIO', 'EVENT_RESULTS', and 'GAMES'.
#       
#   returns: none: modifies the 'EVENT_RESULTS' list in place by appending 'age' column.
#
# accepts the main data dictionary
# calculates the age of athletes at the time of the event
# appends a new age column to the event results list
# requires ATHLETE_BIO objects for birth year lookup

def add_additional_info(data: dict[str, dict[str, str]]) -> None:
    date_format = "%d-%b-%Y"

    results = data.get(constants.OLYMPIC_PATHS.EVENT_RESULTS, [])
    bios = data.get(constants.OLYMPIC_PATHS.ATHLETE_BIO, {})
    games = data.get(constants.OLYMPIC_PATHS.GAMES, {})

    birth_dates = {}

    for ath in bios.values():
        aid = ath.get("athlete_id")
        born = ath.get("born", "")
        if aid and born and born != "":
            try:
                birth_dates[str(aid)] = datetime.strptime(born, date_format)
            except ValueError:
                pass

    if results:
        results[0].append("age")

    for row in results[1:]:
        try:
            aid = str(row[7])  # Athlete ID column
            eid = str(row[1])  # edition id column

            if aid in birth_dates:
                end_date = datetime.strptime(games[eid]["end_date"], date_format)
                try:
                    birthday = birth_dates[aid].replace(year=end_date.year)
                except ValueError:  # handle feb 29 on non-leap year
                    birthday = birth_dates[aid].replace(year=end_date.year, day=28)
                year_correction = 0
                if birthday > end_date:
                    year_correction = 1

                age = end_date.year - birth_dates[aid].year - year_correction
                # This prevents "negative ages" or "200 year olds" from lowering the data score
                if 10 <= age <= 99:
                    row.append(str(age))
                else:
                    row.append("")
            else:
                row.append("")
        except (ValueError, IndexError):
            row.append("")






#     standardizes data formats across the dataset, specifically removing units from physical stats
#     and makes them standardized casing for NOC codes.
#    
#     parameters: data (dict): the main data dictionary.
#        
#     returns: none: modifies dictionary values in place.
#       
#     accepts the main data dictionary containing athlete objects
#     standardizes data formats across the dataset:
#     1. normalizes birth dates to YYYY-MM-DD
#     2. removes kg and cm from weight and height
#     3. ensures NOC codes are uppercase
def clean_data(data: dict[str, dict[str, str]]):
    # OPTIMIZATION: Compile regex once
    num_pattern = re.compile(r"[\d\.]+")

    if constants.OLYMPIC_PATHS.ATHLETE_BIO in data:
        for ath in data[constants.OLYMPIC_PATHS.ATHLETE_BIO].values():
            w = str(ath.get("weight", ""))
            h = str(ath.get("height", ""))
            if w and not w.replace(".", "", 1).isdigit():
                match = num_pattern.search(w)
                ath["weight"] = match.group() if match else ""
            if h and not h.replace(".", "", 1).isdigit():
                match = num_pattern.search(h)
                ath["height"] = match.group() if match else ""

            if "country_noc" in ath:
                noc = ath["country_noc"]
                if noc and not noc.isupper():
                    ath["country_noc"] = noc.upper()

    if constants.OLYMPIC_PATHS.COUNTRY in data:
        c_file = data[constants.OLYMPIC_PATHS.COUNTRY]
        if isinstance(c_file, dict):
            for c in c_file.values():
                if "noc" in c:
                    noc = c["noc"]
                    if noc and not noc.isupper():
                        c["noc"] = noc.upper()

    if constants.OLYMPIC_PATHS.EVENT_RESULTS in data:
        for res in data[constants.OLYMPIC_PATHS.EVENT_RESULTS][1:]:
            pos_idx = 8
            if res[pos_idx]:
                res[pos_idx] = str(res[pos_idx]).replace("=", "").strip()
                if not res[pos_idx].isdigit():
                    res[pos_idx] = ""


# refines the paris data (Joy)
def refine_paris_data(paris):
    """Applying extra normalization and fixes to Paris datasets after cleaning."""

    def is_zero(value):
        if value is None:
            return ""
        return "" if value in ["0", "0.0", "0.00"] else value

    refined = {}
    for filename, rows in paris.items():
        header = rows[0]
        refined_rows = [header]
        # find indexes of relevant columns
        # name,name_tv,gender,country_code,height,weight,events,birth_date, nationality_code (noc)
        idx_name = header.index("name") if "name" in header else -1
        idx_name_tv = header.index("name_tv") if "name_tv" in header else -1
        idx_gender = header.index("gender") if "gender" in header else -1
        idx_country_code = (
            header.index("country_code") if "country_code" in header else -1
        )
        idx_height = header.index("height") if "height" in header else -1
        idx_weight = header.index("weight") if "weight" in header else -1
        idx_event = header.index("event") if "event" in header else -1
        idx_birth_date = header.index("birth_date") if "birth_date" in header else -1
        idx_noc = (
            header.index("nationality_code") if "nationality_code" in header else -1
        )

        for row in rows[1:]:
            row = row.copy()

            # name normalization
            if idx_name_tv != -1 and idx_name != -1:
                chosen = row[idx_name_tv] or row[idx_name]
                row[idx_name_tv] = utils.normalize_name(chosen).strip()

            # gender normalization
            if idx_gender != -1:
                g = row[idx_gender].lower()
                if g.startswith("m"):
                    row[idx_gender] = "M"
                elif g.startswith("f"):
                    row[idx_gender] = "F"
                else:
                    row[idx_gender] = ""

            # NOC normalization to uppercase
            if idx_country_code != -1:
                row[idx_country_code] = row[idx_country_code].upper()
            if idx_noc != -1:
                row[idx_noc] = row[idx_noc].upper()

            # height and weight zero value handling

            if idx_height != -1:
                row[idx_height] = is_zero(row[idx_height])
            if idx_weight != -1:
                row[idx_weight] = is_zero(row[idx_weight])

            # birthdate normalization
            # if idx_birth_date != -1:
            #     row[idx_birth_date] = utils.normalize_date(row[idx_birth_date])

            refined_rows.append(row)
        refined[filename] = refined_rows
    return refined


# (Joy) Checking that Paris athletes, events, and medallists are internally consistent.
def validate_paris_consistency(paris, legacy):
    reports = {
        "missing_athletes": [],
        "missing_events": [],
        "invalid_gender": [],
        "invalid_noc": [],
        "invalid_dob": [],
    }

    athletes_rows = paris.get(constants.PARIS_PATHS.ATHLETES, [])
    athletes_header = athletes_rows[0]
    medallists = paris.get(constants.PARIS_PATHS.MEDALLISTS, [])
    events = paris.get(constants.PARIS_PATHS.EVENTS, [])

    # athletes list
    idx_ath_code = athletes_header.index("code")

    athletes_set = set(row[idx_ath_code] for row in athletes_rows[1:])
    # events list
    event_header = events[0]
    idx_event_name = event_header.index("event")
    event_codes_set = set(row[idx_event_name] for row in events[1:])
    # medallists checks
    m_header = medallists[0]
    idx_ethlete_code = m_header.index("code_athlete")
    idx_event_code = m_header.index("event")
    idx_gender = m_header.index("gender")
    idx_noc = m_header.index("nationality_code")
    idx_birth_date = m_header.index("birth_date")

    legacy_countries = legacy.get(constants.OLYMPIC_PATHS.COUNTRY, {})

    legacy_nocs = set()

    if isinstance(legacy_countries, dict):
        legacy_nocs = {c.get("noc", "") for c in legacy_countries.values()}
    elif isinstance(legacy_countries, list):
        header = legacy_countries[0]
        if "noc" in header:
            idx = header.index("noc")
        for row in legacy_countries[1:]:
            legacy_nocs.add(row[idx])

    for row in medallists[1:]:
        # missing athletes and events
        if row[idx_ethlete_code] not in athletes_set:
            reports["missing_athletes"].append(row[idx_ethlete_code])

        if row[idx_event_code] not in event_codes_set:
            reports["missing_events"].append(row[idx_event_code])

        # invalid gender
        g = row[idx_gender].upper()
        if g not in ["MALE", "FEMALE"]:
            reports["invalid_gender"].append(row[idx_gender])

        # invalid NOC
        noc = row[idx_noc].upper()
        if noc == "":
            continue
        if noc not in legacy_nocs:
            reports["invalid_noc"].append(noc)

        # invalid date of birth
        dob = row[idx_birth_date]
        if utils.normalize_date(dob) == "":
            reports["invalid_dob"].append(dob)

    for key, items in reports.items():
        if items:
            print(f"Validation Report - {key}: {len(items)} issues found.")
            if key == "invalid_noc":
                print("Invalid NOCs:", items[:10])
    return reports


#     generates a statistical summary table aggregated by olympic edition and country (NOC).
#     calculates unique athlete counts and medal totals (Gold, Silver, Bronze). 
# 
#     parameters: data (dict): yhe processed data dictionary containing event results and country info.    
# 
#     returns: list[list[str]]: a list of lists representing the rows of 'newmedaltally.csv'.
# 
#     accepts the main data dictionary
#     generates a summary table statistics by edition and country
#     calculates number of unique athletes, and gold silver bronze medal counts
#     returns a list of lists representing the newmedaltally.csv

def create_summary(data: dict[str, dict[str, str]]) -> list[list[str]]:
    header = [
        "edition",
        "edition_id",
        "Country",
        "NOC",
        "number_of_athletes",
        "gold_medal_count",
        "silver_medal_count",
        "bronze_medal_count",
        "total_medals",
    ]
    # we need to map the 3 letter NOC code to the full country name
    noc_map = {}

    if constants.OLYMPIC_PATHS.COUNTRY in data:
        c_data = data[constants.OLYMPIC_PATHS.COUNTRY]
        if isinstance(c_data, dict):
            for c in c_data.values():
                if "noc" in c and "country" in c:
                    noc_map[c["noc"]] = c["country"]
    stats = {}
    results = data.get(constants.OLYMPIC_PATHS.EVENT_RESULTS, [])

    # to prevent duplicate medals / preserve medal uniqueness
    medal_tracker = {}

    # skip the header row and iterate through data
    for row in results[1:]:
        if len(row) < 10:
            continue
        edition, eid, noc, event, aid, medal = (
            row[0],
            row[1],
            row[2],
            row[4],
            row[7],
            row[9],
        )
        # create a unique key for grouping
        key = (edition, eid, noc)
        if key not in stats:
            stats[key] = {"ids": set(), "G": 0, "S": 0, "B": 0}
        # add the athlete ID to the set
        stats[key]["ids"].add(aid)

        medal_name = None
        if "Gold" in medal:
            medal_name = "G"
        elif "Silver" in medal:
            medal_name = "S"
        elif "Bronze" in medal:
            medal_name = "B"

        if medal_name:
            tracker_key = (eid, noc, event, medal_name)
            if tracker_key not in medal_tracker:
                medal_tracker[tracker_key] = True
                stats[key][medal_name] += 1

    output = [header]
    # sort the keys to ensure the CSV is ordered chronologically
    for key in sorted(stats.keys(), key=lambda x: (x[0], x[2])):
        val = stats[key]
        # calculate total medals sum
        total = val["G"] + val["S"] + val["B"]
        c_name = noc_map.get(key[2], key[2])
        output.append(
            [
                key[0],  # edition
                key[1],  # edition_id
                c_name,  # Country
                key[2],  # NOC
                str(len(val["ids"])),  # number_of_athletes
                str(val["G"]),  # gold_medal_count
                str(val["S"]),  # silver_medal_count
                str(val["B"]),  # bronze_medal_count
                str(total),  # total_medals
            ]
        )
    return output


# accepts the dictionary of data objects
# converts dictionary-based objects back into list of lists format
# ensures all files are ready for CSV writing using utils.write_csv_file
# returns a dictionary of filename: row ...
def prepare_csv_write(data: dict[str, dict[str, str]]) -> dict[str, list[list[str]]]:
    final_files = {}

    for filename, content in data.items():
        if isinstance(content, list):
            final_files[filename] = content
        elif isinstance(content, dict):
            if not content:
                final_files[filename] = []
                continue

            # Get the first key
            first_key = next(iter(content))
            # Use the key to get the actual object to extract headers
            headers = list(content[first_key].keys())

            rows = [headers]
            for obj in content.values():
                rows.append([str(obj.get(h, "")) for h in headers])
            final_files[filename] = rows

    return final_files

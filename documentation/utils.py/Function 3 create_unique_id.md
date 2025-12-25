## Function Documentation: create_unique_id() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Creates a unique identifier (key) from an object by combining specific column values into a comma-separated lowercase string.

## Purpose ##
This function generates unique keys for dictionary-based data structures. It combines values like name, country, and birthdate to create a unique identifier (e.g., "michael phelps,usa,1985-06-30") that enables fast O(1) lookups and duplicate detection during data merging.

## Parameters ##

data (dict[str, str]): Dictionary containing athlete or entity data
column_names (list[str]): List of column names to use for creating the unique ID
is_paris_names (bool): Optional flag for Paris data special handling (default: False)


## Returns ##

str: Comma-separated lowercase unique identifier string


## Algorithm (Pseudocode) ##
create_unique_id(data, column_names, is_paris_names)
1. out = ""
2. for i, name in enumerate(column_names):
3.     if i != 0:
4.         out += ","
5.     id_part = data[name]
6.     if is_paris_names and name == "name_tv":
7.         if not id_part:
8.             non_tv_name = data["name"].split(" ")
9.             id_part = " ".join([last_name] + [other_names])
10.    out += id_part.lower()
11. return out

## How It Works ##

Initialize output string - Creates empty string for building ID
Loop through column names - Processes each specified column
Add comma separator - Adds comma between parts (not before first part)
Extract value - Gets value from data dictionary using column name
Handle Paris special case - If Paris data and name_tv is empty, reorganize regular name (last name first)
Convert to lowercase - Ensures case-insensitive matching
Append to output - Builds complete ID string
Return ID - Returns final unique identifier


## Variables ##

n = number of columns in column_names list


## Time Complexity Analysis ##
Operation Count
Line 1: String initialization = 1
Lines 2-10: Loop over n columns = n
    Line 3-4: Conditional comma addition = n
    Line 5: Dictionary lookup = n
    Lines 6-9: Paris special case handling (worst case) = n
    Line 10: Lowercase and concatenation = n
Total loop operations = 5n
Line 11: Return = 1
## T(n) Calculation ##
T(n) = 1 + 5n + 1
T(n) = 5n + 2
## Big-O Analysis ##
T(n) = 5n + 2
O(n)
The dominant factor is n (number of columns). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the number of columns used in the unique ID.

## Example Usage ##
python# Olympic athlete data
athlete_data = {
    "athlete_id": "1",
    "name": "Michael Phelps",
    "country_noc": "USA",
    "born": "1985-06-30"
}

column_names = ["name", "country_noc", "born"]

unique_id = create_unique_id(athlete_data, column_names, False)
# Returns: "michael phelps,usa,1985-06-30"

# Paris athlete data with empty name_tv
paris_data = {
    "name": "Jean Pierre Martin",
    "name_tv": "",
    "country_code": "FRA",
    "birth_date": "1990-05-15"
}

column_names = ["name_tv", "country_code", "birth_date"]

unique_id = create_unique_id(paris_data, column_names, True)
# Returns: "martin jean pierre,fra,1990-05-15"
# (name reorganized: last name first)

## Key Features ##

Comma-separated format - Easy to parse and read
Case-insensitive - All lowercase for consistent matching
Paris fallback - Handles empty name_tv by reorganizing regular name
Flexible columns - Can use any combination of columns
Deterministic - Same input always produces same output


## Common Column Combinations ##
For athletes:

["name", "country_noc", "born"] - Standard athlete ID

For countries:

["noc"] - Simple country code ID

For Paris athletes:

["name_tv", "country_code", "birth_date"] - Paris athlete ID with fallback


## END OF DOCUMENTATION ##
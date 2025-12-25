## Function Documentation: create_athlete_edition_id_map() 
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Creates a global mapping that associates each athlete ID with the year of their first Olympic appearance. This map is used by normalize_date() for intelligent date parsing.

## Purpose ##
When parsing 2-digit birth years (e.g., "13-Aug-69"), the function needs context to determine if the year is 1969 or 2069. By knowing when an athlete competed, we can infer their likely birth year. This function builds a lookup table mapping athlete IDs to their competition years, enabling smart date inference.

## Parameters ##

event_data (list[list[str]]): Event results data containing athlete IDs and edition IDs
editions (list[list[str]]): Olympic games data containing edition IDs and years


## Returns ##

None: Modifies global athlete_edition_map dictionary in-place


## Algorithm (Pseudocode) 
create_athlete_edition_id_map(event_data, editions)
1.  global athlete_edition_map
2.  edition_year_idx = 3
3.  edition_id_idx = 1
4.  edition_map = {}
5.  for row in editions[1:]:
6.      edition_map[row[edition_id_idx]] = row[edition_year_idx]
7.  athlete_id_idx = 7
8.  edition_id_idx = 1
9.  for row in event_data[1:]:
10.     if row[athlete_id_idx] not in athlete_edition_map:
11.         athlete_edition_map[row[athlete_id_idx]] = edition_map[row[edition_id_idx]]

## How It Works ##
## Phase 1: Build Edition Map (Lines 2-6) ##

Set column indices - edition_year at index 3, edition_id at index 1
Initialize edition map - Create empty dictionary
Loop through editions - For each Olympic edition (skipping header):

Map edition_id - year (e.g., "52" - "2024")

## Phase 2: Build Athlete-Edition Map (Lines 7-11) ##

Set column indices - athlete_id at index 7, edition_id at index 1
Loop through event results - For each competition result (skipping header):

Check if athlete already in map (only record first appearance)
If not in map, add athlete_id - year mapping using edition_map

## Variables ##

n = number of edition rows + number of event result rows


## Time Complexity Analysis ##
Operation Count
Lines 1-6: Build edition map
Lines 1-3: Assignments = 3
Line 4: Dictionary creation = 1
Lines 5-6: Loop over e editions, create mapping = 2e
Total = 2e + 4
Lines 7-11: Build athlete-edition map
Lines 7-8: Assignments = 2
Lines 9-11: Loop over r results = r
    Line 10: Dictionary lookup (O(1)) = r
    Line 11: Dictionary assignment = r (worst case, all unique athletes)
Total = 3r + 2
## T(n) Calculation ##
Let n = e + r (editions + results):
T(n) = (2e + 4) + (3r + 2)
T(n) = 2e + 3r + 6
Since n = e + r:
T(n) = 3n + 6
## Big-O Analysis ##
T(n) = 3n + 6
O(n)
The dominant factor is n (total records). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of editions and results.

## Example Usage ##
python# Event results data
event_data = [
    ["edition", "edition_id", "country_noc", "sport", "event", "result_id", "athlete", "athlete_id", ...],
    ["1896 Summer Olympics", "1", "USA", "Athletics", "100m", "1", "Carl Lewis", "123", ...],
    ["2000 Summer Olympics", "25", "AUS", "Swimming", "200m Free", "2", "Ian Thorpe", "456", ...],
    ["2024 Summer Olympics", "52", "USA", "Swimming", "100m Free", "3", "Katie Ledecky", "789", ...]
]

# Editions data
editions = [
    ["edition", "edition_id", "year", "start_date", ...],
    ["1896 Summer Olympics", "1", "1896", "06-Apr-1896", ...],
    ["2000 Summer Olympics", "25", "2000", "15-Sep-2000", ...],
    ["2024 Summer Olympics", "52", "2024", "26-Jul-2024", ...]
]

create_athlete_edition_id_map(event_data, editions)

# Result: athlete_edition_map = {
#     "123": "1896",
#     "456": "2000",
#     "789": "2024"
# }

## How It's Used ##
When normalize_date() encounters a 2-digit year like "69" for athlete ID "123":

Looks up athlete_edition_map["123"] - "1896"
Knows athlete competed in 1896
Infers birth year must be 1800s, not 2000s
Converts "69" - "1869" (not "1969" or "2069")


## Key Features ##

First appearance only - Records athlete's earliest Olympic competition
Global state - Uses global variable for access by other functions
Two-stage mapping - First maps editions, then maps athletes
Smart date parsing - Enables context-aware date inference
Prevents duplicates - Only adds athlete if not already in map

 
## Why This Matters ##
Without this function:

"13-Aug-69" could be 1869, 1969, or 2069 - ambiguous

## With this function: ##

If athlete competed in 1896, birth year is likely 1869
If athlete competed in 2024, birth year is likely 1969
Smart inference based on competition context



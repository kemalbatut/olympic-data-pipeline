## Function Documentation: prepare_csv_write() ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Converts dictionary-based data objects back into list of lists format suitable for CSV file writing. Ensures all files are ready to be written using utils.write_csv_file().

## Purpose ##
This function prepares the final data for output by converting dictionary objects (used for fast lookups during processing) back into the list of lists format required by CSV writers. It handles both dictionary-type data (athlete bios, countries) and list-type data (event results) appropriately.

## Parameters ##

data (dict[str, dict[str, str]]): Main data dictionary containing all Olympic data in various formats


## Returns ##

dict[str, list[list[str]]]: Dictionary mapping filenames to CSV-ready data (list of lists with headers)


## Algorithm (Pseudocode) ##
prepare_csv_write(data)
1.  final_files = {}
2.  for filename, content in data.items():
3.      if isinstance(content, list):
4.          final_files[filename] = content
5.      elif isinstance(content, dict):
6.          if not content:
7.              final_files[filename] = []
8.              continue
9.          first_key = next(iter(content))
10.         headers = list(content[first_key].keys())
11.         rows = [headers]
12.         for obj in content.values():
13.             rows.append([str(obj.get(h, "")) for h in headers])
14.         final_files[filename] = rows
15. return final_files

How It Works
## Main Processing (Lines 1-14) ##

Initialize final_files dictionary - Create empty dict for output
Loop through each file - Process all files in data dictionary
Check content type - Determine if content is list or dictionary
If list - Keep as-is (already in correct format)
If dictionary - Convert to list of lists:

Check if empty, return empty list if so
Get first key to extract headers
Extract all header names from first object
Create rows list starting with header row
Loop through all objects and convert to lists
Each object value becomes a row with values in header order


Store in final_files - Map filename to converted data
Return result - Return complete dictionary ready for CSV writing


## Variables ##

n = total number of data objects/rows across all files


## Time Complexity Analysis ## 

## Operation Count ##
Line 1: Initialization
Line 1: Dictionary creation = 1
Lines 2-14: Process files
Line 2: Loop over files = n (processing all data objects)
Lines 3-4: Type check and assignment for lists = n (worst case)
Lines 5-14: Type check and conversion for dicts = n (worst case)
    Line 6-8: Empty check = constant per file
    Lines 9-10: Get first key and headers = constant per file
    Line 11: Create header row = constant per file
    Lines 12-13: Loop through objects and convert = n (one per object)
Line 14: Assignment = constant per file
Line 15: Return
Line 15: Return statement = 1

## T(n) Calculation ## 
T(n) = 1 + n + n + 1
T(n) = 2n + 2 

## Big-O Analysis ##
T(n) = 2n + 2
O(n)
The dominant factor is n (total objects). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of data objects being converted.

## Example Usage ##
python# Input: Dictionary format
data = {
    "olympic_athlete_bio.csv": {
        "michael phelps,usa,1985-06-30": {
            "athlete_id": "1",
            "name": "Michael Phelps",
            "country_noc": "USA",
            "born": "1985-06-30"
        },
        "usain bolt,jam,1986-08-21": {
            "athlete_id": "2",
            "name": "Usain Bolt",
            "country_noc": "JAM",
            "born": "1986-08-21"
        }
    },
    "olympic_athlete_event_results.csv": [
        ["edition", "edition_id", "country_noc", "sport", "event"],
        ["2024 Summer Olympics", "52", "USA", "Swimming", "100m Freestyle"]
    ]
}

result = prepare_csv_write(data)

# Output: List of lists format
result = {
    "olympic_athlete_bio.csv": [
        ["athlete_id", "name", "country_noc", "born"],  # Header
        ["1", "Michael Phelps", "USA", "1985-06-30"],    # Row 1
        ["2", "Usain Bolt", "JAM", "1986-08-21"]         # Row 2
    ],
    "olympic_athlete_event_results.csv": [
        ["edition", "edition_id", "country_noc", "sport", "event"],
        ["2024 Summer Olympics", "52", "USA", "Swimming", "100m Freestyle"]
    ]
}

## Type Handling ##
List Content (Already CSV-ready):

Action: Keep as-is, no conversion needed
Example: Event results already in list format

## Dictionary Content (Needs conversion): 

Action: Extract headers from first object, convert all objects to rows
Example: Athlete bios stored as dictionaries during processing

## Empty Dictionary:

Action: Return empty list []
Prevents: Errors when trying to extract headers from empty data


## Why This Matters ##
During processing, we use dictionaries for:

Fast lookups - O(1) access by unique key
Duplicate detection - Easy to check if athlete exists
Data merging - Simple to combine datasets

For CSV output, we need lists because:

CSV format - Rows and columns structure
Write compatibility - csv.writer expects list of lists
Header preservation - First row must be column names


## END OF DOCUMENTATION ##
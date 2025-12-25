## Function Documentation: find_next_id() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Scans through a dataset to find the maximum ID value and sets a global tracker to the next available ID for that dataset type.

## Purpose ##
This function initializes ID tracking for athletes and event results. It finds the highest existing ID in the dataset and sets the global next_ids dictionary so that new records (from Paris 2024) get unique IDs that don't conflict with existing ones.

## Parameters ##

data (list[list[str]]): CSV data as list of lists (with header row)
key (str): Dataset identifier ("ATHLETE_BIO" or "EVENT_RESULTS")
index (int): Column index where the ID is located

## Returns ##

int: The next available ID (maximum + 1)

## Algorithm (Pseudocode) ##
find_next_id(data, key, index)
1. global next_ids
2. maximum = 0
3. for i in range(1, len(data)):
4.     id = int(data[i][index])
5.     if id > maximum:
6.         maximum = id
7. next_ids[key] = maximum + 1
8. return next_ids[key]

## How It Works ##

Declare global - Access global next_ids dictionary
Initialize maximum - Start with 0 as baseline
Loop through data rows - Skip header (start at index 1)
Extract ID - Get ID value at specified column index
Convert to integer - Parse string to int for comparison
Track maximum - Update maximum if current ID is larger
Set next ID - Store (maximum + 1) in global dictionary
Return next ID - Return the next available ID value

## Variables ##

n = number of rows in the dataset

## Time Complexity Analysis ##
Operation Count
Line 1: Global declaration = 1
Line 2: Assignment = 1
Lines 3-6: Loop over n-1 rows (skipping header) = n-1
    Line 4: Index access and int conversion = n-1
    Line 5-6: Comparison and conditional assignment = n-1
Total loop = 3(n-1)
Line 7: Dictionary assignment = 1
Line 8: Return = 1
## T(n) Calculation ##
T(n) = 1 + 1 + 3(n-1) + 1 + 1
T(n) = 4 + 3n - 3
T(n) = 3n + 1
## Big-O Analysis ##
T(n) = 3n + 1
O(n)
The dominant factor is n (number of rows). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the number of rows in the dataset.

## Example Usage ##
python# Olympic athlete bio data
athlete_data = [
    ["athlete_id", "name", "country_noc", "born"],
    ["1", "Michael Phelps", "USA", "1985-06-30"],
    ["2", "Usain Bolt", "JAM", "1986-08-21"],
    ["135584", "Last Athlete", "FRA", "2000-01-01"]
]

next_id = find_next_id(athlete_data, "ATHLETE_BIO", 0)
Scans column 0 (athlete_id)
Finds maximum: 135584
Sets next_ids["ATHLETE_BIO"] = 135585
Returns: 135585

# Event results data
results_data = [
    ["edition", "edition_id", "country_noc", "sport", "event", "result_id", "athlete"],
    ["1896 Summer", "1", "USA", "Athletics", "100m", "1", "Carl Lewis"],
    ["2020 Summer", "51", "JAM", "Athletics", "200m", "271116", "Usain Bolt"]
]

next_id = find_next_id(results_data, "EVENT_RESULTS", 5)
Scans column 5 (result_id)
Finds maximum: 271116
Sets next_ids["EVENT_RESULTS"] = 271117
Returns: 271117

Global State After Execution
python# After both calls above:
next_ids = {
    "ATHLETE_BIO": 135585,
    "EVENT_RESULTS": 271117
}

## Key Features ##

Global state management - Stores ID trackers globally for access by other functions
Prevents ID conflicts - Ensures new records get unique IDs
Flexible column index - Works with any column position
Simple linear scan - No need for sorting or complex logic
Initialization function - Called once at pipeline startup


## Usage in Pipeline ##
Called twice in main():
python# Find next athlete ID
utils.find_next_id(
    data=olympic_raw_data[constants.OLYMPIC_PATHS.ATHLETE_BIO],
    key="ATHLETE_BIO",
    index=0
)

# Find next result ID
utils.find_next_id(
    data=olympic_raw_data[constants.OLYMPIC_PATHS.EVENT_RESULTS],
    key="EVENT_RESULTS",
    index=5
)
After these calls, get_next_id() can be used to retrieve and increment IDs.

## Why This Matters ##
Without this function:

Paris 2024 athlete with ID "1" would conflict with existing athlete ID "1"
Data corruption and duplicate IDs

## With this function:

Paris 2024 athletes get IDs starting at 135585 (after existing 135584)
No conflicts, clean merge


## END OF DOCUMENTATION ##
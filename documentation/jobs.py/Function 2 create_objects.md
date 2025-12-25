## Function Documentation: create_objects() ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Converts raw CSV data (list of lists) into dictionary objects with unique keys. Each row becomes a dictionary where column headers are keys and row values are values.

## Purpose ##
This function transforms flat CSV data into structured Python objects. It creates unique identifiers for each record (based on name, country, birthdate) which enables fast lookups and duplicate detection during the merge phase. Files that don't need conversion (like event results) are kept in their original list format.

## Parameters ##

data (dict[str, list[list[str]]]): Dictionary mapping filenames to CSV contents (list of lists)
unique_id_columns (dict[str, list[str]]): Dictionary specifying which columns to use for creating unique IDs for each file


## Returns ##

dict[str, dict[str, str] | list[list[str]]]: Dictionary where:

Files requiring conversion: {filename: {unique_id: {header: value, ...}}}
Files not requiring conversion: {filename: [[row1], [row2], ...]}




## Algorithm (Pseudocode) ##
create_objects(data, unique_id_columns)
1.  ret = {}
2.  for filename in data:
3.      if filename in unique_id_columns:
4.          csv = data[filename]
5.          headers = [normalize(h) for h in csv[0]]
6.          filedata = {}
7.          for row in csv[1:]:
8.              row_object = {}
9.              for i in range(len(row)):
10.                 value = row[i].strip()
11.                 if headers[i] == "name":
12.                     value = utils.normalize_name(value)
13.                 row_object[headers[i]] = value
14.             unique_key = utils.create_unique_id(row_object, unique_id_columns[filename])
15.             filedata[unique_key] = row_object
16.         ret[filename] = filedata
17.     else:
18.         ret[filename] = data[filename]
19. return ret

## How It Works ##

Initialize return dictionary - Creates empty dictionary to store converted data
Loop through each file - Iterates over all files in the data dictionary
Check if conversion needed - If filename is in unique_id_columns, convert it
Extract and normalize headers - Gets first row, strips whitespace, converts to lowercase
Process each row - For each data row (skipping header):

Create a dictionary object for the row
Map each value to its corresponding header
Normalize athlete names using the character map
Create a unique key (e.g., "michael phelps,usa,1985-06-30")
Store the row object with its unique key


Keep unchanged files - Files not in unique_id_columns stay as lists
Return result - Returns dictionary with converted and unconverted files


## Variables ##

n = total number of data cells across all files (rows × columns × files)


## Time Complexity Analysis ## 

## Operation Count ##
Lines 1-2: Initialization
Line 1: Dictionary creation = 1
Line 2: Outer loop setup = 1
Lines 3-16: Processing (nested loops over all cells)
Line 3: Condition checks = varies per file
Line 4-6: Assignments and setup = varies per file
Lines 7-15: Nested loops processing all n cells
    - Each cell is visited once
    - Each cell gets stripped, checked, and assigned
    - Total operations proportional to n
Line 16: Final assignment per file
Lines 17-18: Direct assignment for unchanged files
Simple assignment = constant time per file
Line 19: Return
Return statement = 1

## T(n) Calculation ##
Since we process each data cell once (strip, check, assign):
T(n) = 1 + 1 + n + n + n + 1
T(n) = 3n + 3

## Big-O Analysis ##
T(n) = 3n + 3
O(n)

The dominant factor is n (total cells). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of data cells being processed.

## Example Usage ## 
python# Input data structure
data = {
    "olympic_athlete_bio.csv": [
        ["athlete_id", "name", "country_noc", "born"],
        ["1", "Michael Phelps", "USA", "1985-06-30"],
        ["2", "Usain Bolt", "JAM", "1986-08-21"]
    ]
}

unique_id_columns = {
    "olympic_athlete_bio.csv": ["name", "country_noc", "born"]
}

result = create_objects(data, unique_id_columns)

# Output structure:
# {
#     "olympic_athlete_bio.csv": {
#         "michael phelps,usa,1985-06-30": {
#             "athlete_id": "1",
#             "name": "Michael Phelps",
#             "country_noc": "USA",
#             "born": "1985-06-30"
#         },
#         "usain bolt,jam,1986-08-21": {
#             "athlete_id": "2",
#             "name": "Usain Bolt",
#             "country_noc": "JAM",
#             "born": "1986-08-21"
#         }
#     }
# }

## Why Unique Keys Matter ## 
The unique key format (e.g., "michael phelps,usa,1985-06-30") allows us to:

Detect duplicates - Same athlete in multiple datasets
Fast lookups - O(1) dictionary access instead of O(n) list search
Merge datasets - Easy to check if Paris athlete already exists in Olympic data


## END OF DOCUMENTATION ## 
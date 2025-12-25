## Function Documentation: refine_paris_data() ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Applies comprehensive normalization and data quality fixes to Paris 2024 datasets, including name normalization, gender standardization, NOC code formatting, and handling zero values in measurements.

## Purpose ##
This function prepares Paris 2024 data for integration with historical Olympic data. It normalizes column values to match the expected format of legacy data, ensuring consistency across datasets. This includes converting gender values to M/F, normalizing special characters in names, converting dates to ISO format, and handling missing or zero measurements.

## Parameters ##

paris (dict): Dictionary containing Paris 2024 CSV data (athletes, events, medallists, NOCs, teams)


## Returns ##

dict: Refined Paris data dictionary with normalized values


## Algorithm (Pseudocode) ##
refine_paris_data(paris)
1.  def is_zero(value):
2.      if value is None: return ""
3.      return "" if value in ["0", "0.0", "0.00"] else value
4.  refined = {}
5.  for filename, rows in paris.items():
6.      header = rows[0]
7.      refined_rows = [header]
8.      [find 9 column indices: name, name_tv, gender, country_code, height, weight, event, birthdate, noc]
9.      for row in rows[1:]:
10.         row = row.copy()
11.         if idx_name_tv != -1 and idx_name != -1:
12.             chosen = row[idx_name_tv] or row[idx_name]
13.             row[idx_name_tv] = utils.normalize_name(chosen).strip()
14.         if idx_gender != -1:
15.             g = row[idx_gender].lower()
16.             if g.startswith("m"): row[idx_gender] = "M"
17.             elif g.startswith("f"): row[idx_gender] = "F"
18.             else: row[idx_gender] = ""
19.         if idx_country_code != -1:
20.             row[idx_country_code] = row[idx_country_code].upper()
21.         if idx_noc != -1:
22.             row[idx_noc] = row[idx_noc].upper()
23.         if idx_height != -1:
24.             row[idx_height] = is_zero(row[idx_height])
25.         if idx_weight != -1:
26.             row[idx_weight] = is_zero(row[idx_weight])
27.         if idx_birthdate != -1:
28.             row[idx_birthdate] = utils.normalize_date(row[idx_birthdate])
29.         refined_rows.append(row)
30.     refined[filename] = refined_rows
31. return refined

 ## How It Works ##
Helper Function (Lines 1-3)

is_zero() - Converts zero values ("0", "0.0", "0.00") to empty strings

## Main Processing (Lines 4-31) ##

Initialize refined dictionary - Create empty dict for cleaned data
Loop through each file - Process all Paris CSV files
Extract header - Get column names from first row
Find column indices - Locate positions of 9 relevant columns
Loop through data rows - For each row (skipping header):

Copy row - Create copy to avoid modifying original
Normalize name - Remove special characters, use name_tv or fallback to name
Standardize gender - Convert "Male"/"Female"/"M"/"F" to "M" or "F"
Uppercase NOC codes - Convert country_code and nationality_code to uppercase
Handle zero measurements - Replace "0", "0.0", "0.00" with empty string for height/weight
Normalize birthdate - Convert to ISO format (YYYY-MM-DD)


Store refined rows - Add cleaned rows to refined dictionary
Return result - Return complete refined Paris dataset


## Variables ##

n = total number of rows across all Paris CSV files


## Time Complexity Analysis ## 

## Operation Count
Lines 1-4: Helper function and initialization
Lines 1-4: Function definition and dict creation = 2
Lines 5-7: Outer loop setup
Line 5: Loop over f files = f
Lines 6-7: Header operations = 2f
Lines 8: Find column indices
Line 8: 9 index operations per file = 9f
Lines 9-29: Process rows
Line 9: Loop over r rows per file = f*r
Line 10: Copy row = f*r
Lines 11-13: Name normalization check and operation = 3f*r
Lines 14-18: Gender normalization (5 operations) = 5f*r
Lines 19-22: NOC uppercase (4 operations) = 4f*r
Lines 23-26: Height/weight zero handling (4 operations) = 4f*r
Lines 27-28: Birthdate normalization = 2f*r
Line 29: Append row = f*r
Total for row processing = 19f*r
Line 30-31: Final operations
Line 30: Assignment per file = f
Line 31: Return = 1 

## T(n) Calculation ## 
Let n = f*r (total rows across all files):
T(n) = 2 + f + 2f + 9f + 19f*r + f + 1
T(n) = 2 + 13f + 19f*r + 1
T(n) = 19f*r + 13f + 3
Since n = f*r:
T(n) = 19n + 13f + 3
Assuming f is small compared to n:
T(n) = 19n + 3 

## Big-O Analysis ##
T(n) = 19n + 3
O(n)
The dominant factor is n (total rows). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of rows in Paris datasets.

## Example Usage
python# Before refinement:
paris_row = [
    "jean-pierre martin",        # name with special chars
    "Jean-Pierre MARTIN",        # name_tv
    "Male",                      # gender (full word)
    "fra",                       # country_code (lowercase)
    "0.0",                       # height (zero value)
    "75",                        # weight
    "100m Freestyle",            # event
    "15/08/1995",                # birthdate (DD/MM/YYYY)
    "fra"                        # nationality_code (lowercase)
]

refined = refine_paris_data(paris_data)

# After refinement:
refined_row = [
    "jean-pierre martin",        # name unchanged
    "Jean-Pierre Martin",        # normalized (special chars removed)
    "M",                         # gender (standardized)
    "FRA",                       # country_code (uppercase)
    "",                          # height (zero removed)
    "75",                        # weight unchanged
    "100m Freestyle",            # event unchanged
    "1995-08-15",                # birthdate (ISO format)
    "FRA"                        # nationality_code (uppercase)
]

What Gets Normalized
Name Fields:

name_tv - Special characters removed (e-e, n-n, etc.)
Fallback to name if name_tv is empty

## Gender:

"Male", "male", "M", "m" - "M"
"Female", "female", "F", "f" - "F"
Anything else - "" (empty)

 ## Country Codes:

country_code - Converted to uppercase (e.g., "usa" - "USA")
nationality_code - Converted to uppercase (e.g., "fra" - "FRA")

## Measurements:

height - Zero values ("0", "0.0", "0.00") - ""
weight - Zero values ("0", "0.0", "0.00") - ""

## Dates:

birthdate - Converted to ISO format YYYY-MM-DD


## END OF DOCUMENTATION ##
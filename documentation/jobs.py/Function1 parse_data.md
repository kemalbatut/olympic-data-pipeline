
### Function Documentation: parse_data()
File: jobs.py
Author: Yigit Dalkilic

## Overview ## 
Reads multiple CSV files and returns them as a dictionary where each filename maps to its file contents as a list of lists.

## Purpose ## 
This function handles the initial data loading stage of the pipeline. It takes a list of CSV filenames, reads each file using the utility function read_csv_file(), and organizes them into a dictionary structure for easy access. This is the first step in processing both Olympic historical data and Paris 2024 data.

## Parameters ## 

filenames (list[str]): List of CSV file paths to read

Example: ["olympic_athlete_bio.csv", "olympic_athlete_event_results.csv", ...]

## Returns ## 

dict[str, list[list[str]]]: Dictionary mapping filenames to their CSV contents

Key: filename (string)
Value: list of lists where first list is headers, remaining lists are data rows



## Algorithm (Pseudocode) ## 
parse_data(filenames)
1. data = {}
2. for name in filenames:
3.     data[name] = utils.read_csv_file(name)
4. return data

How It Works

Initialize empty dictionary - Creates an empty dictionary to store all file data
Loop through filenames - Iterates over each filename in the input list
Read each file - Calls utils.read_csv_file() to read the CSV file into a list of lists
Store in dictionary - Maps the filename to its contents in the dictionary
Return result - Returns the complete dictionary with all files loaded

## Variables ##

n = number of files in the filenames list

## Time Complexity Analysis ##
## Operation Count ##
LineCodeOperationsCount1data = {}Dictionary creation12for name in filenames:Loop iterationsn3data[name] = utils.read_csv_file(name)Function call + assignment2n4return dataReturn statement1
T(n) Calculation
T(n) = 1 + n + 2n + 1
T(n) = 3n + 2
Big-O Analysis
T(n) = 3n + 2
O(n)
## The dominant factor is n (number of files). Constants (3 and 2) are ignored in Big-O notation.
## The function has linear time complexity relative to the number of files being processed.

## Example Usage ## 
python# Load Olympic historical files
olympic_files = [
    "olympic_athlete_bio.csv",
    "olympic_athlete_event_results.csv",
    "olympics_country.csv",
    "olympics_games.csv"
]

olympic_data = parse_data(olympic_files)

# Result structure:
# {
#     "olympic_athlete_bio.csv": [
#         ["athlete_id", "name", "country_noc", "born", ...],  # header
#         ["1", "Giuseppe Abbagnale", "ITA", "1959-03-24", ...],  # row 1
#         ["2", "Michael Phelps", "USA", "1985-06-30", ...],  # row 2
#         ...
#     ],
#     "olympic_athlete_event_results.csv": [...],
#     ...
# }

## What Gets Loaded ## 
For Olympic data (4 files):

olympic_athlete_bio.csv - ~135,000 athletes
olympic_athlete_event_results.csv - ~271,000 results
olympics_country.csv - ~200 countries
olympics_games.csv - ~50 Olympic editions

For Paris 2024 data (5 files):

paris/athletes.csv - ~11,000 athletes
paris/events.csv - ~300+ events
paris/medallists.csv - ~2,000+ medal records
paris/nocs.csv - ~200 NOC entries
paris/teams.csv - ~800+ team entries
 

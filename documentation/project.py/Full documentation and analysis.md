## UPDATED FUNCTION: main() in project.py
File: project.py
Author: Yigit Dalkilic

## Overview ##
This is the entry point of our Olympic data processing pipeline. It loads CSV files, merges historical Olympic data with Paris 2024 data, cleans everything, and outputs 5 standardized CSV files.

## Purpose ##
The main() function is called by runproject.py to execute the entire project. The autograder requires this exact function name and signature. It coordinates all data processing steps in sequence: loading, refining, merging, cleaning, and outputting data.

## What It Does 3#

Load data - Reads 9 CSV files (4 Olympic + 5 Paris)
Refine Paris data - Normalizes Paris data to match Olympic format
Track IDs - Finds highest existing athlete and result IDs
Create athlete-edition map - Maps athletes to their competition years for smart date parsing
Create Olympic objects - Converts lists to dictionaries with unique keys
Validate Paris data - Checks consistency of Paris datasets
Create Paris objects - Converts Paris lists to dictionaries
Merge - Combines Paris 2024 with historical Olympics
Format game dates - Normalizes Olympic edition dates
Clean - Fixes null values, dates, and inconsistencies
Enrich - Adds calculated fields like athlete ages
Summarize - Generates medal tally by country
Output - Writes 5 CSV files to disk


## Algorithm (Pseudocode) ##
main()
1.  olympic_raw_data = jobs.parse_data(OLYMPIC_PATHS)
2.  paris_raw_data = jobs.parse_data(PARIS_PATHS)
3.  paris_raw_data = jobs.refine_paris_data(paris_raw_data)
4.  utils.find_next_id(olympic_raw_data, "ATHLETE_BIO", 0)
5.  utils.find_next_id(olympic_raw_data, "EVENT_RESULTS", 5)
6.  utils.create_athlete_edition_id_map(olympic_raw_data[EVENT_RESULTS], olympic_raw_data[GAMES])
7.  olympic_unique_columns = {...}
8.  olympic_data = jobs.create_objects(olympic_raw_data, olympic_unique_columns)
9.  jobs.validate_paris_consistency(paris_raw_data, olympic_data)
10. paris_unique_columns = {...}
11. paris_data = jobs.create_objects(paris_raw_data, paris_unique_columns)
12. jobs.add_paris_objects(olympic_data, paris_data)
13. jobs.format_games_dates(olympic_data[GAMES])
14. jobs.clean_data(olympic_data)
15. jobs.add_additional_info(olympic_data)
16. summary_data = jobs.create_summary(olympic_data)
17. final_data = jobs.prepare_csv_write(olympic_data)
18. utils.write_csv_file("new_medal_tally.csv", summary_data)
19. for filename, rows in final_data.items():
20.     if "paris" not in filename:
21.         new_name = f"new_{filename}"
22.         utils.write_csv_file(new_name, rows)
23. print("Success message")

## Variables ##

n = number of output files in loop (n = 4)


## Time Complexity Analysis ##
Operation Count
Lines 1-18: Sequential operations
Each line executes once
Total = 18 operations
Lines 19-22: Loop operations
Line 19: for loop iteration    = n
Line 20: if condition          = n
Line 21: string formatting     = n
Line 22: function call         = n
Total = 4n operations
Line 23: Print statement
Total = 1 operation
## T(n) Calculation ##
T(n) = 18 + 4n + 1
T(n) = 4n + 19
## Big-O Analysis ##
T(n) = 4n + 19
O(n)
The dominant factor is n (linear term). Constants are ignored in Big-O notation.

## Key Changes from Previous Version##

Athlete-edition mapping added (Line 6) - Creates smart date parsing lookup table
Validation order changed (Line 9) - Now validates Paris data BEFORE creating Paris objects
Game date formatting added (Line 13) - Normalizes Olympic edition dates after merging


## Output Files ##

new_olympic_athlete_bio.csv
new_olympic_athlete_event_results.csv
new_olympics_country.csv
new_olympics_games.csv
new_medal_tally.csv


## END OF DOCUMENTATION ##
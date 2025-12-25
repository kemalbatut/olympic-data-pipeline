## NEW FUNCTION: format_games_dates() in jobs.py ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Normalizes date formats in the Olympic games dataset by converting start and end dates to a standardized format.

## Purpose ##
This function ensures all Olympic edition dates follow a consistent format. It processes the games list and normalizes both start_date and end_date columns using the normalize_date() utility function.

## Parameters ##

games (list[list[str]]): Olympic games data with header row and game records


## Returns ##

None: Modifies the games list in-place


## Algorithm (Pseudocode) ##
format_games_dates(games)
1.  header = games[0]
2.  start_date_idx = header.index("start_date")
3.  end_date_idx = header.index("end_date")
4.  for row in games[1:]:
5.      row[start_date_idx] = utils.normalize_date(row[start_date_idx], None)
6.      row[end_date_idx] = utils.normalize_date(row[end_date_idx], None)

## How It Works ##

Extract header - Gets the first row containing column names
Find date column indices - Locates positions of start_date and end_date columns
Loop through games - For each Olympic edition (skipping header):

Normalize start_date using normalize_date() with None as athlete_id
Normalize end_date using normalize_date() with None as athlete_id


In-place modification - Updates the original games list directly


## Variables ##

n = number of Olympic game editions (rows in games list)


## Time Complexity Analysis ##
Operation Count
Lines 1-3: Setup
Line 1: Assignment = 1
Line 2: Find index = 1
Line 3: Find index = 1
Total = 3
Lines 4-6: Process games
Line 4: Loop over n games = n
Line 5: Normalize start_date = n
Line 6: Normalize end_date = n
Total = 3n
## T(n) Calculation ##
T(n) = 3 + 3n
T(n) = 3n + 3
## Big-O Analysis ##
T(n) = 3n + 3
O(n)
The dominant factor is n (number of games). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the number of Olympic editions.

## Key Changes from Previous Version ##

Now actually implemented (was just pass before)
Performs real validation checks
Provides detailed console output
Called BEFORE creating Paris objects (to catch issues early) 

## END OF DOCUMENTATION ## 
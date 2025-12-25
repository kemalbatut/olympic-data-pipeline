## Function Documentation: add_paris_objects() ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Merges Paris 2024 Olympic data with historical Olympic data. Detects duplicate athletes across datasets, assigns unique IDs to new athletes, and creates event result records for Paris 2024 competitions.

## Purpose ##
This function integrates Paris 2024 data into the existing Olympic dataset. It performs duplicate detection by checking if Paris athletes already exist in historical data (using name permutations to handle variations like hyphenated names). New athletes get assigned unique IDs, and all Paris medal results are added to the event results dataset.

## Parameters ##

olympic_data (dict): Dictionary containing historical Olympic data with athlete bio and event results
paris_data (dict): Dictionary containing Paris 2024 data (athletes, events, medallists)


## Returns ##

list[list[str]]: List of new event result rows created from Paris 2024 data


## Algorithm (Pseudocode) ##
add_paris_objects(olympic_data, paris_data)
1.  new_athletes = {}
2.  paris_athletes = paris_data[PARIS_ATHLETES]
3.  paris_athlete_ids = {}
4.  for key in paris_athletes:
5.      split_key = key.split(",")
6.      split_name = split_key[0].split(" ")
7.      names = utils.get_name_permutations(split_name)
8.      potential_matches = [create match strings]
9.      found = False
10.     for match in potential_matches:
11.         if match in olympic_data[ATHLETE_BIO]:
12.             found = True
13.             paris_athlete_ids[code] = existing athlete info
14.             break
15.     if not found:
16.         athlete_id = utils.get_next_id("ATHLETE_BIO")
17.         athlete_name = capitalize(split_name)
18.         new_athletes[key] = {athlete data}
19.         paris_athlete_ids[code] = new athlete info
20. paris_events = paris_data[PARIS_EVENTS]
21. event_result_ids = {}
22. for row in paris_events:
23.     event_result_ids[row[0]] = utils.get_next_id("EVENT_RESULTS")
24. olympic_paris_game = find "2024 Summer Olympics" in games
25. new_event_results = []
26. paris_medallists = paris_data[PARIS_MEDALLISTS]
27. medallist_header = paris_medallists[0]
28. [set header indices for 7 columns]
29. for row in paris_medallists[1:]:
30.     try:
31.         athlete = paris_athlete_ids[code]["name"]
32.         athlete_id = paris_athlete_ids[code]["id"]
33.     except KeyError:
34.         athlete = "placeholder"
35.         athlete_id = 100000
36.     new_event_results.append([result row data])
37. olympic_data[EVENT_RESULTS].extend(new_event_results)
38. return new_event_results

## How It Works ##
## Phase 1: Process Paris Athletes (Lines 1-19) ##

Loop through Paris athletes - Check each Paris athlete
Generate name variations - Create permutations for hyphenated/multi-part names
Check for duplicates - Search Olympic data for matching athletes
If found - Map Paris code to existing Olympic athlete ID
If not found - Create new athlete with new ID and add to tracking

## Phase 2: Process Paris Events (Lines 20-23) ##

Generate event IDs - Assign unique result IDs to each Paris event

## Phase 3: Create Event Results (Lines 24-36) ##

Find Paris game edition - Locate "2024 Summer Olympics" in games data
Extract header indices - Find column positions in medallists file
Loop through medallists - Create result row for each medal winner
Handle missing athletes - Use placeholder for unmatched athletes
Append to results - Add all Paris results to Olympic event results

## Phase 4: Merge Data (Line 37) ##

Extend Olympic data - Add new event results to main dataset


## Variables ##

n = total number of Paris athletes + events + medallist records


## Time Complexity Analysis ## 

## Operation Count ##
Lines 1-3: Initialization
Lines 1-3: Variable assignments = 3
Lines 4-19: Process Paris athletes
Line 4: Loop over paris_athletes = a (number of athletes)
Lines 5-8: String operations per athlete = 4a
Lines 9-14: Loop over potential matches = a·m (m = avg matches per athlete)
Lines 15-19: Create new athlete if not found = a (worst case)
Total = a + 4a + a·m + a = 6a + a·m
Lines 20-23: Process events
Line 22: Loop over events = e (number of events)
Line 23: Get next ID = e
Total = 2e
Lines 24-27: Setup for medallists
Lines 24-27: Assignments = 4
Lines 28: Header index setup
Line 28: 7 index operations = 7
Lines 29-36: Process medallists
Line 29: Loop over medallists = r (number of medallist rows)
Lines 30-35: Try-except and assignments = 3r
Line 36: Append to list = r
Total = 5r
Line 37-38: Final operations
Line 37: Extend list = 1
Line 38: Return = 1
Total = 2

## T(n) Calculation ##
Let n = a + e + r (total records processed):
T(n) = 3 + (6a + a·m) + 2e + 4 + 7 + 5r + 2
T(n) = 6a + a·m + 2e + 5r + 16
Since a·m dominates (checking matches for each athlete):
T(n) = a·m + 6a + 2e + 5r + 16
If we assume m (matches per athlete) is small and bounded:
T(n) = 6a + 2e + 5r + 16
Since n = a + e + r:
T(n) = 6a + 2e + 5r + 16
T(n) ≈ 6n + 16  (simplifying with coefficients)

## Big-O Analysis ##
T(n) = 6n + 16
O(n)
The dominant factor is n (total records). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of Paris records being processed.

## Example Usage ##
python# Paris athlete exists in Olympic data
Input: Paris athlete "Michael Phelps,USA,1985-06-30"
 Output: Links to existing Olympic athlete ID (no new athlete created)

 Paris athlete is new
 Input: Paris athlete "New Athlete,FRA,2000-01-01"
 Output: Creates new athlete with ID 135585, adds to tracking

 Event results
 Input: Paris medallist wins Gold in 100m Freestyle
 Output: Creates event result row linking athlete ID to Paris 2024 edition

## Key Features ##

Name Permutation Matching - Handles variations like "Jean-Pierre Martin" vs "Jean Pierre Martin"
Duplicate Prevention - Avoids creating duplicate athlete records
ID Management - Maintains sequential athlete and result IDs
Error Handling - Uses placeholder for unmatched athletes (KeyError)


END OF DOCUMENTATION

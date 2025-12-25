## Function Documentation: create_summary() ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Generates a medal tally summary table that aggregates statistics by Olympic edition and country, including unique athlete counts and medal counts (Gold, Silver, Bronze).

## Purpose ##
This function creates the new_medal_tally.csv output file. It processes all event results, groups them by edition and country, counts unique athletes, and tallies medals by type. This provides a high-level summary of Olympic performance for each country across all Olympic games.

## Parameters ##

data (dict[str, dict[str, str]]): Main data dictionary containing event results and country information


## Returns ##

list[list[str]]: List of lists representing the medal tally CSV with header and data rows


## Algorithm (Pseudocode) ##
create_summary(data)
1.  header = ["edition", "edition_id", "Country", "NOC", "number_of_athletes", "gold_medal_count", "silver_medal_count", "bronze_medal_count", "total_medals"]
2.  noc_map = {}
3.  if COUNTRY in data:
4.      c_data = data[COUNTRY]
5.      if isinstance(c_data, dict):
6.          for c in c_data.values():
7.              if "noc" in c and "country" in c:
8.                  noc_map[c["noc"]] = c["country"]
9.  stats = {}
10. results = data.get(EVENT_RESULTS, [])
11. for row in results[1:]:
12.     if len(row) < 10: continue
13.     edition, eid, noc, aid, medal = row[0], row[1], row[2], row[7], row[9]
14.     key = (edition, eid, noc)
15.     if key not in stats:
16.         stats[key] = {"ids": set(), "G": 0, "S": 0, "B": 0}
17.     stats[key]["ids"].add(aid)
18.     if "Gold" in medal: stats[key]["G"] += 1
19.     elif "Silver" in medal: stats[key]["S"] += 1
20.     elif "Bronze" in medal: stats[key]["B"] += 1
21. output = [header]
22. for key in sorted(stats.keys(), key=lambda x: (x[0], x[2])):
23.     val = stats[key]
24.     total = val["G"] + val["S"] + val["B"]
25.     c_name = noc_map.get(key[2], key[2])
26.     output.append([key[0], key[1], c_name, key[2], str(len(val["ids"])), str(val["G"]), str(val["S"]), str(val["B"]), str(total)])
27. return output

## How It Works ##
## Phase 1: Initialize Header and NOC Mapping (Lines 1-8) ##

Create header row - Define 9 column headers for medal tally
Initialize NOC map - Create empty dictionary for NOC - country name lookup
Build NOC mapping - Loop through country data to map 3-letter codes to full names

## Phase 2: Process Event Results (Lines 9-20) ##

Initialize stats dictionary - Create empty dict for aggregating data
Get event results - Extract results from main data dictionary
Loop through results - For each result row (skipping header):

Skip rows with insufficient columns
Extract edition, edition_id, NOC, athlete_id, and medal type
Create unique key: (edition, edition_id, NOC)
Initialize stats entry if new key
Add athlete_id to set (ensures unique count)
Increment appropriate medal counter (Gold/Silver/Bronze)



## Phase 3: Generate Output (Lines 21-27) ##

Initialize output - Start with header row
Sort keys - Sort by edition, then by NOC (alphabetical)
Loop through sorted stats - For each (edition, edition_id, NOC):

Calculate total medals
Look up full country name from NOC
Create output row with all statistics
Append to output list


Return result - Return complete medal tally as list of lists


## Variables ##

n = total number of event result rows + country rows + output rows


## Time Complexity Analysis ## 

## Operation Count ##
Lines 1-2: Initialization
Lines 1-2: Create header list and dict = 2
Lines 3-8: Build NOC mapping
Line 3: Condition check = 1
Lines 4-5: Assignments = 2
Lines 6-8: Loop and operations = n (processing country records)
Lines 9-10: Initialize stats
Lines 9-10: Dict creation and get = 2
Lines 11-20: Process results
Lines 11-20: Loop through result rows and process = n (processing result records)
Lines 21-27: Generate output
Lines 21-27: Sort and create output rows = n (creating output records) 

## T(n) Calculation ##
T(n) = 2 + 1 + 2 + n + 2 + n + n
T(n) = 3n + 7 

## Big-O Analysis ##
T(n) = 3n + 7
O(n)
The dominant factor is n. Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of records processed.

## Example Usage ##
python# Input: Event results
results = [
    ["1896 Summer Olympics", "1", "USA", "Athletics", "100m", "1", "Carl Lewis", "123", "1", "Gold", "False"],
    ["1896 Summer Olympics", "1", "USA", "Athletics", "200m", "2", "Carl Lewis", "123", "1", "Gold", "False"],
    ["1896 Summer Olympics", "1", "USA", "Swimming", "100m Free", "3", "Michael Phelps", "456", "1", "Gold", "False"],
    ["1896 Summer Olympics", "1", "JAM", "Athletics", "100m", "4", "Usain Bolt", "789", "2", "Silver", "False"]
]

# Output: Medal tally
output = [
    ["edition", "edition_id", "Country", "NOC", "number_of_athletes", "gold_medal_count", "silver_medal_count", "bronze_medal_count", "total_medals"],
    ["1896 Summer Olympics", "1", "Jamaica", "JAM", "1", "0", "1", "0", "1"],
    ["1896 Summer Olympics", "1", "United States", "USA", "2", "3", "0", "0", "3"]
]

## Output Format ##
Columns in new_medal_tally.csv:

edition - Olympic edition name (e.g., "2024 Summer Olympics")
edition_id - Numeric edition identifier
Country - Full country name (e.g., "United States")
NOC - 3-letter NOC code (e.g., "USA")
number_of_athletes - Count of unique athletes who won medals
gold_medal_count - Total gold medals
silver_medal_count - Total silver medals
bronze_medal_count - Total bronze medals
total_medals - Sum of all medals


## Key Features ##

Unique athlete counting - Uses set to ensure each athlete counted once per country/edition
Medal type aggregation - Separate counts for Gold, Silver, Bronze
NOC to country mapping - Shows full country names, not just codes
Sorted output - Results ordered by edition and NOC alphabetically


## END OF DOCUMENTATION ##
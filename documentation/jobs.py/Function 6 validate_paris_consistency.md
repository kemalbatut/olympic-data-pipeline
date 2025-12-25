## UPDATED FUNCTION: validate_paris_consistency() ##
File: jobs.py
Author: Yigit Dalkilic

## Overview ##
Validates that Paris 2024 data is internally consistent by checking athlete references, event references, gender values, NOC codes, and birth dates across Paris datasets.

## Purpose ##
This function performs comprehensive data quality checks on Paris datasets before integration with Olympic data. It verifies referential integrity between medallists, athletes, and events, validates data format standards, and ensures NOC codes match legacy Olympic country data. This catches data issues early before they propagate through the pipeline.

## Parameters ##

paris: Paris 2024 data dictionary (raw CSV data with lists of lists)
legacy: Historical Olympic data dictionary (converted to objects)


## Returns ##

dict: Reports dictionary containing lists of validation issues found in each category


## Algorithm (Pseudocode) ##
validate_paris_consistency(paris, legacy)
1.  reports = {missing_athletes: [], missing_events: [], invalid_gender: [], invalid_noc: [], invalid_dob: []}
2.  athletes_rows = paris.get(PARIS_ATHLETES, [])
3.  athletes_header = athletes_rows[0]
4.  medallists = paris.get(PARIS_MEDALLISTS, [])
5.  events = paris.get(PARIS_EVENTS, [])
6.  idx_ath_code = athletes_header.index("code")
7.  athletes_set = set(row[idx_ath_code] for row in athletes_rows[1:])
8.  event_header = events[0]
9.  idx_event_name = event_header.index("event")
10. event_codes_set = set(row[idx_event_name] for row in events[1:])
11. m_header = medallists[0]
12. [Extract 5 column indices: athlete_code, event_code, gender, noc, birth_date]
13. legacy_countries = legacy.get(OLYMPIC_COUNTRY, {})
14. legacy_nocs = set()
15. if isinstance(legacy_countries, dict):
16.     legacy_nocs = {extract noc from each country}
17. elif isinstance(legacy_countries, list):
18.     legacy_nocs = {extract noc from header index}
19. for row in medallists[1:]:
20.     if row[athlete_code] not in athletes_set:
21.         reports["missing_athletes"].append(row[athlete_code])
22.     if row[event_code] not in event_codes_set:
23.         reports["missing_events"].append(row[event_code])
24.     g = row[gender].upper()
25.     if g not in ["M", "F"]:
26.         reports["invalid_gender"].append(row[gender])
27.     noc = row[noc_idx].upper()
28.     if noc == "": continue
29.     if noc not in legacy_nocs:
30.         reports["invalid_noc"].append(noc)
31.     dob = row[birth_date]
32.     if utils.normalize_date(dob) == "":
33.         reports["invalid_dob"].append(dob)
34. for key, items in reports.items():
35.     if items:
36.         print(f"Validation Report - {key}: {len(items)} issues found.")
37.         if key == "invalid_noc":
38.             print("Invalid NOCs:", items[:10])
39. return reports

## How It Works ##
## Phase 1: Setup and Data Extraction (Lines 1-12) ##

Initialize reports dictionary - Create structure with 5 validation categories
Extract Paris datasets - Get athletes, medallists, and events from Paris data
Build athlete set - Create set of all valid athlete codes for fast lookup
Build event set - Create set of all valid event names for fast lookup
Extract medallist indices - Find column positions for validation fields

## Phase 2: Build Legacy NOC Set (Lines 13-18) ##

Get legacy countries - Extract Olympic country data
Handle dict format - If countries are objects, extract NOC codes
Handle list format - If countries are lists, find NOC column and extract
Create NOC set - Build set of all valid Olympic NOC codes

## Phase 3: Validate Medallists (Lines 19-33) ##

Loop through medallists - Check each medal record
Validate athlete reference - Check if athlete code exists in athletes dataset
Validate event reference - Check if event name exists in events dataset
Validate gender - Check if gender is "M" or "F" (case-insensitive)
Validate NOC code - Check if NOC exists in legacy Olympic data (skip empty)
Validate birth date - Check if birth date can be normalized successfully

## Phase 4: Report Results (Lines 34-39) ##

Loop through reports - Check each validation category
Print issues - Show count of issues found in each category
Show NOC details - Display first 10 invalid NOCs for debugging
Return reports - Return complete validation results


## Variables ##

n = total number of Paris medallist records


## Time Complexity Analysis ##
Operation Count
Lines 1-18: Setup and index building
Lines 1-6: Assignments and header extraction = 6
Line 7: Build athletes set (iterate a athletes) = a
Lines 8-10: Build events set (iterate e events) = e
Lines 11-12: Extract medallist indices = 7
Lines 13-18: Build legacy NOC set (iterate c countries) = c
Total setup = 13 + a + e + c
Lines 19-33: Validate medallists
Line 19: Loop over n medallists = n
Lines 20-21: Athlete lookup (O(1) set operation) = n
Lines 22-23: Event lookup (O(1) set operation) = n
Lines 24-26: Gender check = 3n
Lines 27-30: NOC check (O(1) set operation) = 3n
Lines 31-33: Date validation = 2n
Total validation = 10n
Lines 34-39: Print results
Lines 34-39: Loop through report categories (max 5) = constant
Total = 5
## T(n) Calculation ##
T(n) = (13 + a + e + c) + 10n + 5
T(n) = 10n + a + e + c + 18
Since n (medallists) typically dominates:
T(n) = 10n + 18
## Big-O Analysis ##
T(n) = 10n + 18
O(n)
The dominant factor is n (medallist records). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the number of Paris medallist records being validated.

## Validation Categories ##
1. Missing Athletes

Check: Medallist references athlete code that doesn't exist in athletes dataset
Impact: Would cause KeyError during data merge

2. Missing Events

Check: Medallist references event that doesn't exist in events dataset
Impact: Orphaned medal records with invalid event names

3. Invalid Gender

Check: Gender value is not "M" or "F" (case-insensitive)
Impact: Gender standardization would fail

4. Invalid NOC

Check: NOC code doesn't exist in Olympic country data
Impact: Country mapping would fail, medal tally would be incomplete
Special: Skips empty NOC values

5. Invalid Date of Birth

Check: Birth date cannot be normalized (returns empty string)
Impact: Age calculations would fail


## Example Output ##
Validation Report - missing_athletes: 2 issues found.
Validation Report - invalid_noc: 1 issues found.
Invalid NOCs: ['XXX']

Return Value Structure
python{
    "missing_athletes": ["ATHLETE001", "ATHLETE002"],
    "missing_events": [],
    "invalid_gender": [],
    "invalid_noc": ["XXX"],
    "invalid_dob": []
}

## Key Features ##

Early detection - Catches issues before data merge
Comprehensive checks - Validates 5 different data quality aspects
Fast lookups - Uses sets for O(1) membership testing
Flexible format handling - Works with both dict and list country data
Empty NOC handling - Skips empty NOC values instead of flagging as invalid
Detailed reporting - Shows count and samples of invalid data


## END OF DOCUMENTATION ##
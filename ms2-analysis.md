## Please check ms2-documentation for per function detailed analysis. This document only satisfies Analysis and Application Description in project requirements ##

## Milestone 2 Analysis ##
Project: Olympic Data Processing Pipeline
Team: G4 Group 2 - Henry, Joy, Batu, Yigit
Course: DSA456 - Data Structures and Algorithms

## Project Overview ##
This project integrates historical Olympic data (1896-2020) with Paris 2024 Olympic data, performing data cleaning, normalization, duplicate detection, and generating standardized output files. The system processes approximately 437,000+ records across 9 input CSV files and produces 5 clean, merged output files.

## Assumptions and Decisions ##
## 2.1 Data Reconciliation - Paris Olympics with Historical Data
Assumption: Paris Athletes May Already Exist in Historical Data
Many Paris 2024 athletes competed in previous Olympics. We assume that if an athlete with similar name and NOC exists, they are the same person.
Decision: Multi-Stage Duplicate Detection

Normalize names - Remove accents using CHARACTER_MAP dictionary (José → Jose)
Create unique keys - Combine name + NOC in lowercase ("michael phelps,usa")
Optional permutation matching - Generate name variations for hyphenated names

Example: "Jean-Pierre Martin" → ["Jean Pierre", "Jean Martin", "Pierre Martin", etc.]


Check each variation - Match against Olympic database using unique key
If match found - Reuse existing athlete_id
If no match - Assign new sequential athlete_id (starting from 135,585)

## Why this approach? ##

Handles spelling variations and name ordering differences
Prevents duplicate athlete records
Maintains data integrity across datasets
Unique keys without birthdate allow more flexible matching

## 2.2 Handling Missing Data
Decision: Preserve Records, Mark Issues
We do NOT drop records with missing data.
Missing Birth Dates:

Normalize to standard format if possible
Store as empty string if normalization fails
Age calculation returns empty string for these athletes
Records remain in system for other analyses

## Missing Height/Weight:

Paris data with "0", "0.0", "0.00" converted to empty string
Removes false zero values
Units (kg, cm) stripped during cleaning
Records preserved without measurements

## Missing NOC Codes:

Validation logs the issue but retains record
Allows manual review and correction later
Historic NOCs (EUN, ROC, IOA, AIN) kept as valid
New NOCs from Paris added to Olympic country list

## Ambiguous 2-Digit Years:

Use athlete competition history for context
Helper function predict_prefix() decrements century until birth year < competition year
If athlete competed in 1896 and birthdate is "69", infer 1869
Without context, fallback attempts to extract any 4-digit year from string

Rationale: Data might be incomplete but still valuable. Dropping records loses information that could be useful for partial analyses.

## Data Structures Used
3.1 Built-in Python Data Structures
We used Python's built-in data structures without writing custom implementations:
## Lists (list[list[str]])
Usage: Raw CSV data storage
Structure:
pythondata = [
    ["athlete_id", "name", "country_noc", "born"],  # Header
    ["1", "Michael Phelps", "USA", "1985-06-30"],   # Row 1
    ["2", "Usain Bolt", "JAM", "1986-08-21"]        # Row 2
]
Why chosen:

Natural representation of CSV structure
Simple iteration with for loops
Direct mapping to file format

## Operations:

Access: O(1) by index
Iteration: O(n)
Append: O(1) amortized

## Dictionaries (dict)
Usage 1: File Data Storage
pythonolympic_raw_data = {
    "olympic_athlete_bio.csv": [[row1], [row2], ...],
    "olympic_athlete_event_results.csv": [[row1], [row2], ...],
}

Key: Filename (str)
Value: List of lists (CSV data)
Why: Organizes multiple files in one structure

## Usage 2: Object Storage with Unique Keys
pythonolympic_data = {
    "olympic_athlete_bio.csv": {
        "michael phelps,usa": {
            "athlete_id": "1",
            "name": "Michael Phelps",
            "country_noc": "USA",
            "born": "1985-06-30"
        },
        "usain bolt,jam": {...}
    }
}

Outer Key: Filename (str)
Inner Key: Unique identifier "name,noc" (str, lowercase)
Value: Athlete object (dict)

## Why chosen:

O(1) lookup time for duplicate detection
Deterministic keys - same athlete always generates same key
Natural representation of objects with named attributes

## Performance comparison:
Without dictionary (linear search):
python# Checking 11,000 Paris athletes against 135,000 Olympic athletes
Time: O(p × a) = O(11,000 × 135,000) = 1.5 billion operations
With dictionary (hash lookup):
python# Same operation with O(1) lookups
Time: O(p) = O(11,000) operations
Improvement: 135,000× faster
Trade-offs:

## Cost: Extra memory for keys (~50 bytes per athlete × 135,000 = ~6.75 MB)
Benefit: Fast lookups during merge (O(1) vs O(a) linear search)
Worth it: Memory cost negligible compared to time savings

## Sets (set)
Usage 1: Unique Athlete Counting
pythonstats[key]["ids"] = set()
stats[key]["ids"].add(athlete_id)
count = len(stats[key]["ids"])

Why: Automatically handles duplicates, O(1) add and membership test
Use case: Medal tally needs count of unique athletes per country/edition

## Usage 2: Duplicate Tracking in add_paris_objects
pythonadded = set()
added.add(f"{code} {full_event}")
if f"{code} {full_event}" in added:  # O(1) check
    # Skip duplicate

Why: Fast duplicate detection for team events

## Usage 3: Validation Checks
pythonathletes_set = set(row[idx] for row in athletes_rows[1:])
if row[idx] not in athletes_set:  # O(1) check
    reports["missing_athletes"].append(row[idx])

Why: Fast membership testing for validation

## Global Dictionaries
Global Variables:
pythonnext_ids = {
    "ATHLETE_BIO": 135585,
    "EVENT_RESULTS": 271117
}

athlete_edition_map = {
    "123": "1896",  # athlete_id → competition_year
    "456": "2000"
}

Why: State management across function calls
Use: ID tracking and date parsing context
Trade-off: Not thread-safe, but acceptable for single-threaded pipeline

## 3.2 Custom Data Structure: dotdict
Implementation:
pythonclass dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
Usage:
pythonOLYMPIC_PATHS.ATHLETE_BIO  # Instead of OLYMPIC_PATHS["ATHLETE_BIO"]


## Why created: 
- Cleaner syntax for constant access
- IDE autocomplete support
- Reduces string literal typos
- Still functions as normal dictionary



## 4. Data Manipulation Flow

##  4.1 General Data Flow ##

CSV Files (Lists) 
    ↓
Raw Data Dictionary {filename: [[rows]]}
    ↓
NOC Merging (combine Paris countries with Olympic)
    ↓
Object Dictionary {filename: {unique_key: {attributes}}}
    ↓
Merged Data (Paris + Olympic)
    ↓
Cleaned Data (normalized dates, NOCs, units)
    ↓
Enriched Data (ages calculated)
    ↓
Summary Data (medal tally)
    ↓
Output Lists [[rows]]
    ↓
CSV Files
## 4.2 Key Transformation: Lists → Dictionaries
Why transform?
Problem with lists - Finding if Paris athlete exists in Olympic data:
python# O(p × a) complexity
for paris_athlete in paris_athletes:
    for olympic_athlete in olympic_athletes:
        if matches(paris_athlete, olympic_athlete):
            found = True
11,000 × 135,000 = 1.5 billion comparisons
Solution with dictionaries:
python# O(p) complexity
olympic_dict = {create_unique_id(ath): ath for ath in olympic_athletes}

for paris_athlete in paris_athletes:
    key = create_unique_id(paris_athlete)
    if key in olympic_dict:  # O(1) lookup
        found = True
11,000 comparisons
Performance improvement: 1.5 billion → 11,000 operations (135,000× faster)

## Runtime Analysis
## 5.1 Variable Definitions

n = number of records in olympic_athlete_event_results.csv (~271,000)
a = number of records in olympic_athlete_bio.csv (~135,000)
p = number of records in paris/athletes.csv (~11,000)
e = number of records in paris/events.csv (~300)
m = number of records in paris/medallists.csv (~2,000)

## 5.2 Runtime to Clean All Data
Function: clean_data(olympic_data)
Operations:
Part 1: Clean Athlete Biographies
pythonfor ath in olympic_data[ATHLETE_BIO].values():  # Iterate a athletes
    ath["born"] = utils.normalize_date(ath["born"], athlete_id)  # O(1)
    if "kg" in ath["weight"]:
        ath["weight"] = ath["weight"].replace("kg", "")
    if "cm" in ath["height"]:
        ath["height"] = ath["height"].replace("cm", "")
    ath["country_noc"] = ath["country_noc"].upper()
# Total: 6a operations
Part 2: Clean Country Data
pythonfor c in olympic_data[COUNTRY].values():  # ~200 countries
    c["noc"] = c["noc"].upper()
# Total: 200 operations (constant)


## T(clean) Calculation:  

T(clean) = 6a + 200
T(clean) = 6a + O(1)
T(clean) = O(a)


## With actual data:##

T(clean) = 6(135,000) + 200
T(clean) = 810,200 operations
Estimated time: ~1 second
Big-O: O(a) - Linear in number of athletes

## 5.3 Runtime to Add Paris Data into Records
Function: add_paris_objects(olympic_data, paris_data)
Operations:
Part 1: Process Paris Athletes
pythonfor key in paris_athletes:  # p athletes
    Generate name permutations (if enabled) = constant k (~1-16)
    Check Olympic athletes (O(1) dict lookup) = k lookups
    Create new athlete or map existing = 1
Total: p × (k + 1) ≈ p operations
Part 2: Process Paris Events
pythonfor row in paris_events:  # e events
    event_result_ids[row[0]] = get_next_id()
Total: e operations
Part 3: Process Teams
pythonfor row in paris_teams:  # ~800 teams
    Parse athletes in team (~10 per team)
    Create results for each athlete
Total: ~8,000 operations (constant relative to dataset)
Part 4: Process Individual Events
pythonfor athlete in paris_athletes:  # p athletes
    Parse events and sports
    Create results (~3 per athlete average)
Total: 3p operations
Part 5: Extend Olympic Data
pythonolympic_data[EVENT_RESULTS].extend(new_event_results)  # m results
## Total: m operations


T(add_paris) Calculation:

T(add_paris) = p + e + 8000 + 3p + m
T(add_paris) = 4p + e + m + 8000

Since p >> 8000:

T(add_paris) = 4p + e + m


With actual data:

T(add_paris) = 4(11,000) + 300 + 2,000
T(add_paris) = 44,000 + 300 + 2,000
T(add_paris) = 46,300 operations
Estimated time: ~3 seconds
Big-O: O(p + e + m)

## 5.4 Runtime to Generate Medal Results for All Games
Function: create_summary(olympic_data)
Operations:
Part 1: Build NOC Mapping
pythonfor c in olympic_data[COUNTRY].values():  # ~200 countries
    noc_map[c["noc"]] = c["country"]
# Total: 200 operations (constant)
Part 2: Process Event Results
pythonfor row in results[1:]:  # n results
    edition, eid, noc, aid, medal = extract_values(row)
    key = (edition, eid, noc)
    
    if key not in stats:  # O(1)
        stats[key] = {"ids": set(), "G": 0, "S": 0, "B": 0}
    
    stats[key]["ids"].add(aid)  # O(1)
    
    if "Gold" in medal:
        stats[key]["G"] += 1
    # Similar for Silver/Bronze
# Total: 10n operations
Part 3: Sort and Generate Output
pythonfor key in sorted(stats.keys()):  # k unique combinations (~5,000)
    val = stats[key]
    total = val["G"] + val["S"] + val["B"]
    c_name = noc_map.get(key[2], key[2])
    output.append([create row])
# Sorting: O(k log k)
# Processing: O(k)
# Total: k log k + k


**T(summary) Calculation:**

T(summary) = 200 + 10n + k log k + k

## With k ≈ 5,000 and n = 271,000:

T(summary) = 200 + 10(271,000) + 5,000 × log₂(5,000) + 5,000
T(summary) = 200 + 2,710,000 + 61,500 + 5,000
T(summary) = 2,776,700 operations

Since n >> k log k:

T(summary) = O(n + k log k)
T(summary) ≈ O(n)  (dominant term)

## With actual data:

Estimated time: ~0.5 seconds

## Big-O:** O(n) - Linear in number of event results

## 6. Overall Pipeline Runtime Analysis

### 6.1 Complete Pipeline Time Complexity

Phase 1: Parse CSV files                    O(n + a + p + e + m)
Phase 2: Combine NOCs                       O(1)  (~200 countries)
Phase 3: Find next IDs                      O(a + n)
Phase 4: Create athlete-edition map         O(n)
Phase 5: Create objects                     O(a + p)
Phase 6: Validate Paris consistency         O(m)
Phase 7: Add Paris objects                  O(p + e + m)
Phase 8: Format games dates                 O(1)  (~50 games)
Phase 9: Clean data                         O(a)
Phase 10: Add additional info               O(a + n)
Phase 11: Create summary                    O(n)
Phase 12: Prepare CSV write                 O(a + n)
Phase 13: Write CSV files                   O(a + n)


**Total:**

T(total) = O(n + a + p + e + m)


**Simplified:** Since n and a dominate:

T(total) = O(n + a)


**With actual data:**

Total records = n + a + p + e + m
              = 271,000 + 135,000 + 11,000 + 300 + 2,000
              = 419,300 records
Measured runtime: ~13 seconds
Rate: ~32,000 records/second




## 7. Space Complexity Analysis

### 7.1 Memory Usage

**Raw Data Storage:**

olympic_raw_data = O(n + a)
paris_raw_data = O(p + e + m)


**Object Storage:**

olympic_data = O(a + n)  # Dictionaries with objects
paris_data = O(p)


**Temporary Structures:**

athlete_edition_map = O(a)
next_ids = O(1)
stats (for summary) = O(k)  # ~5,000 combinations
added set = O(p × events)  # Duplicate tracking


**Total Space:**

Space = O(n + a + p + e + m)
Actual Memory:

Estimated: ~100-150 MB for complete dataset
Peak during object creation (duplicate storage)


# Performance Summary
8.1 Key Operations Performance
OperationTime ComplexityActual TimeRecords ProcessedClean dataO(a)~1 sec135,000 athletesAdd Paris dataO(p + e + m)~3 sec13,300 recordsGenerate medal tallyO(n)~0.5 sec271,000 resultsFull pipelineO(n + a + p + e + m)~13 sec419,300 total
8.2 Data Structure Choice Justification
Dictionary for Athletes:

Need: Fast duplicate detection
Benefit: O(1) lookups vs O(a) linear search
Cost: ~6.75 MB extra memory for keys
Result: 135,000× speed improvement
Worth it: Absolutely - turns hours into seconds

# Set for Unique Counting:

Need: Count unique athletes without manual deduplication
Benefit: O(1) add/check operations
Cost: Minimal memory overhead
Result: Automatic duplicate handling in medal tally

# Lists for CSV Data:

Need: Simple tabular data representation
Benefit: Natural fit for row/column structure
Cost: None - perfect match for use case
Result: Easy iteration and file I/O


# Conclusion #
The Olympic Data Processing Pipeline demonstrates efficient use of Python's built-in data structures to achieve linear time complexity O(n) for processing 400,000+ records. Key design decisions:

Dictionary-based duplicate detection - O(1) lookups instead of O(a) linear search
Unique keys without birthdate - More flexible matching (name + NOC only)
Set-based unique counting - Automatic deduplication for medal tallies
Context-aware date parsing - Uses competition history for smart inference
Optional name permutations - Configurable matching strategy
NOC merging - Adds missing Paris countries to Olympic list
Comprehensive validation - Catches data quality issues early

## Performance characteristics: ##

Time: O(n + a + p + e + m) ≈ O(n + a)
Space: O(n + a + p + e + m)
Throughput: ~32,000 records/second
Scalability: Linear scaling to millions of records

The system successfully merges historical and modern Olympic data while maintaining data integrity and quality. All design decisions prioritize performance without sacrificing correctness.

## END OF MILESTONE 2 ANALYSIS ##

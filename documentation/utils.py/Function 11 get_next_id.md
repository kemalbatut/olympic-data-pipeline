## Function Documentation: get_next_id() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Retrieves the next available ID for a dataset type and automatically increments the global counter for subsequent calls.

## Purpose ##
This function provides unique IDs for new records (Paris 2024 athletes and events). Each call returns the current next ID and increments the counter, ensuring every new record gets a unique, sequential ID that doesn't conflict with existing data.

## Parameters ##

key (str): Dataset identifier ("ATHLETE_BIO" or "EVENT_RESULTS")

## Returns ##

int: The next available ID for this dataset type


## Algorithm (Pseudocode) ##
get_next_id(key)
1. global next_ids
2. ret = next_ids[key]
3. next_ids[key] += 1
4. return ret

## How It Works ##

Declare global - Access global next_ids dictionary
Get current ID - Retrieve current next ID value
Increment counter - Add 1 to prepare for next call
Return current ID - Return the ID that was just retrieved (before increment)

## Variables ##

n = not applicable (constant operations only)

## Time Complexity Analysis ##
Operation Count
Line 1: Global declaration = 1
Line 2: Dictionary lookup and assignment = 2
Line 3: Dictionary lookup, addition, and assignment = 3
Line 4: Return = 1
## T(n) Calculation ##
T(n) = 1 + 2 + 3 + 1
T(n) = 7
## Big-O Analysis ##
T(n) = 7
O(1)
The function has constant time complexity because it performs a fixed number of operations regardless of input.

## Example Usage ##
python# After find_next_id() has set next_ids["ATHLETE_BIO"] = 135585

First Paris athlete
athlete_id_1 = get_next_id("ATHLETE_BIO")
Returns: 135585
next_ids["ATHLETE_BIO"] is now 135586

Second Paris athlete
athlete_id_2 = get_next_id("ATHLETE_BIO")
Returns: 135586
next_ids["ATHLETE_BIO"] is now 135587

Third Paris athlete
athlete_id_3 = get_next_id("ATHLETE_BIO")
Returns: 135587
next_ids["ATHLETE_BIO"] is now 135588

Meanwhile, for event results (after find_next_id() set it to 271117)
result_id_1 = get_next_id("EVENT_RESULTS")
Returns: 271117
next_ids["EVENT_RESULTS"] is now 271118

result_id_2 = get_next_id("EVENT_RESULTS")
Returns: 271118
next_ids["EVENT_RESULTS"] is now 271119

Global State Changes
python# Initial state (after find_next_id calls):
next_ids = {
    "ATHLETE_BIO": 135585,
    "EVENT_RESULTS": 271117
}

# After 3 athlete ID requests and 2 result ID requests:
next_ids = {
    "ATHLETE_BIO": 135588,
    "EVENT_RESULTS": 271119
}

## Key Features ##

Auto-increment - Automatically updates counter after each call
Thread-unsafe - Not safe for concurrent access (fine for single-threaded pipeline)
Simple interface - Just pass the key, get an ID
Sequential IDs - Guarantees consecutive ID assignment
Global state - Maintains state across function calls


Usage in Pipeline
Used extensively in jobs.py when adding Paris data:
python# In add_paris_objects()

# For new Paris athlete
athlete_id = utils.get_next_id("ATHLETE_BIO")
new_athletes[key] = {
    "athlete_id": athlete_id,
    "name": athlete_name,
    ...
}

# For Paris event
event_result_ids[row[0]] = utils.get_next_id("EVENT_RESULTS")

Relationship with find_next_id()
Two-step process:

find_next_id() - Called once at startup

Scans entire dataset
Finds maximum existing ID
Sets initial value in next_ids


get_next_id() - Called many times during processing

Retrieves current ID
Increments for next call
Returns the ID to use

## Why This Matters ##
Problem without this function:

Manual ID tracking required
Risk of duplicate IDs
Complex code to manage counters

Solution with this function:

Simple one-line ID assignment
Guaranteed uniqueness
Centralized ID management

## Important Notes ##

Must call find_next_id() first - This function assumes next_ids[key] already exists
Not reversible - Once incremented, can't go back (unless manually reset)
Single-threaded only - Not thread-safe for concurrent processing
Global dependency - Relies on global next_ids dictionary


## END OF DOCUMENTATION ##
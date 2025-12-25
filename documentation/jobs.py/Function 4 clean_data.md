## Function Documentation: clean_data() ##
File: jobs.py
Author: Yigit Dalkiic

## Overview ##
Standardizes data formats across the Olympic dataset by normalizing birth dates, removing unit suffixes from measurements, and converting country codes to uppercase.

## Purpose ##
This function ensures data consistency by cleaning and standardizing fields in athlete biographies and country data. It removes inconsistencies like "kg" and "cm" suffixes, converts dates to ISO format (YYYY-MM-DD), and standardizes NOC codes to uppercase for uniformity.

## Parameters ##

data (dict[str, dict[str, str]]): Main data dictionary containing athlete bios and country information


## Returns ##

None: Modifies the data dictionary in-place


## Algorithm (Pseudocode) ##
clean_data(data)
1.  if ATHLETE_BIO in data:
2.      for ath in data[ATHLETE_BIO].values():
3.          ath["born"] = utils.normalize_date(ath.get("born", ""))
4.          if "kg" in str(ath.get("weight", "")):
5.              ath["weight"] = ath["weight"].replace("kg", "").strip()
6.          if "cm" in str(ath.get("height", "")):
7.              ath["height"] = ath["height"].replace("cm", "").strip()
8.          if "country_noc" in ath:
9.              ath["country_noc"] = ath["country_noc"].upper()
10. if COUNTRY in data:
11.     c_file = data[COUNTRY]
12.     if isinstance(c_file, dict):
13.         for c in c_file.values():
14.             if "noc" in c:
15.                 c["noc"] = c["noc"].upper()

## How It Works ##
## Phase 1: Clean Athlete Biographies (Lines 1-9) ##

Check if athlete bio exists - Verify ATHLETE_BIO key is in data
Loop through athletes - For each athlete in the bio dictionary:

Normalize birth date - Convert to YYYY-MM-DD format using utils function
Remove weight units - If "kg" appears in weight, remove it and trim spaces
Remove height units - If "cm" appears in height, remove it and trim spaces
Uppercase NOC code - Convert country_noc to uppercase (e.g., "usa" → "USA")



## Phase 2: Clean Country Data (Lines 10-15) ##

Check if country data exists - Verify COUNTRY key is in data
Get country file - Extract country data
Check data type - Ensure it's a dictionary (not a list)
Loop through countries - For each country:

Uppercase NOC code - Convert noc field to uppercase




## Variables ##

n = total number of athlete records + country records


## Time Complexity Analysis ##

## Operation Count ##
Lines 1-9: Clean athlete biographies
Line 1: Condition check = 1
Line 2: Loop over a athletes = a
Line 3: Normalize date function call = a
Lines 4-5: Check and replace weight = 2a
Lines 6-7: Check and replace height = 2a
Lines 8-9: Check and uppercase NOC = 2a
Total = 7a + 1
Lines 10-15: Clean country data
Line 10: Condition check = 1
Line 11: Assignment = 1
Line 12: Type check = 1
Line 13: Loop over c countries = c
Lines 14-15: Check and uppercase NOC = 2c
Total = 2c + 3

## T(n) Calculation ##
Let n = a + c (athletes + countries):
T(n) = (7a + 1) + (2c + 3)
T(n) = 7a + 2c + 4
Since n = a + c:
T(n) = 7a + 2c + 4
T(n) ≈ 7n + 4  (approximating with dominant coefficient)

## Big-O Analysis ##
T(n) = 7n + 4
O(n)
The dominant factor is n (total records). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the total number of athlete and country records.

## Example Usage ##
python# Before cleaning:
athlete = {
    "athlete_id": "1",
    "name": "Michael Phelps",
    "born": "30-06-1985",      # Non-ISO format
    "weight": "91kg",           # Has unit
    "height": "193cm",          # Has unit
    "country_noc": "usa"        # Lowercase
}

clean_data(data)

# After cleaning:
athlete = {
    "athlete_id": "1",
    "name": "Michael Phelps",
    "born": "1985-06-30",       # ISO format YYYY-MM-DD
    "weight": "91",             # Unit removed
    "height": "193",            # Unit removed
    "country_noc": "USA"        # Uppercase
}

## What Gets Cleaned ##
Athlete Bio Fields:

born - Converted to ISO date format (YYYY-MM-DD)
weight - "kg" suffix removed (e.g., "75kg" → "75")
height - "cm" suffix removed (e.g., "180cm" → "180")
country_noc - Converted to uppercase (e.g., "usa" → "USA")

## Country Fields: ##

noc - Converted to uppercase (e.g., "fra" → "FRA")


## Why This Matters ## 

Date consistency - All dates in same format for calculations and sorting
Numeric values - Weight/height can be converted to numbers without parsing units
NOC standardization - Enables accurate country matching and lookups
Data quality - Ensures downstream functions work correctly


## END OF DOCUMENTATION ##
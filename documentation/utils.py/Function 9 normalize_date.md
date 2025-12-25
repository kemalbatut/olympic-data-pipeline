## Function Documentation: check_third_format() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Validates if a date string matches the format "YYYY-MM-MMM" (e.g., "2000-03-Mar"), where year is 4 digits, day is numeric, and month is alphabetic.

## Purpose ##
This helper function checks if a date string follows the Paris 2024 dataset format where year comes first, followed by numeric day, then alphabetic month. It's used by normalize_date() to identify this specific Paris date format. Returns True if the string matches this pattern.

## Parameters ##

s (str): Date string to validate

## Returns ##

bool: True if string matches "YYYY-DD-MMM" format, False otherwise


## Algorithm (Pseudocode) ##
check_third_format(s)
1. parts = s.split("-")
2. if len(parts) != 3:
3.     return False
4. year, day, month = parts
5. if not (year.isdigit() and len(year) == 4):
6.     return False
7. if not day.isdigit():
8.     return False
9. if not month.isalpha():
10.    return False
11. return True

## How It Works ##

Split string - Splits on hyphen delimiter into parts
Check part count - Must have exactly 3 parts (year-day-month)
Unpack parts - Assigns to year, day, month variables (note: year first)
Validate year - Must be exactly 4 digits (e.g., "2000")
Validate day - Must be all digits (e.g., "03")
Validate month - Must be all letters (e.g., "Mar")
Return result - True if all checks pass, False otherwise

## Variables ##

n = length of the input string (constant for validation purposes)

## Time Complexity Analysis ##
Operation Count
Line 1: String split = 1
Line 2: Length check = 1
Line 4: Unpacking = 1
Line 5: isdigit() and length check = 2
Line 7: isdigit() check = 1
Line 9: isalpha() check = 1
Line 11: Return = 1
## T(n) Calculation ##
T(n) = 1 + 1 + 1 + 2 + 1 + 1 + 1
T(n) = 8
## Big-O Analysis ##
T(n) = 8
O(1)
The function has constant time complexity because it performs a fixed number of operations regardless of input.

Example Usage
python# Valid format
result1 = check_third_format("2000-03-Mar")
Returns: True

result2 = check_third_format("2024-15-Aug")
Returns: True

result3 = check_third_format("1996-01-Jan")
Returns: True

Invalid formats
result4 = check_third_format("2000/03/Mar")
Returns: False (wrong delimiter)

result5 = check_third_format("2000-03-03")
Returns: False (month is numeric, not alphabetic)

result6 = check_third_format("03-Mar-2000")
Returns: False (wrong order: day first)

result7 = check_third_format("00-03-Mar")
Returns: False (year is 2 digits, not 4)

result8 = check_third_format("2000-Mar-03")
Returns: False (month and day swapped)

## Valid Examples ##

"2024-26-Jul" 
"2000-15-Sep" 
"1996-01-Jan" 
"2025-31-Dec" 

## Invalid Examples ##

"2024/26/Jul"  (slashes instead of hyphens)
"2024-26-07"  (numeric month)
"26-Jul-2024"  (day-month-year order)
"24-26-Jul"  (2-digit year)
"2024-Jul-26"  (month before day)

## Key Features ##

Year-first format - Unusual ordering with year at the beginning
Hyphen-delimited - Uses hyphens, not spaces or slashes
Mixed numeric/alphabetic - Numeric year and day, alphabetic month
Paris dataset format - Specifically designed for Paris 2024 data
Structure validation only - Doesn't check date validity

## Note on Usage ##
This format appears to be specific to the Paris 2024 dataset structure. The comment in the code indicates this: # 2000-03-12 (paris)
However, the example shows "2000-03-12" which would have a numeric month (12), but the validation expects an alphabetic month. This suggests the format might actually be used after some preprocessing or the example comment may not reflect the actual format this function validates.

## Important Observation ##
The variable naming in line 4 suggests: year, day, month = parts
But the comment example shows: 2000-03-12 which would be year-month-day (ISO format with numeric month).
The actual validation expects: YYYY-DD-MMM with alphabetic month.
This discrepancy suggests the function may validate an intermediate or transformed format rather than raw Paris data.

## END OF DOCUMENTATION ##
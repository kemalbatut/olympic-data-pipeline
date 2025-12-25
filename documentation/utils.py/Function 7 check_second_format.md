## Function Documentation: check_second_format() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Validates if a date string matches the format "D MMMM YYYY" (e.g., "6 December 1886"), where day is numeric, month is alphabetic (full name), and year is 4 digits.

## Purpose ##
This helper function checks if a date string follows the written-out format with full month names commonly found in historical Olympic records. It's used by normalize_date() to determine which parsing strategy to apply. Returns True if the string matches the "6 December 1886" pattern.

## Parameters ##

s (str): Date string to validate

## Returns ##

bool: True if string matches "D MMMM YYYY" format, False otherwise

## Algorithm (Pseudocode) ##
check_second_format(s)
1. parts = s.split(" ")
2. if len(parts) != 3:
3.     return False
4. day, month, year = parts
5. if not day.isdigit():
6.     return False
7. if not month.isalpha():
8.     return False
9. if not (year.isdigit() and len(year) == 4):
10.    return False
11. return True

## How It Works ##

Split string - Splits on space delimiter into parts
Check part count - Must have exactly 3 parts (day month year)
Unpack parts - Assigns to day, month, year variables
Validate day - Must be all digits (e.g., "6")
Validate month - Must be all letters (e.g., "December")
Validate year - Must be exactly 4 digits (e.g., "1886")
Return result - True if all checks pass, False otherwise

## Variables ##

n = length of the input string (constant for validation purposes)

## Time Complexity Analysis ##
Operation Count
Line 1: String split = 1
Line 2: Length check = 1
Line 4: Unpacking = 1
Line 5: isdigit() check = 1
Line 7: isalpha() check = 1
Line 9: isdigit() and length check = 2
Line 11: Return = 1
## T(n) Calculation ##
T(n) = 1 + 1 + 1 + 1 + 1 + 2 + 1
T(n) = 8
## Big-O Analysis ##
T(n) = 8
O(1)
The function has constant time complexity because it performs a fixed number of operations regardless of input.

## Example Usage ##
python# Valid format
result1 = check_second_format("6 December 1886")
Returns: True

result2 = check_second_format("1 January 2000")
Returns: True

result3 = check_second_format("25 March 1975")
Returns: True

Invalid formats
result4 = check_second_format("6-December-1886")
Returns: False (wrong delimiter)

result5 = check_second_format("6 12 1886")
Returns: False (month is numeric, not alphabetic)

result6 = check_second_format("December 6 1886")
Returns: False (wrong order: month first)

result7 = check_second_format("6 Dec 1886")
Returns: False (abbreviated month passes this check, but full name expected)

result8 = check_second_format("6 December 86")
Returns: False (year is 2 digits, not 4)

## Valid Examples ##

"1 January 2024" 
"15 August 1996" 
"31 December 1999" 
"6 December 1886" 

## Invalid Examples ##

"6-December-1886"  (hyphens instead of spaces)
"6/December/1886"  (slashes instead of spaces)
"6 12 1886"  (numeric month)
"December 6 1886"  (month-day order, not day-month)
"6 Dec 1886"  (abbreviated month - though this check would pass)
"06 December 1886"  (leading zero makes day 2 digits - would still pass isdigit())

## Key Features ##

Space-delimited - Uses spaces, not hyphens or slashes
Full month expected - Designed for full month names (January, February, etc.)
4-digit year - Requires complete year (1886, not 86)
Simple validation - Only checks structure, not actual date validity
Format pre-filter - Helps normalize_date() choose correct parser

## Note ##
This function validates format structure only. It doesn't check if:

Day is valid for the month (e.g., "31 February 2000" would pass)
Month name is actually a valid month
Year is reasonable for Olympic data

These semantic validations happen in normalize_date() during actual parsing.

## END OF DOCUMENTATION ## 
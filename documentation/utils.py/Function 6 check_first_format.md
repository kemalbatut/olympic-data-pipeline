## Function Documentation: check_first_format() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Validates if a date string matches the format "DD-MMM-YY" (e.g., "13-Aug-69"), where day is numeric, month is alphabetic (3 letters), and year is 2 digits.

## Purpose ##
This helper function checks if a date string follows a specific format commonly found in Olympic datasets. It's used by normalize_date() to determine which parsing strategy to apply. Returns True if the string matches the "13-Aug-69" pattern.

## Parameters ##

s (str): Date string to validate


## Returns ##

bool: True if string matches "DD-MMM-YY" format, False otherwise

Note: Function signature shows -> str but actually returns bool

## Algorithm (Pseudocode) ##
check_first_format(s)
1. parts = s.split("-")
2. if len(parts) != 3:
3.     return False
4. day, month, year = parts
5. if not day.isdigit():
6.     return False
7. if not month.isalpha():
8.     return False
9. if not (year.isdigit() and len(year) == 2):
10.    return False
11. return True

## How It Works ##

Split string - Splits on hyphen delimiter into parts
Check part count - Must have exactly 3 parts (day-month-year)
Unpack parts - Assigns to day, month, year variables
Validate day - Must be all digits (e.g., "13")
Validate month - Must be all letters (e.g., "Aug")
Validate year - Must be exactly 2 digits (e.g., "69")
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
result1 = check_first_format("13-Aug-69")
 Returns: True

result2 = check_first_format("01-Jan-00")
 Returns: True

 Invalid formats
result3 = check_first_format("13/Aug/69")
 Returns: False (wrong delimiter)

result4 = check_first_format("13-08-69")
 Returns: False (month is numeric, not alphabetic)

result5 = check_first_format("13-Aug-1969")
 Returns: False (year is 4 digits, not 2)

result6 = check_first_format("Aug-13-69")
 Returns: False (wrong order: month first)

result7 = check_first_format("13-August-69")
 Returns: False (month too long, not 3 letters)

## Valid Examples ##

"01-Jan-25" 
"13-Aug-69" 
"31-Dec-99" 
"05-Mar-12" 


## Invalid Examples ##

"1-Jan-25"  (day can be 1 or 2 digits, but isdigit() passes)
"13/Aug/69"  (wrong delimiter)
"13-08-69"  (numeric month)
"13-Aug-1969"  (4-digit year)
"2025-01-13"  (ISO format, wrong order)


## Key Features ##

Simple validation - Only checks format structure, not validity
No date validation - Doesn't check if "31-Feb-99" is valid
Used as pre-filter - Helps normalize_date() choose parsing strategy
Fast checking - Constant time operation
Pattern matching - Specifically for "DD-MMM-YY" format


## Note on Return Type ##
The function signature shows -> str but the implementation returns bool. This is likely a typo in the type hint. The function actually returns True or False.

## END OF DOCUMENTATION ##
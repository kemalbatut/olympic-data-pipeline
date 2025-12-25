## Function Documentation: read_csv_file() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Reads a CSV file and returns its contents as a list of lists, where each inner list represents one row from the file.

## Purpose ##
This function handles CSV file input for the Olympic data pipeline. It opens a file, reads all rows using Python's csv module, and returns the data in a structured format. The first row contains column headers, and subsequent rows contain data records.

## Parameters ##

file_name (str): Path to the CSV file to read


## Returns ##

list[list[str]]: A 2D list where the first element is the header row and remaining elements are data rows


## Algorithm (Pseudocode) ##
read_csv_file(file_name)
1. data_set = []
2. open file with UTF-8-sig encoding
3. csv_reader = csv.reader(file)
4. for row in csv_reader:
5.     data_set.append(row)
6. return data_set

## How It Works ##

Initialize empty list - Creates empty list to store all rows
Open file - Opens CSV file with UTF-8-sig encoding (handles BOM)
Create CSV reader - Uses Python's csv.reader for proper CSV parsing
Read all rows - Iterates through each row and appends to data_set
Return data - Returns complete list of lists


## Variables ##

n = number of rows in the CSV file


## Time Complexity Analysis ##
Operation Count
Line 1: List creation = 1
Line 2: File open = 1
Line 3: CSV reader creation = 1
Lines 4-5: Loop over n rows, append each = 2n
Line 6: Return = 1
## T(n) Calculation ##
T(n) = 1 + 1 + 1 + 2n + 1
T(n) = 2n + 4
## Big-O Analysis ##
T(n) = 2n + 4
O(n)
The dominant factor is n (number of rows). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the number of rows in the CSV file.

## Example Usage ##
python# Read Olympic athlete bio file
data = read_csv_file("olympic_athlete_bio.csv")

# Result structure:
 data[0] = ['athlete_id', 'name', 'country_noc', 'born', ...]  # Header
 data[1] = ['1', 'Michael Phelps', 'USA', '1985-06-30', ...]   # Row 1
 data[2] = ['2', 'Usain Bolt', 'JAM', '1986-08-21', ...]       # Row 2
 ...

## Key Features ##

UTF-8-sig encoding - Handles Byte Order Mark (BOM) in UTF-8 files
Special character support - Correctly reads names with accents (e, n, u, etc.)
Automatic CSV parsing - Handles commas, quotes, and escape characters properly
Header preservation - First row always contains column names


## END OF DOCUMENTATION ##
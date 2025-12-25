## Function Documentation: write_csv_file() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Writes a list of lists to a CSV file, where each inner list represents one row. The first row is the header row.

## Purpose ##
This function handles CSV file output for the Olympic data pipeline. It takes structured data (list of lists) and writes it to a CSV file with proper formatting, encoding, and line endings. This is used to generate all final output files.

## Parameters ##

file_name (str): Path where the CSV file will be created or overwritten
data_set (list[list[str]]): 2D list where first element is header, remaining elements are data rows


## Returns ##

None: Writes file to disk, no return value


## Algorithm (Pseudocode) ##
write_csv_file(file_name, data_set)
1. open file with UTF-8-sig encoding and write mode
2. csv_writer = csv.writer(file)
3. for row in data_set:
4.     csv_writer.writerow(row)

## How It Works ##

Open file for writing - Opens (or creates) file with UTF-8-sig encoding
Create CSV writer - Uses Python's csv.writer for proper CSV formatting
Write all rows - Iterates through each row in data_set and writes it
Auto-close file - File automatically closes after with block completes


## Variables ##

n = number of rows in data_set


## Time Complexity Analysis ##
Operation Count
Line 1: File open = 1
Line 2: CSV writer creation = 1
Lines 3-4: Loop over n rows, write each = 2n
## T(n) Calculation ##
T(n) = 1 + 1 + 2n
T(n) = 2n + 2
## Big-O Analysis ##
T(n) = 2n + 2
O(n)
The dominant factor is n (number of rows). Constants are ignored in Big-O notation.
The function has linear time complexity relative to the number of rows being written.

## Example Usage ##
python# Write medal tally summary
summary_data = [
    ["edition", "edition_id", "Country", "NOC", "gold", "silver", "bronze"],
    ["2024 Summer Olympics", "52", "United States", "USA", "40", "44", "42"],
    ["2024 Summer Olympics", "52", "China", "CHN", "40", "27", "24"]
]

write_csv_file("new_medal_tally.csv", summary_data)

# Creates file: new_medal_tally.csv with properly formatted CSV content

## Key Features ##

UTF-8-sig encoding - Writes BOM for Excel compatibility
Newline handling - Uses newline="" to prevent extra blank lines on Windows
Proper CSV formatting - Handles commas, quotes, and special characters automatically
Overwrite mode - Creates new file or overwrites existing file completely
Special character support - Correctly writes names with accents


## Output Files Generated ##
This function is used to write all 5 final output files:

new_olympic_athlete_bio.csv
new_olympic_athlete_event_results.csv
new_olympics_country.csv
new_olympics_games.csv
new_medal_tally.csv


## END OF DOCUMENTATION ##
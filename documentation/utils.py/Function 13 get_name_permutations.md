## Function Documentation: get_name_permutations() ##
File: utils.py
Author: Yigit Dalkilic

## Overview ##
Generates all potential name variations for an athlete by creating permutations of their last name components while keeping the first name constant.

## Purpose ##
This function handles athletes with hyphenated or multiple last names by generating all possible name orderings. It's used during duplicate detection to match Paris athletes against historical Olympic data, accounting for different name representations.

## Parameters ##

name (list[str]): List of name parts where first element is first name, remaining elements are last name parts

## Returns ##

list[str]: List of all possible full name variations as strings

## Algorithm (Pseudocode) ##
get_name_permutations(name)
1. new_name_list = []
2. for word in name[1:]:
3.     if "-" in word:
4.         unhyphenated = word.split("-")
5.         new_name_list += unhyphenated
6.     else:
7.         new_name_list.append(word)
8. if len(new_name_list) > 1:
9.     permutations = permutations_all_lengths(new_name_list)
10.    return [" ".join([name[0]] + permutation) for permutation in permutations]
11. else:
12.    return [" ".join(name)]

## How It Works ##
## Phase 1: Process Last Names (Lines 1-7) ## 

Initialize list - Create empty list for processed last name parts
Loop through last names - Skip first element (first name), process rest
Check for hyphens - If hyphen found, split into parts
Regular names - If no hyphen, add as-is

## Phase 2: Generate Permutations (Lines 8-12) ##

Check if multiple parts - If more than one last name part:

Call permutations_all_lengths() to get all orderings
Prepend first name to each permutation


Single last name - Simply join first and last name

## Variables ##

n = number of last name parts after hyphen processing

## Time Complexity Analysis ##
Operation Count
Lines 1-7: Process hyphenated names
Lines 2-7: Loop over k last name parts, split if needed = 3k
Lines 8-12: Generate permutations
Lines 9-10: Generate and format n! permutations = n!
## T(n) Calculation ##
T(n) = 3k + n!
T(n) = n!
## Big-O Analysis ##
T(n) = n!
O(n!)
The function has factorial time complexity, but typical names have n=2-4, making this practical.

## Example Usage ##
python# Single last name
result = get_name_permutations(["Michael", "Phelps"])
Returns: ["Michael Phelps"]

# Two-part name
result = get_name_permutations(["Maria", "Garcia", "Lopez"])
Returns: ["Maria Garcia", "Maria Lopez", "Maria Garcia Lopez", "Maria Lopez Garcia"]

# Hyphenated name
result = get_name_permutations(["Jean-Pierre", "Martin"])
Splits "Jean-Pierre" → ["Jean", "Pierre"]
Returns: ["Jean-Pierre Jean", "Jean-Pierre Pierre", "Jean-Pierre Jean Pierre", "Jean-Pierre Pierre Jean"]

## Key Features ##

Hyphen handling - Automatically splits hyphenated names
First name preservation - Always keeps first name at the beginning
All orderings - Generates every possible last name arrangement
Flexible matching - Enables duplicate detection
Smart optimization - Returns single result for simple names


## Why This Matters ##
Problem: Same athlete appears with different name formats

"Jean Martin" vs "Jean-Pierre Martin" vs "Jean Pierre Martin"

Solution: Generate all variations and check each one for matches

## Usage in Pipeline ##
Used in add_paris_objects() to find matching athletes:
pythonsplit_name = split_key[0].split(" ")
names = utils.get_name_permutations(split_name)
potential_matches = [name + f",{split_key[1]},{split_key[2]}" for name in names]

for match in potential_matches:
    if match in olympic_data[ATHLETE_BIO]:
        found = True
        break

## END OF DOCUMENTATION ##
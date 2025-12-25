## Documentation: constants.py ##
File: constants.py
Author: Yigit Dalkilic

## Overview ##
Defines file path constants for Olympic and Paris datasets using a custom dictionary class that enables dot notation access.

## Purpose ##
This module centralizes all CSV file paths used throughout the project, making it easy to reference files consistently. It uses a special dotdict class that allows accessing dictionary values using dot notation (e.g., OLYMPIC_PATHS.ATHLETE_BIO instead of OLYMPIC_PATHS["ATHLETE_BIO"]).

## Contents ##
1. Class: dotdict
Purpose: Extends Python's built-in dict to support attribute-style access.
Features:

Get: obj.key instead of obj["key"]
Set: obj.key = value instead of obj["key"] = value
Delete: del obj.key instead of del obj["key"]

## Implementation: ##
pythonclass dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

2. Olympic Dataset Paths
Variable: OLYMPIC_PATHS
Type: dotdict
Contents:
pythonOLYMPIC_PATHS = {
    "ATHLETE_BIO": "olympic_athlete_bio.csv",
    "EVENT_RESULTS": "olympic_athlete_event_results.csv",
    "COUNTRY": "olympics_country.csv",
    "GAMES": "olympics_games.csv"
}
## Access Examples: ##
python# Dot notation (preferred)
athlete_file = OLYMPIC_PATHS.ATHLETE_BIO  # "olympic_athlete_bio.csv"
results_file = OLYMPIC_PATHS.EVENT_RESULTS  # "olympic_athlete_event_results.csv"

# Dictionary notation (also works)
country_file = OLYMPIC_PATHS["COUNTRY"]  # "olympics_country.csv"

3. Paris Dataset Paths
Variable: PARIS_PATHS
Type: dotdict
Contents:
pythonPARIS_PATHS = {
    "ATHLETES": "paris/athletes.csv",
    "EVENTS": "paris/events.csv",
    "MEDALLISTS": "paris/medallists.csv",
    "NOCS": "paris/nocs.csv",
    "TEAMS": "paris/teams.csv"
}
## Access Examples: ##
python# Dot notation (preferred)
paris_athletes = PARIS_PATHS.ATHLETES  # "paris/athletes.csv"
paris_events = PARIS_PATHS.EVENTS  # "paris/events.csv"

# Dictionary notation (also works)
paris_nocs = PARIS_PATHS["NOCS"]  # "paris/nocs.csv"

# Usage Throughout Project
In project.py:
pythonimport constants

# Parse Olympic files
olympic_raw_data = jobs.parse_data(constants.OLYMPIC_PATHS.values())

# Access specific file
athlete_data = olympic_raw_data[constants.OLYMPIC_PATHS.ATHLETE_BIO]
In jobs.py:
pythonimport constants

# Reference file paths
paris_athletes = paris_data[constants.PARIS_PATHS.ATHLETES]
olympic_countries = olympic_data[constants.OLYMPIC_PATHS.COUNTRY]

## File Structure

project-root/
+-- olympic_athlete_bio.csv
+-- olympic_athlete_event_results.csv
+-- olympics_country.csv
+-- olympics_games.csv
+-- paris/
|   +-- athletes.csv
|   +-- events.csv
|   +-- medallists.csv
|   +-- nocs.csv
|   +-- teams.csv
+-- constants.py

## Why Use dotdict? ##
Without dotdict (standard dictionary):
pythonfile_path = OLYMPIC_PATHS["ATHLETE_BIO"]  # Verbose, requires quotes
With dotdict:
pythonfile_path = OLYMPIC_PATHS.ATHLETE_BIO  # Clean, IDE autocomplete friendly
Benefits:

Cleaner syntax - Easier to read and write
IDE support - Better autocomplete in editors
Less typing - No quotes needed
Still a dict - All dictionary methods still work (.values(), .items(), etc.)

## Key Features ##

Centralized paths - All file locations in one place
Easy maintenance - Change path once, updates everywhere
Type safety - Reduces string typos with constant references
Dot notation - More readable code with attribute access
Backward compatible - Can still use dictionary syntax if needed

## Constants Summary ##
ConstantFile CountPurposeOLYMPIC_PATHS4 filesHistorical Olympic data (1896-2020)PARIS_PATHS5 filesParis 2024 Olympic data

## END OF DOCUMENTATION ##
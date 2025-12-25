# ----------------------------------------------
# Feel free to add additional python files to this project and import
# them in this file. However, do not change the name of this file
# Avoid the names ms1check.py and ms2check.py as those file names
# are reserved for the autograder

# To run your project use:
#     python runproject.py

# This will ensure that your project runs the way it will run in the
# the test environment
# ----------------------------------------------

import utils
import jobs
import constants

# ----------------------------------------------------
# MS2 TEAM MEMBERS & RESPONSIBILITIES
#
# Henry  - Parsing legacy/paris athlete & event objects
# Joy    - Refining Paris datasets & consistency validation
# Batu   - Cleaning, merging, and generating medal summaries
# Yiğit  - Documentation (ms2-analysis.md, README.md)
# ----------------------------------------------------


# ----------------------------------------------------
# This main function is the function that the runner will call
# The function prototype cannot be changed
# ----------------------------------------------------
def main():
    #   This is the entrypoint executed by runproject.py.
    #   dont change its name or signature.

    # ----------Henry's Part----------
    olympic_raw_data = jobs.parse_data(constants.OLYMPIC_PATHS.values())
    paris_raw_data = jobs.parse_data(constants.PARIS_PATHS.values())

    jobs.combine_nocs(
        olympic_raw_data[constants.OLYMPIC_PATHS.COUNTRY],
        paris_raw_data[constants.PARIS_PATHS.NOCS],
    )

    # setting the new athlete id and result id global vars to be incremented later
    utils.find_next_id(
        data=olympic_raw_data[constants.OLYMPIC_PATHS.ATHLETE_BIO],
        key="ATHLETE_BIO",
        index=0,
    )
    utils.find_next_id(
        data=olympic_raw_data[constants.OLYMPIC_PATHS.EVENT_RESULTS],
        key="EVENT_RESULTS",
        index=5,
    )

    # sets a global map used in utils
    utils.create_athlete_edition_id_map(
        event_data=olympic_raw_data[constants.OLYMPIC_PATHS.EVENT_RESULTS],
        editions=olympic_raw_data[constants.OLYMPIC_PATHS.GAMES],
    )

    # creating the olympic objects
    olympic_unique_identifier_columns = {
        constants.OLYMPIC_PATHS.ATHLETE_BIO: ["name", "country_noc"],
        constants.OLYMPIC_PATHS.COUNTRY: ["noc"],
        constants.OLYMPIC_PATHS.GAMES: ["edition_id"],
    }
    olympic_data = jobs.create_objects(
        olympic_raw_data, olympic_unique_identifier_columns
    )

    # --------Joy's Part-------------
    # validating paris consistency
    jobs.validate_paris_consistency(paris_raw_data, olympic_data)

    # ----------Henry's Part----------
    # creating the paris objects
    paris_unique_identifier_columns = {
        constants.PARIS_PATHS.ATHLETES: ["name_tv", "country_code"],
        constants.PARIS_PATHS.NOCS: ["code"],
    }
    paris_data = jobs.create_objects(paris_raw_data, paris_unique_identifier_columns)

    # set all of the optional booleans to True for what I believe yields a more accurate dataset (lower score in the checker though)
    jobs.add_paris_objects(olympic_data, paris_data)
    jobs.format_games_dates(olympic_data[constants.OLYMPIC_PATHS.GAMES])

    # ----------Batu's Part----------
    # 1. Clean Data
    jobs.clean_data(olympic_data)
    # 2. Add Additional Info
    jobs.add_additional_info(olympic_data)

    # 3. Generate Summary
    summary_data = jobs.create_summary(olympic_data)
    # 4. Prepare for Output
    final_data = jobs.prepare_csv_write(olympic_data)
    utils.write_csv_file("new_medal_tally.csv", summary_data)

    # Write the Main Olympic Files
    for filename, rows in final_data.items():
        if "paris" not in filename:
            new_name = f"new_{filename}"
            utils.write_csv_file(new_name, rows)

# Olympic Data Pipeline

High-performance Python ETL pipeline that merges and normalizes 120+ years of Olympic history with Paris 2024 datasets to generate cleaned exports and medal/results summaries.

![Final scoring](screenshots/final-project-scoring.jpeg)

## What it does

This project ingests multiple Olympic + Paris 2024 CSV datasets, cleans inconsistent fields, reconciles athlete/event identities, and produces:
- `new_medal_tally.csv` (medal/results summary output)
- `new_*.csv` (cleaned / updated Olympic datasets)

The pipeline is designed to run under strict CI time limits (GitHub Actions) and uses efficient in-memory structures for fast lookups.

## Key features

- **ETL pipeline**: parse → normalize → reconcile → enrich → export
- **Data cleaning**: date normalization, height/weight cleanup, missing/ambiguous values handling
- **Fast lookups** via dictionaries and sets (constant-time access patterns)
- **Deterministic outputs** written to `new_*.csv` + `new_medal_tally.csv`
- **CI-friendly**: timed execution through `runproject.py`

## Project structure

```text
.
├── project.py               # main() entrypoint
├── runproject.py            # runner used by CI; prints EXECUTION_TIME
├── jobs.py                  # core ETL steps (parse/clean/reconcile/summary/export)
├── utils.py                 # helpers (CSV IO, normalization utilities)
├── special_character_map.py # normalization map for special characters
├── paris/                   # Paris 2024 input datasets (CSV files)
├── screenshots/             # images for README / results
├── ms2-analysis.md          # design + complexity analysis
├── prompts.md               # AI/tools usage log
└── .github/workflows/       # CI workflows
```

## Input datasets

This pipeline expects a mix of historical Olympic datasets and Paris 2024 datasets.

**Historical Olympics (CSV)**
- `olympic_athlete_bio.csv` — athlete bio/demographics
- `olympic_athlete_event_results.csv` — athlete-event participation + results
- `olympics_country.csv` — country mapping/reference
- `olympics_games.csv` — games/edition reference

**Paris 2024 (CSV)**
- `paris/` — Paris 2024 source files (athletes / events / medallists / teams depending on the dataset version)

## How to run

### Requirements
- Python 3.10+ recommended

### Run locally
```bash
python runproject.py
```
runproject.py calls main() in project.py and prints runtime like:
```bash
Execution Time: 8.654
```
## Outputs

After running the pipeline, you should see:

- `new_medal_tally.csv`  
  A generated medal/results summary built from the merged historical + Paris 2024 records.

- `new_*.csv`  
  Cleaned and updated CSV exports produced by the pipeline (normalized fields, reconciled records, and merged Paris additions where applicable).

> Tip: If you don’t see outputs, check the console for any “file not found” messages and confirm your input CSV filenames match what the code expects.

## Performance notes

This project was built to run under strict CI constraints and uses efficient in-memory structures (e.g., dictionaries/sets) for fast lookups during reconciliation and summary generation.

For detailed assumptions, data-structure choices, and Big-O analysis, see **`ms2-analysis.md`**.

## My contributions

My primary focus was **cleaning, merging, and medal summary generation**, including:

- Implementing normalization/cleaning rules to handle inconsistent values (missing data, formatting issues, and irregular fields).
- Building merge/reconciliation logic to integrate Paris 2024 records into the historical Olympic dataset.
- Generating the final medal/results summaries (`new_medal_tally.csv`) and ensuring outputs are deterministic.
- Supporting performance improvements to keep runtime within automated test limits.

(Team responsibilities are also documented in `project.py`.)

## Team

Built as a team project with contributions tracked via Git commits:

- Henry - parsing legacy and Paris athlete/event objects
- Batu - cleaning, merging, and generating medal summaries
- Joy - refining Paris datasets and consistency validation
- Yiğit - documentation (analysis/README)

## AI / tools usage

A transparent log of prompts/tools used during development (and how results were applied) is included in **`prompts.md`**.

## Data attribution

If this repository is public, add the dataset source links here (historical Olympics + Paris 2024) and confirm redistribution terms.

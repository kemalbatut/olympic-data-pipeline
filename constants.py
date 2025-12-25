# use to convert dictionary and allow dot operator use
# dot.notation access to dictionary attributes
class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


raw_olympic_paths = {
    "ATHLETE_BIO": "olympic_athlete_bio.csv",
    "EVENT_RESULTS": "olympic_athlete_event_results.csv",
    "COUNTRY": "olympics_country.csv",
    "GAMES": "olympics_games.csv",
}
OLYMPIC_PATHS = dotdict(raw_olympic_paths)

raw_paris_paths = {
    "ATHLETES": "paris/athletes.csv",
    "EVENTS": "paris/events.csv",
    "MEDALLISTS": "paris/medallists.csv",
    "NOCS": "paris/nocs.csv",
    "TEAMS": "paris/teams.csv",
}
PARIS_PATHS = dotdict(raw_paris_paths)

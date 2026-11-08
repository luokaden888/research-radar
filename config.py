"""Settings for the research radar. Edit these freely; the other files read from here."""

# Topics you care about. A paper is kept if any of these phrases appears
# in its title or abstract (case doesn't matter).
KEYWORDS = [
    "protein design",
    "protein structure prediction",
    "protein language model",
    "drug discovery",
    "macrocycle",
    "macrocyclic",
    "antibody design",
    "molecular generation",
    "cheminformatics",
    "foundation model",
]

# bioRxiv posts hundreds of papers a day across every field of biology.
# Only look in these categories (names must be lowercase, matching bioRxiv's).
BIORXIV_CATEGORIES = {
    "bioinformatics",
    "biophysics",
    "biochemistry",
    "synthetic biology",
}

# How many days back to look on bioRxiv. 2 gives some overlap so nothing is missed.
DAYS_BACK = 2

# How many of the newest matching arXiv papers to grab.
MAX_ARXIV = 50

# ================================================================
# src/eda_engine.py
# ================================================================
# CONTEXT:
#   We have processed-data.csv — clean, typed, enriched by Module 05.
#   Now we need to UNDERSTAND what is in it.
#
# THE BUSINESS QUESTION:
#   The Insurance Risk Manager wants to know:
#     - Which policy types have the highest claim amounts?
#     - Do risk scores and claim amounts correlate as expected?
#     - Are there fraud or claims trends over time?
#
# THE ANALOGY:
#   Imagine you just received a report from every insurance department.
#   Before presenting to executives, you need to read it, find the patterns,
#   and summarise the key findings.
#   EDAEngine reads the insurance data report, finds the patterns,
#   and summarises them.
#
# WHY A CLASS AND NOT JUST FUNCTIONS?
#   Because we need to run 4 different types of analysis and keep ALL results.
#   A class stores everything in self.results so any other module can access:
#     engine.results["group_analysis"]  → group stats
#     engine.results["correlation"]     → correlation pairs
#   Functions would run and throw away results. The class remembers.
#
# DESIGN PRINCIPLE: READ-ONLY
#   EDAEngine never modifies the DataFrame. It only reads and summarises.
#   (Same as DataValidator in Module 05 — analysts inspect, they do not edit.)
# ================================================================

# ── IMPORTS ───────────────────────────────────────────────────────
import sys        # sys: for manipulating Python's module search path
import pathlib    # pathlib: cross-platform file paths

# Walk up from this file's directory until we find config.py
# This makes the import work whether the file is run from any directory
_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd    # pandas: the core Python data library
import numpy as np     # numpy: numerical operations used for correlation matrix

# Import our settings from config.py
from config import (
    INDUSTRY,              # which industry schema ("insurance")
    DATA_PATH,             # where processed-data.csv lives
    REPORTS_DIR,           # where to save the report
    TOP_N_GROUPS,          # how many top groups to show (8)
    CORRELATION_THRESHOLD, # minimum r to include (0.3)
    logger                 # shared logger
)


class EDAEngine:
    """
    Runs Exploratory Data Analysis on the processed insurance dataset.

    WHAT IS EDA?
    ─────────────
    EDA (Exploratory Data Analysis) is the process of examining a dataset
    to discover patterns, relationships, and anomalies before building models.
    It was formalised by statistician John Tukey in 1977 and is now standard
    practice at every data-driven company.

    Every data scientist and analyst runs EDA as their FIRST step after
    receiving clean data. It answers the question: "What is in here?"

    WHAT THIS CLASS DOES:
    ──────────────────────
    Five methods, each answering a different business question:
      1. load()           → How many rows/columns? What types?
      2. profile()        → What are the distributions and completeness?
      3. group_analysis() → How do key metrics vary by category?
      4. correlation()    → Which numeric variables move together?
      5. time_trends()    → How do metrics change over time?

    METHOD CHAIN PATTERN:
    ──────────────────────
    engine.load().profile().group_analysis().correlation().time_trends().report()

    Each method returns self so they can be chained like this.
    This is the same pattern we used in Module 05 ETL.

    Attributes
    ──────────
    df         pd.DataFrame  the loaded processed data
    results    dict          all analysis outputs (keyed by analysis name)
    num_cols   list[str]     numeric column names (set by load())
    cat_cols   list[str]     categorical column names (set by load())
    _status    str           lifecycle state
    """

    def __init__(self):
        """
        Initialise the EDA engine.

        We do NOT load data here — that is load()'s job.
        This separation allows:
          - Object creation without any I/O
          - Testing without needing a real CSV file
          - Clear lifecycle: ready → loaded → analysed → reported
        """
        self.df       = None    # will hold the DataFrame after load()
        self.results  = {}      # will hold all analysis outputs
        self.num_cols = []      # numeric columns (identified in load())
        self.cat_cols = []      # categorical columns (identified in load())
        self._status  = "ready"

        logger.info(f"EDAEngine initialised — industry: {INDUSTRY}")

    def load(self) -> "EDAEngine":
        """
        Load processed-data.csv and identify column types.

        WHY DO WE REMOVE METADATA COLUMNS?
        ─────────────────────────────────────
        Module 05 added three columns starting with _:
          _industry, _processed_at, _pipeline_version
        These describe the pipeline run — NOT the business data.
        Including them in groupby or correlation analysis would add noise.
        We exclude them for analysis but keep the full DataFrame for saving.

        WHY select_dtypes?
        ─────────────────
        select_dtypes(include=["number"]) returns a subset of the DataFrame
        containing ONLY numeric columns (int64, float64).
        select_dtypes(include=["object"]) returns only text/categorical columns.
        This is how pandas separates column types automatically.

        Returns self for method chaining.
        """

        # Verify the input file exists before trying to open it
        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"processed-data.csv not found at: {DATA_PATH}\n"
                "Run Module 05 first:\n"
                "  python run.py\n"
                "Then copy processed-data.csv to data/"
            )

        logger.info(f"[EDA] Loading: {DATA_PATH.name}")

        # pd.read_csv() loads a CSV file from disk into a pandas DataFrame
        # low_memory=False reads the entire file before inferring column types
        # (avoids mixed-type columns on large files)
        self.df = pd.read_csv(DATA_PATH, low_memory=False)

        logger.info(f"[EDA] Loaded {len(self.df):,} rows × {self.df.shape[1]} columns")

        # Remove pipeline metadata columns (start with _) from analysis
        # errors="ignore" means: if a column does not exist, just skip it
        analysis_df = self.df.drop(
            columns=[c for c in self.df.columns if c.startswith("_")],
            errors="ignore"
        )

        # Identify column types using pandas type detection
        # These lists are reused by every subsequent analysis method
        self.num_cols = analysis_df.select_dtypes(include=["number"]).columns.tolist()
        self.cat_cols = analysis_df.select_dtypes(include=["object"]).columns.tolist()

        self._status = "loaded"

        logger.info(
            f"[EDA] Column types: "
            f"{len(self.num_cols)} numeric, "
            f"{len(self.cat_cols)} categorical"
        )

        return self

    def profile(self) -> "EDAEngine":
        """
        Compute a complete statistical profile of the dataset.

        WHY PROFILE FIRST?
        ────────────────────
        Before asking "which policy type has the highest claims?" you need to
        know: "Do we have claim data for all policies, or is 30% missing?"
        The profile gives you confidence in — or warnings about — the data
        before you draw any conclusions.

        WHAT pd.DataFrame.describe() DOES:
        ─────────────────────────────────
        For each numeric column, it computes:
          count  → how many non-null values
          mean   → arithmetic average
          std    → standard deviation (how spread out values are)
          min    → smallest value
          25%    → 25th percentile (first quartile)
          50%    → median (middle value)
          75%    → 75th percentile (third quartile)
          max    → largest value
        """

        logger.info("[EDA] Computing dataset profile...")

        profile = {
            "rows":             len(self.df),
            "columns":          len(self.df.columns),
            "numeric_cols":     len(self.num_cols),
            "categorical_cols": len(self.cat_cols),

            "total_nulls":      int(self.df.isna().sum().sum()),

            "null_pct":         round(
                                    self.df.isna().sum().sum() / self.df.size * 100, 2
                                ),

            "memory_mb":        round(
                                    self.df.memory_usage(deep=True).sum() / 1024**2, 2
                                ),

            "duplicates":       int(self.df.duplicated().sum()),
        }

        if self.num_cols:
            desc = self.df[self.num_cols].describe().round(3)
            profile["descriptive_stats"] = desc.to_dict()

        cat_profiles = {}
        for col in self.cat_cols[:8]:
            vc = self.df[col].value_counts()

            cat_profiles[col] = {
                "unique_count": int(self.df[col].nunique()),
                "top_5":        vc.head(5).to_dict(),
                "null_count":   int(self.df[col].isna().sum()),
            }

        profile["categorical_profiles"] = cat_profiles

        self.results["profile"] = profile

        logger.info(
            f"[EDA] Profile complete — "
            f"{profile['rows']:,} rows | "
            f"{profile['null_pct']}% nulls"
        )

        return self
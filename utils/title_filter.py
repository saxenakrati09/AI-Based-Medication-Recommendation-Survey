import pandas as pd
from typing import List, Tuple

def filter_titles_by_phrases(df: pd.DataFrame, phrases: List[str], title_col: str = 'title') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the DataFrame into two: one with rows whose title contains any of the phrases, and one with the rest.
    Returns (kept, removed)
    """
    pattern = '|'.join([rf"\b{phrase}\b" for phrase in phrases])
    mask = df[title_col].str.lower().str.contains(pattern, case=False, na=False, regex=True)
    removed = df[mask].copy()
    kept = df[~mask].copy()
    return kept, removed

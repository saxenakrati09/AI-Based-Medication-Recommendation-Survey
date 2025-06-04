import pandas as pd
import sys
sys.path.append("..")
from utils.title_filter import filter_titles_by_phrases

EXCLUSION_PHRASES = [
    'drug-drug', 'drug-target interaction', 'drug responses', 'drug discovery', 'molecular medicine',
    'drug repositioning', 'adverse drug event', 'drug sensitivity', 'drug repurposing',
    'treatment outcomes', 'medication prediction based on reviews', 'drug function extraction',
    'drug information extraction', 'safety information', 'genetics', 'genomics', 'molecular',
    'drug-disease association', 'drug synergy', 'drug resistance', 'drug efficacy',
    'drug demand and supply', 'pharmaceutical needs', 'drug side effects', 'drug interactions',
    'drug property prediction', 'precision medicine', 'sentiment'
]

def main():
    df = pd.read_csv('../data/all_papers_dedup.csv')
    kept, removed = filter_titles_by_phrases(df, EXCLUSION_PHRASES, title_col='title')
    kept.to_csv('../data/all_papers_filtered.csv', index=False)
    removed.to_csv('../data/all_papers_removed.csv', index=False)
    print(f"Filtered: {len(kept)} kept, {len(removed)} removed. Saved to ../data/") # 926, 306

if __name__ == "__main__":
    main()

import pandas as pd
from typing import List, Dict

def parse_ieee_csv(csv_path: str) -> List[Dict]:
    df = pd.read_csv(csv_path)
    papers = []
    for _, row in df.iterrows():
        papers.append({
            'title': str(row.get('Document Title', '')),
            'authors': str(row.get('Authors', '')),
            'year': str(row.get('Publication Year', '')),
            'source': 'IEEE_Xplore',
            'raw': row.to_dict()
        })
    return papers

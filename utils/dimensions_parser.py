import pandas as pd
from typing import List, Dict

def parse_dimensions_xlsx(xlsx_path: str) -> List[Dict]:
    df = pd.read_excel(xlsx_path)
    papers = []
    for _, row in df.iterrows():
        papers.append({
            'title': str(row.get('Title', '')),
            'authors': str(row.get('Authors', '')),
            'year': str(row.get('Year', '')),
            'source': 'Dimensions',
            'raw': row.to_dict()
        })
    return papers

from typing import List, Dict
import rispy

def parse_nature_ris(ris_path: str) -> List[Dict]:
    with open(ris_path, 'r', encoding='utf-8') as risfile:
        entries = rispy.load(risfile)
    papers = []
    for entry in entries:
        papers.append({
            'title': entry.get('title', ''),
            'authors': ', '.join(entry.get('authors', [])),
            'year': str(entry.get('year', '')),
            'source': 'Nature',
            'raw': entry
        })
    return papers

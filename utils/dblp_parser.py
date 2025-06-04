import bibtexparser
from typing import List, Dict

def parse_dblp_bib(bib_path: str) -> List[Dict]:
    with open(bib_path, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    papers = []
    for entry in bib_database.entries:
        papers.append({
            'title': entry.get('title', '').strip('{}'),
            'authors': entry.get('author', ''),
            'year': entry.get('year', ''),
            'source': 'DBLP',
            'raw': entry
        })
    return papers

import os
import glob
import pandas as pd
import sys
sys.path.append("..")
from utils.acm_parser import parse_acm_bib
from utils.dblp_parser import parse_dblp_bib
from utils.dimensions_parser import parse_dimensions_xlsx
from utils.ieee_parser import parse_ieee_csv
from utils.nature_parser import parse_nature_ris

def collect_all_papers():
    all_papers = []
    # get path to the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    # ACM
    acm_bib = '../Queries/ACM/acm.bib'
    if os.path.exists(acm_bib):
        all_papers.extend(parse_acm_bib(acm_bib))
    # DBLP
    dblp_bibs = glob.glob('../Queries/DBLP/*.bib')
    for bib in dblp_bibs:
        all_papers.extend(parse_dblp_bib(bib))
    # Dimensions
    dim_xlsx = glob.glob('../Queries/Dimensions/*.xlsx')
    for xlsx in dim_xlsx:
        all_papers.extend(parse_dimensions_xlsx(xlsx))
    # IEEE Xplore
    ieee_csv = '../Queries/IEEE_Xplore/IEEE_Xplore_v1.csv'
    if os.path.exists(ieee_csv):
        all_papers.extend(parse_ieee_csv(ieee_csv))
    # Nature
    nature_ris = glob.glob('../Queries/Nature/*.ris')
    for ris in nature_ris:
        all_papers.extend(parse_nature_ris(ris))
    return all_papers

def main():
    papers = collect_all_papers()
    df = pd.DataFrame(papers)
    # Deduplicate by title (case-insensitive)
    print(f"Collected {len(df)} papers before deduplication.") # 2610
    print(df.head())
    df['title_lower'] = df['title'].str.lower().str.strip()
    df = df.drop_duplicates(subset=['title_lower'])
    df = df.drop(columns=['title_lower'])
    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/all_papers_dedup.csv', index=False)
    print(f"Saved deduplicated papers: {len(df)} rows to data/all_papers_dedup.csv") # 1232

if __name__ == "__main__":
    main()

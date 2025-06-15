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
    """
    Collects all papers from different sources and returns them as a list of dictionaries.
    Sources are: ACM, DBLP, Dimensions, IEEE Xplore, and Nature.
    The list of dictionaries is deduplicated by title (case-insensitive).
    """
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
    """
    Main function to collect, deduplicate, and categorize research papers.

    This function performs the following steps:
    1. Collects papers from various sources and creates a DataFrame.
    2. Deduplicates the DataFrame based on paper titles (case-insensitive).
    3. Splits the DataFrame into two separate categories based on the presence
       of 'arxiv' in any column.
    4. Saves the deduplicated papers into CSV files, distinguishing between
       those with and without 'arxiv' references.

    The resulting CSV files are saved in the '../data/' directory.
    """

    papers = collect_all_papers()
    df = pd.DataFrame(papers)
    # Deduplicate by title (case-insensitive)
    print(f"Collected {len(df)} papers before deduplication.") # 2610
    print(df.head())
    df['title_lower'] = df['title'].str.lower().str.strip()
    df = df.drop_duplicates(subset=['title_lower'])
    df = df.drop(columns=['title_lower'])
    os.makedirs('../data', exist_ok=True)
    # Split based on presence of 'arxiv' in any column
    mask_arxiv = df.apply(lambda row: row.astype(str).str.contains('arxiv', case=False, na=False).any(), axis=1)
    df_arxiv = df[mask_arxiv]
    df_no_arxiv = df[~mask_arxiv]
    df_no_arxiv.to_csv('../data/all_papers_dedup.csv', index=False)
    df_arxiv.to_csv('../data/all_papers_dedup_arxiv.csv', index=False)
    print(f"Saved deduplicated papers without arxiv: {len(df_no_arxiv)} rows to data/all_papers_dedup.csv")
    print(f"Saved deduplicated papers with arxiv: {len(df_arxiv)} rows to data/all_papers_dedup_arxiv.csv")

if __name__ == "__main__":
    main()

import pandas as pd
import argparse
from urllib.parse import urlparse

def extract_unique_domains(df, url_column='URL'):
    """
    Extract unique domain names from a DataFrame column containing URLs.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing URLs.
    - url_column (str): Column name that contains the URLs.
    
    Returns:
    - List of unique domain names.
    """
    domains = df[url_column].dropna().apply(lambda url: urlparse(url).netloc)
    unique_domains = domains.str.lower().str.replace(r"^www\.", "", regex=True).unique()
    return list(unique_domains)

    
    
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Retrieve AI-based medication prediction papers for a specific year.')
    parser.add_argument('--year', type=int, required=True, help='Year for which to retrieve papers (e.g., 2020)')
    # Parse the command line arguments
    args = parser.parse_args()
    
    year = args.year

    # Load the CSV file containing the papers
    input_file = f'../data/ai_medication_prediction_papers_{year}.csv'
    print(f"Loading papers from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} papers from {input_file}")
    
    # print unique domain names
    unique_domains = extract_unique_domains(df)
    print(f"Unique domains found: {len(unique_domains)}")
    print(unique_domains)
    # Filter out non-peer-reviewed papers
    
if __name__ == "__main__":
    main()
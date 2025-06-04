
import pandas as pd
from scholarly import scholarly
import time
import os
import argparse
from tqdm import tqdm


def main():
    # Set up argument parser
    """
    Main function to retrieve AI-based medication prediction papers for a specified year.

    This function uses the `scholarly` library to search and retrieve publications matching
    specific search criteria related to medication prediction and AI. It saves the results
    into a CSV file named with the specified year.

    Command-line arguments:
    --year: The year for which to retrieve papers (e.g., 2020).
    --num_results: The number of results to parse (e.g., 10000).

    The function constructs a search query using the provided year, fetches the results,
    and writes them to a CSV file. It handles exceptions and includes a delay to prevent
    rate limiting.
    """

    parser = argparse.ArgumentParser(description='Retrieve AI-based medication prediction papers for a specific year.')
    parser.add_argument('--year', type=int, required=True, help='Year for which to retrieve papers (e.g., 2020)')
    parser.add_argument('--num_results', type=int, required=True, help='Number of results to parse (e.g., 10000)')
    # Parse the command line arguments
    args = parser.parse_args()
    
    year = args.year
    num_results = args.num_results

    # Define the search query with the specified year
    search_query = (
        'filetype:pdf intitle:("medication prediction" OR "drug prediction" OR "medication recommendation" OR '
        '"drug recommendation" OR "medicine recommendation" OR "medicine prediction" OR '
        '"medicine recommender" OR "drug recommender" OR "medication recommender" OR '
        '"prescription prediction" OR "prescription recommendation" OR "prescription recommender") '
        'intext:("artificial intelligence" OR "machine learning" OR "transformers" OR "reinforcement" OR '
        '"graph" OR "classification" OR "recommend" OR "deep learning" OR "network" OR "convolutional" OR '
        '"embeddings") '
        '-intitle:"medication adherence" -intitle:"medication reconciliation" '
        '-intitle:"adverse drug reaction prediction" -intitle:"pharmacy supply management" '
        '-intitle:"drug-drug interaction" -intitle:"drug-target interaction" -intitle:"drug responses" '
        '-intitle:"drug discovery" -intitle:"molecular medicine" -intitle:"drug repositioning" '
        '-intitle:"adverse drug event prediction" -intitle:"drug sensitivity" -intitle:"drug repurposing" '
        '-intitle:"treatment outcomes" -intitle:"medication prediction based on reviews" '
        '-intitle:"drug function extraction" -intitle:"drug information extraction" '
        '-intitle:"predicting safety information of drugs" -intitle:"drug recommendations based on genetics" '
        '-intitle:"drug recommendations based on molecular data" -intitle:"drug-disease association" '
        '-intitle:"drug synergy" -intitle:"drug resistance" -intitle:"drug efficacy" '
        '-intitle:"drug demand prediction" -intitle:"drug supply prediction" '
        '-intitle:"pharmaceutical needs of pharmacists" -intitle:"pharmaceutical needs of hospitals" '
        '-intitle:"drug property prediction" '
        f'after:{year - 1} before:{year + 1}'
    )

    # Initialize the search
    search_results = scholarly.search_pubs(search_query)

    # Create 'data' folder if it doesn't exist
    data_folder = '../data'
    os.makedirs(data_folder, exist_ok=True)
    # Output CSV file with the year in the filename, saved in 'data' folder
    output_file = os.path.join(data_folder, f'ai_medication_prediction_papers_{year}.csv')

    # Check if the file exists to determine if headers should be written
    file_exists = os.path.isfile(output_file)

    for i in tqdm(range(num_results)):
        try:
            # Retrieve the next publication
            publication = next(search_results)
            # Extract relevant information
            title = publication.get('bib', {}).get('title', '')
            authors = publication.get('bib', {}).get('author', '')
            author_id = publication.get('author_id', '')
            pub_year = publication.get('bib', {}).get('pub_year', '')
            abstract = publication.get('bib', {}).get('abstract', '')
            num_citations = publication.get('num_citations', 0)
            url = publication.get('pub_url', '')
            # Create a DataFrame for the current publication
            df = pd.DataFrame([{
                'Title': title,
                'Authors': authors,
                'Author ID': author_id,
                'Year': pub_year,
                'Citations': num_citations,
                'Abstract': abstract,
                'URL': url
            }])
            # Append the DataFrame to the CSV file
            df.to_csv(output_file, mode='a', index=False, header=not file_exists)
            file_exists = True  # Set to True after the first write
            # Delay to prevent rate limiting
            time.sleep(15)
        except StopIteration:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()

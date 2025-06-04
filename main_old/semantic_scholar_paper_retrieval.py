import requests
import csv
import time
import os

# Search parameters
SEARCH_QUERIES = [
    "medication prediction",
    "drug prediction",
    "medication recommendation",
    "drug recommendation",
    "medicine recommendation",
    "medicine prediction",
    "medicine recommender",
    "drug recommender",
    "medication recommender",
    "prescription prediction",
    "prescription recommendation",
    "prescription recommender"
]
START_YEAR = 2015
END_YEAR = 2025
API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = [
    "title", "authors", "year", "abstract", "venue", "doi", "url", "isOpenAccess", "externalIds"
]
OUTPUT_CSV = "../data/semantic_scholar_papers_2015_2025.csv"

# Helper to flatten author list
def authors_to_str(authors):
    return "; ".join([a.get("name", "") for a in authors])

def fetch_papers(query, year, offset=0, limit=100):
    # export SEMANTIC_SCHOLAR_API_KEY=your_api_key_here <- run on terminal to set your API key
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    headers = {"x-api-key": api_key} if api_key else {}
    params = {
        "query": query,
        "year": year,
        "fields": ",".join(FIELDS),
        "limit": limit,
        "offset": offset
    }
    retries = 0
    while retries < 5:
        response = requests.get(API_URL, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            wait = 2 ** retries
            print(f"Rate limited (429). Retrying in {wait} seconds...")
            time.sleep(wait)
            retries += 1
        else:
            print(f"Error: {response.status_code} for query '{query}' year {year}")
            return None
    print(f"Failed after retries for query '{query}' year {year}")
    return None

def main():
    all_papers = {}
    for query in SEARCH_QUERIES:
        for year in range(START_YEAR, END_YEAR + 1):
            offset = 0
            while True:
                data = fetch_papers(query, year, offset=offset)
                if not data or "data" not in data:
                    break
                papers = data["data"]
                if not papers:
                    break
                for paper in papers:
                    if not paper.get("isOpenAccess", False):
                        continue
                    paper_id = paper.get("paperId") or paper.get("doi") or paper.get("url")
                    if paper_id in all_papers:
                        continue
                    all_papers[paper_id] = {
                        "title": paper.get("title", ""),
                        "authors": authors_to_str(paper.get("authors", [])),
                        "year": paper.get("year", ""),
                        "abstract": paper.get("abstract", ""),
                        "venue": paper.get("venue", ""),
                        "doi": paper.get("doi", ""),
                        "url": paper.get("url", ""),
                        "isOpenAccess": paper.get("isOpenAccess", False),
                        "externalIds": paper.get("externalIds", {})
                    }
                offset += len(papers)
                if len(papers) < 100:
                    break
                time.sleep(1)  # Be polite to the API
    # Write to CSV
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "authors", "year", "abstract", "venue", "doi", "url", "isOpenAccess", "externalIds"])
        writer.writeheader()
        for paper in all_papers.values():
            writer.writerow(paper)
    print(f"Saved {len(all_papers)} open access papers to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

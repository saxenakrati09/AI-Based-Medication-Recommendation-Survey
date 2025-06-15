import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def sanitize_filename(s):
    s = re.sub(r'[^\w\-_\. ]', '_', s)
    return s[:150]

def get_pdf_url_from_doi(doi_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(doi_url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 1. Look for <a> tags with .pdf in href
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '.pdf' in href.lower():
                return urljoin(doi_url, href)
        # 2. Look for <a> or <button> with text containing 'pdf'
        for tag in soup.find_all(['a', 'button']):
            if tag.text and 'pdf' in tag.text.lower():
                href = tag.get('href')
                if href:
                    return urljoin(doi_url, href)
        # 3. Look for meta refresh redirect to PDF
        meta = soup.find('meta', attrs={'http-equiv': 'refresh'})
        if meta and hasattr(meta, 'get'):
            content = meta.get('content', '')
            if isinstance(content, str) and 'url=' in content.lower():
                url = content.split('url=')[-1]
                if '.pdf' in url.lower():
                    return urljoin(doi_url, url)
        return None
    except Exception as e:
        print(f"Error fetching {doi_url}: {e}")
        return None

def try_unpaywall_pdf(doi):
    # Unpaywall API: https://api.unpaywall.org/v2/{doi}?email=YOUR_EMAIL
    # You can set your email here for better results
    email = 'saxenakrati18@gmail.com'
    url = f'https://api.unpaywall.org/v2/{doi}?email={email}'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            best_oa = data.get('best_oa_location')
            if best_oa and isinstance(best_oa, dict):
                pdf_url = best_oa.get('url_for_pdf')
                return pdf_url
    except Exception as e:
        print(f"Unpaywall error for {doi}: {e}")
    return None

def download_pdf(pdf_url, out_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        with requests.get(pdf_url, headers=headers, stream=True, timeout=30) as r:
            if r.status_code == 200 and 'pdf' in r.headers.get('content-type', ''):
                with open(out_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")
    return False

def main():
    os.makedirs('../downloaded_papers', exist_ok=True)
    df = pd.read_csv('../data/all_papers_filtered.csv')
    for idx, row in df.iterrows():
        title = str(row['title'])
        raw = str(row['raw'])
        doi = None
        # Try to extract DOI from raw field
        m = re.search(r"'doi': '([^']+)'", raw)
        if m:
            doi = m.group(1)
        if not doi:
            print(f"No DOI for: {title}")
            continue
        doi_url = f'https://doi.org/{doi}'
        filename = sanitize_filename(title) + '.pdf'
        out_path = os.path.join('../downloaded_papers', filename)
        if os.path.exists(out_path):
            print(f"Already downloaded: {filename}")
            continue
        print(f"Processing: {title}")
        # Try Unpaywall first
        pdf_url = try_unpaywall_pdf(doi)
        if not pdf_url:
            # Try to scrape from publisher
            pdf_url = get_pdf_url_from_doi(doi_url)
        if pdf_url:
            print(f"Downloading PDF: {pdf_url}")
            if download_pdf(pdf_url, out_path):
                print(f"Saved: {filename}")
                time.sleep(2)  # Be polite
                continue
            else:
                print(f"Failed to download PDF for: {title}")
        else:
            print(f"No PDF found for: {title}")
        time.sleep(2)

if __name__ == "__main__":
    main()

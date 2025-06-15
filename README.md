# AI-Based Medication Recommendation Survey

## Systematic Review Code and Resources

This repository contains tools and resources for conducting a systematic review of AI-based medication recommendation systems. The workflow involves querying various databases, processing and filtering the retrieved data, and manually reviewing the results.

### Prerequisites

Ensure you have the following installed:

- Python 3.10

You can install the necessary libraries using pip:

```bash
pip install -r requirements.txt
```

### Workflow

1. **Data Retrieval:**

   Run queries on different databases using their respective websites and download the data. All query details and retrieved papers are stored in the `Queries` folder. Each subdirectory contains the retrieved paper information in various formats as allowed by the databases.

2. **Data Processing:**

   Navigate to the main directory of the repository and execute the following scripts in order:

   - **`processing_data.py`:** 
     - Collects all retrieved papers from the `Queries` folders and processes them into a CSV file.
     - Removes papers from arXiv as they are not peer-reviewed.
     - Run the script with:
       ```bash
       python main/processing_data.py
       ```

   - **`remove_titles_not_in_consideration.py`:** 
     - Filters out papers and phrases not considered in the survey.
     - Saves filtered and excluded papers into separate CSV files.
     - Run the script with:
       ```bash
       python main/remove_titles_not_in_consideration.py
       ```

3. **Manual Review:**

   - Make a copy of `data/all_papers_removed.csv` and rename it to `back_from_removed_manual.csv`.
   - Manually review and sort any incorrect papers that may be about medication recommendation but were removed due to phrase matching in the previous steps.


**Final List of Papers:**

`back_from_removed_manual.csv` + `all_papers_filtered.csv`.


### Folder Structure

- `Queries/`: Contains database queries and retrieved papers.
- `main/`: Contains processing scripts.
- `data/`: Stores processed CSV files.

This workflow ensures a comprehensive and accurate review of AI-based medication recommendation systems by combining automated processing with manual scrutiny.


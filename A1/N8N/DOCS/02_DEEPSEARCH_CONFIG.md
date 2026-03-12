# Technical Guide: DeepSearch Excel Configuration

The operational core of the n8n scientometric workflow logic revolves around the configuration spreadsheet: **DeepSearch.xlsx**. Rather than hardcoding API keys and delays into the visual nodes, n8n reads this file to dynamically route traffic and control rate limits.

This guide provides precise instructions on formatting this control file and outlines the authentication rules for the A1 pipeline.

---

## Anatomy of the DeepSearch Table

The Google Sheet or Local Excel file **must** contain the following **exact column headers** in the first row. The workflow logic is strictly dependent on these identifiers.

| Parameter | Required | Description | Example Target Value |
| :--- | :--- | :--- | :--- |
| **`SOURCE`** | Yes | **Crucial routing variable.** Identifies the database the configuration belongs to. The expected values are: `OPEN ALEX`, `PUBMED`, `SCOPUS`, `SEMANTIC_SCHOLAR`, `GOOGLE_SCHOLAR`, and `AZURE`. | `PUBMED` |
| **`PERSONAL_MAIL`** | Conditional | Required **ONLY** for OpenAlex. Submits the request to the "Polite Pool" to ensure optimal processing speed instead of the standard throttled pool. | `isaac.gavilanes@yachaytech.edu.ec` |
| **`RATE_LIMIT_MS`** | Yes | The millisecond delay interval n8n should enforce between sequential API calls to prevent being IP-banned. A value of `100` means a 0.1s pause. | `100` |
| **`IS_ACTIVE`** | Yes | Boolean toggle. Accepts `TRUE` or `FALSE`. If `FALSE`, the entire pipeline branch for that specific database is bypassed, acting as a structural kill-switch. | `TRUE` |
| **`API KEY`** | Conditional | The authentication token for the Database specified in the SOURCE column. OpenAlex and PubMed can work without one, but Scopus, Semantic Scholar, Google Scholar (SerpApi), and Azure OpenAI strictly require it. | `kqCXHzRYNO4v...` |

*(Note: The n8n workflow expects these headers to be capitalized exactly as shown to ensure reliable data parsing. No trailing spaces).*

---

## Setting It up in n8n

1. Fill out your `DeepSearch.xlsx` containing the structured credentials.
2. Upload this file to your Google Drive ecosystem, specifically where the n8n **Google Sheets Node** has read permutations.
3. Open your n8n canvas. Locate the "Read DeepSearch Config" node at the beginning of the workflow.
4. Ensure the **Document ID** matches the unique ID of your uploaded `DeepSearch.xlsx` file on Google Drive (found in the URL `https://docs.google.com/spreadsheets/d/YOUR_DOCUMENT_ID/edit`).

By centralizing the API keys in one file, you prevent the risk of exporting a JSON workflow that inherently leaks your private authentication tokens.

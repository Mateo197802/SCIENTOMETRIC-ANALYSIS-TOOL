# Technical Guide: DeepSearch Excel Configuration and API Extraction

The operational core of the n8n scientometric workflow is governed by a singular Google Sheet spreadsheet: **DeepSearch.xlsx**. The workflow algorithm reads this file sequentially, determines the target scientific database for each row, and executes scraping protocols using the exact parameters defined in the columns.

This guide provides precise instructions on formatting this control file and outlines the required procedures to obtain API keys for each supported platform.

---

## Part 1: Anatomy of the DeepSearch Table

The Google Sheet **must** contain a designated tab (e.g., `Queries`) featuring the following **exact column headers** in the first row. The workflow logic is strictly dependent on these identifiers for variable mapping.

| Parameter | Required | Description | Example Target Value |
| :--- | :--- | :--- | :--- |
| **`SOURCE`** | Yes | **Crucial routing variable.** Instructs the n8n Switch node on which database API to trigger. It strictly must be one of the following exact strings: `OPEN ALEX`, `PubMed`, `SCOPUS`, `Semantic_Scholar`, or `Google_Schoolar`. | `SCOPUS` |
| **`BOOLEAN SEARCHING STRING`** | Yes | The scientific query to be executed. Accepts advanced Boolean syntax (AND/OR) compliant with the target source's limitations. | `"machine learning" AND "cardiology"` |
| **`BATCH SIZE`** | Yes | The volume of papers to retrieve per pagination loop. Maximum thresholds vary by target (Scopus: 200, Semantic: 100, Scholar: 20). | `50` |
| **`YEAR RANGE`** | Yes | The chronological publication window. The format must adhere to `YYYY-YYYY` to permit internal string bifurcation by n8n. | `2018-2023` |
| **`API KEY`** | Conditional | The authentication token for the Database specified in the SOURCE column. (Further detailed in Part 2). | `a1b2c3d4e5f6...` |
| **`TOTAL BATCHES`** | Yes | The maximum number of `BATCH SIZE` iterations to execute. For instance, a Size of 50 and 4 Batches yields 200 total records. | `4` |
| **`PERSONAL_MAIL`** | Conditional | Required **ONLY** for OpenAlex queries. Submits the request to the "Polite Pool" to ensure optimal processing speed. | `your.email@university.edu` |

*(Note: The workflow expects these headers to be capitalized exactly as shown to ensure reliable data parsing).*

---

## Part 2: Extracting APIs

Different scientific indexes enforce distinct authentication protocols to grant data extraction privileges. The following sections outline the acquisition process for each.

### 1. Scopus (Elsevier)

Scopus enforces strict institutional access limits. It is mandatory to operate within a recognized university network or VPN to access full metadata records.

1. Navigate to the [Elsevier Developer Portal](https://dev.elsevier.com/).
2. Select **My API Key** at the top right of the interface.
3. Authenticate using your Elsevier, Mendeley, or Institutional credentials.
4. Click **Create API Key**.
5. Provide a Label (e.g., `Scraper Project`) and a placeholder URL (e.g., `http://localhost`).
6. **Accept** the Terms of Service and submit the request.
7. **Copy the Alphanumeric String.** Paste it into the `API KEY` column of your DeepSearch sheet on rows where the `SOURCE` is `SCOPUS`.

### 2. PubMed (NCBI E-Utilities)

PubMed permits unauthenticated scraping; however, it rate-limits anonymous requests to 3 per second. Utilizing an API key elevates this threshold to 10 requests per second.

1. Navigate to the [NCBI / PubMed Account page](https://www.ncbi.nlm.nih.gov/account/).
2. Authenticate or register a new account.
3. Access **Account Settings** by clicking the username in the top right corner.
4. Scroll to the **API Key Management** section.
5. Click **Create an API Key**.
6. **Copy the generated Key.** Paste it into the `API KEY` column where the `SOURCE` is `PubMed`.

### 3. Semantic Scholar (S2 API)

Semantic Scholar provides a comprehensive Graph API but severely throttles unauthorized requests.

1. Navigate to the [Semantic Scholar API Form](https://www.semanticscholar.org/product/api).
2. Click **Request API Key**.
3. Complete the required form detailing your research project. Explicitly state the intent to operate a scientometric or bibliometric pipeline.
4. Human approval is typically required, taking several business days.
5. Upon approval, an email containing the `x-api-key` will be dispatched.
6. **Copy the Key.** Paste it into the `API KEY` column where the `SOURCE` is `Semantic_Scholar`.

### 4. OpenAlex

OpenAlex is an open bibliometric database featuring a robust REST API. It **does not require an API Key**.

1. To obtain optimal request speeds, OpenAlex routes traffic containing an email address to a prioritized "Polite Pool".
2. This is achieved by appending a `mailto=your_email` parameter to the HTTP request.
3. **Action:** Leave the `API KEY` column blank (or write `NONE`). Crucially, ensure a valid email address is provided in the **`PERSONAL_MAIL`** column within the DeepSearch sheet.

### 5. Google Scholar (Via SerpAPI)

Google Scholar lacks an official API and actively blocks scraping attempts. Reliable data extraction requires a residential proxy API, such as SerpAPI.

1. Navigate to [SerpAPI](https://serpapi.com/).
2. Select **Register** or **Start Free Trial** (SerpAPI includes 100 free searches per month on its foundational tier).
3. Complete registration and complete email verification.
4. Access the SerpAPI Dashboard.
5. Locate the block labeled **Your Private API Key** on the dashboard.
6. Reveal and copy the 64-character hash string.
7. **Copy the Key.** Paste it into the `API KEY` column where the `SOURCE` is `Google_Schoolar`. Ensure the parameter spelling matches the n8n Switch node expectation precisely (`Google_Schoolar`).

---

> [!TIP]
> **Data Integrity Best Practice:**
> Do not leave blank rows interspersed between queries in the `DeepSearch` file. The n8n "Google Sheets" trigger will sequentially process rows until encountering an empty array, potentially terminating the batch prematurely. Additionally, ensure API keys lack trailing or leading whitespace, as this causes universal "401 Unauthorized" HTTP errors across the pipeline.

# API Key Registration and Tracking Guide

The A1 pipeline interacts with 6 different APIs to extract author data, metadata, and provide AI enriched classifications. Some are entirely free, and others limit throughput or require academic tier keys.

## 1. OpenAlex (Free)

* **Access:** Open access globally without a key.
* **Limits:** Standard limits apply ($\sim 100k$ requests a day). To bypass standard limits and use the *Polite Pool* which processes requests significantly faster, just ensure you add a valid email in the `.env` configuration file or hardcode it in the `openalex.py` module.
* **Variable Required:** `OPENALEX_DELAY=0.1`

## 2. PubMed / E-Utilities (Free)

* **Access:** National Center for Biotechnology Information (NCBI) provides an API key that allows higher request bands.
* **Getting a Key:**
    1. Register at [NCBI](https://www.ncbi.nlm.nih.gov/account/).
    2. Go to the Settings page and select "API Key Management".
    3. Generate and copy the key.
* **Variable Required:** `PUBMED_KEY`

## 3. Scopus (Academic / Institutional)

* **Access:** Elsevier requires an academic institutional account for their deeper author metrics.
* **Getting a Key:**
    1. Go to the [Elsevier Developer Portal](https://dev.elsevier.com/).
    2. Login with an active Institutional Account.
    3. Navigate to "My API Keys" to generate one.
* **Limits:** Usually limits queries to $\sim 10k-20k$ per week depending on the exact institutional contract.
* **Variable Required:** `SCOPUS_KEY`

## 4. Semantic Scholar (Free / Academic)

* **Access:** To prevent rate limits, a form needs to be filled out.
* **Getting a Key:** Fill the form at [Semantic Scholar API](https://www.semanticscholar.org/product/api) describing your research goals. Approval typically arrives within 24-48 hours.
* **Variable Required:** `SEMANTIC_KEY`

## 5. Google Scholar via SerpApi (Premium/Freemium)

* **Access:** SerpApi handles the Google Scholar endpoints to bypass CAPTCHAs.
* **Getting a Key:**
    1. Register at [SerpApi](https://serpapi.com/).
    2. A free tier generally provides 100 successful searches a month. For massive academic datasets (>1000 DOIs), an Enterprise/Academic plan is required.
* **Variable Required:** `SCHOLAR_KEY`

## 6. Genderize.io (Freemium)

* **Access:** No key needed for up to 1,000 requests per day.
* **Handling limits:** The tool incorporates an aggressive internal caching engine `GENDER_CACHE` which prevents making an API call twice if the same first name appears multiple times.

## 7. Azure OpenAI (Enterprise/Premium)

* **Access:** Used strictly for the LLM enrichment stage via GPT-4.
* **Getting a Key:**
    1. Create a Microsoft Azure Account.
    2. Request access to the Azure OpenAI service (requires corporate/academic email validation).
    3. Deploy a `gpt-4o` model inside your resource group.
    4. Navgiate to "Keys and Endpoints".
* **Variable Required:** `AZURE_OPENAI_KEY` & `AZURE_OPENAI_ENDPOINT`

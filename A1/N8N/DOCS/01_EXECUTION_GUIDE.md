# A1 Scientometric Tool Execution Guide (n8n)

This guide walks you through the comprehensive end-to-end execution of the Scientometric Analysis Tool using **n8n**. Unlike Phase 0, the A1 architecture fundamentally shifts from Boolean searching arrays to a highly stable **DOI-list based extraction logic**.

## 1. Prerequisites

1. An active n8n instance (Local or Cloud).
2. The core workflow imported into the Canvas (`A1 SCIENTOMETRIC ANALYSIS TOOL.json`).
3. An active **Google Workspace Connection** established within your n8n Credentials (to read Google Drive folders and Google Sheets).

## 2. Setting Up the Target Directories

The workflow operates autonomously by reading standard CSV inputs and flushing data to an output sheet.

1. **Create the Input Folder:** In your Google Drive, create a specific folder designated solely for your input batches. (For example, name it `CSV_INPUT_PHASE`).
2. **Extract the Folder ID:** Open the folder in Google Drive. Copy the Alphanumeric ID from the URL (e.g., `1dD0ZN7zZ0K3J4HU_NpSC59kB6r6xtAC0`).
3. **Configure the Trigger Node:** In the n8n canvas, locate the **"Search CSV folder" (Google Drive node)**. Click it and paste your Folder ID into the filter parameter.

## 3. Formatting the Input File

Instead of querying strings, the pipeline expects precise document identifiers.

1. Create a raw `.csv` file.
2. Ensure there is at least one column exactly titled **`DOI`**.
3. List all your targeted DOIs continuously below (e.g., `10.1007/s11030-021-10217-3`).
4. **Upload this `.csv` file into your `CSV_INPUT_PHASE` Google Drive folder.**

## 4. Establishing Authentication

1. Configure your `DeepSearch.xlsx` document containing your API Keys, Delays (`RATE_LIMIT_MS`), and module toggles (`IS_ACTIVE=TRUE`). (See `02_DEEPSEARCH_CONFIG.md` for structure).
2. Link this specific sheet to the corresponding initial configuration node in n8n.

## 5. Execution Workflow

1. Click **"Execute Workflow"** organically in the n8n interface.
2. **The Pipeline Flow:**
    - The Google Drive node will read your `.csv` input sheet and iterate row by row across the DOIs.
    - It routes the DOI sequentially through OpenAlex, PubMed (identifying Ghost Authors), Scopus (Author Metrics), Semantic Scholar (Influence Citations), and SerpApi (Google Scholar Interests).
    - It leverages the *Global Cache Node* to minimize API redundant calls.
    - Finally, it executes the LLM Azure OpenAI Node to profile the author backgrounds using the `genderize.io` fallback regex framework.
3. **Final Result:** The output will sequentially append to an aggregate Google Sheet designated at the workflow's conclusion, containing exactly the strict 42-column scientometric variables requested for every author parsed natively from the input DOIs.

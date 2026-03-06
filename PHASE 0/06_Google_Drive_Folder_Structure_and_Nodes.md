# Technical Guide: Google Drive Folder Structure and n8n Node Allocation

To ensure that the scientometric data extracted by the workflow is organized, stored reliably, and easily accessible, a strict directory structure must be established within Google Drive. Furthermore, specific nodes within the n8n JSON architecture must be explicitly configured to target these directories.

This document details the required folder hierarchy in Google Drive and provides precise instructions on linking these locations to the corresponding n8n automation nodes.

---

## Phase 1: Establishing the Google Drive Architecture

The automated workflow relies on specific locations to read parameters and save the resulting CSV files. Therefore, the folder structure must be created strictly as follows before initiating any execution.

1. **Access Google Drive:** Navigate to your primary Google Drive account.
2. **Create the Master Directory:** In "My Drive" (Mi unidad), create a main project folder.
   - *Example:* `SCIENTOMETRIC ANALYSIS`
3. **Create the Phase Directory:** Inside the main project folder, create a subfolder designated for this primary extraction phase.
   - *Example:* `PHASE_0`
4. **Create the Database Subfolders:** Inside `PHASE_0`, create five identical subfolders, exactly matching the names of the target databases to prevent data mixing:
   - `Google_Schoolar`
   - `Open_Alex`
   - `PUBMED`
   - `SCOPUS`
   - `Semantic_Scholar`
5. **Place the Configuration File:** Ensure that your Google Sheet control document, exactly named `DeepSearch`, is placed at the root of the `PHASE_0` directory, parallel to the five subfolders.

---

## Phase 2: Configuring Data Input Nodes (Reading DeepSearch)

To initiate the workflow, n8n must first locate and read the `DeepSearch` Google Sheet. This is handled by two specific nodes at the very beginning of the layout.

### Node 1: "Download Queries"

This node physically locates the Google Sheet file to trigger the iteration.

1. Open the n8n workflow canvas.
2. Locate and double-click the node labeled **Download Queries** (a Google Drive node type).
3. Ensure the Credentials are correctly set to your authenticated Google Drive account.
4. In the **File ID** or **File** field, click the search/list icon.
5. Navigate through your Drive structure (`My Drive > SCIENTOMETRIC ANALYSIS > PHASE_0`) and select the `DeepSearch` file.

### Node 2: "Get row(s) in sheet"

This node extracts the tabular data from the located file.

1. Double-click the node labeled **Get row(s) in sheet** (a Google Sheets node type).
2. Ensure the Credentials are set to your corresponding Google Sheets account.
3. In the **Document ID** field, locate and select the `DeepSearch` file.
4. In the **Sheet Name** field, ensure it targets the correct tab containing your parameters (e.g., `Queries` or `Sheet1`).

---

## Phase 3: Configuring Data Output Nodes (Saving CSV Files)

The workflow consists of five distinct branches, each assigned to scrape a specific database. At the end of every branch is a specific Google Drive node tasked with uploading the generated CSV file.

You must manually configure each of these nodes to point to the correct subfolder created during Phase 1.

### 1. Scopus Branch

1. Locate the **Save Scopus1** node.
2. Double-click to open its properties.
3. In the **Folder ID** field, navigate to `My Drive > SCIENTOMETRIC ANALYSIS > PHASE_0` and unambiguously select the **`SCOPUS`** folder.

### 2. OpenAlex Branch

1. Locate the **Upload file1** node (situated at the end of the OpenAlex execution branch).
2. Double-click to open its properties.
3. In the **Folder ID** field, navigate to your root structure and meticulously select the **`Open_Alex`** folder.

### 3. Semantic Scholar Branch

1. Locate the **Save Semantic** node.
2. Double-click to open its properties.
3. In the **Folder ID** field, traverse to your project directory and strictly select the **`Semantic_Scholar`** folder.

### 4. PubMed Branch

1. Locate the **Save PubMed** node.
2. Double-click to open its properties.
3. In the **Folder ID** field, drill down into your Google Drive path and selectively target the **`PUBMED`** folder.

### 5. Google Scholar Branch

1. Locate the **Save Scholar** node.
2. Double-click to open its properties.
3. In the **Folder ID** field, navigate to the storage array and explicitly select the **`Google_Schoolar`** folder.

---

## Integrity Validation

Following the configuration of these seven critical nodes (two inputs, five outputs), it is highly recommended to click the **Save** button in the n8n interface.

By hardcoding the Folder IDs and File IDs directly into these specific nodes via the visual navigator, n8n will permanently retain the exact Google Drive routing, guaranteeing that all scraped scientific literature is securely grouped by source provider without human intervention.

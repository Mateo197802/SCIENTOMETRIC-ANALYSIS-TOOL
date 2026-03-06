# Technical Guide: Workflow Architecture and Data Extraction

The n8n scientometric workflow is an advanced orchestration system designed to automate large-scale academic literature retrieval, bibliometric standardization, and AI-driven data enrichment.

This document details the internal mechanics of the tool and provides a comprehensive dictionary of the specific structured data extracted from the five supported scientific databases.

---

## Part 1: Core Workflow Architecture

The automation is structured as a robust looping pipeline consisting of the following sequential phases:

### 1. Ingestion Phase

Upon manual execution, a Google Drive node seeks the `DeepSearch` spreadsheet. A subsequent Google Sheets node extracts every row of configuration parameters (Keywords, API keys, Batch Sizes, and the target Source Database).

### 2. Routing Phase

An n8n **Switch** node evaluates the `SOURCE` variable from the current row. Based on this string, the workflow selectively activates one of five independent application branches (Scopus, PubMed, Semantic Scholar, OpenAlex, or Google Scholar) and bypasses the rest.

### 3. Execution & Pagination Phase

The active branch triggers an **HTTP Request** node to query the respective REST API. The workflow incorporates custom JavaScript-based pagination logic (`batch_size`, `start_index`, `page_counter`). It continually loops HTTP requests until the `TOTAL BATCHES` parameter is met or the API runs out of query results.

### 4. Normalization Phase (The "Lukas Technique")

Scientific APIs return deeply nested, inconsistent JSON arrays (or XML in PubMed’s case). The workflow utilizes custom Code nodes to normalize this data into a flat, standardized format.

- **Unrolling Authors:** The framework employs a specific computational technique to unroll the authors. Instead of generating one row per paper, **it generates one distinct row per author per paper.** If a paper has ten authors, it outputs ten rows. This is critical for granuluar geographical and bibliometric analysis.

### 5. Semantic Enrichment Phase (LLM Integration)

Academic APIs often return unstructured affiliation strings (e.g., "Department of Cardiology, General Hospital, 123 Main St, Springfield"). The workflow intercepts this raw string and transmits it to a Large Language Model (Azure OpenAI or Local Ollama). The LLM is strictly prompted to analyze the string and output a standardized **2-letter ISO 3166-1 alpha-2 country code** (e.g., US, FR, JP), enabling robust macro-geographical statistical analysis.

### 6. Archival Phase

The flattened, enriched JSON array is converted into a standard CSV file and pushed to the designated Google Drive subfolder, incrementing the filename by page number.

---

## Part 2: Extracted Data Dictionary

Regardless of the database queried, the workflow is engineered to normalize and output a consistent set of columns. Below is the specification of the data extracted per row.

### Core Paper Metrics

*Data shared identically across all authors belonging to the same publication.*

| Column Header | Description | Provider Support |
| :--- | :--- | :--- |
| **`PAPER_TITLE`** | The standardized title of the academic publication. | All Branches |
| **`DOI`** | The Digital Object Identifier string. | All Branches |
| **`YEAR`** | The specific year of publication. | All Branches |
| **`SOURCE_DB`** | The origin database of the record (e.g., "Scopus", "PubMed"). | All Branches |

### Author-Level Granular Metrics

*Data distinct to the specific author occupying the current row.*

| Column Header | Description | Provider Support |
| :--- | :--- | :--- |
| **`AUTHOR_NAME`** | The formatted name of the researcher. | All Branches |
| **`AUTHOR_POSITION`** | The ranked position within the author list. Categorized strictly as `first`, `middle`, or `last`. | All Branches |
| **`AUTHOR_ID`** | The proprietary internal ID assigned by the source database (Extremely vital for cross-referencing). | Scopus, OpenAlex, Semantic, Scholar |
| **`ORCID`** | The universal Open Researcher and Contributor ID. Extracted aggressively direct from metadata if available. | Scopus, OpenAlex, PubMed, Semantic |
| **`AFFILIATION`** | The raw string detailing the university, hospital, or corporate laboratory. | All Branches |
| **`GEOLOCATION_COUNTRY`** | The normalized 2-letter ISO code denoting the country of the affiliation. Inherited via LLM Extraction or direct API mapping. | All Branches |

### Advanced Bibliometric Indices (Author Profile)

*Data extracted by querying the specific Author Profile endpoint using the `AUTHOR_ID` (Requires a secondary API lookup within the loop).*

| Column Header | Description | Provider Support |
| :--- | :--- | :--- |
| **`total_citations`** | The cumulative aggregate of citations accrued by the author across their entire catalog. | Scopus, OpenAlex, Semantic, Scholar |
| **`hindex`** | The Hirsch index, measuring both productivity and citation impact. | Scopus, OpenAlex, Semantic, Scholar |
| **`i10index`** | The number of publications by the author with at least 10 citations. | OpenAlex, Scholar |
| **`consecutive_years`** | A calculated temporal metric assessing the current continuous streak of years the author has published at least one paper. | Scopus, OpenAlex, Semantic, Scholar |
| **`seniority`** | A calculated categorical variable (`Early`, `Mid`, `Senior`) based on the total temporal length of the author's publishing career. | Scopus, OpenAlex, Semantic, Scholar |
| **`keywords` / `interests`** | Representational concepts or MeSH terms associated with the author's historical output or the specific paper. | PubMed, OpenAlex, Scholar |

> [!NOTE]
> **Provider Null Variables:** Due to API limitations, not all databases support advanced profile metrics. When an API does not provide a metric (e.g., PubMed does not calculate an `hindex`), the system will gracefully degrade the output to `"N/A"` or `"0"` to prevent pipeline failure and maintain structural integrity in the resulting CSV matrix.

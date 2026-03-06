# Scientometric Analysis Tool

Welcome to the **Scientometric Analysis Tool** repository. This project is a comprehensive, automated data engineering framework built on **n8n** to extract, normalize, and enrich bibliometric and scientometric data from major academic databases.

The core objective of this tool is to automate systematic literature reviews and large-scale academic metadata retrieval. By integrating multiple scientific APIs and Artificial Intelligence (LLMs), it standardizes nested JSON structures into analysis-ready, flat CSV formats.

---

## Project Structure

The operational core and technical documentation for this tool are organized within the `PHASE 0` directory. This directory contains detailed, step-by-step guides covering deployment, configuration, and the internal algorithmic architecture of the workflow.

### Documentation Index (`PHASE 0/`)

* **`01_N8N_Local_Deployment_Guide.md`**: Instructions for securely hosting and running the n8n automation engine locally via Docker.
* **`02_Google_Cloud_APIs_Setup_Guide.md`**: Steps to configure a Google Cloud Project, enable Google Drive/Sheets APIs, and generate OAuth2 credentials for secure data handling.
* **`03_Ollama_Local_LLM_Integration.md`**: Guide for deploying Ollama locally to utilize Large Language Models (LLMs) for semantic text extraction without relying on paid cloud endpoints.
* **`04_Importing_JSON_Workflow_n8n.md`**: Procedural steps to successfully import the pre-built scientometric workflow (JSON format) into your n8n workspace.
* **`05_DeepSearch_Configuration_and_APIs.md`**: Explanation of the `DeepSearch .xlsx` control matrix layout and detailed instructions for obtaining API keys for Scopus, PubMed, Semantic Scholar, and SerpAPI (Google Scholar).
* **`06_Google_Drive_Folder_Structure_and_Nodes.md`**: Mandatory protocol for structuring the Google Drive directories to ensure scraped data is correctly routed and isolated by origin database.
* **`07_Workflow_Architecture_and_Data_Extraction.md`**: Deep dive into the tool's internal mechanics (routing, pagination, data unrolling) and a data dictionary of the fields extracted per database.
* **`08_Acknowledgement_Lukas.md`**: Formal recognition of the foundational Python logic and data normalization techniques ("The Lukas Technique") that inspired the architecture of this n8n implementation.

### Configuration Template

* **`DeepSearch .xlsx`**: The master control sheet template used to feed keywords, parameters, and API keys into the n8n scraping loop.

---

## Core Capabilities

1. **Multi-Database Integration:** Capable of querying Scopus, PubMed, OpenAlex, Semantic Scholar, and Google Scholar (via SerpAPI).
2. **Granular "1-to-1" Author Mapping:** Automatically unrolls deeply nested authorship arrays to generate one structured row per author per paper, enabling precise entity tracking.
3. **Advanced Bibliometric Indices:** Programmatic extraction of complex metrics such as H-index, total lifetime citations, and consecutive publishing years.
4. **AI-Driven Geolocation:** Utilizes LLMs to parse unstructured affiliation text and output standardized ISO country codes for macro-geographical statistical modeling.

---

##  Getting Started

To begin using this tool, please navigate to the `PHASE 0/` directory and sequentially follow manuals `01` through `06` to stand up your environment.

**Disclaimer:** Ensure compliance with the respective Terms of Service and API usage limits of the scientific databases queried by this tool.

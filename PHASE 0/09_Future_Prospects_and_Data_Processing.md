# Future Prospects: Advancing Data Processing and Metadata Extraction

As Phase 0 successfully establishes the foundational architecture for automated, large-scale literature retrieval and standardization via n8n, the logical progression of this project shifts towards the enhancement of downstream data processing.

This document outlines the strategic roadmap and future prospects for the Scientometric Analysis Tool, focusing specifically on how the generated CSV datasets will be parsed, molded, and enriched in subsequent phases.

---

## The Next Strategic Step: Molding CSV Processing Tools

The current workflow excels at scraping and unrolling author data into standardized flat files separated by database source. However, the raw JSON responses from providers like Scopus, OpenAlex, and Semantic Scholar contain significantly more rich metadata than what is currently being captured in the primary output matrix.

**The immediate next objective is to engineer advanced, programmatic CSV processing tools (likely via Python Pandas scripts or additional n8n analytical sub-workflows) designed to dig deeper into the raw data layer.**

### Core Objectives for the Next Processing Phase

#### 1. Advanced Metadata Extraction

We aim to refactor the data-handling scripts to extract deeper layers of bibliometric intelligence that are presently discarded during the flattening process, such as:

* **Funding Entities & Sponsors:** Capturing the specific grant numbers and funding organizations supporting the research.
* **Journal Impact Metrics:** Extracting not just the journal name, but its associated SNIP (Source Normalized Impact per Paper) or CiteScore directly from the metadata if provided.
* **Reference Networks:** Pulling the raw list of citations *made by* the paper (the bibliography) to enable dynamic citation network analysis and co-citation clustering.
* **Open Access Classification:** Categorizing the exact type of Open Access (Gold, Green, Bronze) to analyze accessibility trends.

#### 2. Cross-Database Deduplication & Merging

Since the current architecture saves files in isolated folders (`PHASE_0/SCOPUS`, `PHASE_0/PUBMED`, etc.), the next critical tool must be capable of ingesting these disparate CSVs and performing intelligent deduplication.

* The system must use the `DOI` (Digital Object Identifier) as the primary key to merge records.
* It must intelligently resolve conflicts when two databases report slightly different citation counts for the exact same paper.

#### 3. Temporal and Geographical AI Enrichment

While we currently use an LLM (Azure OpenAI/Ollama) to extract the Country Code from an affiliation string, future processing tools will expand on this:

* **Entity Resolution:** Utilizing AI to standardize university names (e.g., merging "Mass. Inst. of Tech", "MIT", and "Massachusetts Institute of Technology" into a single entity ID).
* **Keyword Harmonization:** Using NLP to group synonymous author-provided keywords into standardized thematic clusters for clearer trend analysis.

---

## Conclusion

The architecture built in Phase 0 has successfully solved the problem of *data acquisition*. The upcoming prospect is to solve the problem of *data depth*. By molding our CSV parsing tools to capture this extended metadata, the Scientometric Analysis Tool will transition from a powerful search engine into a holistic, predictive bibliometric intelligence platform.

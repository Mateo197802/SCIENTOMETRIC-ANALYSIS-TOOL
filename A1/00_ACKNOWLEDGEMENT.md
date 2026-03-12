# Formal Acknowledgment and Technical Credits

This document serves as a formal recognition of the methodologies and algorithmic structures implemented within the Scientometric Analysis tool.

## Technical Acknowledgment: The "Lukas Technique"

A significant portion of the data normalization success within this architecture is directly attributed to the data-unrolling methodology conceptually pioneered by **Lukas**.

Prior to this implementation, handling highly nested, multi-author JSON arrays from disparate commercial scientific APIs (such as Scopus or Semantic Scholar) presented a severe structural bottleneck. The standard approach of retaining one row per publication severely limited granular bibliometric analysis, rendering deep geolocation and individual author tracking mathematically intractable.

The integration of what is internally documented within the codebase as the **"Lukas Technique"** revolutionized the pipeline's capability. By enforcing a strict logic that iterates over the `authorships` array and forcefully unrolls the JSON object to output **one distinct row per author per paper**, the system achieved a level of relational flatness required for advanced scientometric modeling.

### Key Contributions Implemented

1. **Granular Author Unrolling:** Transitioning the dataset from a `1-to-N` document model to a `1-to-1` author-entity model.
2. **Positional Tracking Logic:** The algorithm that accurately tags researchers as `first`, `middle`, or `last` author based on their array index—a critical metric in assessing academic contribution weight.
3. **Cross-Referencing Feasibility:** By isolating individual Author IDs per row, the Lukas methodology made it structurally possible to execute secondary API hits (Author Profile lookups) to extract advanced metrics like H-index and total citations downstream.

We extend our sincere gratitude to Lukas for providing the conceptual baseline that elevated this data extraction pipeline and analytics-ready data engineering framework.

Specifically, the original Python scripts and Jupyter notebooks designed by Lukas contained within the `author-info-scraping-main` repository—which initially demonstrated how to extract and compute h-index, classify authors by seniority, and parse geolocation data using the OpenAlex and SerpAPI endpoints—served as the core inspirational blueprint for this project.

## Technical Acknowledgment: Gender Inference & Author Profiling

We also extend our deep appreciation to **Kaushik Madapati** and **Rahul** for their structural contributions and conceptual logic regarding the author profiling workflow, initially derived from the methodologies within the `Harvard-Capstone-main` project.

Their strategic input fundamentally shaped the efficiency and cost-effectiveness of the enrichment phase.

### Core Logic & Prototyping Contributions

1. **Global Caching Logic:** The implementation of a global caching system (`GENDER_CACHE` and `SCHOLAR_CACHE`) that significantly minimizes system overhead by tracking unique names and parameters prior to external queries, preventing redundant API calls and mitigating rate limits.
2. **Probability Cutoffs and Regex Fallback Methodology:** Rahul's insight into establishing strict probability cutoffs (e.g., >0.8) for gender inference and incorporating a cost-effective, multi-tiered fallback loop. This methodology optimizes API usage by prioritizing Regex term-frequency filtering of "he/him" and "she/her" pronouns in Google Search snippets, escalating to deeper LLM agent analysis only as a last resort for ambiguous results.
3. **ORCID & Author-Centric Query Paradigms:** Conceptual frameworks regarding the granular extraction of department and employment data through ORCID integrations, paving the way for targeted author-centric profiling.
4. **Mock Data and Prototyping Architectures:** The provision of the core testing architecture and JSON mock payloads (such as `openalex_results.json` and initial `sample_dois.csv` sets) by Kaushik Madapati greatly accelerated the isolated testing phase for the pipeline orchestrator without burning through active API keys.

*The success, stability, and computational efficiency of this scientometric tool are heavily indebted to these foundational logic contributions.*

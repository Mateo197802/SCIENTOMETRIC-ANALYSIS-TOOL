# Reproducible Validation of an Author-Level Scientometric Analysis Tool Against Published Bibliometric Benchmarks

Authors:
Affiliations:
Corresponding author:

## Abstract

Background: Scientometric studies are increasingly used to characterize research fields, collaboration structures, country participation, institutional productivity, and citation impact. However, many analyses remain difficult to reproduce because corpus construction, author disambiguation, affiliation normalization, and multi-source metadata enrichment are often handled manually or through platform-specific workflows.

Objective: We describe and propose the validation of a DOI-driven Scientometric Analysis Tool designed to generate reproducible author-level, paper-level, affiliation-level, and country-level outputs from closed or query-derived corpora. The objective is to validate the tool against published scientometric benchmarks rather than to make claims from a single unpublished corpus.

Methods: The validation study will reconstruct corpora from published scientometric studies that report a search strategy or corpus-construction method, time range, inclusion and exclusion criteria, final document count, and bibliometric outputs. Candidate benchmarks include studies on academic publishing, mindfulness research, and multi-criteria decision-aid methods. Reconstructed corpora will be normalized into DOI-first input tables and processed through OpenAlex, PubMed, Semantic Scholar, ORCID, Genderize, and deterministic schema-bound profile classification. A second metadata run will evaluate Scopus and Google Scholar/SerpAPI enrichment where access is confirmed. Outputs will be compared with benchmark publications using document-count agreement, DOI reconciliation, country and institutional rank overlap, author overlap where available, authorship-position patterns, citation indicators, and a structured mismatch ledger.

Preliminary status: The current pipeline has already completed a closed-corpus stress test with 1,158 DOI values, 7,361 author-paper records, 5,675 distinct valid OpenAlex author identifiers, and 35 output fields. These outputs support engineering feasibility, but they are not sufficient for final scientific validation. Final results require benchmark reruns and the planned second metadata expansion.

Conclusions: A validation-first design creates a stronger publication pathway for the tool by testing whether it can reproduce peer-reviewed scientometric findings within explainable database, API, and deduplication differences. The manuscript will report final benchmark comparisons only after the second run and manual audit are complete.

Keywords: scientometrics; bibliometrics; author disambiguation; OpenAlex; Semantic Scholar; ORCID; Scopus; Google Scholar; reproducibility; research collaboration.

## Introduction

Scientometric and bibliometric analyses are widely used to map the structure of scientific fields, identify leading institutions and countries, quantify co-authorship patterns, and examine citation influence. These studies often inform research policy, capacity-building strategies, and field-level self-assessment. Yet their reproducibility depends heavily on decisions that are not always fully auditable: database selection, query syntax, inclusion filters, deduplication, author disambiguation, affiliation normalization, and the extraction of author-level variables.

Author-level analysis is especially difficult. A single paper can contain many authors, each with multiple institutional affiliations and identifiers distributed across bibliographic systems. Country-level analyses can also be misinterpreted if publication-time affiliation is confused with nationality, residence, ethnicity, or study setting. A reproducible tool must therefore preserve the paper-author structure, track provenance, make missingness explicit, and avoid causal interpretation when only descriptive metadata are available.

The current project was reframed after the June 30 project meeting. The primary manuscript should not claim that a single closed corpus proves tool validity. Instead, the tool should be validated by reproducing results from published scientometric studies whose methods and outputs are already available in peer-reviewed literature. This validation-first strategy tests whether the pipeline can reproduce accepted findings when supplied with equivalent corpus-construction rules.

We therefore propose a methodological validation study of the Scientometric Analysis Tool. The tool ingests closed DOI lists or query-derived records, retrieves and reconciles metadata from multiple public sources, constructs a master author-paper table, validates CSV and JSON parity, and generates benchmark comparison outputs. The manuscript will focus on reproducibility, error tracing, and transparent mismatch explanation rather than on a new standalone descriptive analysis.

The first validation phase will use three candidate benchmarks: Yan and Wang's bibliometric analysis of academic publishing; Baminiwatta and Solangaarachchi's analysis of mindfulness research; and Basilio et al.'s systematic review of multi-criteria decision-aid methods. These studies were selected because they report corpus construction, time windows, filtering logic, final document counts, and bibliometric outputs that can be used as reference targets.

## Methods

### Study Design

This is a methodological validation study. Each selected published scientometric study functions as an external benchmark. The tool will be evaluated by reconstructing the benchmark corpus as closely as possible, processing it through the same author-level pipeline, and comparing the resulting outputs with the benchmark publication.

The validation target is not perfect numerical identity. Bibliographic databases evolve, APIs expose different metadata fields, and citation counts change over time. The target is reproducible comparability: similar denominators, stable leading countries and institutions, consistent author and collaboration patterns where measurable, and a transparent explanation for all major discrepancies.

[[FIGURE_1_VALIDATION_WORKFLOW]]

Figure 1. Validation-first workflow for the Scientometric Analysis Tool. Published benchmark studies define the corpus; the tool reconstructs and enriches the corpus, builds the author-paper table, and compares outputs against external reference results through a mismatch ledger.

### Benchmark Selection

Benchmark studies were selected using five criteria: explicit query or corpus-construction method; defined time range; inclusion or exclusion filters; final document count; and reported bibliometric outputs such as authorship, affiliation, country, institution, collaboration, or citation indicators.

The current benchmark set includes:

Yan and Wang (2023): a Web of Science bibliometric analysis of academic publishing from 1970 to 2020, reporting 2,217 documents and outputs related to countries, institutions, productive authors, and cited articles.

Baminiwatta and Solangaarachchi (2021): a Web of Science analysis of mindfulness research from 1966 to 2021, reporting 16,581 publications and outputs related to country collaboration, co-authorship, and citation bursts.

Basilio et al. (2022): a Web of Science and Scopus analysis of multi-criteria decision-aid methods from 1977 to April 2022, reporting 35,643 retrieved records and 23,494 analyzed records, with outputs related to authors, countries, institutions, and citation patterns.

Mejia et al. (2021) will be used as methodological support for citation-network and semantic-analysis framing, but it will not be treated as a direct validation benchmark unless its corpus construction can be reconstructed with sufficient precision.

[[FIGURE_2_BENCHMARK_MATRIX]]

Figure 2. Candidate benchmark matrix for the first validation phase. Published document counts are treated as external denominators; reproduced counts will be reported after reruns and source-specific mismatch analysis.

### Corpus Reconstruction and DOI Normalization

For each benchmark, the reported search equation, database source, time range, document-type filters, language filters, and exclusion criteria will be extracted into a structured validation protocol. Retrieved records will be normalized to a DOI-first input table whenever DOI values are available. Records without resolvable DOI values will be retained in a loss log so that denominator differences can be explained rather than silently dropped.

When a benchmark was originally generated in Web of Science or Scopus, the closest available reconstruction route will be used. If exact platform access is unavailable, OpenAlex and other accessible sources will be used for approximation, but the mismatch ledger will explicitly mark this as a source-difference limitation.

### Metadata Retrieval and Enrichment

The first validation run will use the current implemented pipeline. OpenAlex provides work-level metadata, authorships, author identifiers, institutions, country codes, concepts, citation counts, works counts, and author-level indicators where available. PubMed adds biomedical metadata when DOI, PMID, or PMCID matching is possible. Semantic Scholar contributes paper and author metadata and can strengthen identifier reconciliation. ORCID enrichment is used to recover author identifiers and employment or affiliation history where publicly available. Genderize provides name-based gender inference with caching to reduce repeated requests; this field is treated as inferred and never as self-identified gender.

The profile-classification layer uses deterministic, schema-bound LLM output to classify author research profiles from available publication metadata. This output is explicitly considered inferential and requires manual validation before substantive interpretation.

### Author-Paper Table Construction

The pipeline unrolls nested paper-authorship metadata into an author-paper table. Each row represents an author-paper observation rather than a unique individual. Core variables include DOI, paper title, publication year, author name, OpenAlex author identifier, ORCID, authorship position, corresponding-author status where available, publication-time affiliation, institution identifier, country code, author-level bibliometric indicators, PubMed metadata, Semantic Scholar metadata, ORCID employment fields, name-based gender inference, inferred research profile, and missing-value provenance.

This structure preserves the denominator required for paper-level, author-level, country-level, and institution-level analyses. It also prevents incorrect aggregation, such as treating author-paper records as unique researchers without deduplication by stable identifier.

### Data Validation and Quality Control

The validation layer performs CSV and JSON parity checks, schema checks, DOI reconciliation, row-count validation, missingness profiling, and field-coverage summaries. DOI reconciliation requires every input DOI to be accounted for as present or missing in the final table. Missing identifiers, unresolved authors, ambiguous affiliations, and incomplete enrichment are logged rather than overwritten.

Quality control will include a manual audit sample for author disambiguation, affiliation-country assignment, corresponding-author detection, and profile classification. Authorship position will be analyzed descriptively and will not be interpreted as evidence of research leadership quality or extractive collaboration by itself.

### Benchmark Comparison

The primary comparison endpoints are final document count, DOI resolution rate, country distribution, institutional distribution, productive-author overlap where available, collaboration patterns, authorship-position patterns, corresponding-author patterns, citation indicators, and source-specific mismatch categories.

For country and institutional outputs, the tool will compare top-ranked entities, rank overlap, and percentage-share differences where the benchmark publication reports comparable values. Citation and h-index indicators will be interpreted cautiously because source snapshots and citation coverage vary across APIs.

### Second Metadata Run

The current manuscript base intentionally treats results as interim. A second metadata run is required to evaluate whether Scopus identifiers, affiliation history, citation metadata, and Google Scholar/SerpAPI checks materially improve corpus reconstruction and author-level validation. These sources should be described as metadata-access dependencies until the team confirms access and executes the rerun.

[[FIGURE_3_SECOND_RUN_EXPANSION]]

Figure 3. Boundary between current preliminary outputs and the planned second-run validation layer. Current outputs support methods and stress-test reporting; final benchmark conclusions require Scopus and Google Scholar/SerpAPI expansion or a documented decision that these sources are unavailable.

### Reproducibility

All pipeline steps will be versioned in the repository. Generated CSV, JSON, figure, and comparison outputs should be reproducible from committed scripts and fixed input files. API dates, database snapshots, query strings, software versions, and source-specific limitations will be recorded in the validation log.

## Preliminary Results

### Pipeline Stress Test

The tool has completed a closed-corpus stress test with 1,158 DOI values. The processed output contains 7,361 author-paper records, 5,675 distinct valid OpenAlex author identifiers, and 35 output fields. The run demonstrates that the pipeline can ingest a fixed DOI corpus, retrieve multi-source metadata, construct an author-paper table, and pass DOI reconciliation and CSV/JSON parity checks.

These values should be interpreted as engineering and workflow evidence only. They do not establish external validity because the stress-test corpus is not itself a published benchmark with peer-reviewed reference outputs.

### Benchmark Readiness

Three benchmark studies have been identified for the first validation phase. Yan and Wang (2023) is the recommended first benchmark because its corpus size is moderate and its reported outputs align closely with the current tool: countries, institutions, productive authors, and cited papers. Baminiwatta and Solangaarachchi (2021) adds a larger collaboration-network benchmark. Basilio et al. (2022) provides a larger multi-source benchmark that will test the tool's capacity to handle Scopus-linked corpus reconstruction and country/institution summaries.

### Current Output Boundary

At this stage, the manuscript can report the tool architecture, variable dictionary, validation strategy, benchmark-selection rationale, and stress-test feasibility. It should not yet report final benchmark reproduction results. Those results require the second metadata run, benchmark-specific corpus reconstruction, comparison tables, and manual audit.

## Discussion

This validation-first approach creates a stronger and more defensible manuscript than a corpus-specific descriptive analysis. It directly tests whether the tool can reproduce the outputs of published scientometric studies and makes discrepancies auditable. The mismatch ledger is central: it turns disagreement into evidence about source coverage, DOI availability, database drift, author disambiguation, and affiliation normalization.

The tool's main contribution is the construction of a reproducible author-paper evidence layer that preserves provenance and denominator logic. This is important because many scientometric claims depend on whether the denominator is a paper, an author-paper record, a deduplicated author, an institution, or a country. By keeping these levels explicit, the tool reduces the risk of overinterpretation.

Several outputs require careful interpretation. Affiliation country reflects the institution listed at publication time, not nationality, residence, ethnicity, or study setting. Name-based gender inference is not self-identified gender. LLM-based profile classification is a structured inference and requires manual validation. Citation indicators are source-dependent and can change over time. Authorship order and corresponding-author status are descriptive signals, not standalone proof of leadership quality or collaboration equity.

## Limitations and Next Steps

The current manuscript is a base draft. Final results depend on reconstructing the benchmark corpora and completing the second metadata run. The main limitations to resolve are Scopus access, Google Scholar/SerpAPI access, DOI coverage for records without DOI, database snapshot drift, author disambiguation, affiliation normalization, and manual validation of inferred fields.

The immediate next steps are: finalize the first benchmark protocol; reconstruct the Yan and Wang corpus; run the pipeline on the reconstructed input table; generate comparison tables; document denominator losses; decide whether Scopus and Google Scholar/SerpAPI enrichment are required before manuscript submission; and complete a manual audit sample.

## Conclusions

The Scientometric Analysis Tool is best positioned as a reproducible validation platform for author-level scientometric analysis. The manuscript should demonstrate that the tool can reproduce published benchmark outputs within explainable source differences. The current stress-test run supports feasibility, but final claims should wait for benchmark reruns, second-run metadata enrichment, and manual audit.

## Declarations

Data availability: To be completed after benchmark corpus reconstruction.

Code availability: The tool is maintained in the project repository and should be linked after the validation branch is finalized.

Ethics: The study uses bibliographic and author metadata from public or institutionally accessible scholarly databases. No patient-level data are analyzed.

Competing interests:

## References to Complete

Yan L, Wang Z. Mapping the Literature on Academic Publishing: A Bibliometric Analysis on WOS. SAGE Open. 2023. doi:10.1177/21582440231158562.

Baminiwatta A, Solangaarachchi I. Trends and Developments in Mindfulness Research over 55 Years. Mindfulness. 2021;12:2099-2116. doi:10.1007/s12671-021-01681-x.

Basilio MP, Pereira V, Costa HG, Santos M, Ghosh A. A Systematic Review of the Applications of Multi-Criteria Decision Aid Methods (1977-2022). Electronics. 2022;11(11):1720. doi:10.3390/electronics11111720.

Mejia C, Wu M, Zhang Y, Kajikawa Y. Exploring Topics in Bibliometric Research Through Citation Networks and Semantic Analysis. Frontiers in Research Metrics and Analytics. 2021;6. doi:10.3389/frma.2021.742311.

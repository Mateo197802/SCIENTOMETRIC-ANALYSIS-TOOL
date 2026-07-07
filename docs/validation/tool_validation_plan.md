# Scientometric Analysis Tool Validation Plan

## Working Title

Reproducible Validation of a DOI-Driven Author-Level Scientometric Analysis Tool
Against Published Bibliometric Benchmarks

## Objective

Validate the Scientometric Analysis Tool by reproducing selected results from
published scientometric studies with transparent corpus-construction rules. The
goal is to test whether the pipeline can generate comparable document counts,
country and institutional distributions, authorship-position summaries,
collaboration patterns, and bibliometric indicators from the same input rules.

## Study Design

This is a methodological validation study. Each benchmark study functions as a
reference standard for a specific reproducible corpus definition. The tool will
be run on reconstructed benchmark corpora, and its outputs will be compared with
the published results.

## Validation Workflow

1. Extract the benchmark's query, time range, database source, document-type
   filters, language filters, and final document count.
2. Reconstruct the corpus through the closest available API route.
3. Normalize retrieved identifiers into a DOI-first input table.
4. Run the Scientometric Analysis Tool on the closed input set.
5. Generate `MASTER_AUTHOR_TABLE.csv` and `MASTER_AUTHOR_TABLE.json`.
6. Validate CSV/JSON parity, DOI reconciliation, and author-paper row integrity.
7. Compare the tool outputs against published benchmark results.
8. Log every mismatch by source: database coverage, missing DOI, deduplication,
   author disambiguation, affiliation normalization, or unavailable citation
   metadata.

## Tool Components to Describe in the Methods

The manuscript should explicitly describe each pipeline layer:

- closed-corpus input handling from DOI or query-derived records;
- OpenAlex metadata retrieval for works, authorships, institutions, countries,
  concepts, citations, and author-level indicators;
- PubMed enrichment for biomedical metadata when PMID/PMCID or DOI matching is
  available;
- Semantic Scholar enrichment for author and paper metadata;
- ORCID enrichment for author identifiers and employment/affiliation history
  where available;
- Genderize name-based inference, including caching and the limitation that it
  is not self-identified gender;
- deterministic LLM profile classification with schema-bound output and manual
  validation requirement;
- CSV and JSON parity validation;
- DOI reconciliation;
- figure generation and benchmark comparison tables;
- optional Scopus and Google Scholar/SerpAPI expansion for richer validation
  when access is confirmed.

## Extracted Author-Level Variables

The current master table is designed to capture:

- DOI and paper-level bibliographic metadata;
- publication year and title;
- author name and OpenAlex author identifier;
- ORCID where available;
- authorship position;
- corresponding-author flag where available;
- publication-time affiliation string;
- institution identifier and country code;
- OpenAlex h-index, works count, and citation indicators;
- PubMed and Semantic Scholar identifiers or metadata where matched;
- ORCID employment information where available;
- name-based gender inference;
- inferred disciplinary or research profile;
- provenance and missing-value sentinels for downstream validation.

## Primary Comparison Endpoints

| Endpoint | Comparison method |
|---|---|
| Final document count | Absolute and percentage difference from published count |
| DOI reconciliation | Number and percentage of benchmark records resolved to DOI |
| Country distribution | Rank overlap, top-country agreement, and share difference |
| Institutional distribution | Rank overlap and leading-institution agreement |
| Productive authors | Top-author overlap where author-level reporting is available |
| Collaboration patterns | Country or institution co-authorship comparability |
| Citation indicators | Directional agreement and mismatch logging by source coverage |

## Proposed Acceptance Logic

The validation should not require perfect identity with the original papers,
because database snapshots and APIs change over time. A result should be treated
as acceptable when:

- the reconstructed corpus count is close to the published denominator or the
  loss is fully explained;
- top countries and institutions show stable rank-order agreement;
- large discrepancies are traced to explicit source differences;
- the tool emits reproducible logs and comparison tables for every mismatch.

## Benchmark Execution Order

1. Yan & Wang, 2023: first benchmark because the corpus is smaller and the
   reported outputs are directly aligned with current tool capabilities.
2. Baminiwatta & Solangaarachchi, 2021: second benchmark because it adds
   collaboration-network validation at medium scale.
3. Basilio et al., 2022: third benchmark because it tests multi-source corpus
   reconstruction and larger-scale author, country, and institution outputs.

## Role of the Prior Stress-Test Corpus

The prior closed DOI corpus should be described only as a stress-test case that
demonstrated pipeline operation on a large fixed DOI set. It can support
engineering validation, figure design, and runtime estimates, but it should not
be used as the primary evidence that the tool is scientifically valid.

## Deliverables Before the Strategy Call

1. Restructured Google Doc with the validation framing.
2. Benchmark-source table with the three candidate studies.
3. Short slide deck for the meeting.
4. Repository cleanup removing the obsolete corpus-specific manuscript assets.
5. Local validation plan committed with the codebase.

## Public Draft Boundaries

Public-facing drafts should mention Scopus and Google Scholar/SerpAPI only as
metadata-access dependencies. They should not include financing or payment
details until the group decides how access will be handled.

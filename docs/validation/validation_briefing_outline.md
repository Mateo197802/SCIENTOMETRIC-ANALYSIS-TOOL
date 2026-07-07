# Validation Briefing Outline

## Slide 1 - Reframed Project

**Title:** Scientometric Analysis Tool: validation-first publication strategy

Core message: the project is no longer framed as a new ML4Africa-specific
scientometric paper. The publication target is a tool-validation manuscript.

## Slide 2 - Why the Scope Changed

- A corpus-specific analysis is useful but does not prove that the tool is
  generally reliable.
- A validation manuscript needs external reference results.
- Published scientometric studies provide peer-reviewed targets for
  replication.

## Slide 3 - Validation Claim

The tool should reproduce comparable document counts, country and institutional
patterns, authorship-position summaries, and bibliometric indicators when given
the same corpus-construction rules used in published studies.

## Slide 4 - Benchmark Candidates

| Study | Count | Main validation target |
|---|---:|---|
| Yan & Wang, 2023 | 2,217 | countries, institutions, authors, cited papers |
| Baminiwatta & Solangaarachchi, 2021 | 16,581 | collaboration and citation-network patterns |
| Basilio et al., 2022 | 23,494 analyzed | authors, countries, institutions, multi-source corpus |

## Slide 5 - Tool Workflow

Benchmark query or DOI set -> DOI-first input table -> OpenAlex/PubMed/Semantic
Scholar/ORCID/Genderize/Azure OpenAI -> master author-paper table -> DOI and
CSV/JSON validation -> benchmark comparison tables.

## Slide 6 - What Will Be Compared

- final document count;
- DOI reconciliation;
- country and institutional distributions;
- productive-author overlap;
- authorship-position and corresponding-author patterns;
- citation indicators where available;
- mismatch reasons by source and database coverage.

## Slide 7 - Role of the Prior Closed DOI Corpus

The prior processed corpus remains useful as a stress-test and case-study
reference for runtime, scale, reconciliation, and figure design. It is not the
central scientific validation claim.

## Slide 8 - Decisions Needed

1. Confirm the first benchmark to reproduce.
2. Confirm which metadata sources are required for the first validation run.
3. Decide the minimum acceptable comparison table for a manuscript draft.
4. Assign benchmark extraction, API execution, manual audit, and writing tasks.

## Short Speaking Script

The revised direction is validation-first. We should not argue that one
unpublished corpus proves the tool. Instead, we should test the tool against
published scientometric studies that already report their corpus construction,
time range, filters, final counts, and bibliometric outputs. If the tool
reproduces those results within explainable database and API differences, then
we have a stronger, publishable methodological claim.

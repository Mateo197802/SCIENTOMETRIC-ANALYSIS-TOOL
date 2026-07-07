# Scientometric Tool Validation Briefing - Speaker Notes

## Slide 1

The revised direction is validation-first. The manuscript should not be framed
as a new ML4Africa-specific analysis. It should be framed as a tool-validation
paper.

## Slide 2

The reason is methodological. A single unpublished corpus is useful for testing
the engineering pipeline, but it cannot prove that the tool reproduces accepted
scientometric results. Published benchmarks solve that problem.

## Slide 3

The validation claim is simple: if we give the tool the same corpus rules used
in published studies, it should reproduce comparable counts, country patterns,
affiliation patterns, authorship signals, and citation indicators.

## Slide 4

The first three candidate benchmarks are Yan and Wang 2023, Baminiwatta and
Solangaarachchi 2021, and Basilio et al. 2022. I recommend starting with Yan
and Wang because it is smaller and closer to the current output structure.

## Slide 5

The methods section should expose the full workflow: input corpus definition,
DOI normalization, OpenAlex, PubMed, Semantic Scholar, ORCID, Genderize, Azure
OpenAI classification, CSV/JSON validation, DOI reconciliation, and benchmark
comparison.

## Slide 6

The deliverable is a reproducibility audit. We need document count comparison,
DOI reconciliation, country and institution rank overlap, author overlap where
available, citation comparison where possible, and a mismatch log.

## Slide 7

The prior closed DOI corpus should stay as a stress-test case. It helps show
that the tool runs at scale, but it is not the proof of scientific validity.

## Slide 8

The meeting decision is operational: choose the first benchmark, choose the
metadata sources, decide the minimum comparison table, and assign execution and
writing responsibilities.

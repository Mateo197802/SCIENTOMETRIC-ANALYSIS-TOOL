# June 30 Scope Reframe

## Decision

The project should be framed as a validation study of the Scientometric Analysis
Tool, not as a standalone manuscript about the ML4Africa corpus.

## Rationale

The tool needs evidence that it can reproduce results that have already passed
peer review through conventional scientometric workflows. A still-unpublished
corpus cannot serve as the primary validation benchmark because there is no
external reference result against which the pipeline can be compared.

## Revised Claim

When supplied with a reproducible corpus definition from an existing
scientometric study, the tool should reproduce comparable document counts,
affiliation patterns, authorship-position patterns, country-level summaries,
and bibliometric indicators within explainable differences caused by database
coverage, API access, deduplication rules, and metadata availability.

## Role of the Prior Closed DOI Corpus

The prior closed DOI corpus remains useful as an internal stress-test and
case-study reference because it has already exercised the pipeline at scale:

- closed DOI ingestion;
- metadata retrieval from OpenAlex, PubMed, Semantic Scholar, ORCID, Genderize,
  and Azure OpenAI;
- author-paper table construction;
- DOI reconciliation;
- CSV/JSON parity checks;
- figure generation and communication assets.

It should not be presented as the central manuscript claim.

## Immediate Outputs

1. A validation-source table listing two or three published scientometric
   studies with reproducible corpus construction.
2. A tool-validation plan describing how each benchmark will be reproduced.
3. A short presentation for the next strategy meeting.
4. A restructured working Google Doc that starts from validation rather than
   from corpus-specific findings.

## Access Dependencies

The validation run should check whether Scopus API entitlement and Google
Scholar access through SerpAPI are required for each benchmark. Public drafts
should describe these as access dependencies, not as funding decisions.

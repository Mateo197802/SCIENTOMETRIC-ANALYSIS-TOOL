# ML4Africa Scientometric Manuscript Design

## Objective

Produce a complete, journal-neutral original research manuscript in academic
English from the audited ML4Africa scientometric outputs. The manuscript will
foreground the scientific findings on geographic collaboration, authorship
leadership, and bibliometric impact. The Scientometric Analysis Tool will be
reported as the reproducible methodological infrastructure that generated the
author-level dataset.

The final deliverables are:

1. an editable Microsoft Word manuscript;
2. a matching local PDF used for visual quality assurance;
3. original manuscript figures and supplementary tables;
4. a verified bibliography with persistent identifiers;
5. an uploaded copy in the user-provided Word Online document.

## Approved Editorial Decisions

- Language: academic English.
- Article type: original observational scientometric research.
- Editorial positioning: findings first.
- Journal targeting: journal-neutral.
- Main analytical domains: collaboration, leadership, and bibliometric impact.
- Supplementary domains: name-inferred gender and LLM-inferred disciplinary
  profile.
- Approved title:

  **Geographic Patterns of Scientific Leadership and Bibliometric Impact in
  the ML4Africa Research Corpus**

## Corpus Definition and Scope

The study population is a closed list of 1,158 DOI values supplied by the
ML4Africa team led by Leo Celi. The manuscript must call this the "ML4Africa
closed DOI corpus" or equivalent language.

The manuscript must not claim that:

- the corpus is a systematic review;
- the corpus is an exhaustive census of African ML4H research;
- all included studies were identified through a reproducible database search;
- affiliation country represents nationality, ethnicity, origin, or residence.

The observed publication years extend from 1974 through 2025. The final
manuscript will report the distribution by year and explain that corpus
eligibility was determined upstream by the ML4Africa team. No selection
criteria or search strategy will be fabricated.

## Central Research Questions

1. What proportion of papers in the ML4Africa closed DOI corpus contain only
   African affiliations, mixed African and outside-African affiliations, no
   detected African affiliation, or only unknown affiliations?
2. In mixed Africa-outside collaborations, how often are first, last, and
   corresponding authorship positions occupied by African-affiliated,
   outside-African-affiliated, shared-region, or unknown-affiliation authors?
3. How do OpenAlex author-level H-index distributions differ descriptively
   between African and outside-African publication-time affiliations?
4. How do collaboration volume, leadership participation, and H-index
   distributions vary across affiliation countries?

The study is descriptive. It will not infer causality, individual nationality,
research extraction, migration, or inequitable intent from authorship position
or bibliometric indicators.

## Manuscript Architecture

### Title Page

- Approved title.
- Article type: Original Research.
- Running title: `Scientific leadership in the ML4Africa corpus`.
- Author names, order, affiliations, corresponding author, and ORCID values
  will not be invented. The draft will contain a clearly separated authorship
  confirmation field for completion by the study team.

### Structured Abstract

Use the headings:

- Background
- Methods
- Results
- Conclusions

The abstract will include the audited corpus size, author-paper record count,
distinct OpenAlex author count, collaboration composition, mixed-collaboration
leadership percentages, and regional H-index medians. Conclusions will remain
descriptive and avoid causal or normative overstatement.

### Introduction

The introduction will proceed from broad to specific:

1. expansion of machine learning for health and the importance of locally
   embedded scientific capacity;
2. geographic concentration of research resources and bibliometric visibility;
3. authorship position and corresponding authorship as imperfect but useful
   indicators of scientific leadership;
4. limitations of conventional citation metrics and affiliation-based
   geographic inference;
5. the evidence gap addressed by an author-level analysis of the ML4Africa
   corpus;
6. explicit study objective and research questions.

### Methods

#### Study Design

Describe a cross-sectional observational scientometric analysis of a closed DOI
corpus. State the extraction and analysis date because author-level citation
metrics can change over time.

#### Data Source and Eligibility

Report that the 1,158 DOI values were supplied by the ML4Africa team. State that
upstream corpus construction was outside the present analysis and that this
study did not reproduce a literature search.

#### Scientometric Analysis Tool

Document the executed pipeline in sufficient detail for reproducibility:

```text
Closed DOI list
  -> OpenAlex work and author profiles
  -> PubMed metadata and author reconciliation
  -> Semantic Scholar metadata and author reconciliation
  -> identifier/name consolidation
  -> ORCID employment enrichment
  -> Genderize name-based inference
  -> Azure OpenAI disciplinary classification
  -> 35-column author-paper master table
  -> validated CSV/JSON parity
  -> DOI reconciliation
  -> analytical tables and figures
```

Scopus and Google Scholar modules exist in the codebase but were disabled for
the completed corpus and must not be represented as contributing data sources
to the reported results.

#### Variables Extracted

Group the 35 master-table fields by provenance:

- Paper identity and publication metadata: title, DOI, year, open-access
  status, and funding.
- Authorship: display name, position, corresponding-author flag, affiliation,
  affiliation country, OpenAlex author ID, and ORCID.
- OpenAlex author metrics: works count, citations, H-index, i10-index,
  two-year mean citedness, topics, primary topic, and keywords.
- PubMed: PMID, MeSH terms, funding, matched author name, and affiliation.
- Semantic Scholar: influential citation count, author identity fields,
  H-index, and citation count. Citation-context coverage is zero and this field
  will not be analyzed.
- ORCID: latest returned employment summary.
- Enrichment: name-inferred gender and LLM-inferred disciplinary profile.

A supplementary variable dictionary will define every field, source, unit of
analysis, missing-value sentinel, and analytical use.

#### Author Reconciliation and Deduplication

Report the two distinct reconciliation layers accurately:

1. Cross-source author matching uses persistent identifiers where available,
   primarily ORCID and Scopus identifiers.
2. The consolidation stage normalizes names and merges exact, contained, or
   same-surname/first-initial variants within a paper.

For downstream distinct-person estimates, valid OpenAlex author IDs are the
primary identity key. Documented fallback records use normalized author names.
The limitations of homonyms, name changes, transliteration, and incomplete
identifiers will be explicit.

#### Geographic Classification

Geography is based on `GEO_COUNTRY_OA`, representing the first
publication-time institution returned for the OpenAlex authorship or an
authorship-level country fallback. ISO country codes are classified using the
repository's explicit African-country set.

At DOI level, mutually exclusive collaboration categories are:

- Africa-only known affiliations;
- mixed Africa and outside-Africa affiliations;
- no African affiliation detected;
- unknown affiliations only.

These categories describe observed affiliations, not researcher origin.

#### Leadership Measures

For the 499 mixed-collaboration DOI values, first, last, and corresponding
authorship are summarized using DOI-level denominators.

- First and last authorship derive from OpenAlex author position.
- Corresponding authorship derives from the OpenAlex corresponding-author flag.
- A paper can have corresponding authors from both geographic regions.
- Missing or unknown affiliation evidence is retained as an explicit category.

Country-specific leadership percentages use the number of mixed papers in
which each African affiliation country appears as the denominator.

#### Bibliometric Impact

OpenAlex H-index, citation count, and works count are author-profile metrics
observed at extraction time. Regional summaries use one observation per
distinct author and affiliation region. Country summaries use one observation
per distinct author and affiliation country. An author associated with more
than one region or country can contribute once to each relevant stratum.

Report medians and interquartile ranges. Interpret comparisons descriptively;
do not attribute observed differences causally to geography.

#### Secondary and Supplementary Measures

- `GENDER` is inferred from first names using Genderize with a minimum
  probability threshold of 0.80. It is not self-identified gender and will not
  appear as a primary finding.
- `PROFILE_CLASSIFICATION` is generated by Azure OpenAI at temperature 0 using
  a fixed taxonomy and author-level metadata. It remains an automated
  classification requiring manual validation.

Both analyses will be placed in the supplement with explicit validity limits.

#### Data Validation and Reproducibility

Document:

- exact CSV/JSON row and schema parity;
- 1,158 of 1,158 input DOI values represented in the final output;
- 7,361 author-paper records;
- 5,675 distinct valid OpenAlex author IDs;
- deterministic analytical exports;
- version-controlled source code and tests;
- machine-readable source tables underlying every figure.

#### Statistical Analysis

The primary analysis is descriptive:

- counts and percentages at DOI level;
- medians and interquartile ranges for skewed bibliometric variables;
- country selection for visualization based on prespecified sample-size
  thresholds, not outcome magnitude;
- percentages rounded to one decimal place.

No causal model or unplanned null-hypothesis significance test will be added to
the main manuscript. Any later inferential analysis requires a separate
protocol amendment.

### Results

Use the following order:

1. Corpus integrity, publication-year distribution, and metadata coverage.
2. DOI-level collaboration composition.
3. Regional first, last, and corresponding authorship in mixed collaborations.
4. Country-level leadership participation in mixed collaborations.
5. Regional bibliometric impact distributions.
6. Country-level bibliometric impact distributions.

Every numerical statement must trace to a committed CSV or JSON output.

### Discussion

The discussion will include:

1. concise summary of principal findings;
2. comparison with prior research on global-health authorship, African research
   leadership, ML4H capacity, and citation inequality;
3. interpretation of the difference between collaboration presence and
   leadership participation;
4. implications for ML4Africa research governance, capacity strengthening,
   equitable partnership design, and transparent contribution reporting;
5. limitations of a supplied closed corpus, affiliation-based geography,
   authorship-position proxies, dynamic bibliometric metrics, database
   coverage, author disambiguation, and automated supplementary classifications;
6. recommendations for prospective validation and longitudinal analyses.

The term "parachute research" may appear only as a literature concept and must
not be assigned to individual papers or countries from authorship position
alone.

### Conclusion

Restate only what the data directly support: the observed geographic structure
of collaboration, leadership participation, and bibliometric impact within the
ML4Africa closed DOI corpus.

### End Matter

Include:

- acknowledgments;
- funding statement;
- conflicts of interest;
- author contributions using CRediT roles;
- data availability;
- code availability;
- ethics statement explaining that the study uses public bibliographic
  metadata and no participant-level health data;
- references.

Unknown consortium-specific declarations will be grouped into a clearly marked
editorial completion section rather than fabricated.

## Figure and Table Plan

### Main Figures

1. **Study workflow and data architecture.** Original diagram showing the
   closed DOI input, executed APIs, author reconciliation, master-table
   construction, validation, and analysis.
2. **Corpus and collaboration composition.** Composite of corpus overview,
   metadata coverage, and DOI-level collaboration categories.
3. **Leadership in mixed collaborations.** Composite of regional leadership
   roles and African-country role participation.
4. **Regional bibliometric impact.** OpenAlex H-index distributions for African
   and outside-African affiliation strata.
5. **Country-level bibliometric impact.** Median and interquartile-range
   H-index plot for selected countries.

### Main Tables

1. Corpus characteristics and field coverage.
2. Collaboration and leadership results with explicit denominators.
3. Regional bibliometric summaries.

### Supplementary Material

- Complete variable dictionary.
- Full country participation table.
- Full country leadership table.
- Name-inferred gender analysis.
- LLM-inferred disciplinary-profile analysis.
- DOI reconciliation and metadata coverage.
- Technical API and missingness notes.
- Reproducibility information and software versions.

## External Literature and Citation Standards

The evidence search will prioritize:

1. peer-reviewed primary studies on global-health authorship and African
   scientific leadership;
2. peer-reviewed research on machine learning for health capacity and
   geographic representation;
3. methodological papers for OpenAlex, Semantic Scholar, ORCID, PubMed, and
   name-based gender inference;
4. authoritative API documentation when no peer-reviewed methods source
   describes a specific field;
5. reporting guidance relevant to bibliometric and observational studies.

References must be verified against the publisher, PubMed, Crossref, or DOI
record. The manuscript will use numbered Vancouver-style citations for broad
biomedical compatibility.

Figures from third-party articles will not be copied unless they are explicitly
openly licensed and scientifically necessary. The default is to create original
schematics and figures, cite the supporting literature, and avoid copyright
risk.

## Word Document Design

- Microsoft Word `.docx`, US Letter page size.
- Single-column manuscript layout.
- 1-inch margins.
- Readable serif body font with a restrained sans-serif heading hierarchy.
- Continuous line numbering where supported.
- Page numbers in the footer.
- Figures placed after first mention for the working draft, with full legends.
- Tables created as editable Word tables, not raster images.
- References formatted with hanging indents and live DOI hyperlinks.
- Supplement begins on a new page with independent figure/table numbering.

The manuscript will be rendered to PDF and every page visually inspected for
clipping, broken tables, low-resolution figures, orphan headings, and citation
formatting defects before upload.

## Word Online Delivery

After local validation, the final `.docx` will be uploaded to the user-provided
Yachay Tech SharePoint/Word Online location. The uploaded document will be
opened and checked for:

- successful file replacement or insertion;
- preserved headings, tables, figures, and references;
- correct title;
- visible page count and final section;
- no upload or synchronization error.

The existing shared document will not be deleted. If Word Online requires a
choice between replacing content and uploading a separate file, the safer
non-destructive option will be used unless the page clearly identifies the
linked file as the intended manuscript target.

## Acceptance Criteria

The work is complete when:

- the manuscript uses the approved title and findings-first structure;
- all primary numerical claims trace to committed analysis outputs;
- no unsupported corpus-selection claim is present;
- the executed and disabled data sources are distinguished accurately;
- collaboration and leadership denominators are explicit;
- affiliation is never conflated with nationality or origin;
- gender and disciplinary profile remain supplementary;
- references are verified and contain DOI/URL identifiers where available;
- all main figures are original and publication-ready;
- the Word document renders without visual defects;
- the final document is present and readable in the specified Word Online
  location.

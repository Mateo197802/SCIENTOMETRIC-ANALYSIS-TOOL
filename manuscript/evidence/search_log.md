# Literature Search and Verification Log

## Scope

The evidence search was designed to support a journal-neutral original
scientometric manuscript based on a closed ML4Africa DOI corpus. It was not a
systematic review and was not used to redefine or expand the supplied corpus.
Searches focused on directly relevant empirical authorship studies,
bibliometric-method papers, reporting guidance, and official documentation for
the executed data sources.

## Search date

All retained records were checked on 2026-06-14.

## Search lanes and queries

| Lane | Query examples | Sources searched | Retention rule |
|---|---|---|---|
| African research participation and leadership | `"sub-Saharan Africa" authorship first last bibliometric`; `Africa global health authorship representation local author` | PubMed, publisher sites, Crossref | Retain primary bibliometric studies with explicit affiliation and byline-position methods. |
| AI/ML for health in Africa | `"artificial intelligence" healthcare Africa bibliometric authorship institutions` | Springer, Crossref | Retain a directly relevant African AI-for-health landscape analysis for contextual comparison. |
| Leadership interpretation | `first last corresponding authorship leadership proxy global health`; `ICMJE author order contribution` | PubMed, ICMJE | Retain empirical studies using byline position and official guidance showing that position is an incomplete contribution proxy. |
| Bibliometric indicators | `h-index advantages limitations micro level`; `Hirsch h-index original paper` | Crossref, publisher records, PubMed | Retain the original H-index proposal and a comparative limitations paper. |
| Scholarly data sources | `OpenAlex cite paper official`; `PubMed about official`; `Semantic Scholar corpus API paper`; `ORCID persistent identifier official` | Official documentation, arXiv, ACL Anthology, NCBI, ORCID | Retain the canonical resource paper or official technical documentation used by the pipeline. |
| Name-based gender inference | `Genderize accuracy diverse nationality`; `name-to-gender inference services validation` | PLOS, PubMed Central, Crossref | Retain validation studies that quantify performance variation and state construct limitations. |
| Reporting | `STROBE cross-sectional reporting guideline`; `ICMJE manuscript references authorship` | Publisher records, ICMJE | Retain established reporting and authorship guidance. |

## Verification procedure

1. DOI metadata were resolved through the Crossref REST API.
2. Biomedical study titles, abstracts, publication details, and PMIDs were
   checked through NCBI PubMed E-utilities.
3. Publisher pages were used for online-first versus issue-year differences,
   article numbers, and full author lists when needed.
4. OpenAlex, PubMed, ORCID, Semantic Scholar, and ICMJE claims were checked
   against their official documentation or canonical resource papers.
5. Claims were recorded as bounded paraphrases in `evidence_matrix.csv`;
   abstract wording was not copied into the manuscript.

## Important decisions

- The Kondo article was published online in 2023 and assigned to volume 5 in
  2025. The Vancouver reference uses the issue year, 2025.
- The term `authorship parasitism` is retained only as the title and defined
  construct of Rees et al. The present analysis does not observe study sites
  and therefore cannot assign that label to any paper, author, or country.
- First, last, and corresponding authorship are treated as observable byline
  positions and imperfect leadership signals, not direct measures of
  contribution, control, seniority, or research ethics.
- Geographic categories represent institutional affiliation evidence at the
  publication level. They do not represent nationality, ethnicity, origin, or
  residence.
- Name-based gender and LLM-based professional-profile variables are
  exploratory supplementary analyses only.

## Excluded or deprioritized records

- Narrative commentaries without reproducible authorship data were excluded.
- Near-duplicate single-journal studies were deprioritized when they did not
  add a distinct specialty, design, or limitation.
- Papers that inferred extractive practice solely from author order were not
  used to classify this corpus.
- Commercial database marketing pages were not used when a canonical paper or
  official technical document was available.
- Scopus and Google Scholar documentation was not retained because those
  integrations were disabled for the completed analytical run.

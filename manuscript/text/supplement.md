# Supplementary Material

## Supplementary Methods

### Complete master-table schema

The final master table contains 35 fields spanning paper metadata, authorship, institutional affiliation, bibliometric indicators, cross-source identifiers, ORCID employment, name-inferred gender, and LLM-inferred professional profile. Supplementary Table S1 defines the source, analytical level, type, configured missing-value sentinels, analytical use, and principal limitation for every field.

{{SUPPLEMENTARY_TABLE:S1}}

**Supplementary Table S1. Variable dictionary for the 35-field master author-paper table.** Primary variables contributed directly to the main collaboration, leadership, or bibliometric analyses. Supplementary variables were retained for traceability, future analyses, or explicitly exploratory classifications.

### Missing-value handling and field coverage

The analysis treated empty values and configured sentinels such as `No data`, `N/A`, `UNKNOWN`, `NOT_FOUND`, `NO_ORCID`, `NO_ID`, `SKIP`, and source-specific fallback values as missing where appropriate. Zero values in numerical source fields were preserved because the executed pipeline used zero both as a valid value and, in some fallback records, as an unavailable default. This ambiguity is reported as a limitation and is one reason the main impact analysis prioritized valid OpenAlex author identities.

Supplementary Table S2 reports field coverage across 7,361 author-paper records. Citation-context text from Semantic Scholar was unpopulated in the completed run. PubMed author-name and affiliation matches were limited because the strict cross-source matcher required ORCID for PubMed linkage.

{{SUPPLEMENTARY_TABLE:S2}}

**Supplementary Table S2. Field coverage in the final master table.** Coverage excludes configured missing-value sentinels. A populated field is not equivalent to independent validation.

### DOI reconciliation and publication years

DOI normalization removed `https://doi.org/`, `http://doi.org/`, and `doi:` prefixes and converted values to lowercase. Every one of the 1,158 input DOI values was found in the final output. Publication years were summarized from one row per normalized DOI.

{{SUPPLEMENTARY_TABLE:S3}}

**Supplementary Table S3. Publication-year distribution for distinct DOI values.** The closed corpus included single records dated 1974 and 2005, three records dated 2022, and 1,153 records dated 2023-2025. No post hoc date exclusion was applied.

### Name-inferred gender

The pipeline excluded likely institutional authors when the consolidated name matched any of the case-insensitive tokens `group`, `network`, `study`, `collaborators`, `team`, `consortium`, or `committee`. For other records, the first whitespace-delimited token was lowercased and stripped to ASCII letters. Genderize was queried with the normalized first name and, when available, the two-letter affiliation-country code. Predictions were accepted when probability was at least 0.80.

Accepted predictions were cached in memory by normalized first name during the run. Because the cache key did not include country, a previously accepted name prediction could be reused for a later record with a different country context. The output schema retained the categorical result but did not retain the API probability. These design choices limit retrospective threshold auditing.

The `GENDER` variable is a binary name-inferred label with `Unknown` and `N/A` states. It is not self-identified gender, legal sex, biological sex, or a validated individual attribute. It cannot represent nonbinary identities in the implemented schema. Aggregate findings therefore remain exploratory.

### LLM-inferred professional profile

Azure OpenAI GPT-4o assigned one category from the following taxonomy: `CLINICAL`, `COMPUTER_SCIENCE`, `BIOINFORMATICS`, `HYBRID_MED_TECH`, `BASIC_LIFE_SCIENCES`, `PHYSICAL_SCIENCES`, `ENGINEERING_MATH`, `SOCIAL_SCIENCES_HUMANITIES`, `OTHER_SCIENCES`, or `UNKNOWN`. The prompt prioritized author-level affiliation, ORCID employment, OpenAlex lifetime topics and concepts, and PubMed affiliation; paper MeSH terms were labeled as secondary context. Missing-value sentinels were explicitly excluded from inference. The API call used temperature 0.0 and required the output format `CATEGORY | GENDER`.

The analytical `BASE_PROFILE` variable used only the category token before the separator. Categories were aggregated after deduplicating author identities within affiliation region and selecting the modal category when repeated records disagreed. The taxonomy and individual classifications were not independently evaluated by domain experts. They should be interpreted as LLM-inferred metadata, not ground truth.

### Country-level analyses

Supplementary Table S4 contains the full country participation table for countries appearing in at least five papers. Paper counts are distinct DOI values. Author-paper records and distinct author keys use different units and should not be compared as if they were equivalent.

{{SUPPLEMENTARY_TABLE:S4}}

**Supplementary Table S4. Country participation and role counts.** Countries represent publication-time affiliation evidence. A paper can contribute to multiple country rows.

Supplementary Table S5 reports African-country leadership participation within mixed collaborations. The denominator for each country is the number of mixed papers containing at least one author affiliated with that country. First-, last-, and corresponding-author percentages are independent and can overlap.

{{SUPPLEMENTARY_TABLE:S5}}

**Supplementary Table S5. African-country leadership participation in mixed collaborations.**

Supplementary Table S6 contains H-index distributions for all countries meeting the configured minimum author threshold. One observation was retained per author-country pair.

{{SUPPLEMENTARY_TABLE:S6}}

**Supplementary Table S6. OpenAlex H-index distributions by affiliation country.**

### Software and validation

The analysis and manuscript assets were produced in Python 3.12 using pandas, matplotlib, Pillow, and python-docx. Repository tests validate master-output parity, schema completeness, DOI reconciliation, missing-value handling, paper-level denominators, author identity keys, regional and country deduplication, deterministic manuscript tables, figure existence, image readability, SVG timestamp removal, and exact 35-variable dictionary coverage.

## Supplementary Results

### Name-inferred gender composition

Among author-paper records with a known name-inferred binary label, female labels represented 33.7% of African-affiliation records and 34.3% of outside-African-affiliation records. For African affiliations, female labels represented 39.1% of known first-author records, 26.3% of known last-author records, and 35.8% of known corresponding-author records. For outside-African affiliations, the respective values were 38.7%, 22.7%, and 29.3%.

{{SUPPLEMENTARY_TABLE:S7}}

**Supplementary Table S7. Exploratory name-inferred gender summaries by affiliation region and role.** Denominators include only records with a known binary name-inferred label. Results do not represent self-identified gender.

### LLM-inferred professional-profile composition

After deduplication within affiliation region, `COMPUTER_SCIENCE` was the largest LLM-inferred category among African-affiliated authors (1,506; 56.5%), followed by `HYBRID_MED_TECH` (516; 19.4%), `CLINICAL` (193; 7.2%), and `BIOINFORMATICS` (124; 4.7%). Among outside-African-affiliated authors, `COMPUTER_SCIENCE` accounted for 1,070 (40.2%), `HYBRID_MED_TECH` for 619 (23.3%), `CLINICAL` for 353 (13.3%), `SOCIAL_SCIENCES_HUMANITIES` for 249 (9.4%), and `BIOINFORMATICS` for 139 (5.2%).

{{SUPPLEMENTARY_TABLE:S8}}

**Supplementary Table S8. Exploratory LLM-inferred professional-profile composition by affiliation region.** Labels were generated automatically at temperature 0.0 from available professional metadata and were not independently expert validated.

## Supplementary Limitations

1. Name inference is culturally and linguistically variable, and the implemented binary schema cannot represent the full range of gender identities.
2. The in-memory first-name cache did not condition reuse on country, and API probabilities were not retained in the final schema.
3. LLM temperature 0.0 improves repeatability for a fixed model deployment but does not guarantee validity, invariance across model versions, or freedom from systematic bias.
4. Institutional affiliation and professional topics can be missing, stale, or ambiguous, directly affecting profile classification.
5. Country participation is based on one retained OpenAlex institution or authorship-country fallback and can underrepresent multiple affiliations.
6. The source corpus was closed and supplied by the research team; supplementary findings should not be generalized to the full African machine-learning-for-health literature.

# Geographic Patterns of Scientific Leadership and Bibliometric Impact in the ML4Africa Research Corpus

**Authors:** [Editorial completion required: confirm the full author list, order, degrees, and group authorship.]

**Affiliations:** [Editorial completion required: confirm institutional affiliations for all authors.]

**Corresponding author:** [Editorial completion required: confirm corresponding author name, postal address, and email.]

## Abstract

### Background

Machine learning for health research involving African institutions is expanding, but aggregate publication counts do not show how collaboration, prominent byline positions, and researcher-level bibliometric indicators are geographically distributed. We mapped these dimensions in a closed corpus supplied by the ML4Africa research team.

### Methods

We conducted a descriptive scientometric analysis of 1,158 DOI values supplied as a fixed corpus rather than identified through a systematic literature search. The Scientometric Analysis Tool retrieved and reconciled metadata from OpenAlex, PubMed, Semantic Scholar, and ORCID; performed supplementary enrichment using Genderize and Azure OpenAI; and produced a validated 35-field author-paper table. Scopus and Google Scholar integrations were implemented but disabled for the completed run. Publication-time institutional country evidence was classified as Africa, outside Africa, or unknown. Papers were categorized as Africa-only, mixed Africa/outside-Africa, no African affiliation detected, or unknown-only. First, last, and corresponding authorship were summarized within mixed collaborations. OpenAlex H-index, citation, and works-count distributions were described after person-level deduplication.

### Results

All 1,158 DOI values were reconciled, yielding 7,361 author-paper records and 5,675 distinct valid OpenAlex author identifiers. The corpus contained 533 Africa-only papers (46.1%), 499 mixed-collaboration papers (43.1%), 93 papers with no African affiliation detected (8.0%), and 33 unknown-only papers (2.8%). Within mixed collaborations, African-only affiliations accounted for 40.9% of first-author positions, 49.9% of last-author positions, and 37.9% of corresponding-author positions. Outside-African-only affiliations accounted for 54.3%, 46.5%, and 51.9%, respectively; 6.8% of mixed papers had corresponding authors from both regions. The median OpenAlex H-index was 5 (interquartile range [IQR], 2-11) among 2,663 African-affiliated authors and 13 (IQR, 5-29) among 2,658 outside-African-affiliated authors.

### Conclusions

The ML4Africa corpus combines substantial Africa-only production with extensive international collaboration. Mixed papers showed near balance in last authorship but lower African representation in first and corresponding authorship, alongside a marked descriptive difference in cumulative bibliometric indicators. These patterns identify measurable areas for longitudinal monitoring; they do not by themselves establish contribution, seniority, research quality, or inequitable practice.

**Keywords:** scientometrics; machine learning for health; Africa; authorship; research collaboration; bibliometric impact; OpenAlex

## Introduction

Machine learning and artificial intelligence are increasingly applied to health research involving African populations, institutions, and data environments. A broad bibliometric review of artificial intelligence for healthcare in Africa identified rapid growth, substantial international participation, and concentration of output among a limited group of countries and institutions, with South Africa occupying a prominent position within the continent [1]. Publication growth, however, is only one dimension of research capacity. The distribution of authorship, institutional affiliation, and cumulative scholarly visibility can reveal additional features of how a research field is organized.

Authorship order is often used in bibliometric studies as an observable, if imperfect, indicator of scientific leadership and career visibility. Analyses of health research concerning sub-Saharan Africa have reported that local representation can decline in first or last positions when collaborations include institutions from high-income settings [2,3]. These findings have motivated calls to examine not only whether African-affiliated researchers appear in a byline, but also where they appear and whether representation changes across collaboration types.

The empirical literature also demonstrates that no single authorship pattern characterizes African or global-health research. Studies have reported papers with no author affiliated with the country where the research was conducted [4], increasing African first and last authorship within a capacity-building funder portfolio [5], persistent underrepresentation in prominent positions within individual journals [6], and inequalities within long-standing international collaborations [7]. Similar patterns have been documented in a UK-based global-health research group [8], global oncology [9], and global emergency medicine [10]. These studies differ in discipline, corpus construction, geographic definition, and time period, which limits direct comparison and supports corpus-specific analysis.

Byline position cannot establish an individual's contribution, authority, or accountability. The International Committee of Medical Journal Editors defines authorship through contribution, critical manuscript participation, approval, and accountability, and notes that author-order conventions are determined by author groups [11]. First, last, and corresponding positions are therefore treated here as leadership signals that require contextual interpretation rather than direct measurements of intellectual ownership or research equity.

The ML4Africa team assembled a closed set of DOI values related to its research-mapping objectives. A closed corpus provides a defined analytical denominator but is not equivalent to an exhaustive field search. Before the present analysis, the project developed the Scientometric Analysis Tool to expand each DOI into linked paper, author, affiliation, identifier, and bibliometric records while preserving a reproducible paper-level relationship.

This study aimed to describe geographic patterns of collaboration, prominent authorship positions, and researcher-level bibliometric impact within the supplied ML4Africa corpus. The research questions were: (1) what proportion of papers contained only African affiliations, mixed African and outside-African affiliations, no detected African affiliation, or only unknown affiliations; (2) how were first, last, and corresponding authorship distributed within mixed collaborations; and (3) how did OpenAlex bibliometric indicators vary between affiliation regions and among the countries most represented in the author-level data?

## Methods

### Study design

We performed a descriptive cross-sectional scientometric analysis of a fixed DOI corpus. The analytical workflow and reporting were structured to make the corpus definition, units of analysis, variables, missingness, transformations, and limitations explicit. No causal estimand was specified and no hypothesis-testing framework was applied.

### Corpus and unit of analysis

The source file contained 1,158 unique DOI values supplied directly by the ML4Africa research team. The DOI list was treated as an immutable input set. It was not generated by the Scientometric Analysis Tool, and no claims are made that it exhaustively represents machine learning for health research in Africa.

Three units were distinguished. A **paper** was a unique normalized DOI. An **author-paper record** was one consolidated author linked to one DOI. A **distinct author** was defined for downstream analysis using a valid OpenAlex author identifier when available; otherwise, a normalized author-name key was used. Country-level impact analyses used one observation per author-country pair, whereas regional impact analyses used one observation per author-region pair.

### Scientometric Analysis Tool

The pipeline processed each DOI sequentially with checkpoint/resume support. OpenAlex formed the primary paper and authorship layer. PubMed and Semantic Scholar supplied complementary biomedical and scholarly metadata and could add source-fallback author records when persistent-identifier matching did not connect a source author to an OpenAlex authorship. A within-paper compressor then merged likely duplicate author records. ORCID employment information and supplementary automated classifications were added after consolidation. The final output was written to CSV and JSON with a fixed 35-column schema.

The completed run used OpenAlex, PubMed, Semantic Scholar, ORCID, Genderize, and Azure OpenAI. Scopus and Google Scholar modules existed in the codebase but were disabled for the completed corpus run and did not contribute to the reported results.

{{FIGURE:1}}

**Figure 1. Scientometric Analysis Tool workflow.** The fixed ML4Africa DOI corpus was expanded through executed scholarly metadata sources, identifier reconciliation, within-paper consolidation, supplementary enrichment, schema-controlled export, and DOI/format validation. The final author-paper table contained 7,361 records and 5,675 distinct valid OpenAlex author identifiers. Scopus and Google Scholar integrations were not used for the completed run.

### Data-source APIs and extracted variables

OpenAlex is an open scholarly knowledge graph connecting works, authors, institutions, and related entities through a REST API and downloadable data [12]. For each DOI, the pipeline retained paper title, publication year, open-access status, funder metadata, author display name, author position, corresponding-author indicator, first listed institution, evidenced country, OpenAlex author identifier, works count, citation count, H-index, i10-index, two-year mean citedness, topics, primary topic, and concepts.

PubMed, maintained by the National Library of Medicine, was queried by DOI to retrieve PMID, Medical Subject Headings, funding agencies, author names, affiliations, and available ORCID identifiers [13]. Semantic Scholar supplied paper-level influential-citation counts and author-level identifiers and bibliometric fields; its scholarly data infrastructure is described in the S2ORC resource paper [14]. The public ORCID API was queried for the most recent visible employment organization and department associated with a consolidated ORCID iD. ORCID iDs are persistent person identifiers, although downstream records may be absent, incomplete, private, or unauthenticated [15].

The complete variable dictionary, source, level, missing-value sentinels, analytical use, and limitations are provided in Supplementary Table S1.

### Author reconciliation and deduplication

Cross-source author matching prioritized persistent identifiers. PubMed records were linked when ORCID matched the consolidated OpenAlex record. Semantic Scholar records were linked when ORCID or a Scopus identifier present in OpenAlex matched the external identifier returned by Semantic Scholar. Unmatched source authors could be retained as explicit `PubMed_Fallback` or `Semantic_Fallback` records rather than silently discarded.

After source retrieval, within-paper consolidation normalized names by removing diacritics, punctuation, case, and spacing. Records were merged when normalized full names were identical or contained one another, or when surname and first initial matched. This fallback increased retention across name variants but could merge different people with similar names. For downstream person-level analyses, the identity key was `oa:<OpenAlex ID>` for valid OpenAlex identifiers and `name:<normalized full name>` otherwise. Fallback source sentinels were not counted as valid OpenAlex identifiers.

### Geographic classification

For each OpenAlex authorship, the tool retained the first listed institution and its country code. If no institution was listed, the first country in the OpenAlex authorship-level country array was used. Country codes in a predefined African-country set were classified as **Africa**; other known codes were classified as **outside Africa**; missing or sentinel values were classified as **unknown**.

These categories represent publication-time institutional affiliation evidence. They do not measure nationality, ethnicity, country of origin, residence, study site, data source, or the location where the research was conducted. Multi-affiliated authors were represented by the first retained OpenAlex institution in the completed output.

### Collaboration and leadership outcomes

Each paper was assigned to one mutually exclusive collaboration category from the set of known and unknown author-region values:

- **Africa-only known affiliations:** all known affiliations were African.
- **Mixed Africa + outside:** at least one known African and one known outside-African affiliation.
- **No African affiliation detected:** all known affiliations were outside Africa.
- **Unknown affiliations only:** no known affiliation country was available.

Within the 499 mixed papers, first-author, last-author, and corresponding-author affiliations were summarized as Africa only, outside Africa only, both regions, or unknown only. Multiple corresponding authors could produce the both-regions category. Byline positions were interpreted as descriptive leadership signals and not as complete contribution measures [11].

Country participation was summarized using distinct DOI counts, author-paper records, distinct author keys, and counts of papers containing a first, last, or corresponding author affiliated with each country. Country-specific mixed-collaboration leadership percentages used, as denominator, mixed papers containing at least one author affiliated with that African country. Because role percentages were calculated independently, they could overlap.

### Bibliometric outcomes

Primary bibliometric outcomes were OpenAlex H-index, cumulative citation count, and cumulative works count retrieved from author profiles. The H-index combines output and citation information [16] but is strongly associated with publication volume and cumulative citations and should not be interpreted as a standalone measure of scientific quality [17].

Regional summaries retained one observation per author identity and affiliation region. Country summaries retained one observation per author identity and affiliation country. We reported sample size, median, and IQR. Figure 4 limited the visual x-axis to the 99th percentile to preserve readability; all available values contributed to the reported medians and quartiles.

### Supplementary automated classifications

Name-inferred gender and LLM-inferred professional profile were prespecified as exploratory supplementary variables. For non-institutional author names, Genderize was queried using the first normalized name token and the available two-letter affiliation-country code. Predictions with probability greater than or equal to 0.80 were accepted; other responses remained unknown. Institutional or consortium-like names were excluded using a regular expression. Accepted results were cached in memory by normalized first name during execution.

Name-based gender inference does not measure self-identified gender, cannot represent nonbinary identities in the implemented binary schema, and varies across naming systems and populations. Validation studies report high aggregate performance for some services but meaningful context-specific differences [18,19]. Accordingly, these outputs were analyzed only in aggregate and are not part of the primary findings.

Azure OpenAI GPT-4o assigned one professional-domain category from a fixed taxonomy using available author-level affiliations, ORCID employment, OpenAlex topics and concepts, and PubMed affiliation, with paper-level MeSH terms as secondary context. The call used temperature 0.0 and a rigid output format. The categories were clinical, computer science, bioinformatics, hybrid medical technology, basic life sciences, physical sciences, engineering/mathematics, social sciences/humanities, other sciences, or unknown. These labels were not independently expert validated and were restricted to the supplement.

### Data validation and reproducibility

The analysis loader required CSV and JSON row-count parity, identical column sets, and the complete expected 35-field schema. DOI values were normalized by removing DOI URL prefixes and converting to lowercase. Every input DOI was compared with the final output. Missing-value sentinels were explicitly treated as absent in coverage analyses. Numerical manuscript tables and all figures were generated from committed machine-readable outputs by deterministic Python scripts. Automated tests covered loading, DOI reconciliation, collaboration classification, identity keys, impact deduplication, country metrics, table generation, figure readability, and deterministic SVG output. Reporting explicitly addressed design, variables, data sources, bias, statistical methods, and limitations in line with relevant observational-reporting principles [20].

### Statistical analysis

Analyses were descriptive. Counts and percentages were reported for paper-level collaboration and leadership outcomes. Medians and IQRs were reported for skewed author-level bibliometric indicators. Percentages were calculated with explicit paper-level denominators and rounded to one decimal place. No p values, confidence intervals, regression models, or causal interpretations were produced for the primary analysis.

### Ethics

The analysis used publicly accessible scholarly metadata and did not involve recruitment, intervention, clinical records, or individual-level health data. Institutional ethics review was not sought. Automated gender and professional-profile outputs concern inferred attributes from public professional metadata; they were retained only for aggregate exploratory analysis, and individual classifications are not reported in the manuscript.

## Results

### Corpus characteristics

All 1,158 input DOI values were present in the final output. The 35-field master table contained 7,361 author-paper records and 5,675 distinct valid OpenAlex author identifiers. Publication years ranged from 1974 to 2025; 1,153 papers (99.6%) were dated 2023-2025, while single records were dated 1974 and 2005. These historical values were retained because the analysis honored the supplied closed corpus rather than applying post hoc date criteria.

Paper title, DOI, year, author name, corresponding-author indicator, and the principal OpenAlex author metrics were populated for all author-paper records. Author position was populated for 98.0%, OpenAlex author identifier for 96.7%, OpenAlex affiliation for 90.5%, affiliation country for 86.3%, consolidated ORCID for 66.9%, name-inferred gender for 86.1%, and LLM-inferred profile classification for 100%. Field-level coverage is reported in Supplementary Table S2.

{{TABLE:1}}

**Table 1. Corpus characteristics and metadata coverage.** Paper counts use distinct normalized DOI values. Author-paper records are not unique people. Coverage percentages use 7,361 author-paper records as denominator and treat configured missing-value sentinels as absent.

### Collaboration composition

Of the 1,158 papers, 533 (46.1%) contained only known African affiliations, 499 (43.1%) contained both African and outside-African affiliations, 93 (8.0%) had known affiliations only outside Africa, and 33 (2.8%) contained only unknown affiliations. Thus, 89.2% of the closed corpus was classified as either Africa-only or mixed collaboration.

{{FIGURE:2}}

**Figure 2. Corpus reconciliation, metadata coverage, and collaboration composition.** Panel A distinguishes DOI-level papers, author-paper records, and distinct valid OpenAlex author identifiers and reports selected field coverage. Panel B classifies all 1,158 papers from publication-time affiliation-country evidence. Geographic categories do not represent nationality or origin.

### Leadership patterns in mixed collaborations

Among the 499 mixed-collaboration papers, first authors were African-affiliated only in 204 papers (40.9%), outside-African-affiliated only in 271 (54.3%), and unknown in 24 (4.8%). Last authors were African-affiliated only in 249 papers (49.9%), outside-African-affiliated only in 232 (46.5%), and unknown in 18 (3.6%).

Corresponding authors were African-affiliated only in 189 mixed papers (37.9%), outside-African-affiliated only in 259 (51.9%), from both regions in 34 (6.8%), and unknown only in 17 (3.4%). The both-regions category was observable for corresponding authorship because a paper could identify multiple corresponding authors.

{{TABLE:2}}

**Table 2. Paper-level collaboration composition and leadership affiliation within mixed collaborations.** Collaboration composition uses all 1,158 papers. Leadership percentages use the 499 mixed-collaboration papers as denominator for each role.

### Country participation and mixed-collaboration leadership

Egypt was the most frequent African affiliation country in the author-level output, appearing in 344 papers and 995 author-paper records, followed by Nigeria (107 papers), Ethiopia (97), Morocco (92), Tunisia (92), South Africa (81), and Algeria (76). Country counts are participation measures and can exceed corpus totals when a paper contains authors from multiple countries.

Among mixed papers, Egypt had the largest country-specific denominator (173 papers). The proportion with an Egyptian-affiliated first author was 37.0%, with an Egyptian-affiliated last author 65.3%, and with an Egyptian-affiliated corresponding author 38.7%. Country-specific patterns varied substantially. For example, Tunisia had African-country participation in 62.5% of first-author, 66.7% of last-author, and 54.2% of corresponding-author positions among its 48 mixed papers. Ghana had corresponding-author participation in 73.9% of 23 mixed papers, whereas South Africa had first-author participation in 22.2%, last-author participation in 33.3%, and corresponding-author participation in 27.8% of 36 mixed papers. These estimates use different country-specific denominators and should not be interpreted as a ranking of research quality.

{{FIGURE:3}}

**Figure 3. Leadership affiliation in mixed collaborations.** Panel A reports role-level affiliation across all 499 mixed papers. Panel B reports African-country participation in each leadership role among mixed papers containing at least one author affiliated with that country; percentages are independent and can overlap. Country labels are affiliation-country codes.

### Regional bibliometric impact

After deduplication within affiliation region, 2,663 African-affiliated authors and 2,658 outside-African-affiliated authors contributed to the OpenAlex impact analysis. The median H-index was 5 (IQR, 2-11) in the African-affiliation stratum and 13 (IQR, 5-29) in the outside-African stratum. Median cumulative citation counts were 100 and 721, respectively, while median works counts were 16 and 53.

{{TABLE:3}}

**Table 3. OpenAlex bibliometric indicators by affiliation region.** One observation was retained per author identity and affiliation region. Values are descriptive author-profile metrics at extraction time.

{{FIGURE:4}}

**Figure 4. OpenAlex H-index distribution by affiliation region.** Boxes show the IQR and the internal line shows the median; points show author-region observations. The axis is limited at the 99th percentile for display, while all observations contributed to summary statistics. No causal inference or quality ranking is implied.

### Country-level bibliometric impact

Among the eight African affiliation countries selected by author sample size for Figure 5, median H-index ranged from 3.0 in Algeria to 10.0 in South Africa. Egypt, Morocco, Tunisia, and Ghana each had a median of 5.0; Ethiopia had a median of 4.0 and Nigeria 3.5. Among the eight selected outside-African affiliation countries, median H-index ranged from 7.0 in India to 29.0 in the Netherlands. Germany and Spain had medians of 28.0 and 26.0, respectively. IQRs were broad in several countries, demonstrating substantial within-country heterogeneity.

{{FIGURE:5}}

**Figure 5. OpenAlex H-index distribution by affiliation country.** Points show medians and horizontal lines show IQRs for countries selected by author sample size within each region. Each observation represents an author-country pair. Country denotes publication-time affiliation, not origin or nationality.

## Discussion

### Principal findings

This analysis converted a closed set of 1,158 ML4Africa DOI values into a validated author-level dataset and identified three principal patterns. First, the corpus was split almost evenly between Africa-only papers (46.1%) and papers combining African and outside-African affiliations (43.1%), indicating that both intraregional production and international collaboration are central to this research collection. Second, mixed collaborations showed role-specific differences: African affiliations were close to parity in last authorship, but appeared less frequently than outside-African affiliations in first and corresponding authorship. Third, cumulative OpenAlex bibliometric indicators were substantially higher in the outside-African affiliation stratum, although both strata contained broad distributions and country-level heterogeneity.

### Interpretation in relation to prior literature

The collaboration pattern is compatible with prior evidence that AI-for-health research concerning Africa is internationally connected and institutionally concentrated [1]. The near-equal number of Africa-only and mixed papers adds a different perspective from studies that focus only on internationally coauthored work: the corpus contains a large body of output produced entirely within known African affiliation networks as well as a similarly large international component.

The role-specific results align with literature showing that aggregate inclusion does not guarantee equal representation across prominent authorship positions [2,6-10]. However, the present corpus does not show a uniform displacement of African affiliations. African-affiliated last authors slightly exceeded outside-African-affiliated last authors in mixed papers, while first and corresponding authorship were more frequently outside-African. This role dependence supports reporting first, last, and corresponding positions separately rather than combining them into a single leadership index.

Rees and colleagues used the term authorship parasitism for research conducted in a country without an author affiliated with that country [4]. The present dataset does not contain a validated study-site variable and therefore cannot apply that construct. A paper classified here as having no African affiliation detected may concern a non-African study within a broader ML4Africa-curated corpus, may have missing affiliation metadata, or may reflect other corpus-selection logic. Authorship order and affiliation composition alone are insufficient to classify a collaboration as extractive or inequitable.

The H-index difference should be interpreted as a difference in cumulative database-recorded profiles, not as evidence of a difference in intrinsic scientific quality. H-index, citation count, and works count are interdependent and reflect career duration, discipline, publication volume, collaboration networks, database coverage, language, institutional resources, and author disambiguation [16,17]. The larger median works and citation counts in the outside-African stratum are therefore part of the interpretation of the H-index difference, not separate confirmation of individual merit.

### Implications for ML4Africa

The results provide a reproducible baseline for monitoring collaboration and leadership within this specific corpus. Future corpus updates could track whether African first and corresponding authorship in mixed papers changes over time, whether joint corresponding authorship becomes more common, and whether country participation broadens beyond the most represented networks. Because country-specific denominators differ, longitudinal within-country monitoring may be more informative than cross-sectional ranking.

The tool also separates metadata acquisition from interpretation. Teams can audit the underlying DOI, author, identifier, affiliation, and coverage records before drawing conclusions. This is particularly important when indicators may influence partnership policy, funding priorities, or institutional narratives. The 35-field schema and complete DOI reconciliation create a foundation for targeted manual validation of ambiguous identities, affiliations, and leadership roles.

### Strengths and limitations

Strengths include a fixed analytical denominator, complete DOI reconciliation, explicit separation of paper and author units, source-level missingness reporting, identifier-aware reconciliation, reproducible figure and table generation, and automated validation of CSV/JSON parity and schema integrity. The analysis also avoids converting byline patterns into unsupported labels of research conduct.

Several limitations are material. First, the DOI list was supplied by the ML4Africa team and was not generated through an exhaustive or reproducible field search; findings apply to this corpus. Second, publication-time affiliation is an imperfect geographic proxy and the completed schema retained only the first OpenAlex institution for each authorship. Third, author identities can be split or merged in OpenAlex, and fallback name rules can merge distinct people or fail to merge variants. Fourth, PubMed, Semantic Scholar, and ORCID coverage was incomplete and uneven. Fifth, corresponding-author flags and author-position conventions vary by source and discipline. Sixth, OpenAlex bibliometric indicators are dynamic and database dependent. Seventh, the analysis was descriptive and did not adjust for career stage, field, publication year, team size, or other potential explanations of impact differences. Finally, name-inferred gender and LLM-inferred professional profiles were not self-reported or independently validated and were therefore restricted to exploratory supplementary reporting.

### Future research

The next analytical stage should combine automated outputs with targeted human validation. A stratified sample of authorship records could be checked against publisher full text for corresponding-author status and multi-affiliation retention. Study-location and data-origin variables would be required before evaluating local authorship relative to where research was conducted. Longitudinal models could then examine changes in leadership while adjusting for year, field, country, team size, and author career stage. Network analysis could further distinguish repeated institutional partnerships from one-time collaborations.

## Conclusions

The ML4Africa research corpus contains both substantial Africa-only scientific production and extensive collaboration with institutions outside Africa. In mixed papers, African affiliations were near parity in last authorship but less frequent in first and corresponding authorship, and cumulative OpenAlex bibliometric profiles were lower on median in the African-affiliation stratum. These findings define auditable patterns and monitoring targets within a closed corpus. They do not establish individual contribution, research quality, causality, or the ethical character of any collaboration.

## Author contributions

[Editorial completion required: confirm the author list and assign CRediT roles, including conceptualization, methodology, software, validation, formal analysis, investigation, data curation, visualization, writing, supervision, project administration, and funding acquisition.]

## Funding

[Editorial completion required: confirm project funding and grant numbers, or state that no specific funding supported this work.]

## Acknowledgements

The authors acknowledge the ML4Africa collaborators who assembled and reviewed the DOI corpus and contributed to the development and evaluation of the Scientometric Analysis Tool. [Editorial completion required: confirm names and obtain permission for named acknowledgements.]

## Competing interests

[Editorial completion required: collect and insert declarations from all authors.]

## Data and code availability

Analysis code, tests, manuscript-generation scripts, and derived aggregate tables are maintained in the project repository: https://github.com/Mateo197802/SCIENTOMETRIC-ANALYSIS-TOOL. Release or redistribution of source and author-level data remains subject to ML4Africa team authorization and applicable source terms.

## References

{{REFERENCES}}

## Supplementary Material

{{SUPPLEMENT}}

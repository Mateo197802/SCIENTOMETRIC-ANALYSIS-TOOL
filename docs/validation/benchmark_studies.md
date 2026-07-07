# Candidate Scientometric Benchmarks

Source note: this table is derived from `ow.pdf`, the benchmark-selection draft
provided after the June 30 meeting.

## Selection Criteria

Candidate benchmarks should report enough information to be reproduced by the
tool:

1. search equation, query, or DOI-corpus construction method;
2. analyzed time range;
3. inclusion and exclusion criteria;
4. final document count;
5. authorship, affiliation, country, citation, or bibliometric outputs.

## Primary Benchmarks

| Study | Corpus construction | Time range | Filters | Final count | Reported outputs usable for validation |
|---|---|---:|---|---:|---|
| Yan, L., & Wang, Z. (2023). Mapping the Literature on Academic Publishing: A Bibliometric Analysis on WOS. SAGE Open. DOI `10.1177/21582440231158562` | Web of Science Core Collection query using synonyms of "academic publishing" across listed indexes | 1970-2020 | English-language documents; excludes reviews, corrections, and biographical notes | 2,217 documents | contributing institutions and countries; productive authors; most-cited articles |
| Basilio, M. P., Pereira, V., Costa, H. G., Santos, M., & Ghosh, A. (2022). A Systematic Review of the Applications of Multi-Criteria Decision Aid Methods (1977-2022). Electronics. DOI `10.3390/electronics11111720` | Long Boolean string for MCDA methods in title, abstract, and keywords; Web of Science plus Scopus | Jan 1977-Apr 2022 | Article type only; Web of Science limited to Core Collection | 35,643 retrieved; 23,494 analyzed | 33,201 authors; 131 countries; country shares; leading institutions |
| Baminiwatta, A., & Solangaarachchi, I. (2021). Trends and Developments in Mindfulness Research over 55 Years. Mindfulness. DOI `10.1007/s12671-021-01681-x` | Web of Science query for "mindfulness" in title, abstract, or keywords | 1966-2021 | Article and review document types with the term in key fields | 16,581 publications | country collaboration networks; co-authorship networks; citation bursts |

## Methodological Support

| Study | Proposed use |
|---|---|
| Mejia, C., Wu, M., Zhang, Y., & Kajikawa, Y. (2021). Exploring Topics in Bibliometric Research Through Citation Networks and Semantic Analysis. Frontiers in Research Metrics and Analytics. DOI `10.3389/frma.2021.742311` | Conceptual support for citation-network and semantic-analysis framing; not a direct replication benchmark unless the original corpus construction can be reconstructed with enough precision |

## Benchmark Ranking

1. Yan & Wang is the cleanest first benchmark because the final count is modest
   and the outputs are close to the current tool's core tables.
2. Baminiwatta & Solangaarachchi is useful as a medium-scale validation case
   with collaboration-network outputs.
3. Basilio et al. is the strongest stress benchmark because it is multi-source,
   larger, and explicitly reports country and institutional distributions.

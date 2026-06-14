# Figure 1 Horizontal Workflow Redesign

## Objective

Redesign Figure 1 so the Scientometric Analysis Tool workflow remains horizontal but is clearly readable when embedded at the manuscript text width in Word and PDF.

## Approved Direction

Use a simplified left-to-right methodological flow:

`Corpus -> Sources -> Reconciliation -> Enrichment -> Validation -> Master table -> Analysis`

The figure will remove the current serpentine reading order, reduce text inside boxes, increase effective type size, and give the three principal metrics stronger visual emphasis.

## Figure Contract

- **Analytical question:** How was the fixed ML4Africa DOI corpus transformed into the author-level analytical outputs reported in the manuscript?
- **Takeaway:** A closed corpus of 1,158 DOI values was processed through identifiable metadata, reconciliation, enrichment, and validation stages to produce a 35-field table with 7,361 author-paper records and 5,675 distinct OpenAlex author identifiers.
- **Visual family:** Process diagram.
- **Variant:** Horizontal linear workflow with a subordinate analytical-output band.
- **Delivery surface:** Journal manuscript embedded in DOCX and PDF.
- **Final width:** Approximately 6.45 inches in the portrait manuscript section.
- **Aspect ratio:** Approximately 2.3:1 to 2.5:1 so the figure remains large enough to read without consuming a full portrait page.
- **Palette:** One teal root for the principal data product, one blue root for the input and outputs, and neutral grey for processing stages.
- **Non-color distinctions:** Numbered stages, direct labels, distinct stage headers, and stronger outlines around the input, master table, and outputs.

## Content Architecture

### Header

- Title: `Scientometric Analysis Tool workflow`
- Subtitle: `Closed-corpus processing from DOI ingestion to author-level analysis`
- The title must be short enough to remain on one line at manuscript width.

### Main Workflow

Seven compact boxes will appear on a single horizontal baseline:

1. **Closed corpus**
   - `1,158 DOI values`
2. **Metadata sources**
   - `OpenAlex`
   - `PubMed`
   - `Semantic Scholar`
3. **Reconciliation**
   - `Author identifiers`
   - `Within-paper duplicates`
4. **Enrichment**
   - `ORCID`
   - `Genderize`
   - `Azure OpenAI`
5. **Validation**
   - `CSV/JSON parity`
   - `Complete DOI coverage`
6. **Master table**
   - `35 fields`
   - `7,361 records`
   - `5,675 OpenAlex IDs`
7. **Analysis**
   - `Collaboration`
   - `Leadership`
   - `Bibliometric impact`

Each box will use a short bold header and no more than three concise lines of supporting text.

### Analytical Output Band

A single lower band will summarize the three manuscript result domains:

- Collaboration composition
- First, last, and corresponding authorship
- Regional and country-level bibliometric impact

The band will connect only to the final `Analysis` stage. It will not introduce a second independent workflow.

### Method Note

The implemented-but-disabled integrations will be removed from the graphic body. The existing manuscript caption already states that Scopus and Google Scholar were not used for the completed run, which is the appropriate location for this caveat.

## Visual Rules

- Use one directional axis from left to right.
- Do not use backward arrows, vertical returns, or crossing connectors.
- Use equal box heights and consistent gaps.
- Use a minimum effective embedded text size equivalent to approximately 9 pt in the Word document.
- Highlight `1,158`, `7,361`, and `5,675` using weight and size, not additional colors.
- Use sentence case throughout.
- Use white or near-white background with restrained outlines.
- Avoid shadows, gradients, icons, decorative illustrations, and redundant legends.
- Keep all content legible in grayscale.

## Implementation

- Replace `_draw_pipeline()` in `scripts/manuscript/build_manuscript_assets.py`.
- Continue generating both:
  - `manuscript/figures/figure_1_pipeline.png`
  - `manuscript/figures/figure_1_pipeline.svg`
- Keep the existing figure filename and manuscript placeholder so no downstream source references change.
- Regenerate the DOCX using `scripts/manuscript/build_manuscript_docx.py`.
- Update the PDF artifact after confirming the DOCX render.

## Validation

The redesign is acceptable only when:

1. The workflow reads unambiguously from left to right.
2. All seven stage headers remain legible at the final manuscript width.
3. No label clips, overlaps, or wraps into more than three supporting lines.
4. The three primary metrics are immediately visible.
5. The figure and caption remain on a coherent manuscript page without unintended overflow.
6. The PNG and SVG contain equivalent content.
7. The DOCX contains five figures and the manuscript validation suite still passes.
8. The first page containing Figure 1 is visually inspected in the regenerated PDF.

## Scope

This change affects only Figure 1 and regenerated manuscript artifacts. It does not alter the underlying data, methodology, captions, tables, results, or the other four figures.

# PDF report changes

[Original report](Report_Before.pdf) and [revised report](Report_After.pdf) use the same saved results from a 25 m plate girder design with a 6 m carriageway, three girders, a 14 degree skew and no footpath. The baseline uses OsdagBridge commit d74f56d. Both PDFs were generated through the Python report entry point without desktop CAD captures.

## Report implementation

- `styles.py` defines the document preamble, page geometry, footer space, table padding, column types, chart palette and repeated column heading macro. Chapters 2 through 5, 7 and 8 use the shared layout. The two-row analysis header retains its own continuation definition.
- `chap3.py` lists selected vehicle classes individually and gives footpath pressure its own table with units and applicability.
- `chap5.py` passes numeric utilization ratios from the summary rows to the plotter. End diaphragm tables read their own force and design results. Girder identifiers align with the first row of a group so they stay clear of the footer when a group crosses pages.
- `charts.py` renders the component checks with a dashed red line at 1.0. Missing values are omitted. Chapter 7 plots girder and bracing weights, concrete volume and reinforcement weight on unit-specific axes. The quantity calculator supplies no separate diaphragm tonnage.
- `report_generator.py` saves the TeX source with its relative image assets, runs pdfLaTeX for cross-references and checks each pass before returning the PDF. Keep the adjacent report_assets directory when moving the TeX source.

## Validation

The baseline has 43 pages and the revised report has 49. The fatigue ratio is 2.15 in both reports. The revised PDF includes four component utilization charts and three material charts. For example, the design summary continues with its column headings on physical page 37.

A second 25 m design with a 9 m carriageway and four girders generated 54 pages. Both revised sources contain 50 longtables with continuation headings. Text-coordinate checks on every page found no body text in the footer band between 47 and 78 PDF points above the bottom edge.

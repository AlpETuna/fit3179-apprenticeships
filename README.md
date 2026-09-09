# Learning a trade building a future

A single-page Vega and Vega-Lite data story about Australian apprenticeships and traineeships, authored by Alp Tuna with acknowledged OpenAI Codex assistance.

## Public site

https://alpetuna.github.io/fit3179-apprenticeships/

The GitHub Pages workflow publishes only `dist/`. The locally prepared submission document and student details are excluded from Git and deployment.

## Structure

- `dist/index.html`: four narrative chapters and twelve figures.
- `dist/specs/`: the actual readable Vega/Vega-Lite JSON specifications.
- `dist/data/`: compact published data, derived measures and provenance.
- `dist/vendor/`: pinned chart libraries and locally served open-source fonts.
- `scripts/build_data.py`: auditable transcription and tabular transformations.
- `scripts/build_specs.py`: chart-specification generator for charts 2–12. Chart 1 is authored directly in its JSON file.

Serve `dist/` over HTTP; opening the HTML as a `file://` URL prevents normal chart-data loading. No application build or server-side service is required.

## Assignment checks

The site has twelve separately specified charts, three distinct map idioms, two statistical sources, author/date/source credits, an AI acknowledgement, visible units and definitions, and optional data tables. All main chapters remain visible on one vertically scrolling webpage.

The proposed advanced idioms are waterfall, choropleth, geographic area cartogram, treemap, heatmap, bump chart, waffle and mosaic. The proportional-symbol map and indexed dumbbell add variety but are not relied on for this conservative advanced-idiom count. The marker determines idiom classifications and effectiveness; no grade is guaranteed.

The rubric's physical hand-drawn sketch and interview are personal submission requirements. They cannot be completed by presenting a digital graphic as a hand-drawn sketch. A scan of the student's genuine sketch can be added to `dist/submission/` when available.

## Licences

Data: NCVER/Commonwealth of Australia and ABS, attributed in `dist/data/README.md` and on the webpage. Fonts: SIL Open Font License, files in `dist/vendor/fonts/`. Vega, Vega-Lite and Vega Embed: BSD-3-Clause, with licences alongside the vendored libraries.

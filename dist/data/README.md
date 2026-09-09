# Data dictionary and provenance

Prepared by Alp Tuna with OpenAI Codex assistance on 9 September 2026.

## Sources

1. **NCVER (2026), Apprentices and trainees 2025: December quarter**, released 22 June 2026. [Official publication](https://www.ncver.edu.au/research-and-statistics/publications/all-publications/apprentices-and-trainees-2025-december-quarter). National Apprentice and Trainee Collection no. 127, March 2026 estimates, activity to 31 December 2025. Numerical values were transcribed from the publication's rendered charts and tables, not inferred from pixel heights. The original charts were not copied. The underlying counts, definitions and dates were checked against the accompanying text.
2. **Australian Bureau of Statistics (2026), National, state and territory population, December 2025**, released 18 June 2026. [Official publication](https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/dec-2025), table “Annual population change at 31 December 2025”. These are the latest releases located as at the preparation date. Recheck release dates before the October submission deadline.
3. **ABS, Australian Statistical Geography Standard Edition 3, 2021 State and Territory boundaries**, [official geographic service](https://geo.abs.gov.au/arcgis/rest/services/ASGS2021/STE/MapServer). Generalised layer 1 was downloaded as GeoJSON in EPSG:4326, with coordinates rounded to three decimal places. The response was simplified for national-scale display. Source copyright is CC BY 4.0 unless otherwise noted.

NCVER attribution: NCVER 2026, *Apprentices and trainees 2025: December quarter*, NCVER, Adelaide. © Commonwealth of Australia 2026. [NCVER copyright terms](https://www.ncver.edu.au/copyright). ABS material is attributed to the Australian Bureau of Statistics; see [ABS copyright](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer).

## Files and fields

| File | Original source | Meaning |
| --- | --- | --- |
| national-series.json | NCVER Figure 1 | Trade and non-trade active contracts at 31 December, 2016–2025. |
| national-total.json | NCVER Figure 1 | Published national active-contract totals, 2016–2025. |
| states.json | NCVER Figure 8; ABS population table | Joined state figures at 31 December 2025, previous-year contracts, published percentage changes and calculated rates. |
| state-history.json | NCVER Figure 8 | Active contracts by state, 2021–2025. |
| population.json | ABS population table | Published population in thousands multiplied by 1,000. Original precision is 100 people. |
| occupations.json | NCVER Figures 4 and 6 | Active contracts by trade/non-trade occupation group, 2021–2025. FullName preserves the published group name. |
| trade-tree.json | NCVER Figure 4 | The seven published trade groups in 2025, with a synthetic hierarchy root used only for layout. The root has no observed count and is not displayed as data. |
| occupation-ranks.json | NCVER Figure 7 | The ten leading non-trade occupations selected by 2025 counts, with annual ranks calculated **within that fixed set**. |
| cohorts.json | NCVER Figure 9 | Published active contracts by selected cohort, 2021–2025. Cohorts overlap. |
| cohort-change.json | NCVER Figure 9 | 2024 and 2025 cohort counts and calculated percentage change. |
| employment-pattern.json | NCVER employment characteristics text, associated with Figure 11 | Published full-time/part-time percentages within trade and non-trade active contracts in 2025. |
| annual-activity.json | NCVER Figure 2 | Trade and non-trade annual commencements, recommencements, completions and cancellations/withdrawals during 2025. |
| abs-states-simplified.geojson | ABS generalised state boundaries | Eight state/territory polygon features, simplified and wound clockwise for Vega/D3 geographic rendering. |

`Contracts`, `Before`, `After` and `Previous` are training contracts, not unique people. `Year` denotes 31 December for active-contract snapshots. `Group` is the NCVER occupational trade classification. `Rate` is contracts per 1,000 residents; `Share`, `Change`, `ChangeFrom2021` and `Percent` are percentage values, not fractions. `Rank` is an integer with 1 representing the largest count in the displayed comparison set.

`Longitude` and `Latitude` in states.json are approximate cartographic label/symbol anchors chosen for legibility; they are not training locations or observations. `Column` and `Row` are schematic tile-map layout coordinates, not geographic measurements.

## Calculations

- State intensity: `Contracts / Population * 1000`. Join the eight state names one-to-one. Denominators include all ages. Contracts may be geographically assigned differently from residence, so this is system intensity rather than a person-based participation rate.
- National intensity: `282430 / 27801023 * 1000 = 10.2` to one decimal. The ABS national figure includes Other Territories; the state maps omit them.
- Annual state changes use NCVER's published one-decimal percentages. Recalculating from rounded counts may differ slightly.
- Waterfall: 372,885 (2022) − 35,640 (2023 change) − 28,165 (2024 change) − 26,650 (2025 change) = 282,430.
- Heatmap: `(Contracts in selected year / Contracts in 2021 - 1) * 100`, separately for each occupation group. Labels are whole percentages; tooltips provide one decimal.
- Cohort index: `2025 Contracts / 2024 Contracts * 100`; 2024 is the common index baseline of 100.
- Cohort share: `Cohort Contracts / National Contracts * 100`. Waffle cell counts round this share to a whole percentage point; the adjacent label uses one decimal.
- Mosaic width: group contracts divided by `208950 + 73475 = 282425`. The 5-contract difference from the national total is not assigned to either group. Height uses published percentages (92.0/8.0 and 55.7/44.3). The area is consequently an approximate share, not an exact count of full-time or part-time contracts.
- Treemap: areas use the seven published group counts, whose sum is 208,945, five below the published trade total of 208,950. The three largest groups sum to 171,550, or 82.1% of the published trade total.
- Tasmania/Victoria intensity ratio is approximately 1.59, i.e. 1.6 times when rounded to one decimal. Both use the same December 2025 reference date.

## Boundary processing

Query: `https://geo.abs.gov.au/arcgis/rest/services/ASGS2021/STE/MapServer/1/query?where=1%3D1&outFields=*&outSR=4326&geometryPrecision=3&f=geojson`

Keep state codes 1–8. Omit offshore polygon parts entirely south of 44°S and islands smaller than 0.002 square degrees. Simplify exterior rings with a Douglas–Peucker tolerance of 0.015 degrees, retaining closed rings. Omit internal holes at this national display scale. Reverse any counter-clockwise exterior rings for Vega's spherical polygon convention. These are cartographic display operations, not changes to contract or population values; the result must not be used as a legal boundary or for local spatial analysis.

## Limits

NCVER counts are independently rounded to the nearest five. Category sums may differ from published totals through rounding and unknown classifications. Recent figures are estimates and may be revised for up to seven quarters. Stock counts must not be added over time. Annual activity counts are different events across different contracts and do not represent a single cohort. In particular, annual completions divided by annual commencements is **not** a completion probability.

The `scripts/build_data.py` script reproduces the tabular JSON from the transcribed source values. `scripts/build_specs.py` documents the Vega/Vega-Lite transformations and chart encodings. The public `specs/` directory holds the actual readable specifications used by the site.

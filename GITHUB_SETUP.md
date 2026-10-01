# GitHub repository setup

Use the following metadata when creating the repository.

## Repository name

`montevideo-spatial-prices-mobility`

## Description

`Reproducible analysis of spatial price dispersion, local market access, inflation, and public-transit connectivity across Montevideo using 63M+ price observations, SIPC microdata, CCZ geography, and STM transport networks.`

## Visibility

Public

## Website

`https://www.diegovallarino.com`

## Topics

- spatial-economics
- urban-economics
- price-dispersion
- inflation
- market-access
- public-transport
- mobility
- spatial-econometrics
- economic-geography
- network-analysis
- montevideo
- uruguay
- sipc
- stm
- geospatial-analysis
- python
- duckdb
- reproducible-research

## License

MIT. The license applies to original code in this repository. External datasets retain the terms and licenses of their respective providers.

## Recommended first release

Tag: `v1.0.0`

Release title: `v1.0.0 — Full reproduction pipeline`

Suggested release text:

> First archived release of the Montevideo spatial-prices and urban-mobility reproduction pipeline. It covers SIPC retail microdata, matched-product local inflation, CCZ relative price levels, local product availability, STM network reconstruction, mobility-market integration, and spatial market-access measures for January 2024–June 2026. Small frozen benchmark outputs are included for automated validation; large raw data are retrieved from their official public sources and are not redistributed in the GitHub repository.

## Upload sequence

1. Create a new empty public GitHub repository with the name above.
2. Do **not** ask GitHub to create another README, license, or `.gitignore`; they are already included here.
3. Upload/commit the complete contents of this folder.
4. Confirm that the `Python syntax check` Action passes.
5. Add the topics above under **About**.
6. Create release `v1.0.0`.
7. Optionally connect the repository to Zenodo and create a DOI for the release.
8. After Zenodo assigns the DOI, add the DOI badge and DOI field to `README.md` and `CITATION.cff`.

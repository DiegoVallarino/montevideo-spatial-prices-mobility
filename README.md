# Spatial Prices, Local Markets, and Urban Mobility in Montevideo

**A reproducible spatial-economics pipeline combining high-frequency retail prices, local market structure, CCZ geography, and public-transport networks.**

Author: **Diego Vallarino**  
Website: **https://www.diegovallarino.com**  
Version: **v1.0.0**  
Reference period: **January 2024–June 2026**

---

## Overview

Consumers do not face a single city-wide price system. Their effective economic opportunity set depends on **which goods are locally available, at what prices, and which alternative markets can be reached through the urban transport network**.

This repository provides the complete reproducibility package for an empirical analysis of those mechanisms in **Montevideo, Uruguay**. It combines Uruguay's **Sistema de Información de Precios al Consumidor (SIPC)** retail-price microdata, official **Centro Comunal Zonal (CCZ)** geography, and the **Sistema de Transporte Metropolitano (STM)** route network.

The project follows the data from raw daily price declarations to monthly store-product prices, a persistent comparable basket, local inflation measures, CCZ relative price levels, local market breadth, transport-network connectivity, and finally potential spatial substitution opportunities across STM-accessible markets.

The repository is intentionally organized around **one canonical pipeline**. Earlier V1/V2/V3/V4/V5 development scripts are preserved under `legacy/` for provenance, but users reproducing the research do not need to choose among them.

---

## Project at a glance

| Dimension | Reference run |
|---|---:|
| Study area | Montevideo, Uruguay |
| Period | Jan 2024–Jun 2026 |
| Months | 30 |
| Raw price scale | 63M+ daily price observations |
| Retail establishments in monthly panel | 418 |
| Products observed | 297 |
| Persistent comparable products | 138 |
| CCZ spatial units | 18 |
| STM route variants | 867 |
| Directed CCZ network links | 107 |
| CCZs in final spatial-access output | 18 |

The small benchmark files distributed in `benchmarks/` provide machine-checkable reference results for the successful run.

---

## Research questions

The pipeline is designed around four related questions:

1. **How heterogeneous are retail price levels and inflation trajectories across Montevideo?**
2. **How does local product availability differ across neighborhoods and CCZs?**
3. **Can public-transport connectivity expand the effective market accessible to households?**
4. **How large are observed price gaps between local markets and alternative markets accessible through the STM network?**

The final stage is descriptive and associational. It quantifies **potential spatial substitution opportunities**, not realized household welfare gains or causal transport effects.

---

## Conceptual pipeline

```text
Official SIPC microdata
        │
        ▼
Daily retail price declarations
        │
        ▼
Store × Product × Month panel
        │
        ▼
Persistent comparable basket
        │
        ├────────────────────┐
        ▼                    ▼
Matched-product          Local product
local inflation          availability
        │                    │
        └──────────┬─────────┘
                   ▼
          CCZ relative prices
                   │
Official STM GIS ──┤
                   ▼
          CCZ mobility network
                   │
                   ▼
        Spatial market access
                   │
                   ▼
 Potential substitution opportunities
```

---

## What the project estimates

The pipeline constructs:

- monthly store-product representative prices;
- a persistent city-wide comparable product basket;
- matched-product month-to-month inflation by neighborhood and CCZ;
- cumulative and period inflation measures by CCZ;
- CCZ product availability and local market breadth;
- product-relative CCZ price levels against a same-product, same-month city benchmark;
- STM route-to-CCZ sequences and a directed CCZ network;
- CCZ-level network centrality/connectivity measures;
- mobility-market interaction diagnostics; and
- potential price-saving opportunities across STM-accessible CCZ destinations.

## What the project does **not** estimate

The spatial-access measures should not be interpreted as:

- realized household savings;
- observed shopping trips;
- passenger flows;
- causal effects of public transport;
- quantity-weighted household welfare changes;
- travel-time-adjusted welfare;
- fare-adjusted net savings; or
- a replacement for Uruguay's official CPI.

The Phase 4E measures are **opportunity measures under observed prices and route connectivity**. They do not include bus fares, travel time, quantities consumed, frequency, transfers, or household-specific preferences.

---

# Reproducing the analysis

## 1. Requirements

The canonical workflow was developed for **Windows + PowerShell + Python**.

Recommended:

- Windows 10/11
- PowerShell 5+ or PowerShell 7+
- Python 3.10–3.12
- sufficient disk space for large SIPC CSV/Parquet files
- internet access for the public-data download stages

Python dependencies are pinned by compatible version ranges in `requirements.txt`.

## 2. Clone the repository

```powershell
git clone https://github.com/YOUR-USERNAME/montevideo-spatial-prices-mobility.git
cd montevideo-spatial-prices-mobility
```

## 3. Run everything

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\reproduce_all.ps1
```

The runner:

1. creates the expected data/output directories;
2. installs Python dependencies;
3. downloads public source files where supported;
4. executes the canonical scripts in dependency order;
5. generates final tables and figures; and
6. compares regenerated outputs against the frozen benchmark files.

## 4. Optional project root

The repository itself can be the project root, or a separate working directory can be used:

```powershell
.\reproduce_all.ps1 -Root "D:\research\montevideo-spatial-prices"
```

The runner sets `INFLACION_ROOT`, which the canonical Python scripts use instead of a user-specific hard-coded path.

## 5. Useful switches

Use raw files already present locally:

```powershell
.\reproduce_all.ps1 -SkipDownload
```

Skip presentation-only CCZ maps:

```powershell
.\reproduce_all.ps1 -SkipMaps
```

Run without benchmark comparison:

```powershell
.\reproduce_all.ps1 -SkipValidation
```

---

# Canonical analytical sequence

The main `scripts/` directory contains one canonical script per stage.

| Step | Script | Purpose |
|---:|---|---|
| 1 | `01_download_sipc_dimensions.ps1` | Download official SIPC product and establishment dimensions |
| 2 | `02_refresh_sipc_prices.py` | Download and audit official SIPC price resources |
| 3 | `03_build_sipc_master.py` | Build normalized master datasets and Montevideo panel |
| 4 | `04_build_spatial_price_index.py` | Collapse to monthly store-product prices and build persistent basket |
| 5 | `05_build_local_inflation.py` | Construct matched-product local inflation |
| 6 | `06_robustify_neighborhood_inflation.py` | Apply stricter neighborhood coverage rules |
| 7 | `07_build_ccz_inflation.py` | Construct robust CCZ inflation measures |
| 8 | `08_make_ccz_maps.py` | Produce CCZ inflation maps |
| 9 | `09_build_ses_local_baskets.py` | Merge local market breadth and SES source |
| 10 | `10_build_relative_price_levels.py` | Construct CCZ structural relative price levels |
| 11 | `11_build_stm_route_geometry.py` | Retrieve and validate official STM route geometries |
| 12 | `12_build_stm_ccz_network.py` | Build route × CCZ sequences and directed mobility network |
| 13 | `13_build_mobility_market_panel.py` | Combine mobility, local markets, inflation, and relative prices |
| 14 | `14_build_spatial_market_access.py` | Estimate spatial substitution opportunities |
| 15 | `15_audit_spatial_access.py` | Independently audit CCZ route accessibility |
| 16 | `16_make_figures.py` | Produce final economic figures |

The exact file-level dependency graph is documented in `docs/PIPELINE.md`.

---

# Methodology

## 1. Daily observations and monthly representative prices

The source price data can contain multiple declarations for the same store-product-day. The canonical price-index stage retains the **latest declaration within each store-product-day** and then collapses daily observations into a monthly representative price.

For store `s`, product `k`, and month `t`, the monthly representative price is the median of valid daily prices:

```text
P_skt = median(P_skdt)
```

The main specification excludes observations flagged as promotions. A sensitivity construction including offers is retained in the processing logic.

This design reduces sensitivity to intraday duplication and isolated daily price noise while preserving exact product identity.

## 2. Persistent comparable basket

Spatial price comparisons require products that are observed broadly enough across establishments and persist through the sample.

The canonical Phase 2A thresholds are:

- at least **30 stores** in an eligible product-month;
- at least **25% of active stores** carrying the product in that month;
- at least **24 eligible months** out of the 30-month sample; and
- median store share of at least **25%**.

The successful reference run yields **138 persistent products**.

The point of the persistent basket is comparability: cross-CCZ differences should not be driven mechanically by completely different local product universes.

## 3. Local matched-product inflation

For a geographic area `i`, product `k`, and consecutive months `t-1` and `t`, the pipeline constructs:

```text
Δ log P_ikt = log(P_ikt / P_ik,t-1)
```

Only products observed in both consecutive months are matched. Monthly local inflation aggregates those product-level log changes and transforms the result back into percentage units.

The approach is implemented separately for neighborhoods and CCZs, with robustness rules governing minimum store and product coverage.

These measures characterize **local price dynamics for comparable products**. They are not intended to reproduce an expenditure-weighted official consumer price index.

## 4. CCZ relative price levels

Inflation and price levels answer different questions. A CCZ can experience relatively low inflation while remaining relatively expensive, or vice versa.

For each CCZ `i`, product `k`, and month `t`, the structural-price stage compares the local median with the Montevideo median for the **same product and same month**:

```text
r_ikt = log(P_ikt / P_Montevideo,kt)
```

Aggregating these within a CCZ gives a product-composition-controlled measure of whether the local market tends to be more or less expensive than the city benchmark.

## 5. Local market breadth

The project separately measures whether a product is persistently available in a CCZ. This avoids treating **price** and **availability** as the same margin.

A thin local market may expose households to fewer product alternatives even if the prices of the products that are observed are not systematically higher.

## 6. STM mobility network

Official STM route geometries are intersected with the 18 CCZ polygons. A route can cross multiple CCZs, so the pipeline preserves the complete ordered route × CCZ structure rather than forcing a route into one zone.

The final reference reconstruction contains:

- **867 STM route variants**;
- all **18 CCZs**; and
- **107 directed CCZ links**.

Network measures include degree, weighted strength, and betweenness-type connectivity metrics.

These are measures of **potential route connectivity**, not passenger volumes.

## 7. Spatial market access

Let `A(i)` denote the set of markets directly accessible from origin CCZ `i` using an observed STM route sequence.

For origin `i`, destination `j`, product `k`, and month `t`, the observed log price gap is:

```text
g_ijkt = log(P_ikt) - log(P_jkt)
```

Two principal summaries are constructed.

### Flexible destination by product

Each product may use its cheapest accessible destination:

```text
g_ikt = max_j∈A(i) [log(P_ikt) - log(P_jkt), 0]
```

The monthly percentage opportunity is summarized as:

```text
Saving_flex_it = 100 × [1 - exp(-mean_k(g_ikt))]
```

This is deliberately an upper-bound style comparison because different products may select different destinations.

### Single accessible destination

For each origin-destination-month combination, the analysis compares the basket of products jointly observed in both markets. The destination generating the largest positive monthly price opportunity is then retained.

This is more restrictive than the product-by-product flexible case because the basket is evaluated against one destination.

Again, neither measure is an observed household saving.

---

# Benchmark validation

The repository includes a compact set of successful-run outputs under `benchmarks/`.

After the pipeline finishes, `verify_reproduction.py` compares regenerated files against those reference outputs using tight numerical tolerances.

Core smoke tests include:

| Check | Expected value |
|---|---:|
| Monthly store-product rows | 1,064,788 |
| Months | 30 |
| Stores | 418 |
| Observed products | 297 |
| Eligible product-months | 4,796 |
| Persistent core products | 138 |
| STM route variants | 867 |
| STM non-maximal variants | 769 |
| STM circular variants | 98 |
| CCZs | 18 |
| Directed CCZ edges | 107 |
| Route × CCZ pairs | 4,673 |
| Direct CCZ pairs in Phase 4E | 294 |
| Core products in Phase 4E prices | 138 |
| CCZ-product-month rows | 70,871 |
| OD-product-month comparisons | 1,122,923 |
| Origins with flexible-access results | 18 |
| Origins with best-destination results | 18 |

Validation output is written to:

```text
logs/reproduction_validation.csv
```

A difference does not automatically imply a coding failure. Mutable official source files can change between runs, which is why exact archival snapshots are recommended for long-horizon reproduction.

---

# Data sources

The workflow relies on public official sources. Source URLs are retained in the canonical scripts and/or generated metadata.

## SIPC retail data

Uruguay public-data resources for:

- daily prices;
- product catalogues; and
- establishments.

The canonical sample uses 2024, 2025, and January–June 2026.

## Montevideo CCZ geography

Official GIS boundaries for Montevideo's **18 Centros Comunales Zonales**.

## STM transport data

Official Montevideo STM route/variant GIS information used to reconstruct route geometry and route-to-CCZ exposure.

## Socioeconomic information

The SES stage uses the official Montevideo CCZ income-quintile file when available and structurally compatible.

A fuller inventory is provided in the documentation and in the scripts that acquire each source.

---

# Important reproducibility distinction

There are two different notions of reproducibility in this project.

## Computational reproducibility

The following are frozen in this repository:

- code;
- transformations;
- thresholds;
- pipeline order;
- benchmark outputs; and
- automated validation logic.

This allows another researcher to audit exactly how the analytical objects are constructed.

## Archival data reproducibility

Some official endpoints are mutable. A file downloaded in the future may not be byte-identical to the file used in the reference run.

For strict long-term reproduction, the exact source snapshots should be archived separately, including SHA-256 hashes. See:

```text
docs/RAW_SNAPSHOT_RECOMMENDATIONS.md
```

A Zenodo research-data deposit is the recommended long-term companion to the GitHub code repository.

---

# SES benchmark caveat

In the frozen `phase3a_inflation_ses_ccz.csv` benchmark supplied from the successful run, SES/quintile fields are missing for all CCZ rows.

Therefore:

- the benchmark validates the inflation/local-basket side of that output;
- it does **not** establish a successful historical SES merge; and
- a later official SES source may populate those fields and cause SES-related columns to differ from the frozen benchmark.

The repository does not silently impute or fabricate those missing benchmark values.

---

# Repository structure

```text
montevideo-spatial-prices-mobility/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── GITHUB_SETUP.md
├── RELEASE_NOTES_v1.0.0.md
├── requirements.txt
├── reproduce_all.ps1
├── verify_reproduction.py
├── MANIFEST_SHA256.csv
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── python-syntax.yml
│
├── scripts/
│   └── canonical analysis pipeline
│
├── benchmarks/
│   └── small frozen reference outputs
│
├── docs/
│   ├── PIPELINE.md
│   ├── REPRODUCIBILITY_AUDIT.md
│   └── RAW_SNAPSHOT_RECOMMENDATIONS.md
│
├── data_raw/
│   └── README.md
├── data_intermediate/
├── data_final/
├── tables/
├── figures/
├── maps/
├── logs/
│
└── legacy/
    └── original_development_scripts/
```

Large generated data are intentionally excluded from Git through `.gitignore`.

---

# Why `legacy/` is retained

The empirical workflow was developed iteratively. Some stages therefore existed as V2, V3, V4, or V5 scripts while data-source issues and geographic/network definitions were being resolved.

Deleting those files would remove useful research provenance. Running them as part of the canonical workflow, however, would make reproduction ambiguous.

Accordingly:

- `scripts/` contains the single frozen canonical implementation;
- `legacy/original_development_scripts/` preserves the development history; and
- `reproduce_all.ps1` calls **only** canonical scripts.

---

# License

Original code in this repository is released under the **MIT License**. See `LICENSE`.

The license applies to the author's code, not to third-party datasets. SIPC, STM, Montevideo GIS, and other external data remain subject to the licenses, terms, and attribution requirements of their original providers.

---

# Citation

If you use the code or reproducibility package, please cite:

> Vallarino, Diego (2026). *Spatial Prices, Local Markets, and Urban Mobility in Montevideo*. Version 1.0.0. Reproducibility software package.

GitHub will also recognize the included `CITATION.cff` file and expose a **Cite this repository** option.

Once a Zenodo DOI is created for release `v1.0.0`, add the DOI to both this section and `CITATION.cff`.

---

# Research-use notes

The principal design choice throughout the project is to separate several margins that are often conflated:

- **price levels** versus **inflation**;
- **product availability** versus **price**;
- **local market breadth** versus **transport connectivity**; and
- **potential access to cheaper markets** versus **realized household behavior**.

This distinction is central to interpreting the outputs correctly. The project is best understood as an empirical framework for **spatial market access and price geography**, rather than as a conventional city-level inflation exercise.

---

## Contact

**Diego Vallarino**  
Economics, finance, econometrics, statistics, and applied AI research  
https://www.diegovallarino.com

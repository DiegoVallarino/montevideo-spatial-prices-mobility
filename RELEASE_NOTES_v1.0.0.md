# v1.0.0 — Full reproduction pipeline

This is the first public reproducibility release of **Spatial Prices, Local Markets, and Urban Mobility in Montevideo**.

The repository reconstructs the empirical workflow from official public sources and covers:

- SIPC daily retail price data for 2024–June 2026;
- monthly store-product price construction;
- a 138-product persistent comparable basket;
- neighborhood and CCZ matched-product inflation;
- CCZ relative price levels;
- local product availability and market breadth;
- official STM route geometries and a directed CCZ mobility network;
- CCZ-level mobility-market integration; and
- potential spatial substitution opportunities across STM-accessible markets.

Small outputs from the successful reference run are stored in `benchmarks/` and are used by `verify_reproduction.py` to test regenerated results. Large raw and intermediate files are not committed to GitHub.

The code is released under the MIT License. External data remain under the licenses and terms of their original providers.

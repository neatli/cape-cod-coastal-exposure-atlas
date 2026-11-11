# Cape Cod Coastal Exposure Atlas

Screening-level look at which parts of Cape Cod sit close to the coast and low to the water.
Project 1 of a 26-week geospatial portfolio.

**This is not** a flood forecast, an engineering study, or a property-level insurance model.

## Question

Which communities and areas on Cape Cod are most exposed to coastal hazards, based on
distance to shoreline and ground elevation?

## Study area

Barnstable County, MA (Cape Cod). _Final boundary choice and reasoning: TBD (week 1)._

## Data

| Layer | Source | License | Notes |
|---|---|---|---|
| County / town boundaries | TBD | | |
| Coastline | TBD | | |
| Elevation (DEM) | USGS 3DEP | Public domain | week 3 |

## Repo layout

```
data/raw/         downloaded source data (not committed)
data/processed/   cleaned outputs (not committed)
notebooks/        exploration
src/              reusable code
scripts/          one-off scripts (env check, downloads)
outputs/figures/  maps that go in the README / case study
docs/             notes on CRS choices, methods, caveats
```

## Setup

```bash
conda env create -f environment.yml
conda activate geoint
python scripts/check_env.py
```

`check_env.py` tests every import, runs a tiny vector + raster smoke test,
and writes the versions to `docs/environment.md`.

## Status

- [x] Repo + README skeleton
- [ ] Environment built and checked
- [ ] Study area picked
- [ ] Boundary + coastline downloaded, CRS checked
- [ ] First map

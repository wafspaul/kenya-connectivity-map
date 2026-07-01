# 🗺️ Kenya Connectivity Map

> An open-access interactive platform visualising internet and electricity access across Kenya's 47 counties — built to make digital infrastructure data understandable and actionable.

**🌍 Live:** [www.kenyaconnectivitymap.co.ke](https://www.kenyaconnectivitymap.co.ke)

---

## What It Shows

The map has six selectable layers, each covering a different dimension of connectivity:

| Layer | What it measures |
|-------|-----------------|
| 📊 Composite Score | Weighted connectivity index combining all four data dimensions |
| 📡 Internet Usage | % of county population using the internet (KNBS / 2022 KDHS) |
| 📶 Tower Density | Mobile cell tower count per 100 km² (OpenCelliD — 144,834 towers) |
| 🚀 Mobile Speeds | Average download speed in Mbps (Ookla Speedtest Intelligence, Q4 2024) |
| ⚡ Electricity Access | % of households with electricity access (2019 Kenya Population & Housing Census) |
| 🎓 Schools (Digital Learning) | % of primary schools with DLP devices installed (ICT Authority DigiSchool), plus 29,700 geolocated schools (Giga/UNICEF-ITU) |

**Electricity overlays** (visible on the Electricity layer):
- 🔌 Transmission grid — 66 kV, 132 kV, and 220 kV lines
- 🟢 Existing mini-grids (22 sites)
- 🟡 Mini-grids under development (26 sites)
- 🟣 Proposed KOSAP mini-grid sites (121 sites)

**School overlays** (visible on the Schools layer):
- 🔵 Primary schools, clustered (20,586 schools)
- 🟣 Secondary schools, clustered (9,081 schools)
- Internet connectivity per school is not yet shown. That data lives in Giga's School Profile API, access requested, approval pending. Markers currently show location and device data only.

Click any county to see its stats in a detailed panel. Use the layer tabs at the top to switch metrics.

---

## Why It Was Built

Kenya's digital infrastructure data exists — but it lives in separate government reports, academic datasets, and PDFs that most people never access. There was no single open tool that let you see internet coverage, tower density, mobile speeds, and electricity access side by side for every county.

This map fills that gap. It is built for businesses planning expansion into underserved markets, NGOs targeting digital inclusion programmes, researchers studying the digital divide, and anyone who needs to understand where connectivity actually stands in Kenya — not at a national average, but county by county.

---

## Data Sources

| Layer | Source | Year | Notes |
|-------|--------|------|-------|
| Internet usage | KNBS / 2022 Kenya Demographic and Health Survey (KDHS) | 2022 | County-level % using internet in past 12 months |
| Tower density | OpenCelliD | 2024 | 144,834 towers filtered to Kenya bounding box |
| Mobile speeds | Ookla Speedtest Intelligence | Q4 2024 | Tile-level data aggregated to county; median download speed |
| Electricity access | 2019 Kenya Population & Housing Census (KNBS) | 2019 | % of households connected to electricity grid |
| Transmission grid | ENERGYDATA.INFO — Kenya Power Grid | 2023 | 66 kV / 132 kV / 220 kV lines; 347 features |
| Mini-grids (existing) | ENERGYDATA.INFO — Kenya Mini-Grid Registry | 2023 | 22 operational sites |
| Mini-grids (development) | ENERGYDATA.INFO — Kenya Mini-Grid Registry | 2023 | 26 sites under development |
| KOSAP sites | ENERGYDATA.INFO — KOSAP Proposed Sites | 2023 | 121 proposed Last Mile Connectivity Programme sites |
| School locations | Giga (UNICEF-ITU School Connectivity Project), School Location API | 2026 | 29,700 geolocated Kenyan schools, licensed under ODbL, credited to Giga and its contributors |
| Digital Literacy Programme (DLP) | ICT Authority DigiSchool dashboard | 2026 | County-level device installation data (learner devices, teacher devices, routers, projectors); scraped from the public dashboard |
| Sub-county boundaries | UN OCHA Common Operational Datasets (COD-AB), admin level 2 | 2019 vintage | 290 sub-counties, used to assign each school to a county and sub-county |

---

## Methodology

### Composite Score

The composite connectivity score combines all four primary data layers using a weighted formula:

```
Composite = (Internet Usage × 0.35) + (Tower Density × 0.25) + (Mobile Speed × 0.25) + (Electricity Access × 0.15)
```

Each dimension is normalised to a 0–100 scale before weighting. Internet usage is weighted most heavily as the most direct measure of digital access; electricity is weighted lower since it is a precondition rather than a connectivity metric itself.

### Data quality notes

- **OpenCelliD** data includes crowd-sourced tower locations which may undercount towers in low-population areas. Tower density figures should be treated as indicative, not comprehensive.
- **Ookla Speedtest** data reflects speeds measured by users who ran a speed test — this introduces a selection bias toward urban and higher-income users. Speeds in rural counties may be overestimated relative to typical user experience.
- **Starlink bias:** Ookla data captures satellite internet (including Starlink) speeds. Counties with even small numbers of Starlink users may show disproportionately high speed scores. This is a known limitation — speed figures should be read alongside tower density to distinguish ground-based from satellite coverage.
- **Electricity data (2019):** The census electricity figures are the most recent county-level data available. Actual current access rates may be higher following KPLC grid expansion and REREC rural electrification since 2019.

---

## Tech Stack

- **[Leaflet.js](https://leafletjs.com/)** — interactive mapping library
- **Plain HTML / CSS / JavaScript** — no frameworks, no build tools, no dependencies beyond Leaflet
- **Single file architecture** — the entire map is one `index.html` file with all data and logic embedded
- **[Vercel](https://vercel.com/)** — hosting, auto-deploys on every push to the `main` branch on GitHub

The decision to use a single HTML file was intentional: it makes the project maximally portable, easy to fork, and deployable anywhere that can serve a static file.

---

## How to Use the Map

1. **Visit** [www.kenyaconnectivitymap.co.ke](https://www.kenyaconnectivitymap.co.ke)
2. **Select a layer** using the tabs at the top (Composite, Internet, Towers, Speed, Electricity)
3. **Click any county** to open a detail panel with its stats, rank, and comparison to the national average
4. **Toggle overlays** on the Electricity layer to show/hide the transmission grid and mini-grid markers
5. **Search** for a specific county using the search bar in the top right

---

## Run Locally

No build step required. Clone the repo and open `index.html` directly in a browser:

```bash
git clone https://github.com/wafspaul/kenya-connectivity-map.git
cd kenya-connectivity-map
# Open index.html in your browser
```

Or serve it locally with any static file server:

```bash
npx serve .
# or
python -m http.server 8080
```

---

## Project Roadmap

- [x] Internet usage layer (KNBS/KDHS)
- [x] Tower density layer (OpenCelliD)
- [x] Mobile speeds layer (Ookla)
- [x] Composite connectivity score
- [x] Electricity access layer (2019 Census)
- [x] Transmission grid overlay (66–220 kV)
- [x] Mini-grid markers (existing, under development, KOSAP proposed)
- [x] Schools layer: DLP device data by county, 29,700 geolocated schools (Giga)
- [x] Sub-county boundaries loaded (OCHA COD-AB), used for the schools spatial join
- [ ] Sub-county / ward-level choropleth for internet and electricity (pending CA, KPLC, REREC data)
- [ ] Per-school internet connectivity (pending Giga School Profile API approval)
- [ ] Fiber / fixed broadband layer (pending data sourcing)
- [ ] Methodology page on the live site
- [ ] Updated electricity data when 2024 KPLC figures are released
- [ ] KPLC infrastructure data (pending formal data request — submitted March 2026)
- [ ] REREC rural electrification data (pending formal data request — submitted March 2026)

---

## Data Requests in Progress

Formal data requests have been submitted to:
- **KPLC (Kenya Power and Lighting Company)** — county-level grid connection data, customer counts, infrastructure coverage
- **REREC (Rural Electrification and Renewable Energy Corporation)** — rural electrification project locations, mini-grid coordinates, KOSAP programme status
- **Giga (UNICEF-ITU)** — School Profile API access, for per-school internet connectivity, coverage, and infrastructure data

Responses pending as of July 2026.

---

## License

Code: [MIT License](LICENSE)

Data layers retain their original licenses:
- KNBS data — public domain (Kenya government open data)
- OpenCelliD — [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- Ookla Speedtest Intelligence — used under Ookla's open data terms
- ENERGYDATA.INFO datasets — Creative Commons Attribution 4.0 International
- Giga school location data — [Open Data Commons Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/), credited to Giga and its contributors; includes data from OpenStreetMap
- DigiSchool / DLP device data — ICT Authority, Kenya government open data
- Sub-county boundaries — UN OCHA Common Operational Datasets (COD-AB)

---

## About

Built by **Paul Wamocha** — AI for Education and Digital Inclusion specialist, digital skills trainer, and data practitioner based in Nairobi, Kenya.

The Kenya Connectivity Map is part of a broader effort to make Kenya's digital infrastructure data publicly accessible and understandable. If you work in connectivity, policy, NGOs, or rural development and would find county-level data useful for your work, reach out.

🔗 [www.kenyaconnectivitymap.co.ke](https://www.kenyaconnectivitymap.co.ke)
🔗 [paulwamocha.work](https://paulwamocha.work)

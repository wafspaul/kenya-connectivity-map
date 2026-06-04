# ARCHITECTURE.md — Kenya Connectivity Map

> Read this before adding new data layers, changing how GeoJSON is processed, or modifying the county panel data flow.

---

## High-Level Architecture

The Kenya Connectivity Map is a **static single-page application** with no backend, no API server, and no database. All data is bundled into a single `index.html` file and rendered client-side using Leaflet.js.

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     index.html (~2.5MB)                  │  │
│  │                                                          │  │
│  │  ┌─────────────┐   ┌──────────────┐   ┌─────────────┐  │  │
│  │  │  Inline CSS  │   │  Inline HTML │   │  Inline JS  │  │  │
│  │  │  (all styles)│   │  (DOM shell) │   │  (all logic)│  │  │
│  │  └─────────────┘   └──────────────┘   └──────┬──────┘  │  │
│  │                                               │          │  │
│  │  ┌────────────────────────────────────────────▼──────┐  │  │
│  │  │                  JavaScript Runtime               │  │  │
│  │  │                                                   │  │  │
│  │  │   ┌──────────────┐    ┌──────────────────────┐   │  │  │
│  │  │   │  LAYERS[]    │    │  Electricity Configs  │   │  │  │
│  │  │   │  config obj  │    │  ELEC_GRID, MG_*      │   │  │  │
│  │  │   └──────┬───────┘    └──────────┬───────────┘   │  │  │
│  │  │          │                        │               │  │  │
│  │  │   ┌──────▼────────────────────────▼───────────┐  │  │  │
│  │  │   │            Leaflet.js Map Engine           │  │  │  │
│  │  │   │   (choropleth layers, GeoJSON overlays,    │  │  │  │
│  │  │   │    tooltips, popups, zoom/pan)              │  │  │  │
│  │  │   └──────────────────────┬────────────────────┘  │  │  │
│  │  │                          │                        │  │  │
│  │  │   ┌───────────────────────▼──────────────────┐   │  │  │
│  │  │   │           UI Layer                        │   │  │  │
│  │  │   │  County Panel (desktop) / Bottom Sheet    │   │  │  │
│  │  │   │  Legend  │  Rankings Drawer  │  Tab Nav   │   │  │  │
│  │  │   └──────────────────────────────────────────┘   │  │  │
│  │  └───────────────────────────────────────────────┘  │  │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│              External CDN requests (network required)        │
│              ┌───────────────┴───────────────┐               │
│              ▼                               ▼               │
│   CartoDB Positron tiles            Leaflet.js + CSS         │
│   (base map imagery)                (from cdnjs.cloudflare)  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Vercel CDN Edge  │
                    │  (static delivery) │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   GitHub (main)    │
                    │  auto-deploy on    │
                    │     git push       │
                    └────────────────────┘
```

---

## Frontend Responsibilities

This app has no backend, so the frontend handles everything:

**Data layer**
- Stores all county-level datasets as inline JavaScript objects (arrays or objects keyed by county name)
- Stores all GeoJSON feature collections inline (county boundaries, electricity grid lines, mini-grid points)
- Performs coordinate system detection and conversion at render time (EPSG:3857 → WGS84)

**Map rendering**
- Initialises Leaflet map with CartoDB Positron base tiles
- Renders choropleth county fills based on the active layer's `property` value
- Renders electricity overlay layers (grid lines, mini-grid markers) conditionally
- Handles hover/click interactions: tooltip on hover, county panel update on click

**UI / State management**
- Tracks active layer key, active county, open/closed state of panel and drawers
- Re-renders legend, panel content, and rankings drawer on layer switch
- Handles responsive layout switching between desktop panel and mobile bottom sheet
- Manages tab state within the county panel (contextual: shows only active layer's section by default)

**No backend responsibilities** — there is no authentication, no data persistence, no server-side rendering, no API calls to a proprietary backend.

---

## API Communication Strategy

**There is no backend API.** The app makes two categories of external requests only:

### 1. CDN dependencies (load-time, read-only)
```
https://cdnjs.cloudflare.com   → Leaflet JS + CSS
https://{a-d}.basemaps.cartocdn.com → Base map tiles (on pan/zoom)
https://fonts.googleapis.com   → Google Fonts (Inter / system fallback)
```

### 2. No data API
All county data, GeoJSON boundaries, and infrastructure overlays are **embedded inline** in `index.html`. There are no `fetch()` calls to external data endpoints.

**If a future version adds a data API**, establish these conventions:
- Base URL via a top-of-file constant: `const API_BASE = 'https://api.example.com/v1'`
- All responses in `{ data: {...}, error: null }` envelope
- HTTP errors: surface in a top-level `showError(message)` UI function, never silently swallow
- Use `async/await`, not `.then()` chains

---

## Authentication and Authorisation

**None.** The app is fully public, read-only, and requires no login. All data is intentionally open — sourced from public datasets (KNBS, OpenCelliD, Ookla).

If authentication is added in future (e.g., for a paid data access tier):
- Use Vercel's built-in auth or a third-party provider (Auth0, Supabase Auth)
- Never roll a custom auth implementation in a single HTML file
- Gate data fetches server-side, not client-side

---

## Data Sources and Schema

### County boundary GeoJSON
- 47 counties, WGS84 (EPSG:4326)
- Each feature has a `properties.county` string key that must match `countyLookup[]`
- Used as the base layer for all choropleth renders

### LAYERS[] — Choropleth data config

Each entry in the `LAYERS` array defines one map layer:

```js
{
  key: String,           // unique identifier, used as active layer reference
  label: String,         // display name in tab nav
  property: String,      // key to look up in countyData[] for this layer's values
  colors: String[],      // ordered hex array, low → high
  thresholds: Number[],  // breakpoints matching colors array
  description: String,   // shown in county panel header
}
```

### County data lookup table
```js
countyLookup = {
  "Nairobi": {
    internet_pct: Number,      // KNBS KDHS 2022, % households with internet
    tower_density: Number,     // OpenCelliD, towers per 100 km²
    download_speed: Number,    // Ookla Q4 2024, Mbps (null if Starlink-excluded)
    elec_pct: Number,          // KNBS Census 2019, % households with electricity
    composite: Number,         // Weighted score: usage×0.4 + towers×0.2 + speed×0.4
    starlink_flagged: Boolean, // true = excluded from speed ranking
  },
  // ... 46 more counties
}
```

### Electricity overlays
| Variable | Source | Geometry | CRS | Count |
|---|---|---|---|---|
| `ELEC_GRID` | KPLC | LineString | WGS84 | 347 features |
| `MG_EXISTING` | REREC | Point | EPSG:3857 | 22 sites |
| `MG_UNDER_DEV` | REREC | Point | EPSG:3857 | 26 sites |
| `MG_KOSAP` | REREC | Point | EPSG:3857 | 121 sites |

EPSG:3857 → WGS84 conversion is handled by `mgMarker()`:
```js
function mgMarker(coords) {
  // If coordinate magnitude > 180, assume Web Mercator
  if (Math.abs(coords[0]) > 180) {
    return [
      (coords[1] / 20037508.34) * 180 / Math.PI * (180 / Math.PI) * Math.atan(Math.exp(...)),
      (coords[0] / 20037508.34) * 180
    ]
  }
  return coords; // Already WGS84
}
```

---

## Key Architectural Decisions

### Decision 1: Single-file architecture
**Why:** Eliminates build tooling, simplifies deployment to a single `git push`, removes dependency management overhead. The operator (Paul) is a non-developer — zero-friction deployment is a first-class constraint.

**Trade-off:** The file is large (~2.5MB). Future optimisation path: split GeoJSON data to external files loaded via `fetch()`, which would allow gzip compression and browser caching per dataset.

### Decision 2: No backend / all inline data
**Why:** Reduces operational cost to $0 (Vercel free tier), removes server maintenance, and allows fully offline viewing once loaded. All data sources are public and update at most quarterly.

**Trade-off:** Updating data requires editing `index.html` directly. No CMS, no admin UI. Acceptable at current data refresh frequency.

### Decision 3: Leaflet.js over MapboxGL / Deck.gl
**Why:** Leaflet has zero licensing cost, excellent mobile performance on low-end devices (important for Kenya's device distribution), and a small CDN footprint. Mapbox requires an API key and billing.

**Trade-off:** No WebGL rendering. County fills and vector tiles won't match the visual fidelity of Mapbox. Acceptable for a choropleth use case.

### Decision 4: Dual layout (panel + bottom sheet) instead of responsive reflow
**Why:** The desktop panel (318px right sidebar) and mobile bottom sheet (80dvh) have fundamentally different interaction models. A responsive reflow of the same component would require complex CSS transforms. Separate DOM trees are easier to maintain and test.

**Trade-off:** UI changes must be applied in two places. Documented in CLAUDE.md rules.

### Decision 5: EPSG:3857 auto-detection in `mgMarker()`
**Why:** Source data for mini-grids arrived in Web Mercator. Rather than converting offline and re-embedding, runtime detection keeps the raw source data intact and makes future data updates simpler.

**Trade-off:** Slight runtime cost on marker render. Negligible given 22–121 point features.

---

## What to Avoid and Why

| Avoid | Why |
|---|---|
| Adding a Node.js/Express backend | Introduces hosting cost, ops burden, and violates zero-maintenance constraint |
| Leaflet plugins from unknown sources | CDN risk; increases load time; potential security surface |
| Fetching GeoJSON from external URLs at runtime | Adds failure mode; CORS risk; violates offline-capable contract |
| Storing county data in `localStorage` | Data changes with each deploy; stale cache will show wrong values |
| CSS frameworks (Tailwind, Bootstrap) | CDN overhead for a bespoke layout that doesn't benefit from utility classes |
| Inline `style=""` attributes | Makes theming and audit impossible; all styles in `<style>` block |
| Mapbox or Google Maps | Licensing cost, API key management, unnecessary for choropleth use case |

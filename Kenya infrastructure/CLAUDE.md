# CLAUDE.md — Kenya Connectivity Map

> This file is the authoritative guide for any AI assistant or developer working on this codebase. Read it fully before touching anything.

---

## Project Overview

The Kenya Connectivity Map is an interactive, single-page choropleth map showing county-level internet access, mobile tower density, download speeds, and electricity infrastructure across Kenya's 47 counties. It is built as a single HTML file deployed on Vercel and serves as both a public data product and a portfolio piece for a consulting business.

Live: https://kenya-connectivity-map.vercel.app
GitHub: https://github.com/wafspaul/kenya-connectivity-map
Primary file: `index.html` (~2.5 MB, everything in one file)

---

## Stack Summary

| Layer | Technology |
|---|---|
| Map engine | Leaflet.js (CDN) |
| Frontend | Vanilla HTML5 + CSS3 + ES6 JavaScript |
| Data format | GeoJSON (county boundaries + overlay features) |
| Coordinate systems | WGS84 (EPSG:4326) primary; EPSG:3857 auto-converted via `mgMarker()` |
| Hosting | Vercel (static site, no server) |
| Version control | GitHub (`main` → Vercel auto-deploy) |
| Build system | **None.** There is no build step, no bundler, no package.json. |

**There is no backend.** All data is embedded in `index.html` as inline JavaScript objects or fetched from inline GeoJSON blobs. No API calls are made at runtime.

---

## File Structure

This is a **single-file project**. Everything lives in `index.html`:

```
index.html
├── <head>          — CDN links (Leaflet CSS/JS), meta tags, Google Fonts
├── <style>         — All CSS (global, layout, panel, mobile, legend, overlays)
├── <body>          — HTML structure (map div, panel, bottom sheet, controls)
└── <script>        — All JavaScript (data, layer config, event handlers, UI logic)
    ├── DATA SECTION        — Inline GeoJSON and lookup tables
    ├── LAYERS config       — LAYERS[] array defining each map layer
    ├── ELECTRICITY config  — ELEC_GRID, MG_EXISTING, MG_UNDER_DEV, MG_KOSAP data
    ├── Map initialisation  — Leaflet map setup, base tiles
    ├── Layer rendering     — choropleth, tooltip, popup functions
    ├── County panel        — focusPanel(), toggleFullProfile(), tab logic
    ├── Legend              — updateLegend()
    ├── Rankings drawer     — render on layer switch
    └── Mobile handling     — bottom sheet, floating elec-ctrl card
```

When in doubt about where something lives: `Ctrl+F` the function name — it is all in one file.

---

## Coding Conventions

### Naming
- **Functions:** camelCase, verb-first — `updateLegend()`, `focusPanel()`, `mgMarker()`
- **Variables:** camelCase — `countyLookup`, `gridLayer220`, `activeLayerKey`
- **CSS classes:** kebab-case — `panel-body`, `sheet-body`, `mobile-elec-ctrl`
- **IDs:** kebab-case, descriptive — `#map`, `#panel-body`, `#mobile-elec-ctrl`
- **GeoJSON layer variables:** prefixed by type — `gridLayer220`, `gridLayer132`, `mgExistingLayer`
- **Constants / config objects:** ALL_CAPS for top-level config — `LAYERS`, `ELEC_GRID`

### JavaScript
- ES6+ syntax (arrow functions, const/let, template literals, destructuring) is fine
- No TypeScript, no transpilation — write browser-compatible JS directly
- Use `const` by default, `let` only when reassignment is needed, never `var`
- GeoJSON coordinate auto-detection: if `Math.abs(coords) > 180`, treat as EPSG:3857 and convert
- All data should be defined before the functions that consume it

### CSS
- Mobile-first where practical; desktop overrides in `@media (min-width: 768px)`
- Touch targets on mobile: minimum 44px height/width
- Scrollable containers use `-webkit-overflow-scrolling: touch` for iOS
- Do not use CSS variables (`:root {}`) — use explicit hex values so they are easily searchable

### HTML
- Semantic tags where practical (`<section>`, `<aside>`, `<nav>`) inside the panel
- ARIA labels on interactive controls
- No inline `style=""` attributes — all styling goes in the `<style>` block

---

## Rules Claude Must Always Follow

1. **Keep it one file.** Every change goes into `index.html`. Do not split into separate `.js` or `.css` files.
2. **No build tools.** Do not introduce npm, webpack, vite, rollup, or any bundler under any circumstances.
3. **No frameworks.** Do not suggest or add React, Vue, Svelte, or any JS framework. Vanilla JS only.
4. **Coordinate system awareness.** When adding new GeoJSON layers with EPSG:3857 coordinates, always route them through `mgMarker()` or add equivalent auto-detection logic. Never assume WGS84.
5. **County name matching.** County names in all datasets must exactly match the keys in `countyLookup[]`. Mismatches cause silent failures in the panel. Always verify after adding new data.
6. **Sync both files.** After every edit session, copy `index.html` to both:
   - `Desktop--kenya-connectivity-map/index.html`
   - `PAUL--kenya-connectivity-map/index.html`
7. **Test both layouts.** Any UI change must be reviewed at desktop width (1280px+) AND mobile (375px). The panel and bottom sheet are separate DOM trees — a fix in one does not automatically fix the other.
8. **Preserve the LAYERS config contract.** Each entry in `LAYERS[]` must have: `key`, `label`, `property`, `colors[]`, `thresholds[]`, `description`. Do not add ad-hoc properties without updating all consumers.
9. **Handle Starlink outliers.** Ookla download speed data excludes Starlink-flagged counties. If updating speed data, maintain this exclusion flag.
10. **Performance first.** The file is already ~2.5 MB. Do not embed new large datasets without first checking whether they can be simplified or compressed inline.

---

## Rules Claude Must Never Do

- **Never introduce a `package.json`, `node_modules`, or any npm dependency.**
- **Never split `index.html` into multiple files** without an explicit, direct instruction from Paul to do so.
- **Never add a `<script src="">` for a library not already in use**, unless Paul has approved it.
- **Never hard-code county data** that belongs in the data section mid-function. Keep data and logic separated.
- **Never remove the mobile bottom sheet** and replace it with a desktop-only solution. Mobile is a first-class use case.
- **Never change the Vercel deployment configuration** or `vercel.json` without confirming with Paul.
- **Never commit directly to `main`** outside of the established GitHub → Vercel auto-deploy workflow.

---

## How to Run Locally

No build step required. Just open the file:

```bash
# Option 1 — Open directly in browser
open index.html

# Option 2 — Serve locally (avoids some CORS edge cases with file:// protocol)
npx serve .
# or
python3 -m http.server 8080
# then visit http://localhost:8080
```

The map will load fully offline except for the Leaflet tile layer (CartoDB Positron), which requires internet access to render the base map tiles.

---

## Reference Documents

| Document | When to consult |
|---|---|
| `ARCHITECTURE.md` | Before adding a new data layer, changing how GeoJSON is loaded, or modifying the county panel data flow |
| `BRANDING.md` | Before changing any colour, font, spacing, or writing UI copy. This is the single source of truth for visual decisions. |
| `FRONTEND_SPEC.md` | Before adding a new page section, new component, new route (N/A — SPA), or changing layout behaviour. Also covers accessibility requirements. |

---

## Deployment

Push to `main` on GitHub → Vercel auto-deploys within ~60 seconds. No manual deploy step needed.

```bash
git add index.html
git commit -m "feat: [short description]"
git push origin main
```

Verify at https://kenya-connectivity-map.vercel.app after ~60s.

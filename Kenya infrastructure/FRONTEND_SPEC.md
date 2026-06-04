# FRONTEND_SPEC.md — Kenya Connectivity Map

> Read this before adding a new UI section, changing layout behaviour, implementing a new component, or modifying how data flows into the county panel.

---

## Application Structure

This is a **single-page application (SPA) with no client-side routing.** There is exactly one "page" — the map view — and all UI state is managed in memory via JavaScript variables. The URL never changes.

All UI lives in `index.html` and is split into two parallel layout trees:

```
index.html
├── #map                        — Leaflet map container (full viewport)
│   └── #mobile-elec-ctrl       — Floating electricity overlay card (mobile only)
│
├── #panel (desktop only)       — Right sidebar, 318px fixed width
│   ├── #panel-header           — App title + layer tab navigation
│   ├── #panel-body             — County stats, section content
│   │   ├── .layer-sections[]   — One section per LAYERS[] entry
│   │   └── .elec-section       — Electricity infrastructure section
│   └── #legend-panel           — Colour scale legend + overlay key
│
└── #sheet (mobile only)        — Bottom sheet, 80dvh
    ├── #sheet-handle           — Drag handle (decorative)
    ├── #sheet-header           — Tab navigation
    ├── #sheet-body             — Same data sections as #panel-body
    └── #sheet-legend           — Mobile legend
```

**Critical rule:** Any data section or interactive feature that appears in `#panel-body` **must** also appear in `#sheet-body`. They are separate DOM nodes — changes to one do not propagate to the other.

---

## Component Hierarchy

```
App (index.html)
│
├── MapContainer (#map)
│   ├── LeafletMap (Leaflet-managed)
│   │   ├── BaseLayer (CartoDB Positron tiles)
│   │   ├── CountyLayer (GeoJSON choropleth)
│   │   │   └── CountyFeature × 47 (fill, hover, click handlers)
│   │   ├── GridLayer220 (LineString, orange)
│   │   ├── GridLayer132 (LineString, amber)
│   │   ├── GridLayer66 (LineString, yellow)
│   │   ├── MgExistingLayer (CircleMarker × 22, green)
│   │   ├── MgUnderDevLayer (CircleMarker × 26, amber)
│   │   └── MgKosapLayer (CircleMarker × 121, purple)
│   └── MobileElecCtrl (#mobile-elec-ctrl) [mobile only]
│       └── OverlayCheckbox × n
│
├── DesktopPanel (#panel) [desktop only, ≥768px]
│   ├── PanelHeader
│   │   └── LayerTabBar
│   │       └── LayerTab × 5 (one per LAYERS[] entry)
│   ├── PanelBody (#panel-body)
│   │   ├── CountyHeading (county name + active layer value)
│   │   ├── LayerSection × 5 (contextual, only active shown by default)
│   │   ├── ElectricitySection (mini-grid inventory, elec_pct bar)
│   │   └── FullProfileToggle ("▼ View full county profile")
│   └── LegendPanel (#legend-panel)
│       ├── ChoroplethLegend (colour scale + threshold labels)
│       ├── OverlayCheckboxGroup (grid voltage filters)
│       └── MiniGridLegend (appended when on electricity tab)
│
└── MobileSheet (#sheet) [mobile only, <768px]
    ├── SheetHandle
    ├── SheetHeader
    │   └── LayerTabBar (duplicate)
    ├── SheetBody (#sheet-body)
    │   └── [same children as PanelBody]
    └── SheetLegend (duplicate)
```

---

## State Management

There is no state management library. All state is held in plain JavaScript variables at the top of the `<script>` block. State is mutated directly and the relevant UI functions are called manually to re-render.

### Global state variables

```js
let activeLayerKey = 'composite';     // Which LAYERS[] entry is currently active
let activeCounty = null;              // Currently selected county name (string) or null
let fullProfileOpen = false;          // Whether the "full county profile" expand is open
let rankingsDrawerOpen = false;       // Whether the rankings drawer is visible
let overlayStates = {                 // Which infrastructure overlays are toggled on
  grid220: true,
  grid132: true,
  grid66: true,
  mgExisting: true,
  mgUnderDev: true,
  mgKosap: false,
};
```

### State transitions

| Trigger | State change | Side effects |
|---|---|---|
| User clicks a layer tab | `activeLayerKey` → new key | `updateChoropleth()`, `updateLegend()`, `focusPanel()`, re-render rankings if open |
| User clicks a county | `activeCounty` → county name | `focusPanel()`, map flies to county bounds |
| User clicks map background | `activeCounty` → null | `focusPanel()` resets to default state |
| User clicks "View full county profile" | `fullProfileOpen` toggles | Shows/hides hidden layer sections |
| User toggles an overlay checkbox | `overlayStates[key]` toggles | Layer added/removed from Leaflet map |
| User opens rankings drawer | `rankingsDrawerOpen` → true | Drawer renders sorted county list for `activeLayerKey` |
| User switches tab while drawer open | (no direct state change) | Rankings re-render for new `activeLayerKey` |

### Re-render functions

These are the primary functions that update the DOM in response to state changes:

| Function | What it re-renders |
|---|---|
| `updateChoropleth()` | County fill colours based on `activeLayerKey` |
| `updateLegend()` | Legend colour scale and overlay key |
| `focusPanel()` | County panel / bottom sheet content based on `activeCounty` + `activeLayerKey` |
| `toggleOverlay(key)` | Adds/removes a Leaflet layer based on `overlayStates` |
| `renderRankings()` | Rankings drawer sorted list |

**Rule:** Never directly manipulate `innerHTML` of the panel outside of these functions. Route all panel updates through `focusPanel()` to keep state consistent.

---

## API Integration Patterns

There are no API calls in the current implementation. All data is inline.

**If fetch()-based data loading is added in future**, follow this pattern:

```js
async function loadLayerData(layerKey) {
  try {
    showLoadingState(layerKey);
    const res = await fetch(`/data/${layerKey}.geojson`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderLayer(layerKey, data);
  } catch (err) {
    showLayerError(layerKey, err.message);
  } finally {
    hideLoadingState(layerKey);
  }
}
```

Rules for any future fetch:
- Always handle `!res.ok` — a 404 returns a response object, not a thrown error
- Always wrap in try/catch — network failures throw
- Always show a loading indicator before the await and hide it in `finally`
- Never fetch inside a click handler directly — delegate to a named function

---

## Error Handling Conventions

### Data errors (missing county value)
```js
// In focusPanel(), when a county value is null or undefined:
const value = countyLookup[county]?.[property] ?? null;
const display = value !== null ? formatValue(value, layerKey) : '<span class="no-data">No data</span>';
```
- Never show raw `null`, `undefined`, or `NaN` to the user
- Use `'No data'` in muted text colour (`#64748b`) for missing values
- Never hide an entire section because one value is missing — show what you have

### Starlink exclusion (download speed)
```js
if (countyLookup[county].starlink_flagged) {
  // Display: "Speed data excluded (Starlink outlier)"
  // Do not show a blank or zero value
}
```

### Coordinate conversion errors (mini-grid markers)
```js
// mgMarker() should never throw — if coords are malformed, log and skip:
try {
  const latlng = mgMarker(feature.geometry.coordinates);
  L.circleMarker(latlng, options).addTo(layer);
} catch (e) {
  console.warn(`Skipped malformed mini-grid feature: ${feature.properties.name}`, e);
}
```

### County name mismatches
- Log a `console.warn` when a GeoJSON feature's county name has no match in `countyLookup`
- Do not throw or crash — render the county with a neutral fill and no panel data
- Fix the mismatch in the data, not the matching logic

---

## Loading State Conventions

The map loads synchronously from inline data — there are no async loading states for the core map. However, for any future async operation:

```js
function showLoadingState(context) {
  document.querySelector(`[data-loading="${context}"]`)?.classList.add('is-loading');
}
// CSS: .is-loading { opacity: 0.5; pointer-events: none; }
// .is-loading::after { content: 'Loading…'; }
```

Rules:
- Loading states use `opacity: 0.5` + `pointer-events: none` on the affected region, not a full-page overlay
- Use a text indicator ("Loading…"), not a spinner animation — spinners add visual noise on a dark background
- Never block map interaction during a data load — show loading state inside the panel only

---

## Layer Tab Navigation

The layer tab bar appears in both `#panel-header` (desktop) and `#sheet-header` (mobile).

### Tab contract
- One tab per entry in `LAYERS[]`
- Active tab: underline with `#38bdf8`, text weight `600`
- Inactive tab: text colour `#94a3b8`, no underline
- Tab click: calls `setActiveLayer(key)` which updates `activeLayerKey` and triggers all re-renders
- Mobile tabs: horizontally scrollable container, `overflow-x: auto`, no wrap

### Adding a new layer tab
1. Add entry to `LAYERS[]` with all required fields
2. Add corresponding data properties to `countyLookup[]` for all 47 counties
3. Add a `<div class="layer-section" data-layer="[key]">` to both `#panel-body` and `#sheet-body`
4. Add corresponding colour scale and thresholds to `LAYERS[]`
5. Test: click the tab, click a county, verify panel content renders correctly for both null and non-null values

---

## County Panel Sections

### Default (contextual) state
When a user selects a county, the panel shows **only** the active layer's section. All other sections are hidden. This is controlled by:

```js
// In focusPanel():
document.querySelectorAll('.layer-section').forEach(el => {
  el.hidden = el.dataset.layer !== activeLayerKey;
});
```

### Full profile state
When `fullProfileOpen === true`, all layer sections are shown. The toggle button text changes to "▲ Hide full county profile".

```js
function toggleFullProfile(btn) {
  fullProfileOpen = !fullProfileOpen;
  const body = btn.closest('#panel-body, #sheet-body');
  body.querySelectorAll('.layer-section').forEach(el => {
    el.hidden = !fullProfileOpen && el.dataset.layer !== activeLayerKey;
  });
  btn.textContent = fullProfileOpen ? '▲ Hide full county profile' : '▼ View full county profile';
}
```

### Electricity section
The electricity section always shows when the electricity tab is active OR when `fullProfileOpen` is true. It includes:
- `elec_pct` as a percentage with a comparison bar
- Mini-grid inventory filtered to the selected county:
  - Operational: site count + total customer count
  - Under development: site count
  - KOSAP proposed: site count

---

## Tooltip and Popup Conventions

### Hover tooltip (county layer)
- Triggered on `mouseover`, removed on `mouseout`
- Content: `{County name} — {value}{unit}` (e.g., "Nairobi — 84.2%")
- Style: dark background `#1e293b`, `#f1f5f9` text, `12px`, `border-radius: 4px`
- Position: follows cursor via Leaflet's `L.tooltip` with `sticky: true`
- Mobile: hover tooltips are disabled — tap triggers panel update instead

### Infrastructure overlay popups
- Triggered on click/tap
- Mini-grid popup content: site name, county, status, customer count (if operational)
- Grid line popup: voltage class, approximate route name if available
- Style: matches hover tooltip styling

---

## Accessibility Baseline

These are the minimum accessibility requirements for all UI additions:

### Colour contrast
- All text against backgrounds must meet WCAG AA (4.5:1 for body text, 3:1 for large text / UI components)
- The dark theme (`#0f172a` background, `#f1f5f9` text) is compliant by default
- Data layer fill colours are used for geographic areas — always pair with a text label in the panel; never use colour as the sole indicator

### Keyboard navigation
- Layer tabs: navigable via `Tab` key, activated via `Enter` or `Space`
- "View full county profile" toggle: must be reachable via keyboard
- Overlay checkboxes: standard `<input type="checkbox">` — keyboard accessible by default

### Screen reader support
- Map container: `aria-label="Kenya Connectivity Map"` on `#map`
- Layer tabs: `role="tablist"` on container, `role="tab"` on each tab, `aria-selected="true/false"`
- Active county panel: `aria-live="polite"` on `#panel-body` and `#sheet-body` so screen readers announce county changes
- Legend: `aria-label="Map legend"` on the legend container

### Mobile / touch
- Minimum touch target: 44 × 44px for all tappable elements
- Bottom sheet drag handle: `role="button"` with `aria-label="Map information panel"`
- Avoid hover-only interactions — all hover states must have a tap equivalent

### Focus management
- When the rankings drawer opens, move focus to the first item in the list
- When the drawer closes, return focus to the button that opened it

### Reduced motion
```css
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
```
This rule must be present in the `<style>` block.

---

## Responsive Breakpoints

| Breakpoint | Behaviour |
|---|---|
| `< 768px` | Mobile layout: full-viewport map + bottom sheet. `#panel` is hidden. `#mobile-elec-ctrl` is visible. |
| `≥ 768px` | Desktop layout: map with 318px right panel. `#sheet` is hidden. Desktop overlay checkboxes in legend panel. |

There is no intermediate "tablet" layout. The breakpoint is binary: panel or sheet.

**Test at:** 375px (iPhone SE), 390px (iPhone 14), 768px (iPad portrait, is desktop), 1280px (standard desktop).

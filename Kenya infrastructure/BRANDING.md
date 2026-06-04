# BRANDING.md — Kenya Connectivity Map

> The single source of truth for all visual and copy decisions. Consult this before changing any colour, font, spacing, or writing UI text.

---

## Brand Identity

The Kenya Connectivity Map communicates **data authority** and **clarity**. It is a professional tool for understanding infrastructure inequality across Kenya. The visual language should feel like a polished data journalism product — not a government dashboard, not a startup landing page.

**Core personality:** Precise. Considered. Quietly confident.

---

## Colour Palette

### Base Interface Colours

| Role | Name | Hex | Usage |
|---|---|---|---|
| Background | Deep slate | `#0f172a` | Page/map background, dark panels |
| Surface | Dark blue-grey | `#1e293b` | Panel background, card backgrounds |
| Surface elevated | Mid slate | `#334155` | Hover states, dividers, input backgrounds |
| Border | Subtle slate | `#475569` | Panel borders, dividers |
| Text primary | Off-white | `#f1f5f9` | Headings, primary labels |
| Text secondary | Cool grey | `#94a3b8` | Sub-labels, descriptions, metadata |
| Text muted | Dim grey | `#64748b` | Placeholder text, disabled states |
| Accent — interactive | Sky blue | `#38bdf8` | Links, active tab underlines, focus rings |
| Accent — highlight | Cyan | `#22d3ee` | Hover on interactive map elements |

### Choropleth Data Colours

The map uses sequential colour scales — light (low values) to saturated (high values). All scales are perceptually uniform and accessible.

**Composite / Internet Usage — Blue scale**
```
#eff6ff → #bfdbfe → #60a5fa → #2563eb → #1e3a8a
(very low)                              (very high)
```

**Tower Density — Teal scale**
```
#ecfdf5 → #a7f3d0 → #34d399 → #059669 → #064e3b
```

**Download Speed — Purple scale**
```
#faf5ff → #e9d5ff → #c084fc → #9333ea → #581c87
```

**Electricity Access — Amber scale**
```
#fffbeb → #fde68a → #fbbf24 → #d97706 → #78350f
```

### Electricity Infrastructure Overlay Colours

These are the fixed colours for infrastructure feature layers — do not change them without updating the legend simultaneously.

| Feature | Hex | Tailwind reference |
|---|---|---|
| 220 kV grid lines | `#f97316` | orange-500 |
| 132 kV grid lines | `#f59e0b` | amber-400 |
| 66 kV grid lines | `#facc15` | yellow-400 |
| Mini-grid — Operational | `#10b981` | emerald-500 |
| Mini-grid — Under development | `#f59e0b` | amber-400 |
| Mini-grid — KOSAP proposed | `#a78bfa` | violet-400 |

### Status / Feedback Colours

| State | Hex | Usage |
|---|---|---|
| Success | `#10b981` | Data loaded, layer active |
| Warning | `#f59e0b` | Partial data, excluded counties |
| Error | `#f87171` | Load failure, missing data |
| Info | `#38bdf8` | Tooltips, info callouts |

---

## Typography

### Font Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

Inter is loaded from Google Fonts. Always include the system font fallback chain — the map must render correctly on slow connections where the web font hasn't loaded.

**Do not use** serif fonts, display fonts, or decorative typefaces anywhere in the UI.

### Type Scale

| Role | Size | Weight | Line height | Usage |
|---|---|---|---|---|
| Page title | 18px | 700 | 1.2 | App header / branding |
| Section heading | 15px | 600 | 1.3 | Panel section headings ("Internet Access", "Electricity") |
| County name | 16px | 700 | 1.2 | Active county in panel header |
| Body / data label | 13–14px | 400 | 1.5 | County stat values, descriptions |
| Caption / meta | 11–12px | 400 | 1.4 | Data sources, footnotes, layer descriptions |
| Tab label | 12px | 500 | 1 | Layer tab navigation |
| Button / control | 13px | 500 | 1 | Overlay checkboxes, control labels |

**Weight hierarchy:**
- `400` — body, description, metadata
- `500` — controls, tabs, sub-labels
- `600` — section headings
- `700` — county name, page title, key data values

**Never use weight 300 (light)** — it renders poorly on dark backgrounds at small sizes.

### Number display
- Data values: always include the unit inline (`72%`, `4.2 Mbps`, `18.3 / km²`)
- Percentages: round to one decimal place
- Speed: one decimal place (e.g., `12.4 Mbps`)
- Tower density: one decimal place (e.g., `4.2 / 100 km²`)
- Composite score: one decimal place (e.g., `6.1 / 10`)

---

## Spacing and Layout

### Spacing Scale (use multiples of 4px)
```
4px  — micro (icon gap, tight inline spacing)
8px  — small (within-component padding)
12px — base (standard padding inside cards/panels)
16px — medium (section padding, between grouped elements)
24px — large (between distinct sections)
32px — xlarge (major layout gaps)
```

### Desktop Layout
- Map: full viewport (`100vw × 100vh`)
- Right panel: fixed width `318px`, full height, scrollable
- Panel padding: `16px` horizontal, `12px` vertical per section
- Legend panel: max-height `240px`, overflow-y scroll
- Rankings drawer: slides in from right, width `280px`

### Mobile Layout
- Map: full viewport
- Bottom sheet: height `80dvh`, border-radius `16px 16px 0 0` on top edge
- Floating electricity control card (`#mobile-elec-ctrl`): positioned inside `#map`, bottom-left
- All tappable elements: minimum `44 × 44px` touch target
- Tab bar: horizontal scroll on overflow, no wrapping

### Comparison bars (county panel)
- Track: `#334155`, full width, height `6px`, border-radius `3px`
- Fill: uses the active layer's accent colour, border-radius `3px`
- Do not animate on initial render — set width directly

---

## Component Style Philosophy

**Minimal and data-forward.** The map is the product. UI chrome should recede.

Specific principles:

1. **Dark UI, not dark mode.** The dark theme is the only theme. It is not a user toggle — it is the designed state. The dark background makes choropleth fills and infrastructure overlays pop.

2. **No decorative elements.** No gradients on UI chrome, no drop shadows on panels (use border instead), no illustrations, no icons beyond functional ones.

3. **Borders over shadows.** Use `border: 1px solid #475569` to define panel edges. Avoid `box-shadow` on containers — it adds visual noise on dark backgrounds.

4. **Tight information density.** The county panel packs a lot of data into 318px. Prioritise data density over generous whitespace — but never sacrifice legibility. Line height 1.5 on body text is the minimum.

5. **Tabs, not accordion.** Layer navigation is tab-based with an active underline. Do not switch this to an accordion or dropdown — horizontal scanning is faster for 4–5 options.

6. **Progressive disclosure.** The panel shows only the active layer's section by default. The "View full county profile" toggle reveals everything. Preserve this pattern on any new data section added.

7. **Overlay checkboxes.** Infrastructure overlays use native `<input type="checkbox">` with custom CSS styling. Do not replace with toggle switches — the checkbox label + sub-filter pattern is intentional.

---

## Tone of Voice — UI Copy

The map speaks like a data journalist or infrastructure analyst, not a tech startup.

**Write like this:**
> "Download speed excludes counties where Starlink connections represent a statistical outlier."
> "47 counties ranked by composite connectivity score."
> "No data available for this county."

**Not like this:**
> "Oops! We couldn't find data for this county 😬"
> "Unleash the power of Kenya's connectivity data!"
> "Loading your personalised map experience…"

### Copy guidelines

| Context | Tone | Example |
|---|---|---|
| Empty states | Neutral, factual | "No data available." |
| Loading states | Brief, no personality | "Loading…" |
| Data footnotes | Formal, source-cited | "Source: KNBS KDHS 2022" |
| Layer descriptions | Technical but plain English | "Percentage of households with internet access, by county." |
| Error states | Direct, actionable | "Data failed to load. Please refresh the page." |
| Tooltip labels | Concise, unit always included | "Nairobi — 84.2%" |

**Never use:** exclamation marks (except critical errors), emoji in data UI, first-person ("We couldn't…"), passive-aggressive apology copy ("Sorry about that!").

**Always use:** Oxford comma in lists, present tense for data facts, sentence case for headings (not Title Case For Every Word).

---

## Things to Always Avoid in the UI

| Avoid | Why |
|---|---|
| Light backgrounds anywhere | Breaks the dark-themed map contrast |
| Colour fills on UI chrome (buttons, cards) | Use border + transparent background instead |
| Animated transitions > 200ms | Feels sluggish; the map is a tool, not a showcase |
| Pop-up modals for data info | Use the panel / bottom sheet — never block the map |
| Full-bleed images or illustrations | The map is the visual; don't compete with it |
| Rounded corners > 8px | Looks consumer app, not data tool |
| Font sizes below 11px | Illegible on mobile screens at arms length |
| Colour alone to convey meaning | Always pair colour with a label (accessibility) |
| Custom scrollbars | System scrollbars are more trusted on data tools |
| Auto-playing animations | Nothing should move unless the user triggered it |

#!/usr/bin/env python3
"""Dev-time generator for the static SEO pages (counties, blog, data).
Reads the county data embedded in index.html and writes plain HTML files.
No build step on Vercel: run this locally, commit the output.
Usage: python3 tools/build_pages.py
"""
import json, re, os, html, csv, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.kenyaconnectivitymap.co.ke'
TODAY = datetime.date.today().isoformat()
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read().split('\n')

def var_json(name):
    for l in src:
        m = re.match(r'\s*var\s+' + name + r'\s*=\s*', l)
        if m:
            return json.loads(l[m.end():].strip().rstrip(';').split(';//')[0].split('; //')[0])
    raise SystemExit('missing ' + name)

geo = var_json('KENYA_GEOJSON')
counts = var_json('SCHOOLS_COUNTS')
dlp = var_json('DLP_DATA')
emp = var_json('EMPLOYMENT_DATA')
ALIAS = {'Elgeyo-Marakwet': 'Elgeyo Marakwet', "Murang'a": 'Muranga', 'Tharaka-Nithi': 'Tharaka Nithi'}
P = sorted([f['properties'] for f in geo['features']], key=lambda p: -p['composite'])
for i, p in enumerate(P): p['rank'] = i + 1
def slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower().replace("'", '')).strip('-')
for p in P: p['slug'] = slug(p['county'])
def rank_by(key, skip_flag=False):
    xs = [p for p in P if not (skip_flag and p['speed_flag'])]
    xs.sort(key=lambda p: -p[key])
    return {p['county']: i + 1 for i, p in enumerate(xs)}
R_INT, R_ELEC, R_TOW, R_SPD = rank_by('internet_ind'), rank_by('elec_pct'), rank_by('towers_density'), rank_by('speed_dl', True)
NAT_INT, NAT_ELEC = 35.0, 38.7
TIER_TXT = {'High': 'High', 'Medium': 'Medium', 'Low': 'Low', 'Critical': 'lowest'}
esc = html.escape
def ordinal(n): return '%d%s' % (n, 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))

CSS = """:root{--bg:#080d18;--surface:#0e1525;--surface2:#151f35;--border:rgba(255,255,255,.1);--text:#dce8f5;--dim:#9db0c5;--accent:#00c8f0}
*{box-sizing:border-box;margin:0;padding:0}body{background:var(--bg);color:var(--text);font:17px/1.65 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
a{color:var(--accent)}header.site{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:14px 16px;border-bottom:1px solid var(--border);background:var(--surface)}
header.site a.brand{color:var(--text);font-weight:700;text-decoration:none;margin-right:auto}header.site a.brand span{color:var(--accent)}
header.site nav a{color:var(--dim);text-decoration:none;margin-left:16px;font-size:15px}header.site nav a:hover{color:var(--text)}
main{max-width:760px;margin:0 auto;padding:28px 16px 56px}h1{font-size:clamp(26px,5vw,36px);line-height:1.2;margin-bottom:12px}
h2{font-size:22px;margin:32px 0 10px}p{margin:0 0 16px}.lede{color:var(--dim);font-size:18px}.crumbs{font-size:14px;color:var(--dim);margin-bottom:14px}
.cta{display:inline-block;background:var(--accent);color:#04202a;font-weight:700;padding:10px 18px;border-radius:8px;text-decoration:none;margin:6px 0 18px}
table{width:100%;border-collapse:collapse;margin:12px 0 20px;font-size:15px}th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--border)}th{color:var(--dim);font-weight:600}
.wrap{overflow-x:auto}.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0 22px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px}.card b{display:block;font-size:24px;color:var(--accent)}.card small{color:var(--dim)}
ul.plain{list-style:none;columns:2;gap:20px}ul.plain li{margin-bottom:6px}.pn{display:flex;justify-content:space-between;gap:12px;margin-top:28px;font-size:15px}
footer.site{border-top:1px solid var(--border);padding:22px 16px;text-align:center;color:var(--dim);font-size:14px}footer.site a{margin:0 8px}
.src{font-size:14px;color:var(--dim)}.post-meta{color:var(--dim);font-size:14px;margin-bottom:20px}@media(max-width:560px){ul.plain{columns:1}}"""

def page(path, title, desc, body, jsonld=None, og_type='website'):
    url = SITE + '/' + path.strip('/') + ('/' if path.strip('/') else '')
    ld = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(j, ensure_ascii=False) for j in (jsonld or []))
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Paul Wamocha">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Kenya Connectivity Map">
<meta property="og:locale" content="en_KE">
<meta property="og:image" content="{SITE}/social-preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/social-preview.png">
<meta name="theme-color" content="#080d18">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{ld}<style>{CSS}</style>
</head>
<body>
<header class="site"><a class="brand" href="/">Kenya <span>Connectivity</span> Map</a>
<nav><a href="/">Map</a><a href="/counties/">Counties</a><a href="/blog/">Blog</a><a href="/data/">Data</a></nav></header>
<main>
{body}
</main>
<footer class="site"><a href="/">Interactive map</a><a href="/counties/">All 47 counties</a><a href="/blog/">Blog</a><a href="/data/">Data and sources</a><p style="margin-top:10px">Built by <a href="https://paulwamocha.work">Paul Wamocha</a></p></footer>
</body>
</html>
"""
    d = os.path.join(ROOT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(doc)
    return url

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

urls = []  # (url, lastmod, priority)

# ---------- county pages ----------
def county_page(i, p):
    c = p['county']; s = p['slug']
    sc = counts.get(c, [0, 0, 0]); tot_sch = sum(sc)
    d = dlp.get(ALIAS.get(c, c)); e = emp.get(ALIAS.get(c, c))
    para1 = (f"{c} ranks {ordinal(p['rank'])} of 47 counties on my composite connectivity score, at {p['composite']:.1f} out of 100. "
             f"That puts it in the {TIER_TXT[p['tier']]} tier.")
    cmp_i = 'above' if p['internet_ind'] >= NAT_INT else 'below'
    para2 = (f"{p['internet_ind']:.1f}% of people in {c} use the internet. The national figure on this map is {NAT_INT:.0f}%, so the county sits {cmp_i} it, "
             f"in {ordinal(R_INT[c])} place nationally. Electricity access is {p['elec_pct']:.1f}% against a national {NAT_ELEC}%, which ranks {ordinal(R_ELEC[c])}.")
    if p['speed_flag']:
        spd = (f"I flag the speed figure for {c}. A handful of Starlink users can pull a county average up, so I leave {c} out of the speed ranking and read its tower density instead.")
    else:
        spd = (f"Average mobile download speed is {p['speed_dl']:.1f} Mbps, {ordinal(R_SPD[c])} of the 46 counties with an unflagged speed figure. "
               f"Tower density is {p['towers_density']:,.1f} per 100 km², which ranks {ordinal(R_TOW[c])}.")
    rows = [("Composite score", f"{p['composite']:.1f} / 100", f"{ordinal(p['rank'])} of 47", "Weighted blend of the four layers below"),
            ("Internet usage", f"{p['internet_ind']:.1f}%", f"{ordinal(R_INT[c])} of 47", "KNBS / 2022 KDHS"),
            ("Electricity access", f"{p['elec_pct']:.1f}%", f"{ordinal(R_ELEC[c])} of 47", "2019 Population and Housing Census"),
            ("Cell towers per 100 km²", f"{p['towers_density']:,.1f}", f"{ordinal(R_TOW[c])} of 47", "OpenCelliD, Mar 2026"),
            ("Average download speed", "Flagged" if p['speed_flag'] else f"{p['speed_dl']:.1f} Mbps", "n/a" if p['speed_flag'] else f"{ordinal(R_SPD[c])} of 46", "Ookla Speedtest Intelligence, Q1 2026")]
    trs = ''.join(f"<tr><td>{esc(a)}</td><td><strong>{esc(b)}</strong></td><td>{esc(r)}</td><td class='src'>{esc(sr)}</td></tr>" for a, b, r, sr in rows)
    extra = ''
    if tot_sch:
        extra += f"<h2>Schools</h2><p>The Giga school location data lists {tot_sch:,} schools in {c}: {sc[0]:,} primary, {sc[1]:,} secondary and {sc[2]:,} other.</p>"
        if d:
            extra += f"<p>The ICT Authority DigiSchool dashboard shows {d['installed']:,} of {d['total']:,} schools with Digital Learning Programme devices installed ({d['pct']:.1f}%).</p>"
    if e:
        extra += f"<h2>Employment</h2><p>The census lists a labour force participation rate of {e['lfpr']:.1f}% and an unemployment rate of {e['rate']:.1f}% in {c}.</p>"
    prev_p = P[i - 1] if i else None; next_p = P[i + 1] if i < 46 else None
    pn = '<div class="pn"><span>' + (f'<a href="/counties/{prev_p["slug"]}/">&larr; {esc(prev_p["county"])}</a>' if prev_p else '') + '</span><span>' + (f'<a href="/counties/{next_p["slug"]}/">{esc(next_p["county"])} &rarr;</a>' if next_p else '') + '</span></div>'
    body = f"""<p class="crumbs"><a href="/">Map</a> / <a href="/counties/">Counties</a> / {esc(c)}</p>
<h1>{esc(c)} County: internet and electricity coverage</h1>
<p class="lede">{esc(para1)}</p>
<a class="cta" href="/#county={s}">Open {esc(c)} on the map</a>
<div class="cards"><div class="card"><b>{p['composite']:.0f}</b><small>Composite score</small></div><div class="card"><b>{p['internet_ind']:.1f}%</b><small>Use the internet</small></div><div class="card"><b>{p['elec_pct']:.1f}%</b><small>Electricity access</small></div><div class="card"><b>{ordinal(p['rank'])}</b><small>Of 47 counties</small></div></div>
<p>{esc(para2)}</p>
<p>{esc(spd)}</p>
<h2>{esc(c)} data at a glance</h2>
<div class="wrap"><table><tr><th>Measure</th><th>Value</th><th>Rank</th><th>Source</th></tr>{trs}</table></div>
{extra}
<p class="src">All figures come from the datasets listed on the <a href="/data/">data and sources page</a>. The composite score formula is explained in <a href="/blog/how-i-built-the-kenya-connectivity-map/">how I built the map</a>.</p>
{pn}"""
    title = f"{c} County Internet & Electricity Coverage | Kenya Connectivity Map"
    desc = f"{c} County ranks {ordinal(p['rank'])} of 47 on connectivity: {p['internet_ind']:.1f}% internet usage, {p['elec_pct']:.1f}% electricity access and {p['towers_density']:,.1f} cell towers per 100 km²."
    u = page(f"counties/{s}", title, desc, body, [crumbs([("Map", SITE + "/"), ("Counties", SITE + "/counties/"), (c, f"{SITE}/counties/{s}/")])])
    urls.append((u, TODAY, '0.7'))

alpha = sorted(P, key=lambda p: p['county'])
for i, p in enumerate(P): county_page(i, p)

# counties index
rows = ''.join(f"<tr><td><a href='/counties/{p['slug']}/'>{esc(p['county'])}</a></td><td>{p['composite']:.1f}</td><td>{p['tier']}</td><td>{p['internet_ind']:.1f}%</td><td>{p['elec_pct']:.1f}%</td></tr>" for p in P)
body = f"""<p class="crumbs"><a href="/">Map</a> / Counties</p>
<h1>Internet and electricity coverage in all 47 Kenyan counties</h1>
<p class="lede">Here is the full county ranking behind the map, sorted by composite score. Click a county for its page, or open the interactive map to compare layers.</p>
<a class="cta" href="/">Open the interactive map</a>
<div class="wrap"><table><tr><th>County</th><th>Composite</th><th>Tier</th><th>Internet use</th><th>Electricity</th></tr>{rows}</table></div>
<p class="src">Sources: KNBS / 2022 KDHS, 2019 Census, OpenCelliD (Mar 2026), Ookla Speedtest Intelligence (Q1 2026). Full list on the <a href="/data/">data page</a>.</p>"""
urls.append((page('counties', 'Kenya Counties Ranked by Internet & Electricity Coverage', 'All 47 Kenyan counties ranked by a composite of internet usage, cell tower density, mobile speed and electricity access.', body,
    [crumbs([("Map", SITE + "/"), ("Counties", SITE + "/counties/")])]), TODAY, '0.8'))

# ---------- data page + csv ----------
os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
with open(os.path.join(ROOT, 'data', 'kenya_county_connectivity.csv'), 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['county', 'composite_score', 'tier', 'internet_usage_pct', 'electricity_access_pct', 'cell_towers_per_100km2', 'avg_download_mbps', 'speed_flagged', 'area_sqkm'])
    for p in alpha:
        w.writerow([p['county'], p['composite'], p['tier'], p['internet_ind'], p['elec_pct'], p['towers_density'], '' if p['speed_flag'] else p['speed_dl'], int(bool(p['speed_flag'])), round(p['area_sqkm'], 1)])
dataset = {"@context": "https://schema.org", "@type": "Dataset", "name": "Kenya county connectivity indicators",
    "description": "County-level internet usage, electricity access, cell tower density, mobile download speed and a composite connectivity score for all 47 Kenyan counties.",
    "url": SITE + "/data/", "creator": {"@type": "Person", "name": "Paul Wamocha", "url": "https://paulwamocha.work"},
    "spatialCoverage": {"@type": "Place", "name": "Kenya"}, "isAccessibleForFree": True, "keywords": ["Kenya", "internet access", "electricity access", "digital divide", "county data"],
    "variableMeasured": ["Internet usage (%)", "Electricity access (%)", "Cell towers per 100 km2", "Average mobile download speed (Mbps)", "Composite connectivity score"],
    "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": SITE + "/data/kenya_county_connectivity.csv"}],
    "isBasedOn": ["KNBS / 2022 KDHS", "2019 Kenya Population and Housing Census", "OpenCelliD", "Ookla Speedtest Intelligence"]}
SOURCES = [("Internet usage", "KNBS / 2022 Kenya Demographic and Health Survey", "2022"), ("Tower density", "OpenCelliD", "Mar 2026"),
           ("Mobile speed", "Ookla Speedtest Intelligence", "Q1 2026"), ("Electricity access", "2019 Kenya Population and Housing Census", "2019"),
           ("Grid and mini-grids", "ENERGYDATA.INFO Kenya Power Grid and Mini-Grid Registry", "2023"), ("School locations", "Giga (UNICEF/ITU) School Location API", "2026"),
           ("School devices", "ICT Authority DigiSchool dashboard", "2026"), ("Sub-county boundaries", "UN OCHA COD-AB, admin level 2", "2019 vintage")]
srows = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in SOURCES)
body = f"""<p class="crumbs"><a href="/">Map</a> / Data</p>
<h1>Kenya county connectivity data and sources</h1>
<p class="lede">I built the map from public datasets and I list every one of them here. You can download the county table as a CSV.</p>
<a class="cta" href="/data/kenya_county_connectivity.csv" download>Download county CSV (47 rows)</a>
<h2>What is in the file</h2>
<p>One row per county: composite score and tier, internet usage, electricity access, cell towers per 100 km², average mobile download speed and area. Samburu's speed value is blank because I flag it as distorted by a small number of Starlink users.</p>
<h2>Sources</h2>
<div class="wrap"><table><tr><th>Layer</th><th>Source</th><th>Year</th></tr>{srows}</table></div>
<p>Tower density is crowd-sourced and can undercount towers in low-population areas. Speed tests skew toward urban users. Read both with that in mind. The composite formula is in <a href="/blog/how-i-built-the-kenya-connectivity-map/">how I built the map</a>.</p>
<p>Need county analysis for a programme, a network plan or a grant bid? Get in touch through <a href="https://paulwamocha.work">paulwamocha.work</a>.</p>"""
urls.append((page('data', 'Kenya County Connectivity Data & Sources (CSV)', 'Download county-level internet, electricity, tower density and speed data for all 47 Kenyan counties, with a full list of sources.', body,
    [dataset, crumbs([("Map", SITE + "/"), ("Data", SITE + "/data/")])]), TODAY, '0.8'))

# ---------- blog ----------
import blog_posts  # noqa: E402  (tools/blog_posts.py)
posts = blog_posts.build(P, R_INT, R_ELEC)
brows = ''
for po in posts:
    body = f"""<p class="crumbs"><a href="/">Map</a> / <a href="/blog/">Blog</a></p>
<h1>{esc(po['title'])}</h1>
<p class="post-meta">By Paul Wamocha · {po['date']}</p>
{po['html']}
<h2>Explore the data</h2>
<p><a class="cta" href="/">Open the interactive map</a> or browse <a href="/counties/">all 47 counties</a>. County data is on the <a href="/data/">data page</a>.</p>"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": po['title'], "description": po['desc'], "datePublished": po['date'], "dateModified": po['date'],
           "author": {"@type": "Person", "name": "Paul Wamocha", "url": "https://paulwamocha.work"}, "image": SITE + "/social-preview.png",
           "mainEntityOfPage": f"{SITE}/blog/{po['slug']}/", "publisher": {"@type": "Person", "name": "Paul Wamocha"}}
    u = page(f"blog/{po['slug']}", po['title'] + ' | Kenya Connectivity Map', po['desc'], body, [art, crumbs([("Map", SITE + "/"), ("Blog", SITE + "/blog/"), (po['title'], f"{SITE}/blog/{po['slug']}/")])], 'article')
    urls.append((u, po['date'], '0.8'))
    brows += f"<h2 style='margin-top:26px'><a href='/blog/{po['slug']}/'>{esc(po['title'])}</a></h2><p class='post-meta'>{po['date']}</p><p>{esc(po['desc'])}</p>"
urls.append((page('blog', 'Kenya Connectivity Blog | Data Notes on Internet & Electricity', 'Data notes on internet and electricity access across Kenya\'s 47 counties, from the builder of the Kenya Connectivity Map.',
    f"<h1>Kenya connectivity blog</h1><p class='lede'>Notes on what the county data says about internet and electricity access in Kenya.</p>{brows}", [crumbs([("Map", SITE + "/"), ("Blog", SITE + "/blog/")])]), TODAY, '0.7'))

# ---------- sitemap ----------
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
      f'  <url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>']
for u, lm, pr in urls:
    sm.append(f'  <url><loc>{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>')
sm.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write('\n'.join(sm) + '\n')
print('pages:', len(urls) + 1)

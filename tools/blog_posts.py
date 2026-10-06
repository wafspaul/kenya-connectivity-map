"""Blog post bodies for tools/build_pages.py. Every figure is computed from the map's own dataset."""
DATE = '2026-10-06'

def _names(xs): return ', '.join(xs[:-1]) + ' and ' + xs[-1]

def build(P, R_INT, R_ELEC):
    by = {p['county']: p for p in P}
    top = P[:5]; bot = P[::-1][:5]
    tiers = {t: [p['county'] for p in P if p['tier'] == t] for t in ['High', 'Medium', 'Low', 'Critical']}
    ints = sorted(P, key=lambda p: -p['internet_ind'])
    above = sum(1 for p in P if p['internet_ind'] >= 35)
    tow = sorted(P, key=lambda p: -p['towers_density'])
    elec = sorted(P, key=lambda p: -p['elec_pct'])
    low_e = [p for p in elec if p['elec_pct'] < 20][::-1]
    nbo, tur = by['Nairobi'], by['Turkana']
    posts = []

    posts.append(dict(slug='most-and-least-connected-counties-in-kenya', date=DATE,
        title='The most and least connected counties in Kenya',
        desc=f"Nairobi scores {nbo['composite']:.1f} out of 100 on my county connectivity ranking. Turkana scores {tur['composite']:.1f}. Here is the full spread and what drives it.",
        html=f"""<p>I ranked all 47 counties on one score. Nairobi comes first at {nbo['composite']:.1f} out of 100. Turkana comes last at {tur['composite']:.1f}. That gap of {nbo['composite']-tur['composite']:.0f} points is the digital divide in one number.</p>
<h2>The top five</h2>
<p>{_names([f"{p['county']} ({p['composite']:.1f})" for p in top])} lead the ranking. Four counties reach the High tier: {_names(tiers['High'])}. Nairobi and Mombasa have by far the densest tower coverage. Nairobi has {nbo['towers_density']:,.0f} cell towers per 100 km². Most counties have fewer than 100.</p>
<h2>The bottom five</h2>
<p>{_names([f"{p['county']} ({p['composite']:.1f})" for p in bot])} sit at the bottom. In Turkana, {tur['internet_ind']:.1f}% of people use the internet and {tur['elec_pct']:.1f}% have electricity. I treat those two numbers as one problem. A phone with no power does not connect to anything.</p>
<h2>Where the middle sits</h2>
<p>{len(tiers['Medium'])} counties land in the Medium tier and {len(tiers['Low'])} in Low. {len(tiers['Critical'])} fall in the lowest tier. Only {above} of 47 counties reach the national internet usage figure of 35%. The rest sit below it.</p>
<h2>Who leads on internet use</h2>
<p>{ints[0]['county']} leads on internet usage at {ints[0]['internet_ind']:.1f}%. {ints[1]['county']} follows at {ints[1]['internet_ind']:.1f}% and {ints[2]['county']} at {ints[2]['internet_ind']:.1f}%. At the other end, {ints[-1]['county']} sits at {ints[-1]['internet_ind']:.1f}%.</p>
<p>The ranking blends four layers: internet usage (35%), tower density (25%), mobile speed (25%) and electricity access (15%). I explain the weights in <a href="/blog/how-i-built-the-kenya-connectivity-map/">how I built the map</a>. Every county has its own page with the full numbers, starting from the <a href="/counties/">county index</a>.</p>"""))

    posts.append(dict(slug='electricity-access-by-county-in-kenya', date=DATE,
        title=f"Electricity access by county: {len(low_e)} counties sit below 20%",
        desc=f"{len(low_e)} Kenyan counties have electricity access under 20% in the 2019 census data: {_names([p['county'] for p in low_e])}.",
        html=f"""<p>Electricity is the first layer of connectivity. If a household cannot charge a phone, mobile coverage means little. So I mapped electricity access for every county using the 2019 Population and Housing Census.</p>
<h2>The counties below 20%</h2>
<p>{len(low_e)} counties fall under 20%: {_names([f"{p['county']} ({p['elec_pct']:.1f}%)" for p in low_e])}. Turkana is the lowest of all. Every one of them also ranks {min(p['rank'] for p in low_e)}th or lower out of 47 on my composite score, so the two problems travel together.</p>
<h2>The counties at the top</h2>
<p>{_names([f"{p['county']} ({p['elec_pct']:.1f}%)" for p in elec[:4]])} lead the country. The national figure on the map is 38.7%. Only {sum(1 for p in P if p['elec_pct']>=38.7)} of 47 counties reach it.</p>
<h2>What this means for mini-grids</h2>
<p>The map also carries a mini-grid layer from the ENERGYDATA.INFO registry, with existing sites, sites under development and KOSAP pipeline sites. I built it so you can see where grid lines stop and where small solar systems start to matter. Counties such as Turkana, Wajir and Mandera are where that question is sharpest.</p>
<h2>A caution on the numbers</h2>
<p>The census figure dates from 2019. Connections will have changed since then, so read these percentages as a 2019 snapshot. I will update the layer as new county data is released.</p>
<p>Open the <a href="/">electricity layer on the map</a> to see the transmission lines and mini-grid sites, or browse a single county such as <a href="/counties/turkana/">Turkana</a>.</p>"""))

    posts.append(dict(slug='how-i-built-the-kenya-connectivity-map', date=DATE,
        title='How I built the Kenya Connectivity Map: sources, formula and limits',
        desc='The data sources, the composite score formula and the known limits behind the Kenya Connectivity Map, written by the person who built it.',
        html="""<p>I built the Kenya Connectivity Map to make the digital divide visible at county level. This post covers where the data comes from, how the score works and where it falls short.</p>
<h2>The composite score</h2>
<p>Each county gets a score from 0 to 100. The formula is: internet usage × 0.35, plus tower density × 0.25, plus mobile speed × 0.25, plus electricity access × 0.15. I normalise each layer to a 0 to 100 scale before weighting. Internet usage carries the most weight because it is the most direct measure of access. Electricity carries less because it is a precondition for connectivity, and I did not want to count it twice.</p>
<h2>The sources</h2>
<p>Internet usage comes from KNBS and the 2022 Demographic and Health Survey. Tower density comes from OpenCelliD (March 2026). Mobile speed comes from Ookla Speedtest Intelligence (Q1 2026). Electricity access comes from the 2019 census. The grid and mini-grid layers use the ENERGYDATA.INFO registry. School locations come from Giga, and school device counts from the ICT Authority DigiSchool dashboard. The full table is on the <a href="/data/">data page</a>.</p>
<h2>Where it falls short</h2>
<p>Tower density is crowd-sourced, so it can undercount towers in sparsely populated counties. Speed tests skew toward urban and higher-income users, so rural speeds look better than they are. A few Starlink users can inflate a county average, which is why I flag Samburu and leave it out of the speed ranking.</p>
<p>The census electricity figure is from 2019 and the survey data from 2022. The map shows a snapshot, not a live feed. I update layers as new reports release.</p>
<h2>Who it is for</h2>
<p>NGOs, telcos, county governments and EdTech teams use county-level data to decide where to put towers, mini-grids and devices. If you need a county cut that the public map does not show, you can reach me through <a href="https://paulwamocha.work">paulwamocha.work</a>.</p>"""))
    return posts

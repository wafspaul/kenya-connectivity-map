"""Blog post bodies for tools/build_pages.py.
Every figure is computed from the map's own dataset. Style rules (Paul's anti AI cheat sheet):
first person, no dashes of any kind in visible text, no colon titles, no banned vocabulary.
"""
import statistics as st

DATE = '2026-10-06'
UTM = '?utm_source=kenya_connectivity_map&utm_medium=referral'
IMAGES = {
    'kicc': dict(id='1693902997450-7e912c0d3554', name='Kenny Murgor', user='kennymurgor', alt='Nairobi skyline with the KICC tower at the centre'),
    'nairobi_night': dict(id='1741991109902-98bf764fb35d', name='imsogabriel stock', user='imsogabriel', alt='Nairobi skyline lit up at night'),
    'nairobi_day': dict(id='1741991110666-88115e724741', name='imsogabriel stock', user='imsogabriel', alt='Panoramic view of Nairobi city on a sunny day'),
    'tower': dict(id='1660620949746-c0f2a54538ef', name='Zac Gudakov', user='zacgudakov', alt='Tall cell antenna tower against the sky'),
    'phone': dict(id='1697383904932-94304530a3dd', name='Hassan Kibwana', user='kb_photographic', alt='Woman in Nairobi smiling while holding a mobile phone'),
    'student': dict(id='1771412205065-6e8c5ec159bd', name='Mudadi Saidi', user='mudadisaidi', alt='Young ICT student holding a laptop'),
    'pylons': dict(id='1610028290816-5d937a395a49', name='Andrey Metelev', user='metelevan', alt='Electricity pylons silhouetted against a sunset'),
    'lamu': dict(id='1558907530-b6ac430f8a8c', name='Photos By Beks', user='photosbybeks', alt='Wooden boat resting on a shoreline in Kenya'),
    'fibre': dict(id='1594915440248-1e419eba6611', name='Kirill Sh', user='kirill2020', alt='Fibre optic cables plugged into a network switch in a server rack'),
    'substation': dict(id='1509390144018-eeaf65052242', name='American Public Power Association', user='publicpowerorg', alt='Large electrical transformer in a power substation'),
    'dish': dict(id='1745697213293-21d6c972ac1a', name='Bernd Dittrich', user='hdbernd', alt='Large satellite dish against a blue sky'),
}
NUM = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'}


def build(c):
    P, ordn, disp = c['P'], c['ordinal'], c['disp']
    by = {p['county']: p for p in P}
    D, E = c['D'], c['E']
    R_INT, R_ELEC = c['R_INT'], c['R_ELEC']

    def L(name, text=None):
        p = by[name]
        return f'<a href="/counties/{p["slug"]}/">{disp(text or name)}</a>'

    def names(xs): return ', '.join(xs[:-1]) + ' and ' + xs[-1]

    def table(headers, rows):
        h = ''.join(f'<th>{x}</th>' for x in headers)
        r = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in rows)
        return f'<div class="wrap"><table><tr>{h}</tr>{r}</table></div>'

    def src_note(text): return f'<p class="src">{text}</p>'

    tiers = {t: [p['county'] for p in P if p['tier'] == t] for t in ['High', 'Medium', 'Low', 'Critical']}
    nbo, tur = by['Nairobi'], by['Turkana']
    posts = []

    # ------------------------------------------------------------ 1 composite ranking
    top, bot = P[:5], P[::-1][:5]
    ints = sorted(P, key=lambda p: -p['internet_ind'])
    above = sum(1 for p in P if p['internet_ind'] >= 35)
    assert P[0]['county'] == 'Nairobi' and P[-1]['county'] == 'Turkana'
    posts.append(dict(
        slug='most-and-least-connected-counties-in-kenya', date=DATE, img='nairobi_night',
        title='The most and least connected counties in Kenya',
        desc=f"Nairobi scores {nbo['composite']:.1f} out of 100 on my county connectivity ranking and Turkana scores {tur['composite']:.1f}. See the full spread and what drives it.",
        faq=[("Which county is the most connected in Kenya?", f"Nairobi, with a composite score of {nbo['composite']:.1f} out of 100, followed by {P[1]['county']} ({P[1]['composite']:.1f}) and {P[2]['county']} ({P[2]['composite']:.1f})."),
             ("Which county is the least connected in Kenya?", f"Turkana, with a composite score of {tur['composite']:.1f} out of 100. {disp(bot[1]['county'])} ({bot[1]['composite']:.1f}) and {disp(bot[2]['county'])} ({bot[2]['composite']:.1f}) follow.")],
        html=f"""<p>I ranked all 47 counties on one score. Nairobi comes first at {nbo['composite']:.1f} out of 100. Turkana comes last at {tur['composite']:.1f}. That gap of {nbo['composite']-tur['composite']:.0f} points is the digital divide in one number.</p>
<h2>The top five</h2>
<p>{names([f"{L(p['county'])} ({p['composite']:.1f})" for p in top])} lead the ranking. Four counties reach the High tier: {names([L(x) for x in tiers['High']])}. Nairobi and Mombasa have by far the densest tower coverage. Nairobi has {nbo['towers_density']:,.0f} cell towers per 100 km². Most counties have fewer than 100.</p>
<h2>The bottom five</h2>
<p>{names([f"{L(p['county'])} ({p['composite']:.1f})" for p in bot])} sit at the bottom. In Turkana, {tur['internet_ind']:.1f}% of people use the internet and {tur['elec_pct']:.1f}% have electricity. I treat those two numbers as one problem. A phone with no power does not connect to anything.</p>
<h2>Where the middle sits</h2>
<p>{len(tiers['Medium'])} counties land in the Medium tier and {len(tiers['Low'])} in Low. {len(tiers['Critical'])} fall in the lowest tier. Only {above} of 47 counties reach the national internet usage figure of 35%. The rest sit below it.</p>
<h2>Who leads on internet use</h2>
<p>{L(ints[0]['county'])} leads on internet usage at {ints[0]['internet_ind']:.1f}%. {L(ints[1]['county'])} follows at {ints[1]['internet_ind']:.1f}% and {L(ints[2]['county'])} at {ints[2]['internet_ind']:.1f}%. At the other end, {L(ints[-1]['county'])} sits at {ints[-1]['internet_ind']:.1f}%. The <a href="/blog/internet-usage-in-kenya-by-county/">full internet usage table</a> covers all 47 counties.</p>
<p>The ranking blends four layers: internet usage (35% of the score), tower density (25%), mobile speed (25%) and electricity access (15%). I explain the weights in <a href="/blog/how-i-built-the-kenya-connectivity-map/">the post on the data, formula and limits</a>. Every county has its own page with the full numbers, starting from the <a href="/counties/">county index</a>."""))

    # ------------------------------------------------------------ 2 electricity
    elec = sorted(P, key=lambda p: -p['elec_pct'])
    low_e = [p for p in elec if p['elec_pct'] < 20][::-1]
    n_low = len(low_e)
    assert low_e[0]['county'] == 'Turkana' and elec[0]['county'] == 'Nairobi'
    posts.append(dict(
        slug='electricity-access-by-county-in-kenya', date=DATE, img='pylons',
        title=f"{NUM.get(n_low, str(n_low))} Kenyan counties have electricity access below 20%",
        desc=f"{n_low} Kenyan counties sit under 20% electricity access in the 2019 census, led by {disp(low_e[0]['county'])} at {low_e[0]['elec_pct']:.1f}%. See how the rest compare.",
        faq=[("Which Kenyan county has the lowest electricity access?", f"Turkana, at {tur['elec_pct']:.1f}% in the 2019 census data used on the map."),
             ("Which county has the highest electricity access in Kenya?", f"Nairobi, at {nbo['elec_pct']:.1f}%, followed by {elec[1]['county']} ({elec[1]['elec_pct']:.1f}%) and {elec[2]['county']} ({elec[2]['elec_pct']:.1f}%).")],
        html=f"""<p>Electricity is the first layer of connectivity. If a household cannot charge a phone, mobile coverage means little. So I mapped electricity access for every county using the 2019 Population and Housing Census.</p>
<h2>The counties below 20%</h2>
<p>{n_low} counties fall under 20%: {names([f"{L(p['county'])} ({p['elec_pct']:.1f}%)" for p in low_e])}. {L('Turkana')} is the lowest of all. Every one of them also ranks {min(p['rank'] for p in low_e)}th or lower out of 47 on my composite score, so the two problems travel together.</p>
<h2>The counties at the top</h2>
<p>{names([f"{L(p['county'])} ({p['elec_pct']:.1f}%)" for p in elec[:4]])} lead the country. The national figure on the map is 38.7%. Only {sum(1 for p in P if p['elec_pct']>=38.7)} of 47 counties reach it.</p>
<h2>What this means for mini grids</h2>
<p>The map also carries a mini grid layer from the ENERGYDATA.INFO registry, with existing sites, sites under development and KOSAP pipeline sites. I built it so you can see where grid lines stop and where small solar systems start to matter. Counties such as {L('Turkana')}, {L('Wajir')} and {L('Mandera')} are where that question is sharpest.</p>
<h2>A caution on the numbers</h2>
<p>The census figure dates from 2019. Connections will have changed since then, so read these percentages as a 2019 snapshot. I update the layer as new county data is released.</p>
<p>Open the <a href="/#county=turkana">electricity layer on the map</a> to see the transmission lines and mini grid sites. For internet use alongside power, read <a href="/blog/internet-usage-in-kenya-by-county/">internet use in Kenya by county</a>."""))

    # ------------------------------------------------------------ 3 method
    posts.append(dict(
        slug='how-i-built-the-kenya-connectivity-map', date=DATE, img=None,
        title='The data, formula and limits behind the Kenya Connectivity Map',
        desc='The data sources, the composite score formula and the known limits behind the Kenya Connectivity Map, written by the person who built it.',
        faq=[("How is the Kenya Connectivity Map composite score calculated?", "Internet usage counts for 35%, tower density 25%, mobile speed 25% and electricity access 15%. Each layer is scaled to 0 to 100 before weighting."),
             ("Where does the map get its data?", "KNBS and the 2022 Demographic and Health Survey, OpenCelliD, Ookla Speedtest Intelligence, the 2019 census, ENERGYDATA.INFO, Giga and the ICT Authority DigiSchool dashboard.")],
        html="""<p>I built the Kenya Connectivity Map to make the digital divide visible at county level. This post covers where the data comes from, how the score works and where it falls short.</p>
<h2>The composite score</h2>
<p>Each county gets a score from 0 to 100. Internet usage counts for 35%. Tower density counts for 25%, mobile speed for 25% and electricity access for 15%. I scale each layer to 0 to 100 before weighting. Internet usage carries the most weight because it is the most direct measure of access. Electricity carries less because it is a precondition for connectivity, and I did not want to count it twice.</p>
<h2>The sources</h2>
<p>Internet usage comes from <a href="https://www.knbs.or.ke/">KNBS</a> and the 2022 Demographic and Health Survey. Tower density comes from <a href="https://opencellid.org/">OpenCelliD</a> (March 2026). Mobile speed comes from <a href="https://www.ookla.com/">Ookla</a> Speedtest Intelligence (Q1 2026). Electricity access comes from the 2019 census. The grid and mini grid layers use the <a href="https://energydata.info/">ENERGYDATA.INFO</a> registry. School locations come from <a href="https://giga.global/">Giga</a>, and school device counts from the ICT Authority DigiSchool dashboard. The full table is on the <a href="/data/">data page</a>.</p>
<h2>Where it falls short</h2>
<p>Tower density is crowd sourced, so it can undercount towers in sparsely populated counties. Speed tests skew toward urban and higher income users, so rural speeds look better than they are. A few Starlink users can inflate a county average, which is why I flag Samburu and leave it out of the speed ranking.</p>
<p>The census electricity figure is from 2019 and the survey data from 2022. The map shows a snapshot, not a live feed. I update layers as new reports release.</p>
<h2>Who uses it</h2>
<p>NGOs, telcos, county governments and EdTech teams use county level data to decide where to put towers, mini grids and devices. If you need a county cut that the public map does not show, you can reach me through <a href="https://paulwamocha.work">paulwamocha.work</a>.</p>
<p>Each layer has its own write up: <a href="/blog/internet-usage-in-kenya-by-county/">internet use</a>, <a href="/blog/cell-tower-density-in-kenya-by-county/">tower density</a>, <a href="/blog/mobile-internet-speed-in-kenya-by-county/">mobile speed</a> and <a href="/blog/electricity-access-by-county-in-kenya/">electricity access</a>."""))

    # ------------------------------------------------------------ 4 internet usage by county
    ranked = sorted(P, key=lambda p: -p['internet_ind'])
    med = st.median(p['internet_ind'] for p in P)
    ratio = ranked[0]['internet_ind'] / ranked[-1]['internet_ind']
    gap = sorted(P, key=lambda p: R_ELEC[p['county']] - R_INT[p['county']])[::-1][:3]
    rows = [(str(i + 1), L(p['county']), f"{p['internet_ind']:.1f}%", f"{p['elec_pct']:.1f}%") for i, p in enumerate(ranked)]
    assert ranked[0]['county'] == 'Nairobi'
    posts.append(dict(
        slug='internet-usage-in-kenya-by-county', date=DATE, img='kicc',
        title='Internet use in Kenya by county',
        desc=f"{disp(ranked[0]['county'])} has {ranked[0]['internet_ind']:.1f}% internet use and {disp(ranked[-1]['county'])} has {ranked[-1]['internet_ind']:.1f}%. Full ranking of all 47 Kenyan counties from the 2022 survey.",
        faq=[("Which county in Kenya has the highest internet use?", f"{ranked[0]['county']}, where {ranked[0]['internet_ind']:.1f}% of people use the internet, followed by {ranked[1]['county']} ({ranked[1]['internet_ind']:.1f}%) and {ranked[2]['county']} ({ranked[2]['internet_ind']:.1f}%)."),
             ("Which county in Kenya has the lowest internet use?", f"{disp(ranked[-1]['county'])}, at {ranked[-1]['internet_ind']:.1f}%. {disp(ranked[-2]['county'])} ({ranked[-2]['internet_ind']:.1f}%) and {disp(ranked[-3]['county'])} ({ranked[-3]['internet_ind']:.1f}%) are next."),
             ("Where does the county internet data come from?", "The Kenya National Bureau of Statistics and the 2022 Kenya Demographic and Health Survey. It measures the share of individuals who use the internet.")],
        html=f"""<p>{L(ranked[0]['county'])} has the highest internet use in Kenya, with {ranked[0]['internet_ind']:.1f}% of people online. {L(ranked[-1]['county'])} has the lowest at {ranked[-1]['internet_ind']:.1f}%. The top county is {ratio:.1f} times the bottom one. Only {above} of 47 counties reach the 35% national figure I use on the map.</p>
<h2>Counties with the highest internet use</h2>
<p>{names([f"{L(p['county'])} ({p['internet_ind']:.1f}%)" for p in ranked[:6]])} make up the top six. Every other county sits below {ranked[5]['internet_ind']:.1f}%. The median county is at {med:.1f}%, so the leaders pull well clear of the pack.</p>
<h2>Counties with the lowest internet use</h2>
<p>{names([f"{L(p['county'])} ({p['internet_ind']:.1f}%)" for p in ranked[::-1][:6]])} sit at the bottom. In {L(ranked[-1]['county'])} fewer than one person in ten uses the internet.</p>
<h2>Internet use against electricity access</h2>
<p>Internet use and power access usually move together, but not always. {names([f"{L(p['county'])}, which ranks {ordn(R_INT[p['county']])} on internet use and {ordn(R_ELEC[p['county']])} on electricity" for p in gap])}. Those counties use the internet more than their power access would suggest. The <a href="/blog/electricity-access-by-county-in-kenya/">electricity access post</a> covers the other side of the pair.</p>
<h2>What the numbers measure</h2>
<p>The figures come from the 2022 Kenya Demographic and Health Survey, published through <a href="https://www.knbs.or.ke/">KNBS</a>. They count individuals who use the internet, not households with a connection. A survey samples people, so each county figure carries a margin of error. I use it because it is the most recent county level source I can find.</p>
<h2>Internet use in all 47 counties</h2>
{table(['Rank', 'County', 'Internet use', 'Electricity access'], rows)}
<p>Select any county for its own page, or open the <a href="/#county={ranked[0]['slug']}">interactive map</a> and switch to the Internet Usage layer.</p>"""))

    # ------------------------------------------------------------ 5 tower density
    tow = sorted(P, key=lambda p: -p['towers_density'])
    n_lt10 = sum(1 for p in P if p['towers_density'] < 10)
    n_lt1 = sum(1 for p in P if p['towers_density'] < 1)
    n_ge100 = sum(1 for p in P if p['towers_density'] >= 100)
    medt = st.median(p['towers_density'] for p in P)
    rows = [(str(i + 1), L(p['county']), f"{p['towers_density']:,.1f}", f"{p['area_sqkm']:,.0f}") for i, p in enumerate(tow)]
    low_t = tow[::-1][:5]
    assert tow[0]['county'] == 'Nairobi'
    posts.append(dict(
        slug='cell-tower-density-in-kenya-by-county', date=DATE, img='tower',
        title='Cell tower density in Kenya by county',
        desc=f"Nairobi has {nbo['towers_density']:,.0f} cell towers per 100 km² and {disp(low_t[0]['county'])} has {low_t[0]['towers_density']:.1f}. Full ranking of all 47 Kenyan counties from OpenCelliD data.",
        faq=[("Which Kenyan county has the most cell towers per area?", f"Nairobi, with {nbo['towers_density']:,.0f} towers per 100 km². {tow[1]['county']} is second at {tow[1]['towers_density']:,.0f}."),
             ("Which counties have the fewest cell towers per area?", f"{names([disp(p['county']) + ' (' + format(p['towers_density'], '.1f') + ')' for p in low_t[:3]])} towers per 100 km² are the lowest."),
             ("Where does the tower data come from?", "OpenCelliD, a crowd sourced database of cell towers. I use the March 2026 refresh.")],
        html=f"""<p>Nairobi has {nbo['towers_density']:,.0f} cell towers per 100 km². {L(low_t[0]['county'])} has {low_t[0]['towers_density']:.1f}. Part of the gap comes from geography, so I read density next to land area, not on its own.</p>
<h2>The densest counties</h2>
<p>{names([f"{L(p['county'])} ({p['towers_density']:,.0f})" for p in tow[:5]])} lead on towers per 100 km². {n_ge100} counties reach 100 or more. The median county has {medt:.0f}.</p>
<h2>The thinnest coverage</h2>
<p>{names([f"{L(p['county'])} ({p['towers_density']:.1f})" for p in low_t])} have the lowest tower density. {n_lt10} counties fall under 10 towers per 100 km² and {n_lt1} fall under one. {L('Turkana')} covers {tur['area_sqkm']:,.0f} km², about {tur['area_sqkm']/nbo['area_sqkm']:.0f} times the area of Nairobi. Its tower density is {tur['towers_density']:.1f}.</p>
<h2>Why density needs context</h2>
<p>A large county needs far more towers than a small one to post the same density. A low number in a big dry county means few towers are spread over a lot of land. Population weighted coverage would tell a fairer story, but the map does not carry population figures yet. For now, density is the cleanest measure I can source for every county.</p>
<h2>Where the data comes from</h2>
<p>I use <a href="https://opencellid.org/">OpenCelliD</a>, a crowd sourced database, with the March 2026 refresh. The map counts 144,834 towers nationally. Crowd sourcing can undercount towers in sparsely populated areas, so treat the lowest counties as a floor.</p>
<h2>Tower density in all 47 counties</h2>
{table(['Rank', 'County', 'Towers per 100 km²', 'Area (km²)'], rows)}
<p>Tower density counts for 25% of the composite score. Read how the score is built in <a href="/blog/how-i-built-the-kenya-connectivity-map/">the data, formula and limits post</a>, or open the <a href="/#county=nairobi">map</a> and switch to the Tower Density layer.</p>"""))

    # ------------------------------------------------------------ 6 mobile speed
    spd = sorted([p for p in P if not p['speed_flag']], key=lambda p: -p['speed_dl'])
    flagged = [p for p in P if p['speed_flag']][0]
    meds = st.median(p['speed_dl'] for p in spd)
    n25 = sum(1 for p in spd if p['speed_dl'] >= 25)
    n50 = sum(1 for p in spd if p['speed_dl'] >= 50)
    tests = sorted(P, key=lambda p: -p['speed_tests'])
    few = sorted(P, key=lambda p: p['speed_tests'])
    rows = [(str(i + 1), L(p['county']), f"{p['speed_dl']:.1f}", f"{p['speed_tests']:,}") for i, p in enumerate(spd)]
    assert spd[0]['county'] == 'Nairobi' and flagged['county'] == 'Samburu'
    assert by['Kitui']['speed_dl'] > by['Mombasa']['speed_dl'] and spd[1]['county'] == 'Kitui'
    posts.append(dict(
        slug='mobile-internet-speed-in-kenya-by-county', date=DATE, img='phone',
        title='Mobile internet speed in Kenya by county',
        desc=f"Nairobi averages {nbo['speed_dl']:.1f} Mbps on mobile and {disp(spd[-1]['county'])} averages {spd[-1]['speed_dl']:.1f}. Ranking of Kenyan counties by Q1 2026 Ookla download speed.",
        faq=[("Which Kenyan county has the fastest mobile internet?", f"Among counties with a reliable figure, Nairobi leads at {nbo['speed_dl']:.1f} Mbps, followed by {spd[1]['county']} ({spd[1]['speed_dl']:.1f}) and {spd[2]['county']} ({spd[2]['speed_dl']:.1f})."),
             ("Why is Samburu left out of the speed ranking?", f"Samburu shows {flagged['speed_dl']:.1f} Mbps, which would rank first, but a small number of Starlink users can lift a county average. I flag it and leave it out."),
             ("Where does the speed data come from?", "Ookla Speedtest Intelligence for Q1 2026, aggregated to county level.")],
        html=f"""<p>Nairobi has the fastest mobile internet among Kenyan counties with a reliable figure, at {nbo['speed_dl']:.1f} Mbps average download. {L(spd[-1]['county'])} is slowest at {spd[-1]['speed_dl']:.1f} Mbps. The median county sits at {meds:.1f} Mbps, and {n25} of {len(spd)} counties reach 25 Mbps.</p>
<h2>The fastest counties</h2>
<p>{names([f"{L(p['county'])} ({p['speed_dl']:.1f} Mbps)" for p in spd[:5]])} lead the table. Only {n50} counties pass 50 Mbps. {L('Kitui')} ranks second at {by['Kitui']['speed_dl']:.1f} Mbps, ahead of {L('Mombasa')} at {by['Mombasa']['speed_dl']:.1f}, which surprised me. Only {by['Kitui']['speed_tests']:,} tests sit behind Kitui's figure, against {by['Mombasa']['speed_tests']:,} for Mombasa, so a handful of fast connections can move it. It is a reminder that speed tests reflect who ran a test.</p>
<h2>The slowest counties</h2>
<p>{names([f"{L(p['county'])} ({p['speed_dl']:.1f})" for p in spd[::-1][:5]])} have the slowest average downloads. The fastest county is about {spd[0]['speed_dl']/spd[-1]['speed_dl']:.1f} times as fast as the slowest.</p>
<h2>Why I leave Samburu out</h2>
<p>Samburu shows {flagged['speed_dl']:.1f} Mbps, which would put it first by a wide margin. Its tower density is {flagged['towers_density']:.1f} per 100 km² and its internet use is {flagged['internet_ind']:.1f}%. Those numbers do not fit a county with the fastest mobile internet in the country. A few Starlink users in a small sample can lift an average, so I flag Samburu and drop it from the ranking.</p>
<h2>How many tests sit behind each number</h2>
<p>The sample size varies enormously. {L(tests[0]['county'])} has {tests[0]['speed_tests']:,} tests and {L(tests[1]['county'])} has {tests[1]['speed_tests']:,}. {L(few[0]['county'])} has {few[0]['speed_tests']:,} and {L(few[1]['county'])} has {few[1]['speed_tests']:,}. A figure built on a hundred tests is weaker than one built on ten thousand, and speed tests skew toward urban and higher income users. I expect rural speeds to be lower than shown.</p>
<h2>Mobile speed in all counties with a reliable figure</h2>
{table(['Rank', 'County', 'Average download (Mbps)', 'Speed tests'], rows)}
{src_note('Source: Ookla Speedtest Intelligence, Q1 2026, aggregated to county level. Samburu is flagged and excluded.')}
<p>Speed counts for 25% of the composite score. The <a href="/blog/cell-tower-density-in-kenya-by-county/">tower density post</a> covers the other half of the network picture. You can also open the <a href="/#county=nairobi">map</a> and switch to the Speed layer.</p>"""))

    # ------------------------------------------------------------ 7 DLP devices
    tot = sum(d['total'] for d in D.values()); ins = sum(d['installed'] for d in D.values())
    lrn = sum(d['learner'] for d in D.values()); tch = sum(d['teacher'] for d in D.values())
    dl = sorted(D.items(), key=lambda kv: kv[1]['pct'])
    n99 = sum(1 for d in D.values() if d['pct'] >= 99)
    cnt = c['counts']
    sch_total = sum(sum(v) for v in cnt.values())
    big = sorted(((sum(v), k) for k, v in cnt.items()), reverse=True)[:3]
    rows = [(L(k), f"{d['installed']:,}", f"{d['total']:,}", f"{d['pct']:.1f}%") for k, d in sorted(D.items(), key=lambda kv: kv[0])]
    assert dl[3][1]['pct'] > 97
    posts.append(dict(
        slug='digital-literacy-programme-devices-by-county', date=DATE, img='student',
        title='Digital Literacy Programme devices in Kenyan schools by county',
        desc=f"{ins:,} of {tot:,} primary schools have Digital Literacy Programme devices installed. {disp(dl[0][0])} sits lowest at {dl[0][1]['pct']:.1f}%. County by county table.",
        faq=[("How many Kenyan primary schools have Digital Literacy Programme devices?", f"The ICT Authority DigiSchool dashboard shows {ins:,} of {tot:,} primary schools with devices installed, which is {ins/tot*100:.1f}%."),
             ("Which county has the lowest device installation rate?", f"{disp(dl[0][0])}, at {dl[0][1]['pct']:.1f}%, followed by {disp(dl[1][0])} ({dl[1][1]['pct']:.1f}%).")],
        html=f"""<p>The ICT Authority DigiSchool dashboard shows {ins:,} of {tot:,} primary schools with Digital Literacy Programme devices installed. That is {ins/tot*100:.1f}% nationally. The headline is strong. The county detail shows where the last schools are.</p>
<h2>The counties still catching up</h2>
<p>{L(dl[0][0])} has the lowest installation rate at {dl[0][1]['pct']:.1f}%, with {dl[0][1]['installed']:,} of {dl[0][1]['total']:,} schools covered. {L(dl[1][0])} follows at {dl[1][1]['pct']:.1f}%. After those two, {L(dl[2][0])} is at {dl[2][1]['pct']:.1f}%, and every other county is above 97%. {n99} counties are at 99% or higher.</p>
<h2>What the programme has put in schools</h2>
<p>The dashboard counts {lrn:,} learner devices and {tch:,} teacher devices, plus routers and projectors in each county. A router in a school is not the same as a working connection. The map shows device installation only. Whether each school is online is a separate question that this data does not answer.</p>
<h2>Where the schools are</h2>
<p>I also map {sch_total:,} geolocated schools from <a href="https://giga.global/">Giga</a>. {names([f"{L(k)} ({n:,})" for n, k in big])} have the most. The schools layer on the map shows primary and secondary schools as clusters you can zoom into.</p>
<h2>Device installation in all 47 counties</h2>
{table(['County', 'Schools with devices', 'Schools in programme', 'Installed'], rows)}
{src_note('Source: ICT Authority DigiSchool dashboard, 2026. Device counts describe installation, not connectivity.')}
<p>Open the <a href="/#county={by['Samburu']['slug']}">schools layer on the map</a> to see the counties above on the ground. A device needs power before it needs a signal, so read <a href="/blog/electricity-access-by-county-in-kenya/">electricity access by county</a> next.</p>"""))

    # ------------------------------------------------------------ 8 unemployment
    er = sorted(E.items(), key=lambda kv: -kv[1]['rate'])
    top10 = [p['county'] for p in P[:10]]; bot10 = [p['county'] for p in P[-10:]]
    a_top = st.mean(E[x]['rate'] for x in top10); a_bot = st.mean(E[x]['rate'] for x in bot10)
    lf = sorted(E.items(), key=lambda kv: -kv[1]['lfpr'])
    seek = sum(v['seeking'] for v in E.values()); work = sum(v['working'] for v in E.values())
    natl = seek / (seek + work) * 100
    rows = [(L(k), f"{v['rate']:.1f}%", f"{v['lfpr']:.1f}%", ordn(by[k]['rank'])) for k, v in sorted(E.items(), key=lambda kv: kv[0])]
    assert er[0][0] == 'Garissa'
    top3 = er[:3]
    posts.append(dict(
        slug='unemployment-rate-in-kenya-by-county', date=DATE, img='nairobi_day',
        title='Unemployment rate in Kenya by county, 2019 census',
        desc=f"{disp(er[0][0])} has the highest unemployment rate at {er[0][1]['rate']:.1f}% and {disp(er[-1][0])} the lowest at {er[-1][1]['rate']:.1f}%. All 47 Kenyan counties from the 2019 census.",
        faq=[("Which county in Kenya has the highest unemployment rate?", f"{disp(er[0][0])}, at {er[0][1]['rate']:.1f}% in the 2019 census, followed by {disp(er[1][0])} ({er[1][1]['rate']:.1f}%) and {disp(er[2][0])} ({er[2][1]['rate']:.1f}%)."),
             ("Which county has the lowest unemployment rate?", f"{disp(er[-1][0])}, at {er[-1][1]['rate']:.1f}%. {disp(er[-2][0])} ({er[-2][1]['rate']:.1f}%) is next.")],
        html=f"""<p>{L(er[0][0])} has the highest unemployment rate in Kenya at {er[0][1]['rate']:.1f}%. {L(er[-1][0])} has the lowest at {er[-1][1]['rate']:.1f}%. These are 2019 census figures on the ILO definition, and across all counties the rate works out to {natl:.1f}%.</p>
<h2>The highest unemployment counties</h2>
<p>{names([f"{L(k)} ({v['rate']:.1f}%)" for k, v in er[:5]])} lead the table. {names([disp(k) for k, v in top3])} sit far above the rest, and they rank {names([ordn(by[k]['rank']) for k, v in top3])} of 47 on my connectivity score.</p>
<h2>The lowest unemployment counties</h2>
<p>{names([f"{L(k)} ({v['rate']:.1f}%)" for k, v in er[::-1][:5]])} have the lowest rates. A low rate counts people who are looking for work and cannot find it. It does not tell you how many jobs pay well.</p>
<h2>Does connectivity change the picture</h2>
<p>The ten best connected counties on my composite score average {a_top:.1f}% unemployment. The ten least connected average {a_bot:.1f}%. The pattern is not a straight line, because {L('Mombasa')} ranks {ordn(by['Mombasa']['rank'])} on connectivity and still has {E['Mombasa']['rate']:.1f}% unemployment. Labour force participation is close between the two groups, with {st.mean(E[x]['lfpr'] for x in top10):.1f}% in the top ten and {st.mean(E[x]['lfpr'] for x in bot10):.1f}% in the bottom ten.</p>
<h2>Highest labour force participation</h2>
<p>{names([f"{L(k)} ({v['lfpr']:.1f}%)" for k, v in lf[:4]])} have the highest share of adults in the labour force. {L(lf[-1][0])} has the lowest at {lf[-1][1]['lfpr']:.1f}%.</p>
<h2>Unemployment and participation in all 47 counties</h2>
{table(['County', 'Unemployment rate', 'Labour force participation', 'Connectivity rank'], rows)}
{src_note('Source: 2019 Kenya Population and Housing Census, Volume IV, Table 2.8a (KNBS). Connectivity rank is out of 47 on my composite score.')}
<p>The census is from 2019, so these figures predate recent changes in the job market. I will update the layer when KNBS publishes newer county data. Open the <a href="/#county=garissa">employment layer on the map</a> to see the counties side by side.</p>"""))

    # ------------------------------------------------------------ 9 Lamu and the refinery
    lam = by['Lamu']
    R_TOW_L = sorted(P, key=lambda p: -p['towers_density']).index(lam) + 1
    medt2 = st.median(p['towers_density'] for p in P)
    lam_sch = sum(c['counts']['Lamu'])
    assert lam['rank'] == 36 and lam['tier'] == 'Low' and R_ELEC['Lamu'] == 12 and R_INT['Lamu'] == 27
    posts.append(dict(
        stitle='Lamu connectivity data as the refinery breaks ground',
        slug='lamu-county-connectivity-and-the-lamu-refinery', date=DATE, img='lamu',
        title='What the connectivity data says about Lamu as the refinery breaks ground',
        desc=f"Lamu ranks {ordn(lam['rank'])} of 47 on connectivity, with {lam['elec_pct']:.1f}% electricity access but only {lam['towers_density']:.1f} cell towers per 100 km². The county data behind the refinery news.",
        faq=[("How connected is Lamu County?", f"Lamu ranks {ordn(lam['rank'])} of 47 counties on my composite score at {lam['composite']:.1f} out of 100, in the Low tier. Electricity access is {lam['elec_pct']:.1f}% and internet use is {lam['internet_ind']:.1f}%."),
             ("Where is the Lamu refinery being built?", "Business Daily reported that Aliko Dangote broke ground on the refinery in Lamu on 30 September 2026. The articles I could read in full do not name the exact site, so I do not map it.")],
        html=f"""<p>Business Daily reported that Aliko Dangote broke ground on a Sh2 trillion refinery in Lamu on 30 September 2026. A companion report puts the cost at Sh2.1 trillion, a capacity of 700,000 barrels a day and about 60,000 jobs. I read what I could of both pieces, and the exact site, timeline and infrastructure plans sit behind a paywall. So I will not guess at them. What I can do is show you the county the project lands in. The headline sources are <a href="https://www.businessdailyafrica.com/bd/corporate/boss-talk/dangote-breaks-ground-on-sh2trn-lamu-refinery-5616362" rel="noopener">the report on the ceremony</a> and <a href="https://www.businessdailyafrica.com/bd/corporate/industry/early-winners-as-lamu-refinery-project-kicks-off-5615178" rel="noopener">the early winners piece</a>.</p>
<h2>Where Lamu sits today</h2>
<p>{L('Lamu')} ranks {ordn(lam['rank'])} of 47 counties on my composite score, at {lam['composite']:.1f} out of 100. That puts it in the Low tier. Its {lam['area_sqkm']:,.0f} km² hold {lam_sch:,} schools in the Giga data.</p>
<h2>Power is the strong layer</h2>
<p>{lam['elec_pct']:.1f}% of Lamu households have electricity in the 2019 census data. That ranks {ordn(R_ELEC['Lamu'])} of 47 and sits well above the national figure of 38.7%. Of the layers I map, this is where Lamu does best.</p>
<h2>Towers and internet use lag behind</h2>
<p>Tower density is {lam['towers_density']:.1f} per 100 km², which ranks {ordn(R_TOW_L)} of 47. The median county has {medt2:.0f}. Internet use is {lam['internet_ind']:.1f}%, in {ordn(R_INT['Lamu'])} place and below the 35% national figure. A county with this much power and this little coverage has a mismatch worth looking at first.</p>
<h2>A speed figure to read with care</h2>
<p>Lamu averages {lam['speed_dl']:.1f} Mbps on mobile, but only {lam['speed_tests']:,} speed tests sit behind that number. {by['Nairobi']['speed_tests']:,} tests sit behind the Nairobi figure. I treat a figure built on {lam['speed_tests']:,} tests as a hint, not a measurement.</p>
<h2>What I would watch next</h2>
<p>A refinery brings contractors, workers and suppliers who all need reliable mobile and fibre links. The question for planners is whether coverage grows at the pace the construction does. I will update this page when the project publishes site plans or utility requirements. Until then the county numbers are the baseline to measure against.</p>
{table(['Measure', 'Lamu', 'Rank of 47'], [('Composite score', f"{lam['composite']:.1f}", ordn(lam['rank'])), ('Electricity access', f"{lam['elec_pct']:.1f}%", ordn(R_ELEC['Lamu'])), ('Internet use', f"{lam['internet_ind']:.1f}%", ordn(R_INT['Lamu'])), ('Cell towers per 100 km²', f"{lam['towers_density']:.1f}", ordn(R_TOW_L)), ('Unemployment rate (2019)', f"{E['Lamu']['rate']:.1f}%", ordn(sorted(E, key=lambda k: -E[k]['rate']).index('Lamu') + 1))])}
<p>For the full county view, open the <a href="/counties/lamu/">Lamu county page</a> or read <a href="/blog/cell-tower-density-in-kenya-by-county/">tower density across all 47 counties</a>."""))

    # ------------------------------------------------------------ 10 fibre tender
    low8 = [p for p in P if p['tier'] == 'Critical']
    low8.sort(key=lambda p: p['composite'])
    assert len(low8) == 8 and max(p['internet_ind'] for p in low8) < 35
    rows = [(L(p['county']), f"{p['composite']:.1f}", f"{p['internet_ind']:.1f}%", f"{p['towers_density']:.1f}", f"{p['area_sqkm']:,.0f}") for p in low8]
    posts.append(dict(
        stitle="Kenya's $390 million fibre tender and who needs it",
        slug='kenya-fibre-tender-and-the-least-connected-counties', date=DATE, img='fibre',
        title='Kenya opens a $390 million fibre tender. Which counties need it most?',
        desc=f"ICTA's World Bank funded fibre tender closes 29 October 2026. These {len(low8)} counties sit at the bottom of my connectivity ranking.",
        faq=[("What is the ICTA fibre tender?", "ICTA opened an international tender on 16 September 2026 under the Kenya Digital Economy Acceleration Project. The World Bank is financing it with USD 390 million in credits. Lot 1 covers national backbone links and Lot 2 covers cross border and metro links."),
             ("When do bids close?", "Bids close on 29 October 2026 at 10:00 a.m. East African Time at Telposta Towers in Nairobi, according to TechAfrica News.")],
        html=f"""<p>The Information and Communications Technology Authority opened an international tender on 16 September 2026 to expand the national fibre backbone and cross border links. <a href="https://techafricanews.com/2026/09/16/kenya-icta-tender-national-fibre-cross-border-connectivity/" rel="noopener">TechAfrica News reports</a> that the World Bank is financing it with USD 390 million in credits under the Kenya Digital Economy Acceleration Project. Bids close on 29 October 2026.</p>
<h2>What the tender covers</h2>
<p>Lot 1 covers national backbone links, and ICTA plans to appoint between 5 and 20 providers. Lot 2 covers cross border and metro links, with 5 to 8 providers. Winning providers compete for subsidies on designated routes through a reverse auction. Public sector fibre grew from 22,486 km in 2022 to more than 30,400 km today, and the stated target is 100,000 km.</p>
<h2>What nobody has published yet</h2>
<p>The route lists for each lot are not public in the sources I have. That means I cannot tell you which counties will get new fibre. I will add the routes to the map when ICTA names winners and publishes them.</p>
<h2>The counties to check the routes against</h2>
<p>When the routes appear, the first question is whether they reach the counties at the bottom of the ranking. {len(low8)} counties fall in my lowest tier: {names([L(p['county']) for p in low8])}. Together they cover {sum(p['area_sqkm'] for p in low8):,.0f} km², about {sum(p['area_sqkm'] for p in low8)/sum(p['area_sqkm'] for p in P)*100:.0f}% of the country. Not one of them reaches the 35% national internet use figure. {L('Turkana')} sits last at {tur['composite']:.1f}.</p>
{table(['County', 'Composite', 'Internet use', 'Towers per 100 km²', 'Area (km²)'], rows)}
<h2>Why backbone fibre is only half the answer</h2>
<p>Backbone fibre feeds towers. A county with 0.4 towers per 100 km² needs more of them as well as the cable. It also needs power to run them, and {L('Turkana')}, {L('Wajir')} and {L('Mandera')} all sit below 20% electricity access. The <a href="/blog/electricity-access-by-county-in-kenya/">electricity post</a> covers that side.</p>
<p>I will update this post when ICTA names the winners. The county ranking is on the <a href="/blog/most-and-least-connected-counties-in-kenya/">most and least connected counties</a> page."""))

    # ------------------------------------------------------------ 11 coast substations
    kil, kwa, mom = by['Kilifi'], by['Kwale'], by['Mombasa']
    assert kil['elec_pct'] < 38.7 and kwa['elec_pct'] < 38.7
    posts.append(dict(
        stitle='Kilifi and Kwale substations and electricity access',
        slug='kilifi-and-kwale-substations-and-electricity-access', date=DATE, img='substation',
        title='Two new Coast substations, and what Kilifi and Kwale electricity access looks like',
        desc=f"Kenya Power is building Sh765 million of substations in Kilifi and Kwale. Electricity access is {kil['elec_pct']:.1f}% in Kilifi and {kwa['elec_pct']:.1f}% in Kwale, against {mom['elec_pct']:.1f}% in Mombasa.",
        faq=[("What substations is Kenya Power building at the Coast?", "A Sh455 million 132/33kV substation at Bomani in Kilifi County and a Sh310 million 33/11kV substation in Kwale County, together Sh765 million, according to The Star."),
             ("What is electricity access in Kilifi and Kwale?", f"{kil['elec_pct']:.1f}% in Kilifi and {kwa['elec_pct']:.1f}% in Kwale in the 2019 census data on the map, against a national figure of 38.7%.")],
        html=f"""<p>Kenya Power is putting Sh765 million into two substations at the Coast, according to <a href="https://www.the-star.co.ke/news/2026-09-07-kplc-invests-sh765m-in-new-coast-substations" rel="noopener">The Star</a>. The company says demand is outrunning existing capacity.</p>
<h2>The two projects</h2>
<p>The first is a Sh455 million 132/33kV substation at Bomani in Kilifi. It will serve Kikambala, Vipingo, Kanamai and Mtwapa, areas now fed from the Kilifi and Bamburi substations. The Star says Kenya Power is nearing completion. The second is a Sh310 million 33/11kV substation in Kwale with four feeders. It will serve the county headquarters, Kinango, Tiwi and Kombani, and take pressure off the Diani substation. The article gives no completion dates.</p>
<h2>What the map shows for the two counties</h2>
<p>{L('Kilifi')} has {kil['elec_pct']:.1f}% electricity access, which ranks {ordn(R_ELEC['Kilifi'])} of 47. {L('Kwale')} has {kwa['elec_pct']:.1f}% and ranks {ordn(R_ELEC['Kwale'])}. Both sit below the national 38.7%. Next door, {L('Mombasa')} reaches {mom['elec_pct']:.1f}%. The Coast has a gap inside it.</p>
<h2>Capacity and access are different problems</h2>
<p>A new substation protects the supply of people who already have a connection. It does not by itself raise the share of households connected. Kenya Power describes these projects as capacity and reliability work, driven by industrial and commercial growth spilling out of Mombasa. That is good news for the businesses in Vipingo and Mtwapa. The households in the rest of both counties need a connection programme too.</p>
<h2>Connectivity in both counties</h2>
<p>{L('Kilifi')} ranks {ordn(kil['rank'])} overall at {kil['composite']:.1f}, with {kil['internet_ind']:.1f}% internet use. {L('Kwale')} ranks {ordn(kwa['rank'])} at {kwa['composite']:.1f}, with {kwa['internet_ind']:.1f}% internet use. Kwale posts a mobile average of {kwa['speed_dl']:.1f} Mbps from {kwa['speed_tests']:,} tests, the third fastest on the map. Kilifi averages {kil['speed_dl']:.1f} Mbps.</p>
{table(['Measure', 'Kilifi', 'Kwale', 'Mombasa'], [('Electricity access', f"{kil['elec_pct']:.1f}%", f"{kwa['elec_pct']:.1f}%", f"{mom['elec_pct']:.1f}%"), ('Internet use', f"{kil['internet_ind']:.1f}%", f"{kwa['internet_ind']:.1f}%", f"{mom['internet_ind']:.1f}%"), ('Cell towers per 100 km²', f"{kil['towers_density']:.1f}", f"{kwa['towers_density']:.1f}", f"{mom['towers_density']:,.0f}"), ('Composite rank', ordn(kil['rank']), ordn(kwa['rank']), ordn(mom['rank']))])}
{src_note('Electricity access is from the 2019 census. Substation details are from The Star, 7 September 2026.')}
<p>For the full ranking by power, read <a href="/blog/electricity-access-by-county-in-kenya/">electricity access by county</a>."""))

    # ------------------------------------------------------------ 12 satellite to phone
    sparse = sorted([p for p in P if p['towers_density'] < 2], key=lambda p: p['towers_density'])
    assert len(sparse) >= 5
    rows = [(L(p['county']), f"{p['towers_density']:.1f}", f"{p['area_sqkm']:,.0f}", f"{p['internet_ind']:.1f}%", f"{p['elec_pct']:.1f}%") for p in sparse]
    posts.append(dict(
        stitle="Satellite to phone service and Kenya's sparse counties",
        slug='satellite-to-phone-service-and-kenyas-sparse-counties', date=DATE, img='dish',
        title='Satellite to phone service could reach the counties towers miss',
        desc=f"Airtel says its Starlink satellite to phone service is ready, pending approval. {len(sparse)} counties have fewer than two cell towers per 100 km². Here they are.",
        faq=[("What is Airtel's satellite to phone service?", "Airtel Kenya plans a Starlink Direct to Cell service that connects ordinary 4G and 5G smartphones to satellites outside terrestrial coverage. TechTrendsKE reported on 4 August 2026 that it was ready and waiting for approval from the Communications Authority of Kenya."),
             ("Which counties have the fewest cell towers per area?", f"{names([disp(p['county']) + ' (' + format(p['towers_density'], '.1f') + ')' for p in sparse[:4]])} towers per 100 km² are the lowest on the map.")],
        html=f"""<p>Airtel Kenya says its satellite to phone service is ready to launch once the Communications Authority of Kenya approves it. <a href="https://techtrendske.co.ke/2026/08/04/airtel-kenya-satellite-to-phone-service/" rel="noopener">TechTrendsKE reported</a> on 4 August 2026 that the service uses Starlink Direct to Cell satellites, that a pilot has finished, and that no launch date exists. I did not find an approval announcement when I checked.</p>
<h2>How it would work</h2>
<p>Compatible 4G and 5G phones would switch to a satellite link when they leave mobile coverage, with no dish or new device. Earlier trials covered messaging and light data, including WhatsApp and Airtel Money. The article describes it as a complement to the mobile network, not a replacement.</p>
<h2>The counties with the thinnest tower coverage</h2>
<p>{len(sparse)} counties have fewer than two cell towers per 100 km²: {names([L(p['county']) for p in sparse])}. {L(sparse[0]['county'])} is the thinnest at {sparse[0]['towers_density']:.1f}. These are the places where a phone leaves coverage fastest, and the places a satellite link would matter most.</p>
{table(['County', 'Towers per 100 km²', 'Area (km²)', 'Internet use', 'Electricity access'], rows)}
<h2>A phone still needs power</h2>
<p>Satellite coverage solves the signal and leaves the charger problem. Electricity access in these counties runs from {min(p['elec_pct'] for p in sparse):.1f}% to {max(p['elec_pct'] for p in sparse):.1f}%. A phone that cannot be charged at home will not use a satellite link for long. Mini grids and solar matter as much as the launch.</p>
<h2>How I will treat it on the map</h2>
<p>Tower counts will not capture satellite access once it launches. The map will need a separate coverage category once the Communications Authority decides, so it does not call a county unserved when a satellite link covers it. Read <a href="/blog/cell-tower-density-in-kenya-by-county/">tower density across all 47 counties</a> for the baseline."""))

    # ------------------------------------------------------------ 13 power versus internet
    import statistics as _st
    corr = _st.correlation([p['elec_pct'] for p in P], [p['internet_ind'] for p in P])
    pwr = sorted(P, key=lambda p: R_ELEC[p['county']] - R_INT[p['county']])[:5]
    net = sorted(P, key=lambda p: R_INT[p['county']] - R_ELEC[p['county']])[:5]
    rows = [(L(p['county']), ordn(R_ELEC[p['county']]), ordn(R_INT[p['county']])) for p in pwr]
    rows2 = [(L(p['county']), ordn(R_ELEC[p['county']]), ordn(R_INT[p['county']])) for p in net]
    posts.append(dict(
        stitle='Kenyan counties with power but little internet',
        slug='counties-with-power-but-little-internet', date=DATE, img='phone',
        title='Kenyan counties with power but little internet, and the other way round',
        desc=f"Electricity and internet use move together across Kenya's counties, with a correlation of {corr:.2f}. These counties break the pattern, from {disp(pwr[0]['county'])} to {disp(net[0]['county'])}.",
        faq=[("Do counties with more electricity have more internet use?", f"Yes, mostly. Across the 47 counties the correlation between electricity access and internet use is {corr:.2f}, where 1.00 would be a perfect match."),
             ("Which county has more electricity than internet use would suggest?", f"{disp(pwr[0]['county'])} ranks {ordn(R_ELEC[pwr[0]['county']])} on electricity access but {ordn(R_INT[pwr[0]['county']])} on internet use.")],
        html=f"""<p>Power and internet use travel together across Kenya. The correlation between the two across all 47 counties is {corr:.2f}, which is strong. The exceptions are where the story gets useful, because each one points to a different fix.</p>
<h2>Power ahead of internet use</h2>
<p>These counties rank much higher on electricity than on internet use: {names([f"{L(p['county'])} ({ordn(R_ELEC[p['county']])} on power, {ordn(R_INT[p['county']])} on internet)" for p in pwr])}. Electricity is not what holds them back. Devices, data prices, skills and tower coverage are the likelier causes, and the survey data cannot tell me which.</p>
{table(['County', 'Electricity rank', 'Internet use rank'], rows)}
<h2>Internet use ahead of power</h2>
<p>These counties run the other way: {names([f"{L(p['county'])} ({ordn(R_INT[p['county']])} on internet, {ordn(R_ELEC[p['county']])} on power)" for p in net])}. People there get online despite thinner grid access, probably by charging phones away from home or from solar. Better power would raise a ceiling these counties are already pushing against.</p>
{table(['County', 'Electricity rank', 'Internet use rank'], rows2)}
<h2>What the pattern means for planners</h2>
<p>A single connectivity target hides two different jobs. In the first group the work is demand: affordable devices, digital skills and coverage. In the second it is supply: connections, mini grids and reliable charging. The <a href="/blog/most-and-least-connected-counties-in-kenya/">composite score</a> blends them, so I read the two ranks side by side before I draw a conclusion about any one county.</p>
<h2>A caution on the data</h2>
<p>Electricity access comes from the 2019 census and internet use from the 2022 survey, so the two layers are three years apart. A county that connected households after 2019 will look worse on power than it is today. Each full table is in <a href="/blog/internet-usage-in-kenya-by-county/">internet use by county</a> and <a href="/blog/electricity-access-by-county-in-kenya/">electricity access by county</a>."""))

    return posts

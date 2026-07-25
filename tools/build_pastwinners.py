#!/usr/bin/env python3
"""Build past-winners.html — the compiled archive of every awards year."""
import glob, importlib.util, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as _seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
YEARS = ['2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2014']


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def load_year(y):
    spec = importlib.util.spec_from_file_location('yd', os.path.join(ROOT, 'tools', 'yeardata', f'y{y}.py'))
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    return d


def find_cover(year, title):
    covers = {norm(os.path.splitext(os.path.basename(f))[0]): f'assets/covers/{year}/' + os.path.basename(f)
              for f in glob.glob(os.path.join(SITE, f'assets/covers/{year}/*.jpg'))}
    t = norm(title)
    if t in covers:
        return covers[t]
    for k, v in covers.items():
        if k.startswith(t) or t.startswith(k):
            return v
    return None


# ---------------- chrome ----------------
index = open(os.path.join(SITE, 'index.html')).read()
style = re.search(r'<style>.*?</style>', index, re.S).group(0)
header = re.search(r'<div class="rainbow">.*?</nav>', index, re.S).group(0)
footer = re.search(r'<!-- NEWSLETTER -->.*?</footer>', index, re.S).group(0)
for frag in ('#about', '#winners', '#archive', '#roundups', '#enter', '#faq-link', '#video', '#podcast'):
    header = header.replace(f'href="{frag}"', f'href="index.html{frag}"')
    footer = footer.replace(f'href="{frag}"', f'href="index.html{frag}"')
header = header.replace('<a class="nav-logo" href="#">', '<a class="nav-logo" href="index.html">')

WAVE = "M0,26 C240,46 480,6 720,24 C960,42 1200,10 1440,26 L1440,0 L0,0 Z"
def wave(prev, nxt):
    return (f'<div class="wave" style="background:{nxt}" aria-hidden="true">'
            f'<svg viewBox="0 0 1440 48" preserveAspectRatio="none"><path fill="{prev}" d="{WAVE}"/></svg></div>')
YEL, BLK, WHT, CRM = '#F7C731', '#161616', '#ffffff', '#FBF8F1'

extra_css = """
  /* ---------- Past Winners archive ---------- */
  .pw-hero{background:var(--yellow);padding:120px 6vw 90px;}
  .pw-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.3fr .7fr;gap:60px;align-items:center;}
  .pw-hero h1{font-size:clamp(2.3rem,4.6vw,3.7rem);line-height:1.06;text-transform:uppercase;font-weight:900;}
  .pw-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.18rem;line-height:1.7;margin-top:24px;max-width:600px;}
  .pw-hero .hero-stamp img{width:100%;max-width:250px;transform:rotate(-8deg);filter:drop-shadow(0 18px 32px rgba(0,0,0,.14));margin:0 auto;display:block;}
  .pw-year{padding:80px 32px;}
  .pw-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:200px 1fr;gap:50px;align-items:start;}
  .pw-yr{font-family:var(--disp);font-weight:900;font-size:clamp(2.6rem,4.5vw,3.6rem);line-height:1;border-bottom:8px solid var(--yellow);display:inline-block;}
  .pw-count{font-family:var(--serif);font-style:italic;color:#666;margin-top:14px;font-size:.95rem;}
  .pw-summary{font-family:var(--serif);font-size:1.08rem;line-height:1.8;color:#333;max-width:700px;}
  .pw-covers{display:flex;gap:14px;margin:26px 0 6px;flex-wrap:wrap;}
  .pw-covers a{display:block;width:96px;transition:transform .2s;}
  .pw-covers a:hover{transform:translateY(-5px);}
  .pw-covers img{width:100%;aspect-ratio:2/3;object-fit:cover;box-shadow:0 10px 22px rgba(0,0,0,.22);}
  .pw-themes{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0 4px;}
  .pw-theme{font-family:var(--disp);font-weight:700;font-size:.75rem;letter-spacing:.03em;text-transform:uppercase;background:var(--black);color:var(--yellow);padding:6px 13px;}
  .pw-btn{display:inline-block;margin-top:24px;font-family:var(--disp);font-weight:800;font-size:.8rem;letter-spacing:.05em;text-transform:uppercase;text-decoration:none;padding:13px 28px;border:3px solid var(--black);background:var(--yellow);color:var(--black);transition:all .2s;}
  .pw-btn:hover{background:var(--black);color:var(--yellow);}
  @media(max-width:860px){.pw-hero-inner{grid-template-columns:1fr;}.pw-hero .hero-stamp{display:none;}.pw-inner{grid-template-columns:1fr;gap:20px;}}
  @media(max-width:560px){
    .pw-hero{padding:52px 20px 46px;}
    .pw-year{padding:40px 20px;}
    .pw-inner{gap:14px;}
    .pw-covers{margin:18px 0 4px;gap:10px;}
    .pw-covers a{width:62px;}
    .pw-btn{margin-top:16px;}
  }
"""

blocks = []
seo_pages = []
for i, y in enumerate(YEARS):
    d = load_year(y)
    label = getattr(d, 'YEAR_LABEL', y)
    n_books = len(d.WINNERS) + len(d.SHORTLIST) + len([1 for t, a in d.LONGLIST if norm(t) not in
                  {norm(x[2]) for x in d.WINNERS} | {norm(x[0]) for x in d.SHORTLIST}])
    themes = [t[0] for t in (d.TRENDS or [])]
    if getattr(d, 'TRENDS_GROUPED', None):
        themes = [g[0] for g in d.TRENDS_GROUPED]
    hero_themes = getattr(d, 'HERO_THEMES', '') or ''
    covers = []
    for cat, col, t, a in d.WINNERS:
        cov = find_cover(y, t)
        if cov:
            covers.append(f'<a href="{y}.html" title="{esc(t)} — {cat}"><img src="{cov}" alt="{esc(t)} book cover" loading="lazy"></a>')
    winners_line = ' &middot; '.join(f'<b>{esc(t)}</b>' for cat, col, t, a in d.WINNERS)
    theme_chips = ''.join(f'<span class="pw-theme">{esc(t)}</span>' for t in themes)
    bg = 'background:var(--white)' if i % 2 == 0 else 'background:var(--cream)'
    blocks.append(f'''<section class="pw-year" style="{bg}" id="y{y}">
  <div class="pw-inner">
    <div>
      <div class="pw-yr">{label}</div>
      <p class="pw-count">{n_books} books honored</p>
    </div>
    <div>
      <p class="pw-summary">{hero_themes} That year&rsquo;s five winners: {winners_line}.</p>
      <div class="pw-covers">{''.join(covers)}</div>
      {f'<div class="pw-themes">{theme_chips}</div>' if theme_chips else ''}
      <a class="pw-btn" href="{y}.html">See The Full {label} List &#8594;</a>
    </div>
  </div>
</section>''')
    seo_pages.append({'@type': 'ListItem', 'position': i + 1,
                      'item': {'@type': 'WebPage', 'name': f'The {label} Non-Obvious Book Awards',
                               'url': f'{_seo.DOMAIN}/{y}.html'}})

body = ''
for i, b in enumerate(blocks):
    if i > 0:
        prev = WHT if (i - 1) % 2 == 0 else CRM
        nxt = WHT if i % 2 == 0 else CRM
        body += wave(prev, nxt) + '\n'
    body += b + '\n'
last_bg = WHT if (len(blocks) - 1) % 2 == 0 else CRM

TITLE = 'Past Winners — Every Year of the Non-Obvious Book Awards'
META = ('Every year of the Non-Obvious Book Awards since 2014: each year&#39;s five winners, the biggest '
        'themes from the books of that year, and links to every full list.')
SEO_HEAD = _seo.head_block('past-winners.html', TITLE, META.replace('&#39;', "'"))
SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.breadcrumbs(("Home", ""), ("Past Winners", None)),
    {'@type': 'CollectionPage', 'name': TITLE, 'url': f'{_seo.DOMAIN}/past-winners.html',
     'mainEntity': {'@type': 'ItemList', 'itemListElement': seo_pages}},
)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{META}">
{SEO_HEAD}
{SEO_LD}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@700;800;900&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Lora:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
{style}
<style>{extra_css}</style>
</head>
<body>

{header}

<!-- PAST WINNERS HERO -->
<header class="pw-hero">
  <div class="pw-hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">The Award Archive</p>
      <h1>Every Year. <br>Every Winner.</h1>
      <p class="sub">A decade of the Non-Obvious Book Awards, year by year: the five winners, the biggest themes we found in the books of each year, and the full lists behind them.</p>
    </div>
    <div class="hero-stamp">
      <img src="assets/badges/web/seal-black.png" alt="The Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

{body}
{wave(last_bg, '#005E8C')}

{footer}

</body>
</html>
'''
open(os.path.join(SITE, 'past-winners.html'), 'w').write(page)
print('wrote past-winners.html', len(page) // 1024, 'KB,', len(blocks), 'years')

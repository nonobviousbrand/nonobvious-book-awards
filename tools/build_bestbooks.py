#!/usr/bin/env python3
"""Build best-books.html — the hub page for all curated book lists/roundups."""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as _seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')

# (slug, accent-var, display name, blurb)
AWARD_LISTS = [
    ('most-important-books.html', 'purple', 'The Most Important Books', 'Every winner of our Most Important Book award: the books with the biggest ideas about the world we live in.'),
    ('most-original-books.html', 'blue', 'The Most Original Books', 'Every winner of our Most Original Book award: ideas we had simply never seen before.'),
    ('most-useful-books.html', 'teal', 'The Most Useful Books', 'Every winner of our Most Useful Book award: the most practical, immediately applicable reads of the decade.'),
    ('most-entertaining-books.html', 'orange', 'The Most Entertaining Books', 'Every winner of our Most Entertaining Book award: proof that non-fiction can be as fun as it is smart.'),
    ('most-shareable-books.html', 'magenta', 'The Most Shareable Books', 'Every winner of our Most Shareable Book award: the books you finish and immediately tell everyone about.'),
]
TOPIC_LISTS = [
    ('best-books-for-entrepreneurs.html', 'yellow', 'Best Books For Entrepreneurs', 'Our most recommended books for founders and builders, on starting up, raising money and surviving the messy middle.'),
    ('best-ai-books.html', 'cyan', 'Best Books On AI', 'The best books on artificial intelligence we have honored: the optimists, the skeptics, the builders and the investigators.'),
    ('best-marketing-books.html', 'red', 'Best Marketing Books', 'The books that still shape how the best marketers think, on branding, persuasion and why things catch on.'),
    ('best-productivity-books.html', 'green', 'Best Productivity Books', 'The small shelf of books that actually change how people work: habits, focus, timing and doing less, better.'),
    ('best-business-memoirs.html', 'navy', 'Best Business Memoirs', 'First-person stories from founders, CEOs and insiders about what building and leading really looks like.'),
    ('best-creativity-books.html', 'orange', 'Best Books On Creativity & Innovation', 'Where ideas come from, how to champion them, and why the most original thinkers see the world differently.'),
    ('best-leadership-books.html', 'purple', 'Best Leadership Books', 'The books we most recommend on leading teams, building culture and becoming a boss people want to work for.'),
    ('best-communication-books.html', 'blue', 'Best Books On Communication & Storytelling', 'The best books we have honored on talking, writing, listening, arguing and telling stories people remember.'),
    ('best-psychology-books.html', 'magenta', 'Best Books On Psychology & Human Behavior', 'Why we think what we think and do what we do: the best books on the strange workings of the human mind.'),
    ('best-books-south-asian-authors.html', 'lime', 'Best Books From South Asian Authors', 'Award-winning books from an extraordinary group of South Asian authors honored across our first decade.'),
]


def card(slug, accent, name, blurb):
    s = open(os.path.join(SITE, slug)).read()
    covers = re.findall(r'<div class="ru-cover"><a[^>]*><img src="([^"]+)"', s)[:7]
    count = len(re.findall(r'<div class="ru-row">', s))
    covs = ''.join(f'<img src="{c}" alt="" loading="lazy">' for c in covers)
    return f'''      <a class="bb-card" style="--c:var(--{accent})" href="{slug}">
        <div class="bb-covers">{covs}</div>
        <h3>{name}</h3>
        <p class="bb-blurb">{blurb}</p>
        <span class="bb-more">{count} books &middot; See The List &#8594;</span>
      </a>'''


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
  /* ---------- Best Books hub ---------- */
  .bb-hero{background:var(--yellow);padding:120px 6vw 90px;}
  .bb-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.3fr .7fr;gap:60px;align-items:center;}
  .bb-hero h1{font-size:clamp(2.3rem,4.6vw,3.7rem);line-height:1.06;text-transform:uppercase;font-weight:900;}
  .bb-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.18rem;line-height:1.7;margin-top:24px;max-width:600px;}
  .bb-hero .hero-stamp img{width:100%;max-width:250px;transform:rotate(-8deg);filter:drop-shadow(0 18px 32px rgba(0,0,0,.14));margin:0 auto;display:block;}
  .bb-grid{max-width:1140px;margin:56px auto 0;display:grid;grid-template-columns:repeat(2,1fr);gap:38px;}
  .bb-card{display:block;text-decoration:none;color:var(--ink);background:var(--white);border:3px solid var(--black);border-top:10px solid var(--c);padding:28px 30px 26px;box-shadow:10px 10px 0 rgba(0,0,0,.12);transition:transform .18s,box-shadow .18s;}
  .bb-card:hover{transform:translate(-3px,-3px);box-shadow:14px 14px 0 rgba(0,0,0,.16);}
  .bb-covers{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;}
  .bb-covers img{width:60px;aspect-ratio:2/3;object-fit:cover;box-shadow:0 8px 16px rgba(0,0,0,.2);}
  .bb-card h3{font-family:var(--disp);font-weight:900;font-size:1.35rem;line-height:1.2;margin-bottom:10px;text-transform:uppercase;}
  .bb-blurb{font-family:var(--serif);font-size:.98rem;line-height:1.7;color:#444;}
  .bb-more{display:inline-block;margin-top:16px;font-family:var(--disp);font-weight:800;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;border-bottom:3px solid var(--c);padding-bottom:3px;}
  .bb-head{max-width:1140px;margin:0 auto;text-align:center;display:flex;flex-direction:column;align-items:center;}
  @media(max-width:900px){.bb-grid{grid-template-columns:1fr;}.bb-hero-inner{grid-template-columns:1fr;}.bb-hero .hero-stamp{display:none;}}
  @media(max-width:560px){
    .bb-hero{padding:52px 20px 46px;}
    .bb-grid{margin-top:32px;gap:24px;}
    .bb-card{padding:22px 20px 20px;}
    .bb-covers{margin-bottom:14px;}
    .bb-covers img{width:52px;}
  }
"""

award_cards = '\n'.join(card(*a) for a in AWARD_LISTS)
topic_cards = '\n'.join(card(*t) for t in TOPIC_LISTS)

TITLE = 'Best Books — Curated Reading Lists From The Non-Obvious Book Awards'
META = ('All the best-books reading lists from the Non-Obvious Book Awards: the best books by award '
        'category, for entrepreneurs, on AI, marketing, productivity, business memoirs and more.')
SEO_HEAD = _seo.head_block('best-books.html', TITLE, META)
items = [{'@type': 'ListItem', 'position': i + 1,
          'item': {'@type': 'WebPage', 'name': n, 'url': f'{_seo.DOMAIN}/{s}'}}
         for i, (s, c, n, b) in enumerate(AWARD_LISTS + TOPIC_LISTS)]
SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.breadcrumbs(("Home", ""), ("Best Books", None)),
    {'@type': 'CollectionPage', 'name': TITLE, 'url': f'{_seo.DOMAIN}/best-books.html',
     'mainEntity': {'@type': 'ItemList', 'itemListElement': items}},
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

<!-- BEST BOOKS HERO -->
<header class="bb-hero">
  <div class="bb-hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">Curated Reading Lists</p>
      <h1>The Best Books. <br>By Every Measure.</h1>
      <p class="sub">Fifteen reading lists drawn from more than 800 books honored across a decade of the Non-Obvious Book Awards: by award, by topic, and by the voices behind them.</p>
    </div>
    <div class="hero-stamp">
      <img src="assets/badges/web/seal-black.png" alt="The Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

<!-- ALL LISTS -->
<section style="background:var(--white)">
  <div class="bb-grid" style="margin-top:0">
{award_cards}
{topic_cards}
  </div>
</section>

{wave(WHT, '#005E8C')}

{footer}

</body>
</html>
'''
open(os.path.join(SITE, 'best-books.html'), 'w').write(page)
print('wrote best-books.html', len(page) // 1024, 'KB')

#!/usr/bin/env python3
"""Build a yearly award page from data + the homepage's design system."""
import re, os, html as H
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as _seo
from podcast_guests import was_guest

ROOT = os.path.join(os.path.dirname(__file__), '..')
SITE = os.path.join(ROOT, 'site')

# ---------------- year data (from tools/yeardata/yNNNN.py) ----------------
import sys, importlib.util
_year = sys.argv[1] if len(sys.argv) > 1 else '2023'
_spec = importlib.util.spec_from_file_location('ydata', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yeardata', f'y{_year}.py'))
_d = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_d)
YEAR=_d.YEAR; PREV_YEAR=_d.PREV_YEAR; NEXT_YEAR=_d.NEXT_YEAR; VIDEO_ID=_d.VIDEO_ID
YEAR_LABEL = getattr(_d, 'YEAR_LABEL', str(_d.YEAR))
BOOKSHOP=_d.BOOKSHOP; TRENDS_INTRO=_d.TRENDS_INTRO; TRENDS_URL=_d.TRENDS_URL; TRENDS=_d.TRENDS
WINNERS=_d.WINNERS; SHORTLIST=_d.SHORTLIST; LONGLIST=_d.LONGLIST
OVERRIDES_DATA = getattr(_d, 'OVERRIDES', {})
TRENDS_GROUPED = getattr(_d, 'TRENDS_GROUPED', None)
HERO_SUB = getattr(_d, 'HERO_SUB', None)
PARTNER = getattr(_d, 'PARTNER', None)
HERO_SEAL = getattr(_d, 'HERO_SEAL', 'assets/badges/web/seal-black.png')
WINNER_BLURBS = getattr(_d, 'WINNER_BLURBS', {})
SHORTLIST_BLURBS = getattr(_d, 'SHORTLIST_BLURBS', {})
HERO_THEMES = getattr(_d, 'HERO_THEMES', None)
# ---------------- cover matching ----------------
import glob
def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
covers = {}
for f in glob.glob(os.path.join(SITE, f'assets/covers/{YEAR}/*.jpg')):
    covers[norm(os.path.splitext(os.path.basename(f))[0])] = f'assets/covers/{YEAR}/' + os.path.basename(f)

OVERRIDES = OVERRIDES_DATA
def find_cover(title):
    if title in OVERRIDES:
        return covers.get(OVERRIDES[title])
    t = norm(title)
    if t in covers: return covers[t]
    for k, v in covers.items():
        if k.startswith(t) or t.startswith(k): return v
    return None

unmatched = [t for t,_ in LONGLIST if not find_cover(t)]
print('unmatched:', unmatched)

from PIL import Image as _PILImage
def cover_style(cov):
    """Square/landscape covers get letterboxed (contain) instead of cropped."""
    if not cov: return ''
    try:
        w, h = _PILImage.open(os.path.join(SITE, cov)).size
    except Exception:
        return ''
    return ' style="object-fit:contain;background:#fff"' if w / h > 0.72 else ''

# ---------------- Amazon affiliate links ----------------
import json as _json
AFF_TAG = 'influenmarket-20'
try:
    _ISBNS = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yeardata', 'isbns.json'))).get(str(YEAR), {})
except Exception:
    _ISBNS = {}
def aff(title):
    isbn = _ISBNS.get(norm(title))
    return f'https://www.amazon.com/dp/{isbn}/?tag={AFF_TAG}' if isbn else None


# ---------------- reusable chrome from homepage ----------------
index = open(os.path.join(SITE, 'index.html')).read()
style = re.search(r'<style>.*?</style>', index, re.S).group(0)
header = re.search(r'<div class="rainbow">.*?</nav>', index, re.S).group(0)
footer = re.search(r'<!-- NEWSLETTER -->.*?</footer>', index, re.S).group(0)
for frag in ('#about','#winners','#archive','#roundups','#enter','#faq-link','#video','#podcast'):
    header = header.replace(f'href="{frag}"', f'href="index.html{frag}"')
    footer = footer.replace(f'href="{frag}"', f'href="index.html{frag}"')
header = header.replace('<a class="nav-logo" href="#">', '<a class="nav-logo" href="index.html">')

WAVE = "M0,26 C240,46 480,6 720,24 C960,42 1200,10 1440,26 L1440,0 L0,0 Z"
def wave(prev, nxt):
    return (f'<div class="wave" style="background:{nxt}" aria-hidden="true">'
            f'<svg viewBox="0 0 1440 48" preserveAspectRatio="none"><path fill="{prev}" d="{WAVE}"/></svg></div>')
YEL, BLK, WHT, CRM = '#F7C731', '#161616', '#ffffff', '#FBF8F1'

extra_css = """
<style>
  /* ---------- Year page ---------- */
  .year-hero{padding:84px 32px 88px;}
  .partner-band{background:var(--white);padding:54px 32px;}
  .partner-inner{max-width:900px;margin:0 auto;display:grid;grid-template-columns:auto 1fr;gap:44px;align-items:center;border:3px solid var(--black);box-shadow:12px 12px 0 var(--yellow);padding:34px 44px;background:var(--white);}
  .partner-inner img{height:64px;width:auto;display:block;}
  .partner-inner .pk{font-family:var(--disp);font-weight:800;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:#888;margin-bottom:8px;}
  .partner-inner p{font-size:1rem;line-height:1.75;color:#333;}
  @media(max-width:700px){.partner-inner{grid-template-columns:1fr;gap:22px;text-align:center;}.partner-inner img{margin:0 auto;}}
  .year-kicker-row{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:14px;}
  .year-pager{display:flex;gap:12px;margin-top:34px;flex-wrap:wrap;}
  .year-pager a{font-family:var(--disp);font-weight:700;font-size:.82rem;letter-spacing:.02em;text-transform:uppercase;text-decoration:none;color:var(--black);border:3px solid var(--black);padding:10px 18px;transition:all .2s;}
  .year-pager a:hover{background:var(--black);color:var(--yellow);}
  .hero-mini-stats{display:flex;gap:26px;margin-top:30px;flex-wrap:wrap;}
  .hero-mini-stats span{font-family:var(--disp);font-weight:800;font-size:.9rem;text-transform:uppercase;letter-spacing:.02em;}
  .hero-mini-stats b{font-size:1.5rem;display:block;line-height:1.1;}
  .hero-themes{font-family:var(--serif);font-style:italic;font-size:1.02rem;line-height:1.65;color:#3a3a3a;margin-top:22px;max-width:560px;padding-left:18px;border-left:5px solid var(--black);}
  .win-card .cover img{width:100%;height:100%;object-fit:cover;display:block;}
  .win-card .cover{padding:0;background:#e8e8e8;}
  /* shortlist (dark) */
  .shortlist{background:var(--black);color:var(--white);}
  /* blurb-mode winners (feature rows) */
  .win-rows{margin-top:14px;}
  .win-row{display:grid;grid-template-columns:175px 1fr;gap:42px;padding:46px 0;border-bottom:1px solid rgba(0,0,0,.1);align-items:start;}
  .win-row:last-child{border-bottom:none;padding-bottom:10px;}
  .win-row .cover img{width:100%;box-shadow:10px 10px 0 rgba(0,0,0,.14);transition:transform .2s;}
  .win-row .cover a:hover img{transform:translateY(-4px);}
  .win-row h3{font-family:var(--disp);font-weight:900;font-size:1.65rem;line-height:1.15;margin:12px 0 4px;}
  .win-row .author{font-family:var(--serif);font-style:italic;color:#555;font-size:1.02rem;margin-bottom:14px;}
  .win-row .blurb{font-size:1rem;line-height:1.8;color:#333;max-width:640px;}
  .win-row .cat-tag{display:inline-block;color:var(--white);font-family:var(--disp);font-weight:800;font-size:.72rem;letter-spacing:.05em;text-transform:uppercase;padding:6px 14px;}
  .buy-btn{display:inline-block;font-family:var(--disp);font-weight:800;font-size:.76rem;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;padding:11px 24px;border:3px solid var(--black);transition:all .2s;margin-top:16px;margin-right:10px;}
  .buy-btn.amz{background:#FF9900;color:var(--black);}
  .buy-btn.amz:hover{background:var(--black);color:#FF9900;}
  .buy-btn.local{background:#45114F;border-color:#45114F;color:var(--white);}
  .buy-btn.local:hover{background:transparent;color:#45114F;}
  .buy-btn.sm{padding:7px 15px;font-size:.66rem;border-width:2px;margin-top:10px;margin-right:8px;}
  .sl-row .buy-btn.local:hover{background:transparent;color:#c9a3d6;border-color:#8a5f99;}
  .sl-row .buy-btn.amz:hover{background:transparent;color:#FF9900;border-color:#FF9900;}
  .buy-btn.pod{background:var(--white);border-color:var(--black);color:var(--black);}
  .buy-btn.pod:hover{background:var(--yellow);border-color:var(--black);color:var(--black);}
  .sl-row .buy-btn.pod{border-color:var(--white);}
  .sl-row .buy-btn.pod:hover{background:var(--yellow);border-color:var(--yellow);}
  @media(max-width:640px){.win-row{grid-template-columns:1fr;gap:22px;}.win-row .cover img{max-width:190px;}}
  /* blurb-mode shortlist (2-up rows) */
  .sl-duo{display:grid;grid-template-columns:repeat(2,1fr);gap:46px 56px;margin-top:56px;}
  .sl-row{display:grid;grid-template-columns:125px 1fr;gap:26px;align-items:start;}
  .sl-row img{width:100%;box-shadow:0 12px 26px rgba(0,0,0,.45);transition:transform .2s;}
  .sl-row a:hover img{transform:translateY(-4px);}
  .sl-row .t{font-family:var(--disp);font-weight:800;font-size:1.05rem;line-height:1.25;}
  .sl-row .a{font-family:var(--serif);font-style:italic;font-size:.86rem;color:#b9b9b9;margin:4px 0 10px;}
  .sl-row .blurb{font-size:.9rem;line-height:1.7;color:#c9c9c9;}
  @media(max-width:980px){.sl-duo{grid-template-columns:1fr;}}
  @media(max-width:480px){.sl-row{grid-template-columns:1fr;}.sl-row img{max-width:150px;}}
  .shortlist .divider{background:var(--yellow);}
  .shortlist .kicker{color:var(--yellow);}
  .sl-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:30px;margin-top:56px;}
  .sl-card{text-align:left;}
  .sl-card img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block;box-shadow:0 12px 26px rgba(0,0,0,.45);transition:transform .2s;}
  .sl-card:hover img{transform:translateY(-6px);}
  .sl-card .t{font-family:var(--disp);font-weight:700;font-size:.92rem;line-height:1.3;margin-top:14px;}
  .sl-card .a{font-family:var(--serif);font-style:italic;font-size:.82rem;color:#b9b9b9;margin-top:3px;}
  /* longlist */
  .longlist{background:var(--cream);}
  .ll-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:26px 22px;margin-top:56px;}
  .book{display:block;text-decoration:none;color:var(--ink);}
  .book img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block;box-shadow:0 8px 18px rgba(0,0,0,.14);transition:transform .2s, box-shadow .2s;background:#e8e8e8;}
  .book:hover img{transform:translateY(-5px);box-shadow:0 14px 26px rgba(0,0,0,.2);}
  .book .t{font-family:var(--disp);font-weight:700;font-size:.8rem;line-height:1.3;margin-top:10px;}
  .book .a{font-family:var(--serif);font-style:italic;font-size:.74rem;color:#666;margin-top:2px;}
  .book .no-cover{width:100%;aspect-ratio:2/3;background:var(--black);color:var(--yellow);display:flex;align-items:center;justify-content:center;text-align:center;padding:14px;font-family:var(--disp);font-weight:700;font-size:.85rem;}
  .ll-foot{margin-top:60px;display:flex;gap:20px;align-items:center;flex-wrap:wrap;}
  /* trends */
  .trends{background:var(--white);}
  .trend-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:34px 40px;margin-top:60px;}
  .trend{border-top:6px solid var(--black);padding-top:20px;}
  .trend .trend-stack{width:100%;display:block;margin-bottom:18px;box-shadow:0 10px 24px rgba(0,0,0,.14);transition:transform .2s;}
  .trend:hover .trend-stack{transform:translateY(-4px);}
  .trend .n{font-family:var(--disp);font-weight:900;font-size:.78rem;letter-spacing:.02em;text-transform:uppercase;color:var(--gray);}
  .trend h3{font-family:var(--disp);font-weight:800;font-size:1.15rem;text-transform:uppercase;margin:6px 0 8px;letter-spacing:.02em;}
  .trend p{color:#444;font-size:.92rem;line-height:1.6;}
  /* grouped macro/micro trends */
  .macro-block{margin-top:70px;}
  .macro-band{display:grid;grid-template-columns:1.1fr .9fr;gap:0;border:3px solid var(--black);border-top-width:8px;background:var(--black);color:var(--white);align-items:stretch;}
  .macro-band img{width:100%;height:100%;object-fit:cover;display:block;}
  .macro-body{padding:38px 40px;display:flex;flex-direction:column;justify-content:center;}
  .macro-body .n{font-family:var(--disp);font-weight:900;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;}
  .macro-body h3{font-family:var(--disp);font-weight:900;font-size:2rem;margin:8px 0 12px;color:var(--white);}
  .macro-body p{font-family:var(--serif);font-style:italic;color:#c9c9c9;font-size:.98rem;line-height:1.65;}
  .micro-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:34px 40px;margin-top:38px;}
  .trend.micro h3{font-size:1.05rem;text-transform:none;}
  @media(max-width:980px){.micro-grid{grid-template-columns:1fr;}.macro-band{grid-template-columns:1fr;}.macro-band img{min-width:0;height:auto;}.macro-body{min-width:0;}}
  .trends .ll-foot{margin-top:56px;}
  .trend-grid.wide{grid-template-columns:repeat(2,1fr);gap:44px 48px;}
  @media(max-width:980px){.trend-grid{grid-template-columns:repeat(2,1fr);}}
  @media(max-width:560px){.trend-grid.wide{grid-template-columns:1fr;}}
  @media(max-width:560px){.trend-grid{grid-template-columns:1fr;}}
  /* enter cta band */
  .cta-band{background:var(--yellow);text-align:center;}
  .cta-band .wrap{display:flex;flex-direction:column;align-items:center;}
  @media(max-width:980px){.sl-grid{grid-template-columns:repeat(3,1fr);}.ll-grid{grid-template-columns:repeat(3,1fr);}}
  @media(max-width:560px){.sl-grid{grid-template-columns:repeat(2,1fr);}.ll-grid{grid-template-columns:repeat(3,1fr);}
    .year-hero{padding:48px 20px 44px;}
    .win-row{padding:30px 0;gap:18px;}
    .win-row .cover img{max-width:115px;}
    .sl-row img{max-width:105px;}
    .sl-duo{gap:30px 36px;margin-top:32px;}
    .sl-grid{margin-top:30px;gap:20px;}
    .ll-grid{margin-top:30px;gap:16px 12px;}
    .book .t{font-size:.68rem;margin-top:7px;}
    .book .a{font-size:.64rem;}
    .ll-foot{margin-top:36px;}
    .trend-grid{margin-top:32px;gap:24px;}
  }
</style>
"""

def esc(s): return H.escape(s, quote=False)

win_cards = []
for cat, color, title, author in WINNERS:
    cov = find_cover(title)
    img = f'<img src="{cov}" alt="{esc(title)} book cover"{cover_style(cov)}>' if cov else esc(title)
    if aff(title):
        img = f'<a href="{aff(title)}" target="_blank" rel="noopener sponsored">{img}</a>'
    win_cards.append(f'''      <div class="win-card">
        <div class="cover">{img}</div>
        <span class="cat-tag" style="background:var(--{color})">{cat}</span>
        <h3>{esc(title)}</h3><p class="author">{esc(author)}</p>
      </div>''')

win_rows = []
for cat, color, title, author in WINNERS:
    cov = find_cover(title)
    img = f'<img src="{cov}" alt="{esc(title)} book cover">' if cov else esc(title)
    if aff(title):
        img = f'<a href="{aff(title)}" target="_blank" rel="noopener sponsored">{img}</a>'
    blurb = WINNER_BLURBS.get(norm(title), '')
    win_rows.append(f'''      <div class="win-row">
        <div class="cover">{img}</div>
        <div>
          <span class="cat-tag" style="background:var(--{color})">{cat} &middot; {YEAR_LABEL} Winner</span>
          <h3>{esc(title)}</h3><p class="author">by {esc(author)}</p>
          <p class="blurb">{blurb}</p>
          <div>{f'<a class="buy-btn amz" href="{aff(title)}" target="_blank" rel="noopener sponsored">Buy Amazon</a>' if aff(title) else ''}{f'<a class="buy-btn local" href="{_seo.bookshop_url(_ISBNS.get(norm(title)))}" target="_blank" rel="noopener sponsored">Buy Local</a>' if _seo.bookshop_url(_ISBNS.get(norm(title))) else ''}{f'<a class="buy-btn pod" href="https://www.nonobvious.com/podcast" target="_blank" rel="noopener">Listen To Episode</a>' if was_guest(author) else ''}</div>
        </div>
      </div>''')
WINNERS_BODY = (f'<div class="win-rows">{chr(10).join(win_rows)}</div>' if WINNER_BLURBS
                else f'<div class="win-grid">{chr(10).join(win_cards)}</div>')

sl_cards = []
for title, author in SHORTLIST:
    cov = find_cover(title)
    slimg = f'<img src="{cov}" alt="{esc(title)} book cover"{cover_style(cov)}>' if cov else f'<div class="no-cover" style="aspect-ratio:2/3;background:#232323;color:var(--yellow);display:flex;align-items:center;justify-content:center;text-align:center;padding:14px;font-family:var(--disp);font-weight:700;font-size:.85rem;">{esc(title)}</div>'
    if aff(title):
        slimg = f'<a href="{aff(title)}" target="_blank" rel="noopener sponsored">{slimg}</a>'
    sl_cards.append(f'''      <div class="sl-card">{slimg}<div class="t">{esc(title)}</div><div class="a">{esc(author)}</div></div>''')

sl_rows = []
for title, author in SHORTLIST:
    cov = find_cover(title)
    slimg = f'<img src="{cov}" alt="{esc(title)} book cover">' if cov else ''
    if aff(title) and slimg:
        slimg = f'<a href="{aff(title)}" target="_blank" rel="noopener sponsored">{slimg}</a>'
    blurb = SHORTLIST_BLURBS.get(norm(title), '')
    sl_rows.append(f'''      <div class="sl-row">
        <div>{slimg}</div>
        <div><div class="t">{esc(title)}</div><div class="a">by {esc(author)}</div><p class="blurb">{blurb}</p><div>{f'<a class="buy-btn amz sm" href="{aff(title)}" target="_blank" rel="noopener sponsored">Buy Amazon</a>' if aff(title) else ''}{f'<a class="buy-btn local sm" href="{_seo.bookshop_url(_ISBNS.get(norm(title)))}" target="_blank" rel="noopener sponsored">Buy Local</a>' if _seo.bookshop_url(_ISBNS.get(norm(title))) else ''}{f'<a class="buy-btn pod sm" href="https://www.nonobvious.com/podcast" target="_blank" rel="noopener">Listen To Episode</a>' if was_guest(author) else ''}</div></div>
      </div>''')
SHORTLIST_BODY = (f'<div class="sl-duo">{chr(10).join(sl_rows)}</div>' if SHORTLIST_BLURBS
                  else f'<div class="sl-grid">{chr(10).join(sl_cards)}</div>')

ll_cards = []
for title, author in LONGLIST:
    cov = find_cover(title)
    img = f'<img src="{cov}" alt="{esc(title)} book cover" loading="lazy"{cover_style(cov)}>' if cov else f'<div class="no-cover">{esc(title)}</div>'
    href = aff(title)
    if href:
        ll_cards.append(f'''      <a class="book" href="{href}" target="_blank" rel="noopener sponsored" title="{esc(title)} by {esc(author)}">{img}<div class="t">{esc(title)}</div><div class="a">{esc(author)}</div></a>''')
    else:
        ll_cards.append(f'''      <div class="book" title="{esc(title)} by {esc(author)}">{img}<div class="t">{esc(title)}</div><div class="a">{esc(author)}</div></div>''')

VIDEO_SECTION = (f'''
<!-- ANNOUNCEMENT VIDEO -->
<section class="video">
  <div class="wrap">
    <div class="head" style="text-align:center;display:flex;flex-direction:column;align-items:center;">
      <div class="divider"></div>
      <p class="kicker">Watch The Announcement</p>
      <h2>The {YEAR_LABEL} winner announcement show.</h2>
    </div>
    <div class="video-frame">
      <iframe src="https://www.youtube.com/embed/{VIDEO_ID}" title="The {YEAR_LABEL} Non-Obvious Book Awards winner announcement" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
  </div>
</section>''') if VIDEO_ID else ''
BOOKSHOP_BTN = ('    <div class="ll-foot">\n'
                f'      <a class="btn btn-dark" href="{BOOKSHOP}" target="_blank">Shop the {YEAR_LABEL} List on Bookshop.org</a>\n'
                '    </div>') if BOOKSHOP else ''
LONGLIST_TITLE = getattr(_d, 'LL_TITLE', None) or (
    f'The 100 Best Non-Fiction Books of {YEAR}.' if len(LONGLIST) >= 90
    else f'The Best Non-Fiction Books of {YEAR}.')
SL_LEDE = getattr(_d, 'SL_LEDE', None) or 'The finalists — narrowed from the longlist and revealed during the live announcement show.'
LONGLIST_SECTION = (f'''{wave(BLK, CRM)}

<!-- LONGLIST -->
<section class="longlist">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker">The Longlist</p>
    <h2>{LONGLIST_TITLE}</h2>
    <p class="lede">Every longlist selection from {YEAR_LABEL}, listed alphabetically. Each of these books was read and selected by our review team from 1,000+ entries.</p>
    <div class="ll-grid">
{chr(10).join(ll_cards)}
    </div>
{BOOKSHOP_BTN}
  </div>
</section>

{wave(CRM, YEL)}''') if LONGLIST else wave(BLK, YEL)

PALETTE = ['blue','teal','orange','magenta','purple','green','cyan','lime','navy','red','yellow','blue']
trend_cards = []
for i, (name, blurb) in enumerate(TRENDS):
    col = PALETTE[i % len(PALETTE)]
    timg_rel = f'assets/trends/{YEAR}/trend-{i+1:02d}.jpg'
    timg = (f'<img class="trend-stack" src="{timg_rel}" alt="The books behind the {esc(name)} trend — a stack of {YEAR_LABEL} longlist titles" loading="lazy">'
            if os.path.exists(os.path.join(SITE, timg_rel)) else '')
    trend_cards.append(f'''      <div class="trend" style="border-color:var(--{col})">
        {timg}<div class="n">Trend {i+1:02d}</div>
        <h3>{esc(name)}</h3>
        <p>{esc(blurb)}</p>
      </div>''')

TREND_GRID_CLASS = 'trend-grid'
_t1 = os.path.join(SITE, f'assets/trends/{YEAR}/trend-01.jpg')
if os.path.exists(_t1):
    _w, _h = _PILImage.open(_t1).size
    if _w / _h > 1.3:
        TREND_GRID_CLASS = 'trend-grid wide'

MACRO_PALETTE = ['blue','magenta','teal','purple','orange','green']
grouped_html = ''
if TRENDS_GROUPED:
    blocks = []
    for gi, (macro, micros) in enumerate(TRENDS_GROUPED):
        col = MACRO_PALETTE[gi % len(MACRO_PALETTE)]
        macro_img = f'assets/trends/{YEAR}/macro-{gi+1}.jpg'
        micro_cards = []
        for mi, (mname, mblurb) in enumerate(micros):
            letter = 'abc'[mi]
            mimg = f'assets/trends/{YEAR}/micro-{gi+1}{letter}.jpg'
            micro_cards.append(f'''        <div class="trend micro" style="border-color:var(--{col})">
          <img class="trend-stack" src="{mimg}" alt="The books behind the {esc(mname)} micro-trend" loading="lazy">
          <div class="n">{esc(macro)} &rsaquo; Micro-Trend {mi+1}</div>
          <h3>{esc(mname)}</h3>
          <p>{esc(mblurb)}</p>
        </div>''')
        blocks.append(f'''    <div class="macro-block">
      <div class="macro-band" style="border-color:var(--{col})">
        <img src="{macro_img}" alt="The {esc(macro)} macro trend — books from the {YEAR_LABEL} longlist" loading="lazy">
        <div class="macro-body">
          <div class="n" style="color:var(--{col})">Macro Trend {gi+1:02d}</div>
          <h3>{esc(macro)}</h3>
          <p>One of the six overarching macro trends of {YEAR_LABEL} &mdash; explored through the three micro-trends below.</p>
        </div>
      </div>
      <div class="micro-grid">
{chr(10).join(micro_cards)}
      </div>
    </div>''')
    grouped_html = '\n'.join(blocks)

trends_section = ''
if TRENDS_GROUPED:
    trends_link = (f'\n    <div class="ll-foot"><a class="btn btn-ghost" href="{TRENDS_URL}" target="_blank">'
                   f'Read the Full Trend Report &#8594;</a></div>') if TRENDS_URL else ''
    trends_section = f'''
{wave(CRM, WHT)}

<!-- BOOK TRENDS (MACRO + MICRO) -->
<section class="trends">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker">The Biggest Book Trends of {YEAR_LABEL}</p>
    <h2>Six macro trends.<br>Eighteen micro-trends.</h2>
    <p class="lede">{esc(TRENDS_INTRO)}</p>
{grouped_html}{trends_link}
  </div>
</section>

{wave(WHT, CRM)}
'''
elif TRENDS:
    trends_link = (f'\n    <div class="ll-foot"><a class="btn btn-ghost" href="{TRENDS_URL}" target="_blank">'
                   f'Read the Full Trend Report &#8594;</a></div>') if TRENDS_URL else ''
    trends_section = f'''
{wave(CRM, WHT)}

<!-- BOOK TRENDS -->
<section class="trends">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker">The Biggest Book Trends of {YEAR_LABEL}</p>
    <h2>What the year's books<br>were really about.</h2>
    <p class="lede">{esc(TRENDS_INTRO)}</p>
    <div class="{TREND_GRID_CLASS}">
{chr(10).join(trend_cards)}
    </div>{trends_link}
  </div>
</section>

{wave(WHT, BLK)}'''
else:
    trends_section = f'\n{wave(CRM, BLK)}'

# ---------------- SEO / GEO ----------------
import seo as _seo
from podcast_guests import was_guest

META_DESC = (f"The best non-fiction and business books of {YEAR_LABEL}, chosen by the Non-Obvious Book Awards: "
             f"the {len(WINNERS)} winners, the {len(SHORTLIST)}-book shortlist and the full {len(LONGLIST)}-book longlist.")
PAGE_TITLE = f"Best Non-Fiction Books of {YEAR_LABEL} | The Non-Obvious Book Awards"
SEO_HEAD = _seo.head_block(f'{YEAR}.html', PAGE_TITLE, META_DESC)

def _abs_cover(title):
    rel = find_cover(title)
    return f"{_seo.DOMAIN}/{rel}" if rel else None

_books = []
for _cat, _col, _t, _a in WINNERS:
    _books.append(_seo.book(_t, _a, isbn=_ISBNS.get(norm(_t)), image=_abs_cover(_t), url=aff(_t),
                            award=f"{_cat} Book of {YEAR_LABEL} — Non-Obvious Book Awards Winner"))
for _t, _a in SHORTLIST:
    _books.append(_seo.book(_t, _a, isbn=_ISBNS.get(norm(_t)), image=_abs_cover(_t), url=aff(_t),
                            award=f"Non-Obvious Book Awards {YEAR_LABEL} Shortlist"))
for _t, _a in LONGLIST:
    _books.append(_seo.book(_t, _a, isbn=_ISBNS.get(norm(_t)), url=aff(_t),
                            award=f"Non-Obvious Book Awards {YEAR_LABEL} Longlist"))

SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.breadcrumbs(("Home", ""), ("Past Winners", "index.html#archive"), (f"{YEAR_LABEL} Awards", None)),
    _seo.item_list(
        f"The Best Non-Fiction Books of {YEAR_LABEL} — Non-Obvious Book Awards",
        META_DESC,
        _books,
        f"{_seo.DOMAIN}/{YEAR}.html"),
)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Best Non-Fiction Books of {YEAR_LABEL} | The Non-Obvious Book Awards</title>
<meta name="description" content="{META_DESC}">
{SEO_HEAD}
{SEO_LD}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@600;700;800;900&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
{style}
{extra_css}
</head>
<body>

{header}

<!-- YEAR HERO -->
<header class="hero year-hero">
  <div class="hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">The Award Archive</p>
      <h1>The {YEAR_LABEL}<br>Book Awards</h1>
      <p class="sub">{HERO_SUB or f"Five winners, ten shortlist selections and a longlist of the year's best non-fiction books — chosen from more than 1,000 entries and announced live in December {YEAR_LABEL}."}</p>
      {f'<p class="hero-themes">{HERO_THEMES}</p>' if HERO_THEMES else ''}
      <div class="year-pager">
        {f'<a href="{PREV_YEAR}.html">&#8592; {"2014/15" if PREV_YEAR==2014 else PREV_YEAR}</a>' if PREV_YEAR else ''}
        <a href="index.html#archive">All Years</a>
        {f'<a href="{NEXT_YEAR}.html">{NEXT_YEAR} &#8594;</a>' if NEXT_YEAR else ''}
      </div>
    </div>
    <div class="hero-stamp">
      <img src="{HERO_SEAL}" alt="The {YEAR_LABEL} Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

{(f'<!-- MEDIA PARTNER -->' + chr(10) + f'<section class="partner-band">' + chr(10) + f'  <div class="partner-inner">' + chr(10) + f'    <a href="{PARTNER["url"]}" target="_blank" rel="noopener"><img src="{PARTNER["logo"]}" alt="{PARTNER["name"]} logo"></a>' + chr(10) + f'    <div><p class="pk">In Full Media Partnership With {PARTNER["name"]}</p><p>{PARTNER["text"]}</p></div>' + chr(10) + f'  </div>' + chr(10) + f'</section>') if PARTNER else ''}

<!-- WINNERS -->
<section class="winners" id="winners">
  <div class="wrap">
    <div class="winners-head">
      <div>
        <div class="divider"></div>
        <p class="kicker">The {YEAR_LABEL} Winners</p>
        <h2>The Best Non-Obvious<br>Books of the Year</h2>
      </div>
    </div>
    {WINNERS_BODY}
  </div>
</section>

{wave(WHT, CRM)}
{VIDEO_SECTION}
{trends_section}

<!-- SHORTLIST -->
<section class="shortlist">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker">The Shortlist</p>
    <h2>Ten shortlist selections.</h2>
    <p class="lede" style="color:#c9c9c9">{SL_LEDE}</p>
    {SHORTLIST_BODY}
  </div>
</section>

{LONGLIST_SECTION}

<!-- ENTER CTA -->
<section class="cta-band">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker">Your Turn</p>
    <h2>Think a book belongs on this list?</h2>
    <p class="lede" style="text-align:center">Entries for the 2026 Non-Obvious Book Awards are now open — and it costs nothing to enter.</p>
    <a class="btn btn-dark" style="margin-top:30px" href="index.html#enter">How To Enter &#8594;</a>
  </div>
</section>

{wave(YEL, '#005E8C')}

{footer}

</body>
</html>
'''

out = os.path.join(SITE, f'{YEAR}.html')
open(out, 'w').write(page)
print('wrote', out, len(page)//1024, 'KB')

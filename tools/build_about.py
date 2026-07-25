#!/usr/bin/env python3
"""Build about.html from the homepage chrome + About content."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as _seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')

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
  /* ---------- About page ---------- */
  .about-hero{background:var(--yellow);padding:150px 6vw 90px;}
  @media(max-width:560px){.about-hero{padding:52px 20px 46px;}}
  .about-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.4fr .6fr;gap:60px;align-items:center;}
  .about-hero h1{font-size:clamp(2.4rem,5vw,4rem);line-height:1.04;text-transform:uppercase;letter-spacing:.02em;font-weight:900;}
  .about-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.15rem;line-height:1.65;margin-top:22px;max-width:560px;color:#222;}
  .about-hero .hero-stamp img{width:100%;max-width:230px;display:block;margin:0 auto;}
  .belief{max-width:860px;margin:0 auto;}
  .belief p{font-size:1.05rem;line-height:1.85;color:#333;margin-bottom:22px;}
  .pull{font-family:var(--serif);font-style:italic;font-size:1.5rem;line-height:1.55;color:var(--black);border-left:6px solid var(--yellow);padding:8px 0 8px 28px;margin:36px 0;}
  .steps-grid{max-width:1060px;margin:56px auto 0;display:grid;grid-template-columns:repeat(3,1fr);gap:34px;}
  .step{background:var(--white);border:3px solid var(--black);padding:34px 30px;box-shadow:10px 10px 0 var(--black);}
  .step .n{font-family:var(--disp);font-weight:900;font-size:2.2rem;color:var(--black);}
  .step h3{font-family:var(--disp);font-weight:800;font-size:1.15rem;text-transform:uppercase;margin:10px 0 10px;}
  .step p{font-size:.95rem;line-height:1.7;color:#333;}
  .themes-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px;}
  .theme-chip{font-family:var(--disp);font-weight:800;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;color:#fff;padding:8px 16px;}
  .company{background:var(--black);color:var(--white);}
  .company .kicker{color:var(--yellow);}
  .company h2{color:var(--white);}
  .company .divider{background:var(--yellow);}
  .company-inner{max-width:860px;margin:0 auto;text-align:center;}
  .company p{font-size:1.05rem;line-height:1.85;color:#cfcfcf;margin:22px 0 34px;}
  /* publishers mosaic */
  .pubs{background:var(--white);}
  .partners{background:var(--white);padding-top:0;}
  .partner-logos{display:flex;gap:70px;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:46px;}
  .partner-logos img{height:58px;width:auto;display:block;}
  .partner-logos a{display:block;transition:transform .2s;}
  .partner-logos a:hover{transform:translateY(-3px);}
  @media(max-width:560px){.partner-logos{gap:40px;}.partner-logos img{height:42px;}}
  .pubs-mosaic{max-width:1100px;margin:52px auto 0;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:26px 34px;}
  .pubs-mosaic img{height:26px;width:auto;max-width:95px;object-fit:contain;opacity:.75;filter:grayscale(35%);transition:all .2s;}
  .pubs-mosaic img.feat{height:44px;max-width:150px;opacity:1;filter:none;}
  .pubs-mosaic img:hover{opacity:1;filter:none;transform:scale(1.08);}
  .pubs-foot{text-align:center;font-family:var(--serif);font-style:italic;color:#777;font-size:.95rem;margin-top:44px;}
  .founder{background:var(--cream);}
  .founder-inner{max-width:1060px;margin:0 auto;display:grid;grid-template-columns:.72fr 1.28fr;gap:64px;align-items:start;}
  .founder-photo img{width:100%;display:block;border:3px solid var(--black);box-shadow:14px 14px 0 var(--yellow);}
  .founder-photo .placeholder{width:100%;aspect-ratio:4/5;border:3px solid var(--black);box-shadow:14px 14px 0 var(--yellow);background:var(--cream);display:flex;align-items:center;justify-content:center;font-family:var(--disp);font-weight:900;font-size:4rem;color:#ccc;}
  .founder-body h2{margin-bottom:6px;}
  .founder-role{font-family:var(--serif);font-style:italic;font-size:1.05rem;color:#666;margin-bottom:22px;}
  .founder-body p{font-size:1rem;line-height:1.8;color:#333;margin-bottom:16px;}
  @media(max-width:980px){.steps-grid{grid-template-columns:1fr;}.founder-inner{grid-template-columns:1fr;gap:40px;}.founder-photo{max-width:340px;}}
  @media(max-width:860px){.about-hero-inner{grid-template-columns:1fr;}.about-hero .hero-stamp{display:none;}}
  @media(max-width:560px){.founder-photo{max-width:230px;}}
"""

# publisher logo mosaic (featured logos first, larger)
import glob as _glob
_pubdir = os.path.join(SITE, 'assets', 'publishers')
_feat = sorted(_glob.glob(os.path.join(_pubdir, 'feat-*')))
_small = sorted(_glob.glob(os.path.join(_pubdir, 'pub-*')))
def _pubname(p):
    base = os.path.splitext(os.path.basename(p))[0]
    return base.split('-',1)[1].replace('-',' ').title()
_tags = []
for p in _feat:
    rel = 'assets/publishers/' + os.path.basename(p)
    _tags.append(f'<img class="feat" src="{rel}" alt="{_pubname(p)} logo" loading="lazy">')
for p in _small:
    rel = 'assets/publishers/' + os.path.basename(p)
    _tags.append(f'<img src="{rel}" alt="{_pubname(p)} logo" loading="lazy">')
PUB_MOSAIC = '\n      '.join(_tags)
PUB_COUNT = len(_tags)

# founder headshot: use the real photo if present, else a styled placeholder
FOUNDER_IMG = ('<img src="assets/founder.jpg" alt="Rohit Bhargava, founder of the Non-Obvious Book Awards">'
               if os.path.exists(os.path.join(SITE, 'assets', 'founder.jpg'))
               else '<div class="placeholder">RB</div>')

# ---------------- SEO / GEO ----------------
SEO_HEAD = _seo.head_block('about.html', 'About — The Non-Obvious Book Awards', 'The Non-Obvious Book Awards curate the best non-fiction books of the year — no categories, no entry fees, judged by people who love books.')
SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.person(),
    _seo.breadcrumbs(("Home", ""), ("About", None)),
    {"@type": "AboutPage", "url": _seo.DOMAIN + "/about.html", "name": "About the Non-Obvious Book Awards",
     "about": {"@id": _seo.DOMAIN + "/#organization"}},
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About — The Non-Obvious Book Awards</title>
<meta name="description" content="The Non-Obvious Book Awards curate the best non-fiction books of the year — no categories, no entry fees, judged by people who love books.">
{SEO_HEAD}
{SEO_LD}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@700;800&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Lora:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
{style}
<style>{extra_css}</style>
</head>
<body>

{header}

<!-- ABOUT HERO -->
<header class="about-hero">
  <div class="about-hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">About The Awards</p>
      <h1>We Curate The Best<br>Non-Fiction Books<br>Of The Year.</h1>
      <p class="sub">The Non-Obvious Book Awards are curated, judged and created for people who love books. Especially non-fiction books.</p>
    </div>
    <div class="hero-stamp">
      <img src="assets/badges/web/seal-black.png" alt="The Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

<!-- BELIEF -->
<section style="background:#fff">
  <div class="wrap">
    <div class="belief">
      <div class="divider"></div>
      <p class="kicker">Our Philosophy</p>
      <h2 style="margin-bottom:26px">We believe in the power of books.</h2>
      <p>Unlike other industry awards programs, books are not entered into predefined categories and authors or publishers are not charged a fee to enter a book. Rather than creating a profit-making venture, we focus on selecting the very best books of the year and sharing them with our global audience.</p>
      <div class="pull">The Non-Obvious Book Awards are curated, judged and created for people who love books. Especially non-fiction books.</div>
    </div>
  </div>
</section>

<!-- FOUNDER VIDEO -->
<section class="video" id="video" style="background:#fff;padding-top:0">
  <div class="wrap" style="padding-top:0">
    <div class="head">
      <div class="divider"></div>
      <p class="kicker">A Welcome From Our Founder</p>
      <h2>Did you write a book this year?</h2>
      <p class="lede">Watch this short message about the awards from our founder Rohit Bhargava, on what makes these awards different &mdash; and why you should enter your book for the 2026 competition!</p>
    </div>
    <div class="video-frame">
      <iframe src="https://www.youtube.com/embed/JCsdBrvhodI" title="A welcome from Rohit Bhargava — Non-Obvious Book Awards 2026" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
  </div>
</section>

{wave(WHT, CRM)}

<!-- HOW IT WORKS -->
<section style="background:var(--cream)">
  <div class="wrap">
    <div class="head" style="text-align:center;display:flex;flex-direction:column;align-items:center;">
      <div class="divider"></div>
      <p class="kicker">How The Awards Work</p>
      <h2>From Hundreds Of Books To Five Winners</h2>
    </div>
    <div class="steps-grid">
      <div class="step">
        <div class="n">01</div>
        <h3>The Longlist</h3>
        <p>Every year we start by selecting a Longlist of our favorite books of the year &mdash; selected from hundreds of books submitted every year.</p>
      </div>
      <div class="step">
        <div class="n">02</div>
        <h3>The Shortlist</h3>
        <p>This is followed by our Shortlist of the top books of the year &mdash; the finalists revealed during our live announcement show.</p>
      </div>
      <div class="step">
        <div class="n">03</div>
        <h3>Five Winners</h3>
        <p>Then we select winners based on five themes &mdash; importance, originality, readability, usefulness, and shareability.</p>
        <div class="themes-row">
          <span class="theme-chip" style="background:var(--purple)">Important</span>
          <span class="theme-chip" style="background:var(--blue)">Original</span>
          <span class="theme-chip" style="background:var(--orange)">Entertaining</span>
          <span class="theme-chip" style="background:var(--teal)">Useful</span>
          <span class="theme-chip" style="background:var(--magenta)">Shareable</span>
        </div>
      </div>
    </div>
    <div style="text-align:center;margin-top:56px">
      <a class="btn" href="enter.html">Learn How To Enter</a>
    </div>
  </div>
</section>

{wave(CRM, WHT)}

<!-- PUBLISHERS -->
<section class="pubs">
  <div class="wrap">
    <div class="head" style="text-align:center;display:flex;flex-direction:column;align-items:center;">
      <div class="divider"></div>
      <p class="kicker">Who Enters</p>
      <h2>Publishers From Around The World</h2>
      <p class="lede" style="max-width:760px">Every year our awards attract entries from a wide diversity of publishers around the world &mdash; of all categories and sizes. That includes the Big Five publishers and their many imprints, celebrated university presses, and scores of acclaimed independent and boutique publishing houses.</p>
    </div>
    <div class="pubs-mosaic">
      {PUB_MOSAIC}
    </div>
    <p class="pubs-foot">A selection of the 250+ publishers and imprints whose books have been entered into the Non-Obvious Book Awards.</p>
  </div>
</section>

<!-- MEDIA PARTNERSHIPS -->
<section class="partners">
  <div class="wrap">
    <div class="head" style="text-align:center;display:flex;flex-direction:column;align-items:center;">
      <div class="divider"></div>
      <p class="kicker">Amplified By The Best In Business Media</p>
      <h2>Media Partnerships</h2>
      <p class="lede" style="max-width:760px">Our annual selections don&rsquo;t just live on this site. Over the years we have teamed up with some of the biggest names in business media to share the best books of the year with millions of readers &mdash; including a full media partnership with <b>Inc.</b> magazine to present the Inc. Non-Obvious Book Awards, and a partnership with <b>Entrepreneur</b> magazine spotlighting the big ideas from each year&rsquo;s winning books.</p>
    </div>
    <div class="partner-logos">
      <a href="https://www.inc.com/nonobviousbooks" target="_blank" rel="noopener"><img src="assets/partners/inc-logo.svg" alt="Inc. magazine logo"></a>
      <a href="https://www.entrepreneur.com" target="_blank" rel="noopener"><img src="assets/partners/entrepreneur-logo.svg" alt="Entrepreneur magazine logo"></a>
    </div>
  </div>
</section>

{wave(WHT, CRM)}

<!-- FOUNDER -->
<section class="founder">
  <div class="founder-inner">
    <div class="founder-photo">
      {FOUNDER_IMG}
    </div>
    <div class="founder-body">
      <div class="divider"></div>
      <p class="kicker">About The Founder</p>
      <h2>Rohit Bhargava</h2>
      <p class="founder-role">Founder, The Non-Obvious Company &middot; 3-time WSJ Bestselling Author</p>
      <p>Rohit Bhargava is on a mission to inspire more non-obvious thinking. He is the 3-time Wall Street Journal and USA Today bestselling author of ten books and is widely considered one of the most entertaining and original speakers on trends, innovation and marketing in the world.</p>
      <p>Rohit has shared the stage with big personalities like Jay Leno, Elon Musk and will.i.am and been invited to deliver &ldquo;non-boring&rdquo; keynotes and workshops in 32 countries around the world to change the way teams and leaders think at the World Bank, NASA, Intel, LinkedIn, Coca-Cola, Disney and hundreds of other well-known organizations. Prior to becoming an entrepreneur and founding the Non-Obvious Company and Ideapress Publishing, he spent 15 years leading marketing strategy at Ogilvy and Leo Burnett where he advised global brands on human behavior, marketing and storytelling.</p>
      <p>Outside his speaking and consulting, Rohit has taught persuasive speaking and global marketing as an adjunct professor at Georgetown University, is frequently quoted in the global media and has written for Inc, Entrepreneur and GQ magazines. Rohit lives in the Washington DC area with his wife and is a proud dad of two boys. He loves the Olympics (he's been to six!) and actively hates cauliflower.</p>
    </div>
  </div>
</section>

{wave(WHT, BLK)}

<!-- COMPANY -->
<section class="company">
  <div class="company-inner">
    <div class="divider" style="margin:0 auto 24px"></div>
    <p class="kicker">Who's Behind This</p>
    <h2>About The Non-Obvious Company</h2>
    <p>These awards are organized and judged by the team at the Non-Obvious Company. We believe the world needs more non-obvious thinkers. Our mission is to help leaders, organizations and curious minds learn the habits that allow them to see what others miss and face the unknown. We do this through our published books, popular keynotes, custom workshops, annual book awards and our weekly Non-Obvious Insights Show hosted by our founder Rohit Bhargava.</p>
    <a class="btn" style="border-color:var(--yellow);background:var(--yellow);color:var(--black)" href="https://nonobvious.com" target="_blank" rel="noopener">Visit NonObvious.com</a>
  </div>
</section>

{wave(BLK, '#005E8C')}

{footer}

</body>
</html>
"""

open(os.path.join(SITE, 'about.html'), 'w').write(page)
print('wrote about.html', len(page)//1024, 'KB')

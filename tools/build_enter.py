#!/usr/bin/env python3
"""Build enter.html (How To Enter, 2026 entries open) from the homepage chrome."""
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
  /* ---------- Enter page ---------- */
  .enter-hero{background:var(--yellow);padding:150px 6vw 90px;}
  @media(max-width:560px){.enter-hero{padding:52px 20px 46px;}}
  .enter-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.4fr .6fr;gap:60px;align-items:center;}
  .enter-hero h1{font-size:clamp(2.4rem,5vw,4rem);line-height:1.04;text-transform:uppercase;letter-spacing:.02em;font-weight:900;}
  .enter-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.15rem;line-height:1.65;margin-top:22px;max-width:560px;color:#222;}
  .enter-hero .hero-stamp img{width:100%;max-width:230px;display:block;margin:0 auto;}
  .open-pill{display:inline-flex;align-items:center;gap:10px;background:var(--black);color:var(--yellow);font-family:var(--disp);font-weight:800;font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;padding:10px 20px;margin-bottom:22px;}
  .open-pill .dot{width:10px;height:10px;border-radius:50%;background:#3ddc84;animation:pulse 1.6s infinite;}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
  .fact-grid{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:40px;text-align:center;}
  .fact .big{font-family:var(--disp);font-weight:900;font-size:1.6rem;line-height:1.15;margin-bottom:8px;}
  .fact .label{font-family:var(--serif);font-style:italic;color:#555;font-size:.95rem;}
  .rules{max-width:860px;margin:0 auto;}
  .rule{display:grid;grid-template-columns:64px 1fr;gap:26px;padding:34px 0;border-bottom:1px solid rgba(0,0,0,.1);}
  .rule:last-child{border-bottom:none;}
  .rule .n{font-family:var(--disp);font-weight:900;font-size:1.6rem;color:var(--black);width:64px;height:64px;border:3px solid var(--black);display:flex;align-items:center;justify-content:center;background:var(--yellow);}
  .rule h3{font-family:var(--disp);font-weight:800;font-size:1.2rem;text-transform:uppercase;letter-spacing:.02em;margin-bottom:8px;}
  .rule p{font-size:1rem;line-height:1.75;color:#333;}
  .policies{background:var(--black);color:var(--white);}
  .policies .kicker{color:var(--yellow);}
  .policies h2{color:var(--white);}
  .policies .divider{background:var(--yellow);}
  .policy-grid{max-width:1000px;margin:48px auto 0;display:grid;grid-template-columns:repeat(3,1fr);gap:34px;text-align:left;}
  .policy{border-top:5px solid var(--yellow);padding-top:18px;}
  .policy h3{font-family:var(--disp);font-weight:800;font-size:1.05rem;text-transform:uppercase;margin-bottom:10px;}
  .policy p{font-size:.95rem;line-height:1.7;color:#cfcfcf;}
  .address-band{background:var(--cream);}
  .address-inner{max-width:1000px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start;}
  .address-card{background:var(--white);border:3px solid var(--black);padding:38px 40px;box-shadow:10px 10px 0 var(--black);}
  .address-card .kicker{margin-bottom:14px;}
  .address-card address{font-style:normal;font-family:var(--disp);font-weight:700;font-size:1.15rem;line-height:1.8;}
  .promise h2{margin-bottom:16px;}
  .promise p{font-size:1.02rem;line-height:1.8;color:#333;}
  @media(max-width:980px){.fact-grid{grid-template-columns:repeat(2,1fr);}.policy-grid{grid-template-columns:1fr;}.address-inner{grid-template-columns:1fr;}}
  @media(max-width:860px){.enter-hero-inner{grid-template-columns:1fr;}.enter-hero .hero-stamp{display:none;}}
"""

# ---------------- SEO / GEO ----------------
SEO_HEAD = _seo.head_block('enter.html', 'How To Enter — The 2026 Non-Obvious Book Awards', 'Entries for the 2026 Non-Obvious Book Awards are now open. No entry fee, no categories to pick — send two print copies by October 31, 2026.')
SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.breadcrumbs(("Home", ""), ("How To Enter", None)),
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>How To Enter — The 2026 Non-Obvious Book Awards</title>
<meta name="description" content="Entries for the 2026 Non-Obvious Book Awards are now open. No entry fee, no categories to pick — send two print copies by October 31, 2026.">
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

<!-- ENTER HERO -->
<header class="enter-hero">
  <div class="enter-hero-inner">
    <div>
      <span class="open-pill"><span class="dot"></span>2026 Entries Now Open</span>
      <div class="divider"></div>
      <p class="kicker">Have A Great Book?</p>
      <h1>How To Submit <br>A Book</h1>
      <p class="sub">Entries for the 2026 Non-Obvious Book Awards are officially open. Here's everything you need to know to enter &mdash; and why we make it easier than any other book awards program.</p>
    </div>
    <div class="hero-stamp">
      <img src="assets/badges/web/seal-black.png" alt="The Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

<!-- KEY FACTS -->
<section style="background:#fff">
  <div class="fact-grid">
    <div class="fact"><div class="big">$0</div><div class="label">No entry fee &mdash; ever</div></div>
    <div class="fact"><div class="big">2 Copies</div><div class="label">Print books, galleys or ARCs</div></div>
    <div class="fact"><div class="big">Oct 31, 2026</div><div class="label">Submission deadline</div></div>
    <div class="fact"><div class="big">December</div><div class="label">Winners announced</div></div>
  </div>
</section>

{wave(WHT, CRM)}

<!-- HOW TO ENTER -->
<section style="background:var(--cream)">
  <div class="wrap">
    <div class="head" style="text-align:center;display:flex;flex-direction:column;align-items:center;">
      <div class="divider"></div>
      <p class="kicker">The Rules</p>
      <h2>Entering Is Simple</h2>
    </div>
    <div class="rules">
      <div class="rule">
        <div class="n">1</div>
        <div>
          <h3>Check Your Eligibility</h3>
          <p>To be considered for the 2026 Non-Obvious Book Awards, books must have a publication date between November 2025 and December 2026 and be available in print &mdash; no books that are available only as ebooks or audiobooks will be considered. We accept galleys, ARCs or final copies for review. We do not review books in digital format.</p>
        </div>
      </div>
      <div class="rule">
        <div class="n">2</div>
        <div>
          <h3>Any Book With Business Applications</h3>
          <p>All entered books must have applications for business, but do not necessarily need to be officially categorized as a business book. We are happy to consider any non-fiction book that can help make a business leader or entrepreneur more successful or smarter. And remember &mdash; you don't pick a category. Every book is simply submitted, and our judges award winners in the category they believe fits best.</p>
        </div>
      </div>
      <div class="rule">
        <div class="n">3</div>
        <div>
          <h3>Tell Us Why It's Non-Obvious</h3>
          <p>Just let us know when you enter what makes the book a non-obvious submission and why we should consider it. Cover letters, press materials and any other resources may be submitted along with the books. Please do not send more than two copies of the book!</p>
        </div>
      </div>
      <div class="rule">
        <div class="n">4</div>
        <div>
          <h3>Send Two Copies By October 31, 2026</h3>
          <p>There is no fee to be considered, but we must receive two physical copies of any book entered by 10/31/26. If additional review copies are required, our team will contact you. Winners are announced every December!</p>
        </div>
      </div>
    </div>
  </div>
</section>

{wave(CRM, BLK)}

<!-- POLICIES -->
<section class="policies">
  <div class="wrap" style="text-align:center">
    <div class="divider" style="margin:0 auto 24px"></div>
    <p class="kicker">The Fine Print</p>
    <h2>A Few Things To Know</h2>
    <div class="policy-grid">
      <div class="policy">
        <h3>No Returns</h3>
        <p>Physical manuscripts, galleys or books will not be returned. Plan accordingly &mdash; and know they'll be read with care.</p>
      </div>
      <div class="policy">
        <h3>No Bribes (Even Chocolate)</h3>
        <p>We do not accept any sorts of payments or bribes in order to consider a book &mdash; even particularly delicious chocolate. If any chocolate does accompany your submission, you can expect that it also will not be returned.</p>
      </div>
      <div class="policy">
        <h3>Not A For-Profit Venture</h3>
        <p>There is no application fee to submit your book for consideration. We do not run this book program as a for-profit venture. Instead, we believe in the power of great books and want to help share them with the world.</p>
      </div>
    </div>
  </div>
</section>

{wave(BLK, CRM)}

<!-- ADDRESS + PROMISE -->
<section class="address-band">
  <div class="address-inner">
    <div class="address-card">
      <p class="kicker">Where To Send Your Book</p>
      <address>
        Non-Obvious Book Awards <br>
        To: Awards Coordinator <br>
        2961-A Hunter Mill Rd. #630 <br>
        Oakton, VA 22124
      </address>
    </div>
    <div class="promise">
      <div class="divider"></div>
      <p class="kicker">Our Promise</p>
      <h2>Every Book Gets A Fair Chance</h2>
      <p>Every book entered will receive full consideration and be reviewed carefully by our team. We deeply respect authors and the time and care it takes to write any book &hellip; and we promise to give every submission a fair chance, regardless of the topic, publisher, author or commercial success of the book.</p>
    </div>
  </div>
</section>

{wave(CRM, '#005E8C')}

{footer}

</body>
</html>
"""

open(os.path.join(SITE, 'enter.html'), 'w').write(page)
print('wrote enter.html', len(page)//1024, 'KB')

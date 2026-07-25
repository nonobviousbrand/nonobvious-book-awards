#!/usr/bin/env python3
"""Build faq.html from the homepage chrome + FAQ content."""
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

# ---------------- FAQ content ----------------
FAQS = [
 ("Why do you do this list?",
  """<p>There are two reasons we do this list: first and foremost because we love books and we don't believe there are enough efforts within the industry or media to promote non-fiction books specifically. The second reason is that we're invested in building a more Non-Obvious world for us all. We believe in the power of non-obvious ideas, and want to honor them whether we're the ones coming up with them or not!</p>"""),
 ("How are books chosen as winners?",
  """<p>We consider every aspect of a book, from its writing and quality of the ideas to the originality of the work. We are, of course, looking for &ldquo;Non-Obvious&rdquo; ideas above all. What this means to us is a concept or way of thinking that we haven't seen before. Something uniquely interesting and useful. An idea that makes us think.</p>"""),
 ("How can I submit a book?",
  """<p>Submissions for the 2026 Non-Obvious Book Awards are <strong>now open</strong>! The deadline to receive ALL submissions is October 31, 2026. Winners are announced every December.</p>
<p>Books can be submitted directly by authors, publishers, publicists, moms or anyone else who believes a book might be a good candidate for an award. We don't place artificial limits on books that can be submitted and we do consider EVERY book that is suggested to us. Every year we also specifically approach certain authors and publishers to request books that we believe have strong merit for consideration in our awards program.</p>
<p>In order to submit your book to the program, just send TWO review copies to the address noted on the <a href="index.html#enter">How To Enter</a> section.</p>"""),
 ("Do you accept digital submissions?",
  """<p>No &mdash; we only accept physical book submissions for this award. Ebooks or audio versions of books or any other digital format of a book are not eligible for these awards.</p>"""),
 ("Will you reimburse me for the shipping expenses?",
  """<p>Nope, but good on you for asking. We admire your frugality.</p>"""),
 ("Why don't you use industry-standard categories?",
  """<p>Most book awards will subdivide books they consider into categories such as leadership or sales. The problem with this is, well &hellip; obvious. What category would you put a book on sales leadership?</p>
<p>So instead of forcing submissions into a single limiting category (or having you worry that maybe you unintentionally picked the wrong category and therefore made it harder for your book to win), we have created our own categories for how we award winners (see below). Books are NOT submitted to a particular category. Instead they are simply submitted and we will award them based on the category we believe fits best.</p>"""),
 ("What are the main categories for winners?",
  """<p>As noted above, we don't segment our award winners into industry categories. Instead, we select our five favorite books of the year in the following categories:</p>
<ul class="cat-list">
<li><span class="dot" style="background:var(--purple)"></span><b>Most Important Book Of The Year</b> &mdash; A big idea that can make a difference in the world and in your life.</li>
<li><span class="dot" style="background:var(--blue)"></span><b>Most Original Book Of The Year</b> &mdash; A unique idea that you're unlikely to find anywhere else.</li>
<li><span class="dot" style="background:var(--orange)"></span><b>Most Entertaining Book Of The Year</b> &mdash; A readable and high impact idea + story that you won't be able to put down.</li>
<li><span class="dot" style="background:var(--teal)"></span><b>Most Useful Book Of The Year</b> &mdash; A practical idea with real down-to-earth advice on how to use it in your daily life.</li>
<li><span class="dot" style="background:var(--magenta)"></span><b>Most Shareable Book Of The Year</b> &mdash; A viral idea that people will (or should) be talking about in conversation.</li>
</ul>"""),
 ("How many books do you consider every year?",
  """<p>It's hard to say since we are always reading and evaluating &mdash; but this past year was our most popular yet and we considered well over 1000 titles for the awards. Making our list is highly competitive and we believe that's an important element of keeping the quality of our winners high.</p>"""),
 ("Is this award a big deal?",
  """<p>That is a hard question for us to answer, but yes &mdash; yes it is. We might be biased though. Objectively, we can tell you that we receive and review a LOT of books and every year less than 10% merit inclusion on our Longlist. And there are only ten books on our Shortlist and five top award winners &mdash; so mathematically that's pretty selective.</p>"""),
 ("Your branding isn't terrible. Is that intentional?",
  """<p>Yes it is, thanks for noticing! When putting together this program, we did an extensive review of ALL the other popular book awards programs in the industry. A sad many of them have a logo that most authors would be embarrassed to put on the cover of your book if they won it.</p>
<p>For us, branding is very important and we want everything we do to look great. We want you to use it too. So if you are an author reading this and you do win, you can expect we will not use sneaky upselling tactics like charging you money to download a high res graphic of the award badge. You will get the materials and you can use them however you like. And hopefully you won't be embarrassed by them when you do.</p>"""),
 ("When are winners announced?",
  """<p>We generally announce our Longlist selections in mid-November. We follow this with a LIVE broadcast of our selections for the Shortlist, as well as five individual winners in each of our main categories in early December. See the past live broadcasts for award announcements on our <a href="https://www.youtube.com/rohitbhargava" target="_blank" rel="noopener">YouTube channel here &raquo;</a></p>"""),
 ("I'm angry that you missed [insert book title here]. Where do I direct my outrage?",
  """<p>Since we're limited in what we can select, every year there are great books that don't make the long or short list. We're sorry that the one you loved (or one you wrote) didn't make it, but we do take a lot of time to try and be as inclusive as we can. If you do want to suggest one, though, please do and we'll definitely add it to our own personal reading list!</p>"""),
]

items = []
for i, (q, a) in enumerate(FAQS):
    op = ' open' if i == 0 else ''
    items.append(f"""      <details class="faq-item"{op}>
        <summary><span class="q-no">{i+1:02d}</span><span class="q-text">{q}</span><span class="q-toggle" aria-hidden="true"></span></summary>
        <div class="faq-a">
{a}
        </div>
      </details>""")
faq_html = '\n'.join(items)

extra_css = """
  /* ---------- FAQ page ---------- */
  .faq-hero{background:var(--yellow);padding:150px 6vw 90px;}
  @media(max-width:560px){.faq-hero{padding:52px 20px 46px;}}
  .faq-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.4fr .6fr;gap:60px;align-items:center;}
  .faq-hero h1{font-size:clamp(2.4rem,5vw,4rem);line-height:1.04;text-transform:uppercase;letter-spacing:.02em;font-weight:900;}
  .faq-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.15rem;line-height:1.65;margin-top:22px;max-width:560px;color:#222;}
  .faq-hero .hero-stamp img{width:100%;max-width:230px;display:block;margin:0 auto;}
  .faq-list{max-width:860px;margin:0 auto;}
  .faq-item{border-bottom:1px solid rgba(0,0,0,.12);}
  .faq-item summary{list-style:none;cursor:pointer;display:flex;align-items:baseline;gap:22px;padding:26px 4px;}
  .faq-item summary::-webkit-details-marker{display:none;}
  .q-no{font-family:var(--disp);font-weight:800;font-size:.85rem;color:#b5b5b5;letter-spacing:.02em;flex:0 0 auto;}
  .q-text{font-family:var(--disp);font-weight:800;font-size:1.15rem;line-height:1.35;flex:1;}
  .q-toggle{flex:0 0 auto;width:26px;height:26px;position:relative;align-self:center;}
  .q-toggle::before,.q-toggle::after{content:'';position:absolute;background:var(--black);left:50%;top:50%;transform:translate(-50%,-50%);}
  .q-toggle::before{width:16px;height:3px;}
  .q-toggle::after{width:3px;height:16px;transition:transform .18s;}
  details[open] .q-toggle::after{transform:translate(-50%,-50%) scaleY(0);}
  details[open] summary .q-text{color:var(--black);}
  .faq-a{padding:0 52px 30px;max-width:720px;}
  .faq-a p{font-size:1rem;line-height:1.75;color:#333;margin-bottom:14px;}
  .faq-a a{color:var(--black);font-weight:700;}
  .cat-list{list-style:none;margin:8px 0 16px;padding:0;}
  .cat-list li{display:flex;align-items:baseline;gap:12px;font-size:1rem;line-height:1.7;color:#333;margin-bottom:10px;}
  .cat-list .dot{flex:0 0 12px;width:12px;height:12px;border-radius:50%;position:relative;top:1px;}
  .faq-cta{background:var(--black);color:var(--white);text-align:center;}
  .faq-cta h2{color:var(--white);}
  .faq-cta .divider{background:var(--yellow);margin:0 auto 24px;}
  .faq-cta .lede{color:#cfcfcf;margin:18px auto 34px;}
  @media(max-width:860px){
    .faq-hero-inner{grid-template-columns:1fr;}
    .faq-hero .hero-stamp{display:none;}
    .faq-a{padding:0 4px 26px;}
  }
"""

# ---------------- SEO / GEO ----------------
def _strip(html_str):
    t = re.sub(r'<[^>]+>', ' ', html_str)
    t = t.replace('&ldquo;','"').replace('&rdquo;','"').replace('&rsquo;',"'").replace('&mdash;',' - ').replace('&amp;','&').replace('&hellip;','...')
    return re.sub(r'\s+', ' ', t).strip()

SEO_HEAD = _seo.head_block('faq.html', 'FAQ — The Non-Obvious Book Awards',
    'Frequently asked questions about the Non-Obvious Book Awards — how to enter, how winners are chosen, and what makes these awards different.')
SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.breadcrumbs(("Home", ""), ("FAQ", None)),
    {"@type": "FAQPage",
     "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}}
        for q, a in FAQS
     ]},
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FAQ — The Non-Obvious Book Awards</title>
<meta name="description" content="Frequently asked questions about the Non-Obvious Book Awards — how to enter, how winners are chosen, and what makes these awards different.">
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

<!-- FAQ HERO -->
<header class="faq-hero">
  <div class="faq-hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">Good Questions, Non-Obvious Answers</p>
      <h1>Frequently Asked<br>Questions</h1>
      <p class="sub">Thanks for your interest in our awards! Here are a few things we are commonly asked &mdash; along with some answers.</p>
    </div>
    <div class="hero-stamp">
      <img src="assets/badges/web/seal-black.png" alt="The Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

<!-- FAQ LIST -->
<section style="background:#fff">
  <div class="wrap">
    <div class="faq-list">
{faq_html}
    </div>
  </div>
</section>

{wave(WHT, BLK)}

<!-- CTA -->
<section class="faq-cta">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker" style="color:var(--yellow)">Still Have A Question?</p>
    <h2>Think a book belongs here?</h2>
    <p class="lede">Entries for the 2026 Non-Obvious Book Awards are now open. There's no entry fee, no categories to pick, and every submitted book gets read.</p>
    <a class="btn" style="border-color:var(--yellow);background:var(--yellow);color:var(--black)" href="index.html#enter">See How To Enter</a>
  </div>
</section>

{wave(BLK, '#005E8C')}

{footer}

</body>
</html>
"""

open(os.path.join(SITE, 'faq.html'), 'w').write(page)
print('wrote faq.html', len(page)//1024, 'KB')

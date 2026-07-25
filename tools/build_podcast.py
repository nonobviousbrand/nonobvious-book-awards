#!/usr/bin/env python3
"""Build podcast.html — The Non-Obvious Show, framed for the book-awards audience."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as _seo, json

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

EPISODES = [
    ('sabina', 83, 'How To Be A Better Boss', 'Sabina Nawaz',
     'In this episode, Sabina Nawaz shares insights from her extensive leadership experience, focusing on how pressure, power, and self-awareness influence effective management. Discover practical microhabits and strategies to become a better boss and navigate the loneliness at the top.'),
    ('nilofer', 82, 'How To Overcome the Daily Norms Holding You Back', 'Nilofer Merchant',
     'Nilofer Merchant discusses the hidden norms shaping our work environment, how to challenge them, and reframe our approach to work for greater fulfillment and innovation.'),
    ('markmedley', 81, 'The Curious Optimism of People Who Choose Impossible Quests', 'Mark Medley',
     'Explore the fascinating world of individuals pursuing seemingly impossible goals, the long-term mindset, and the hope and resilience that drive human endeavors. Author Mark Medley shares insights from his book Live to See the Day and stories of explorers, scientists, and dreamers.'),
    ('jennywood', 80, 'Having Wild Courage To Get What You Want', 'Jenny Wood',
     'Explore the unconventional traits of wild courage with Jenny Wood, a NYT best-selling author and founder of Google&rsquo;s Own Your Career program. Discover how embracing weirdness, selfishness, shamelessness, and other traits can propel your career and life forward.'),
    ('justingregg', 79, 'Why We Talk To Cats and Make Everything &ldquo;Humanish&rdquo;', 'Justin Gregg',
     'Explore the fascinating world of anthropomorphism, its impact on human behavior, AI, marketing, and the future of human-like technology with dolphin cognition researcher Justin Gregg.'),
    ('nireyal', 78, 'How Your Beliefs Can Hold You Back &hellip; Or Move You Forward', 'Nir Eyal',
     'Explore the fascinating insights into human perception, beliefs, and the power of persistence with Nir Eyal, author of Beyond Belief. Discover how our brain&rsquo;s predictive processing shapes reality, how beliefs influence behavior, and how anyone can unlock hidden potential.'),
    ('melodywilding', 77, 'How To Manage Your Boss To Win At Work', 'Melody Wilding',
     'Melody Wilding, a human behavior expert and author, shares insights on managing up, understanding human psychology at work, and practical strategies for career success.'),
    ('timminshall', 76, 'The Hidden Secrets of How Stuff Gets Made', 'Tim Minshall',
     'Explore the fascinating world of manufacturing with Tim Minshall, author of &lsquo;How Things Are Made&rsquo;. Discover how everyday products are designed, built and delivered &mdash; and why understanding making matters more than ever.'),
    ('amina', 74, 'Why Your Ambition Is Working Against You', 'Amina AlTai',
     'In this conversation, Amina AlTai discusses her book &lsquo;The Ambition Trap,&rsquo; exploring the duality of ambition and how it can be both a motivating force and a source of pain &mdash; and how to shift toward a healthier, purpose-led ambition.'),
    ('rosalind', 73, 'The Difference Between Mentors and Sponsors', 'Rosalind Chow',
     'In this episode, Dr. Rosalind Chow discusses the crucial differences between mentorship and sponsorship, and how sponsors can change the trajectory of a career by advocating for others when it matters most.'),
    ('tomas', 72, 'Don&rsquo;t Be Yourself: Why Authenticity Is Overrated', 'Tomas Chamorro-Premuzic',
     'In this episode, Tomas challenges conventional wisdom around authenticity, self-belief, and leadership &mdash; and makes the case for why editing yourself can be a smarter path to success.'),
    ('kevinertell', 71, 'How To Avoid the Strategy Trap In Business', 'Kevin Ertell',
     'In this episode, we explore the nuanced relationship between strategy and execution in business, and why great execution of a clear strategy beats a brilliant plan poorly delivered.'),
    ('monica', 70, 'Selling Your Mother: The Mrs. Meyers Clean Day Story', 'Monica Nassif',
     'Monica Nassif&rsquo;s journey with Mrs. Meyer&rsquo;s Clean Day reveals the power of authenticity in branding. By naming the brand after her mother, she created a story that resonated far beyond the cleaning aisle.'),
    ('eliot', 69, 'Telling the Stories of Custodians Saving Dying Traditions', 'Eliot Stein',
     'In a fast-paced world where technology often overshadows cultural heritage, Eliot Stein shares stories of the last custodians keeping rare traditions alive &mdash; and what their devotion teaches the rest of us.'),
    ('marina', 68, 'Why You Should Let People Yell At Your Kids', 'Marina Lopes',
     'Marina Lopes, a Brazilian American journalist, shares insights from her global research on parenting practices around the world &mdash; and what other cultures can teach us about raising resilient kids.'),
]

LINKS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'podcast_links.json')))

cards = []
PLATFORM_LABELS = [('spotify','Spotify'), ('itunes','Apple Podcasts'), ('audible','Audible')]
for key, num, title, author, desc in EPISODES:
    lk = LINKS.get(str(num), {}) or {}
    links_html = ''.join(
        f'<a href="{lk[p]}" target="_blank" rel="noopener">{label}</a>'
        for p, label in PLATFORM_LABELS if lk.get(p))
    cards.append(f'''      <article class="ep-card">
        <a href="https://www.nonobvious.com/podcast" target="_blank" rel="noopener" class="ep-art"><img src="assets/podcast/{key}.jpg" alt="The Non-Obvious Show episode {num} — {author}" loading="lazy"></a>
        <div class="ep-body">
          <span class="ep-num">Episode {num}</span>
          <h3>{title}</h3>
          <p class="ep-guest">with {author}</p>
          <p class="ep-desc">{desc}</p>
          <div class="ep-links">{links_html}</div>
        </div>
      </article>''')
cards_html = '\n'.join(cards)

extra_css = """
  /* ---------- Podcast page ---------- */
  .pod-hero{background:var(--yellow);padding:150px 6vw 90px;}
  @media(max-width:560px){.pod-hero{padding:52px 20px 46px;}}
  .pod-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.3fr .7fr;gap:60px;align-items:center;}
  .pod-hero h1{font-size:clamp(2.4rem,5vw,4rem);line-height:1.04;text-transform:uppercase;letter-spacing:.02em;font-weight:900;}
  .pod-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.15rem;line-height:1.65;margin-top:22px;max-width:560px;color:#222;}
  .pod-hero-art img{width:100%;max-width:320px;display:block;margin:0 auto;box-shadow:14px 14px 0 var(--black);}
  .pod-intro{max-width:860px;margin:0 auto;}
  .pod-intro p{font-size:1.05rem;line-height:1.85;color:#333;margin-bottom:22px;}
  .ep-grid{max-width:1140px;margin:56px auto 0;display:grid;grid-template-columns:repeat(2,1fr);gap:44px 48px;}
  .ep-card{display:grid;grid-template-columns:180px 1fr;gap:26px;align-items:start;}
  .ep-art img{width:100%;display:block;box-shadow:8px 8px 0 var(--black);transition:transform .2s;}
  .ep-art:hover img{transform:translateY(-4px);}
  .ep-num{font-family:var(--disp);font-weight:800;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;background:var(--black);color:var(--yellow);padding:5px 12px;display:inline-block;margin-bottom:10px;}
  .ep-body h3{font-family:var(--disp);font-weight:800;font-size:1.08rem;line-height:1.3;margin-bottom:4px;}
  .ep-guest{font-family:var(--serif);font-style:italic;color:#666;font-size:.92rem;margin-bottom:10px;}
  .ep-desc{font-size:.9rem;line-height:1.7;color:#444;}
  .ep-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;}
  .ep-links a{font-family:var(--disp);font-weight:700;font-size:.68rem;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;color:var(--black);border:2px solid var(--black);padding:6px 12px;transition:all .15s;background:var(--white);}
  .ep-links a:hover{background:var(--black);color:var(--yellow);}
  .pod-cta{background:var(--black);color:var(--white);text-align:center;}
  .pod-cta h2{color:var(--white);}
  .pod-cta .divider{background:var(--yellow);margin:0 auto 24px;}
  .pod-cta .lede{color:#cfcfcf;margin:18px auto 34px;}
  @media(max-width:980px){.ep-grid{grid-template-columns:1fr;}}
  @media(max-width:860px){.pod-hero-inner{grid-template-columns:1fr;}.pod-hero-art{display:none;}.ep-card{grid-template-columns:130px 1fr;gap:18px;}}
  @media(max-width:560px){.ep-card{grid-template-columns:96px 1fr;gap:14px;}}
"""

# ---------------- SEO / GEO ----------------
SEO_HEAD = _seo.head_block('podcast.html', 'The Non-Obvious Show Podcast — Be More Interesting',
    'The Non-Obvious Show — Rohit Bhargava interviews the authors behind the books we celebrate, including many selected from the annual Non-Obvious Book Awards.')
_series = {"@type": "PodcastSeries", "@id": _seo.DOMAIN + "/podcast.html#series",
    "name": "The Non-Obvious Show",
    "description": "A podcast where Rohit Bhargava interviews fascinating authors and thinkers to help you be more interesting.",
    "url": _seo.DOMAIN + "/podcast.html",
    "webFeed": "https://nonobvious.libsyn.com/rss",
    "author": _seo.person()}
SEO_LD = _seo.ld(
    _seo.organization(),
    _seo.breadcrumbs(("Home", ""), ("Podcast", None)),
    _series,
    *[{"@type": "PodcastEpisode", "episodeNumber": num, "name": f"Ep. {num}: {title}",
       "description": desc, "partOfSeries": {"@id": _seo.DOMAIN + "/podcast.html#series"}}
      for key, num, title, author, desc in EPISODES],
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Non-Obvious Show Podcast — Be More Interesting</title>
<meta name="description" content="The Non-Obvious Show — Rohit Bhargava interviews the authors behind the books we celebrate, including many selected from the annual Non-Obvious Book Awards.">
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

<!-- PODCAST HERO -->
<header class="pod-hero">
  <div class="pod-hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">Be More Interesting</p>
      <h1>The Non-Obvious <br>Show Podcast</h1>
      <p class="sub">Loved a book from our lists? Hear the story behind it. On The Non-Obvious Show, Rohit Bhargava sits down with the authors themselves &mdash; many drawn straight from the Book Awards longlist.</p>
    </div>
    <div class="pod-hero-art">
      <img src="assets/podcast-art.jpg" alt="The Non-Obvious Show with Rohit Bhargava — podcast artwork">
    </div>
  </div>
</header>

{wave(YEL, CRM)}

<!-- EPISODES -->
<section style="background:var(--cream)">
  <div class="wrap">
    <div class="head" style="text-align:center;display:flex;flex-direction:column;align-items:center;">
      <div class="divider"></div>
      <p class="kicker">Recent Episodes</p>
      <h2>Meet The Authors Behind The Books</h2>
    </div>
    <div class="ep-grid">
{cards_html}
    </div>
    <div style="text-align:center;margin-top:64px">
      <a class="btn btn-dark" href="https://www.nonobvious.com/podcast" target="_blank" rel="noopener">More Episodes &rarr;</a>
    </div>
  </div>
</section>

{wave(CRM, WHT)}

<!-- ABOUT THE SHOW -->
<section style="background:#fff">
  <div class="wrap">
    <div class="pod-intro">
      <div class="divider"></div>
      <p class="kicker">About The Show</p>
      <h2 style="margin-bottom:26px">Books that expand your way of thinking.</h2>
      <p>Can diversity be funny? Who owns the air? Why don&rsquo;t companies practice more common sense? The answers to these questions are not so obvious &hellip; and that&rsquo;s the point.</p>
      <p>Each week Rohit interviews an author whose book offers an inspiring form of non-obvious thinking on topics such as afrofuturism, technoableism, and existential hope. The featured books include those selected from the annual Non-Obvious Book Awards, and other books that he has recently found captivating &mdash; so if a book on our longlist caught your eye, there&rsquo;s a good chance you can hear its author tell the story behind it here.</p>
    </div>
  </div>
</section>

{wave(WHT, BLK)}

<!-- CTA -->
<section class="pod-cta">
  <div class="wrap">
    <div class="divider"></div>
    <p class="kicker" style="color:var(--yellow)">Listen Anywhere</p>
    <h2>New episodes every week.</h2>
    <p class="lede">The Non-Obvious Show is available on Spotify, Apple Podcasts and Audible. Explore the full episode archive for more conversations with award-winning authors.</p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap">
      <a class="btn" style="border-color:var(--yellow);background:var(--yellow);color:var(--black)" href="https://open.spotify.com/show/4oJta8F88JXqwaHQL7KXXh" target="_blank" rel="noopener">Spotify</a>
      <a class="btn" style="border-color:var(--yellow);background:var(--yellow);color:var(--black)" href="https://podcasts.apple.com/us/podcast/the-non-obvious-show/id1751547493" target="_blank" rel="noopener">Apple Podcasts</a>
      <a class="btn" style="border-color:var(--yellow);background:transparent;color:var(--yellow)" href="https://www.nonobvious.com/podcast" target="_blank" rel="noopener">See All Episodes</a>
    </div>
  </div>
</section>

{wave(BLK, '#005E8C')}

{footer}

</body>
</html>
"""

open(os.path.join(SITE, 'podcast.html'), 'w').write(page)
print('wrote podcast.html', len(page)//1024, 'KB')

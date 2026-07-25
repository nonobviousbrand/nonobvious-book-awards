#!/usr/bin/env python3
"""Build award-category roundup topic pages (e.g. Most Useful winners across all years).

Usage: python3 build_topic.py useful
"""
import glob, importlib.util, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as _seo
from podcast_guests import was_guest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
AFF_TAG = 'influenmarket-20'
YEARS = ['2014', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


# ---------------- topic configs ----------------
TOPICS = {
    'useful': {
        'slug': 'most-useful-books.html',
        'cat_match': 'useful',
        'kicker': 'Award Winner Roundups',
        'h1': 'The Most Useful<br>Business Books Of<br>The Past Decade',
        'title': 'The Most Useful Business Books of the Past Decade | Non-Obvious Book Awards',
        'meta': ('The most useful business and non-fiction books of the past decade — every winner of the '
                 'Most Useful Book award from the Non-Obvious Book Awards, 2014 to today.'),
        'intro': ('Every year since 2014, the Non-Obvious Book Awards have honored one book as the '
                  '<b>Most Useful Book of the Year</b>: the book our judges believe delivers the most '
                  'practical, immediately applicable ideas of any book published that year. Collected here for '
                  'the first time: every winner, in one definitive reading list.'),
        'accent': 'teal',
        'badge': 'assets/badges/generic/USEFUL-generic.png',
        'blurbs': {
            'everybodywrites': 'The book that declared "everyone is a writer now". Ann Handley\'s field guide to creating ridiculously good content remains the standard for anyone who writes for business, from emails to entire marketing campaigns.',
            'tedtalks': 'TED curator Chris Anderson reveals how the world\'s best speakers build talks that spread: the closest thing there is to an official manual for modern public speaking.',
            'exactlywhattosay': 'Phil M. Jones distills persuasion into a set of "magic words": precise phrases that change how people respond to you in sales conversations, negotiations and everyday influence.',
            'factfulness': 'Hans Rosling\'s data-driven case that the world is better than you think, and a training manual for the ten instincts that distort how leaders read the world. Bill Gates called it one of the most important books he\'s ever read.',
            'writingtopersuade': 'Longtime New York Times op-ed editor Trish Hall spent years deciding which arguments worked. Here she shares what actually changes minds, and why facts alone never do.',
            'trueorfalse': 'Former CIA analyst Cindy Otis delivers a practical guide to spotting misinformation and fake news: a skill that has only become more essential every year since it won.',
            'thinkagain': 'Adam Grant\'s blockbuster on the power of rethinking: why the smartest people update their views, and how intellectual humility beats being right. A modern classic of useful thinking.',
            'thinking101': 'Yale psychologist Woo-kyoung Ahn turns her famous "Thinking" course into a guide to the reasoning errors we all make, and the research-backed ways to fix them.',
            'outragemachine': 'Tobias Rose-Stockwell maps how social media turned outrage into a business model, and gives readers practical tools to resist the machine and communicate better online.',
            'negotiatingwhileblack': 'Damali Peterman delivers sharp, real-world negotiation strategy that acknowledges what most negotiation books ignore: who you are changes the conversation. Useful for every negotiator, essential for many.',
            'wildcourage': 'Ex-Google executive Jenny Wood reclaims nine "bad" traits, from weird to selfish, as the courage skills that actually get you what you want at work and in life.',
        },
    },
    'important': {
        'slug': 'most-important-books.html',
        'cat_match': 'important',
        'kicker': 'Award Winner Roundups',
        'h1': 'The Most Important<br>Non-Fiction Books<br>Of The Past Decade',
        'title': 'The Most Important Non-Fiction Books of the Past Decade | Non-Obvious Book Awards',
        'meta': ('The most important non-fiction and business books of the past decade — every winner of the '
                 'Most Important Book award from the Non-Obvious Book Awards, 2014 to today.'),
        'intro': ('Every year since 2014, the Non-Obvious Book Awards have honored one book as the '
                  '<b>Most Important Book of the Year</b>: the book with the biggest ideas about the world '
                  'we live in, and the one our judges believe matters most. Collected here: every winner, in one '
                  'definitive reading list.'),
        'accent': 'purple',
        'badge': 'assets/badges/generic/IMPORTANT-generic.png',
        'blurbs': {
            'theconfidencecode': 'Journalists Katty Kay and Claire Shipman investigate the science of self-assurance, and why closing the confidence gap matters as much as competence for women at work.',
            'persuadable': 'Al Pittampalli makes the counterintuitive case that the willingness to change your mind, being persuadable, is a defining strength of modern leadership.',
            'givework': 'Samasource founder Leila Janah argues the surest way to end global poverty is not charity but work, and shows how giving work transforms lives and communities.',
            'bullshitjobs': 'Anthropologist David Graeber names the phenomenon everyone recognized but no one discussed: jobs that even the people doing them believe are meaningless, and what that does to us.',
            'secondhand': 'Adam Minter follows our castoffs through the hidden global economy of secondhand goods, revealing what really happens to the things we give away.',
            'makechange': 'Activist Shaun King draws on his years at the center of modern movements to lay out how outrage becomes organized, durable change.',
            'thelonelycentury': 'Economist Noreena Hertz documents how loneliness became a defining condition of our age, reshaping our health, our economies and our politics, and what it takes to reconnect.',
            'stolenfocus': 'Johann Hari investigates why the world stopped paying attention, and shows that our attention crisis is not a personal failing but something being done to us.',
            'howbigthingsgetdone': 'Megaproject expert Bent Flyvbjerg distills a lifetime of data on why big projects fail, and the surprising factors behind the rare ones that succeed. Essential for anyone leading anything ambitious.',
            'bravenewwords': 'Khan Academy founder Salman Khan offers the most credible early map of how AI will transform how our kids learn, and why that future is more hopeful than we fear.',
            'moralambition': 'Rutger Bregman challenges the most talented people of our generation to stop wasting their careers, and redirect their ambition toward the world\'s biggest problems.',
        },
    },
    'original': {
        'slug': 'most-original-books.html',
        'cat_match': 'original',
        'kicker': 'Award Winner Roundups',
        'h1': 'The Most Original<br>Non-Fiction Books<br>Of The Past Decade',
        'title': 'The Most Original Non-Fiction Books of the Past Decade | Non-Obvious Book Awards',
        'meta': ('The most original non-fiction books of the past decade — every winner of the Most Original '
                 'Book award from the Non-Obvious Book Awards, 2014 to today.'),
        'intro': ('Every year since 2014, the Non-Obvious Book Awards have honored one book as the '
                  '<b>Most Original Book of the Year</b>: the book unlike anything else published that '
                  'year, built on an idea we had simply never seen before. Collected here: every winner, in one '
                  'definitive reading list.'),
        'accent': 'blue',
        'badge': 'assets/badges/generic/ORIGINAL-generic.png',
        'blurbs': {
            'thedoodlerevolution': 'Sunni Brown makes the serious case for doodling as a thinking tool: a visual language that unlocks memory, insight and better ideas in even the most buttoned-up workplaces.',
            'messy': 'Tim Harford argues that disorder, in our desks, our plans and our lives, is a creative force, and that our instinct to tidy everything comes at a real cost.',
            'winbigly': 'Dilbert creator Scott Adams dissects the persuasion techniques that powered one of the most unlikely campaigns in political history: a provocative field guide to influence in a post-fact world.',
            'winnerstakeall': 'Anand Giridharadas\'s unsparing look at how the global elite\'s worldchanging efforts often protect the very systems that created the problems: a book that reframed an entire debate about philanthropy.',
            'nineliesaboutwork': 'Marcus Buckingham and Ashley Goodall take aim at the workplace\'s most cherished orthodoxies, from culture to feedback to work-life balance, and explain what the evidence actually says.',
            'thelostfamily': 'Libby Copeland explores how at-home DNA tests are upending identity, exposing family secrets and rewriting what it means to be related.',
            'whenweceasetounderstandtheworld': 'Benjam\u00edn Labatut\'s genre-defying account of the scientists whose discoveries brushed against madness: a book that reads like nothing else honored in our awards\' history.',
            'allthelivingandthedead': 'Hayley Campbell spends time with the people who work with death, from embalmers to executioners to gravediggers, to ask what their work teaches the rest of us about living.',
            'pockets': 'Hannah Carlson turns an everyday afterthought into a revelatory cultural history: who gets pockets, who doesn\'t, and what that says about power, gender and design.',
            'trashtalk': 'Rafi Kohan explores the art, science and psychology of talking trash, from locker rooms to boardrooms, and what verbal combat reveals about competition itself.',
            'dinnerwithkingtut': 'Sam Kean joins the experimental archaeologists recreating the sounds, smells and tastes of the ancient world: history you can practically eat.',
        },
    },
    'entertaining': {
        'slug': 'most-entertaining-books.html',
        'cat_match': 'entertaining',
        'kicker': 'Award Winner Roundups',
        'h1': 'The Most Entertaining<br>Non-Fiction Books<br>Of The Past Decade',
        'title': 'The Most Entertaining Non-Fiction Books of the Past Decade | Non-Obvious Book Awards',
        'meta': ('The most entertaining non-fiction books of the past decade — every winner of the Most '
                 'Entertaining Book award from the Non-Obvious Book Awards, 2014 to today.'),
        'intro': ('Every year since 2014, the Non-Obvious Book Awards have honored one book as the '
                  '<b>Most Entertaining Book of the Year</b>: proof that non-fiction can be every bit as '
                  'fun as it is smart. Collected here: every winner, in one definitive reading list.'),
        'accent': 'orange',
        'badge': 'assets/badges/generic/ENTERTAINING-generic.png',
        'blurbs': {
            'dataclysm': 'OkCupid co-founder Christian Rudder mines millions of data points to reveal who we really are when we think nobody\'s watching: funny, fascinating and occasionally alarming.',
            'disrupted': 'Journalist Dan Lyons\'s riotous memoir of going from Newsweek to a tech startup at age 50: still one of the funniest and sharpest books ever written about startup culture.',
            'fiftyinventionsthatshapedthemoderneconomy': 'Tim Harford spins the stories of fifty unlikely inventions, from barbed wire to the barcode, that quietly built the modern economy.',
            'theformula': 'Network scientist Albert-L\u00e1szl\u00f3 Barab\u00e1si reveals the universal laws behind success, and why performance alone is never enough.',
            'junior': 'Thomas Kemeny\'s irreverent, genuinely useful guide to surviving and thriving in advertising: career advice that reads like entertainment.',
            'lurking': 'Joanne McNeil tells the history of the internet from the perspective that matters most and gets written about least: the user\'s.',
            'fourlostcities': 'Annalee Newitz tours four vanished metropolises, from \u00c7atalh\u00f6y\u00fck to Cahokia, to uncover why cities die and what our own urban future can learn from theirs.',
            'atlasoftheinvisible': 'James Cheshire and Oliver Uberti turn overlooked data into breathtaking maps and graphics that make the invisible patterns of our world impossible to unsee.',
            'thetheoryofeverythingelse': 'From the co-host of No Such Thing As A Fish, a joyful tour of the world\'s weirdest theories and the brilliant eccentrics who believed them.',
            'stickynotes': 'Teacher Matthew Eicheldinger\'s collection of funny, tender true stories from the classroom: the book behind the beloved viral videos.',
            'thefutureofstorytelling': 'Charles Melcher charts how stories are evolving beyond the page and screen into immersive, interactive experiences that are rewriting the storyteller\'s craft.',
        },
    },
    'shareable': {
        'slug': 'most-shareable-books.html',
        'cat_match': 'shareable',
        'kicker': 'Award Winner Roundups',
        'h1': 'The Most Shareable<br>Non-Fiction Books<br>Of The Past Decade',
        'title': 'The Most Shareable Non-Fiction Books of the Past Decade | Non-Obvious Book Awards',
        'meta': ('The most shareable non-fiction books of the past decade — every winner of the Most Shareable '
                 'Book award from the Non-Obvious Book Awards, 2014 to today.'),
        'intro': ('Every year since 2014, the Non-Obvious Book Awards have honored one book as the '
                  '<b>Most Shareable Book of the Year</b>: the book you finish and immediately have to '
                  'tell everyone about. Collected here: every winner, in one definitive reading list.'),
        'accent': 'magenta',
        'badge': 'assets/badges/generic/SHAREABLE-generic.png',
        'blurbs': {
            'howtheworldseesyou': 'Sally Hogshead flips personal branding on its head: forget how you see the world. discover how the world sees you, and lead with what makes you fascinating.',
            'smalldata': 'Brand detective Martin Lindstrom shows how tiny human clues, like a worn sneaker or a fridge magnet, reveal desires that big data completely misses.',
            'hitrefresh': 'Satya Nadella\'s inside account of transforming Microsoft by putting empathy at the center of one of the world\'s most powerful companies.',
            'rebeltalent': 'Harvard\'s Francesca Gino makes the research-backed case that the most valuable people at work are the ones who break the rules: constructively.',
            'latebloomers': 'Rich Karlgaard pushes back on our obsession with early achievement and celebrates the quiet power of blooming on your own schedule.',
            'humankind': 'Rutger Bregman\'s hopeful history argues that most people, most of the time, are fundamentally decent, and that believing it changes everything.',
            'move': 'Parag Khanna maps the forces, climate, economics, demographics, that will make the next decades the most mobile in human history, and where we\'ll all go.',
            'quit': 'Poker champion Annie Duke dismantles our worship of grit and teaches the most undervalued skill in business and life: knowing when to walk away.',
            'yourbrainonart': 'Susan Magsamen and Ivy Ross share the new science of neuroaesthetics: how making and experiencing art measurably transforms our brains, bodies and lives.',
            'supercommunicators': 'Charles Duhigg decodes the secret language of connection, and shows how anyone can learn the skills that make conversations actually work.',
            'carelesspeople': 'Sarah Wynn-Williams\'s explosive insider memoir of life among Facebook\'s leadership: the book everyone in tech spent the year talking about.',
        },
    },
}


from topics_curated import CURATED
TOPICS.update(CURATED)


# ---------------- gather winners ----------------
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


def build(topic_key):
    cfg = TOPICS[topic_key]
    isbns_all = json.load(open(os.path.join(ROOT, 'tools', 'yeardata', 'isbns.json')))
    entries = []
    if 'books' in cfg:  # curated list, given newest-first
        for bk in cfg['books']:
            y, t, a, tag = bk[:4]
            cover_override = bk[4] if len(bk) > 4 else None
            label = '2014/15' if y == '2014' else y
            isbn = isbns_all.get(y, {}).get(norm(t))
            full_tag = tag[1:] if tag.startswith('!') else f'{label} &middot; {tag}'
            entries.append({
                'year': y, 'label': label, 'tag': full_tag, 'title': t, 'author': a,
                'cover': cover_override or find_cover(y, t), 'isbn': isbn,
                'aff': f'https://www.amazon.com/dp/{isbn}/?tag={AFF_TAG}' if isbn else None,
                'shop': _seo.bookshop_url(isbn),
                'blurb': cfg['blurbs'].get(norm(t), ''),
                'award': None if tag.startswith('!') else f'Non-Obvious Book Awards {label} {tag}',
                'no_year_link': tag.startswith('!') or not y.isdigit(),
            })
    else:
        for y in YEARS:
            d = load_year(y)
            label = getattr(d, 'YEAR_LABEL', y)
            for cat, col, t, a in d.WINNERS:
                if cfg['cat_match'] in cat.lower():
                    isbn = isbns_all.get(y, {}).get(norm(t))
                    entries.append({
                        'year': y, 'label': label, 'tag': f'{label} &middot; {cat} Winner', 'title': t, 'author': a,
                        'cover': find_cover(y, t), 'isbn': isbn,
                        'aff': f'https://www.amazon.com/dp/{isbn}/?tag={AFF_TAG}' if isbn else None,
                        'shop': _seo.bookshop_url(isbn),
                        'blurb': cfg['blurbs'].get(norm(t), ''),
                        'award': f'{cat} Book of {label} — Non-Obvious Book Awards Winner',
                    })
        assert entries, 'no winners matched'
        entries.reverse()  # most recent winner first
    assert entries, 'no books'

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
  /* ---------- Topic roundup page ---------- */
  .topic-hero{background:var(--yellow);padding:120px 6vw 90px;}
  .topic-hero-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:1.3fr .7fr;gap:60px;align-items:center;}
  .topic-hero h1{font-size:clamp(2.3rem,4.6vw,3.7rem);line-height:1.06;text-transform:uppercase;font-weight:900;}
  .topic-hero .sub{font-family:var(--serif);font-style:italic;font-size:1.18rem;line-height:1.7;margin-top:24px;max-width:600px;}
  .hero-disclaimer{font-size:.82rem;color:#6b5a10;margin-top:18px;max-width:560px;line-height:1.6;}
  .topic-hero .hero-stamp img{width:100%;max-width:240px;transform:none;filter:drop-shadow(0 18px 32px rgba(0,0,0,.16));margin:0 auto;display:block;}
  .roundup{max-width:960px;margin:0 auto;}
  .ru-row{display:grid;grid-template-columns:180px 1fr;gap:44px;padding:52px 0;border-bottom:1px solid rgba(0,0,0,.1);align-items:start;}
  .ru-row:last-child{border-bottom:none;}
  .ru-cover img{width:100%;box-shadow:10px 10px 0 rgba(0,0,0,.14);transition:transform .2s;}
  .ru-cover a:hover img{transform:translateY(-4px);}
  .ru-year{display:inline-block;font-family:var(--disp);font-weight:900;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;background:var(--black);color:var(--yellow);padding:6px 14px;margin-bottom:14px;}
  .ru-body h3{font-family:var(--disp);font-weight:900;font-size:1.7rem;line-height:1.15;margin-bottom:6px;}
  .ru-body .auth{font-family:var(--serif);font-style:italic;color:#555;font-size:1.05rem;margin-bottom:16px;}
  .ru-body p.blurb{font-size:1rem;line-height:1.8;color:#333;max-width:640px;}
  .ru-links{margin-top:20px;display:flex;gap:14px;flex-wrap:wrap;}
  .ru-btn{display:inline-block;font-family:var(--disp);font-weight:800;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;padding:12px 22px;border:3px solid var(--black);background:var(--yellow);color:var(--black);transition:all .2s;}
  .ru-btn:hover{background:var(--black);color:var(--yellow);}
  .ru-btn.ghost{background:transparent;}
  .ru-btn.ghost:hover{background:var(--black);color:var(--white);}
  .ru-btn.amz{background:#FF9900;border-color:var(--black);color:var(--black);}
  .ru-btn.amz:hover{background:var(--black);color:#FF9900;}
  .ru-btn.local{background:#45114F;border-color:#45114F;color:var(--white);}
  .ru-btn.local:hover{background:transparent;color:#45114F;}
  .ru-btn.pod{background:var(--white);border-color:var(--black);color:var(--black);}
  .ru-btn.pod:hover{background:var(--yellow);}
  @media(max-width:860px){.topic-hero-inner{grid-template-columns:1fr;}.topic-hero .hero-stamp{display:none;}}
  @media(max-width:640px){.ru-row{grid-template-columns:1fr;gap:24px;}.ru-cover img{max-width:200px;}}
  @media(max-width:560px){
    .topic-hero{padding:52px 20px 46px;}
    .ru-row{padding:30px 0;gap:16px;}
    .ru-cover img{max-width:120px;}
  }
"""

    rows = []
    for e in entries:
        cover_html = (f'<a href="{e["aff"]}" target="_blank" rel="noopener sponsored"><img src="{e["cover"]}" '
                      f'alt="{e["title"]} by {e["author"]} — book cover" loading="lazy"></a>') if e['cover'] else ''
        links = []
        if e['aff']:
            links.append(f'<a class="ru-btn amz" href="{e["aff"]}" target="_blank" rel="noopener sponsored">Buy Amazon</a>')
        if e.get('shop'):
            links.append(f'<a class="ru-btn local" href="{e["shop"]}" target="_blank" rel="noopener sponsored">Buy Local</a>')
        if was_guest(e['author']):
            links.append('<a class="ru-btn pod" href="https://www.nonobvious.com/podcast" target="_blank" rel="noopener">Listen To Episode</a>')
        if not e.get('no_year_link'):
            links.append(f'<a class="ru-btn ghost" href="{e["year"]}.html">All {e["label"]} Winners &#8594;</a>')
        rows.append(f'''      <div class="ru-row">
        <div class="ru-cover">{cover_html}</div>
        <div class="ru-body">
          <span class="ru-year">{e["tag"]}</span>
          <h3>{e["title"]}</h3>
          <p class="auth">by {e["author"]}</p>
          <p class="blurb">{e["blurb"]}</p>
          <div class="ru-links">{''.join(links)}</div>
        </div>
      </div>''')

    # ---------------- SEO ----------------
    page_title = cfg['title']
    seo_head = _seo.head_block(cfg['slug'], page_title, cfg['meta'])
    books = [_seo.book(e['title'], e['author'], isbn=e['isbn'],
                       image=f"{_seo.DOMAIN}/{e['cover']}" if e['cover'] else None,
                       url=e['aff'],
                       award=e['award'])
             for e in entries]
    seo_ld = _seo.ld(
        _seo.organization(),
        _seo.breadcrumbs(("Home", ""), ("Best Books Roundups", "index.html#archive"), (page_title.split('|')[0].strip(), None)),
        _seo.item_list(page_title.split('|')[0].strip(), cfg['meta'], books, f"{_seo.DOMAIN}/{cfg['slug']}"),
    )

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<meta name="description" content="{cfg['meta']}">
{seo_head}
{seo_ld}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@700;800;900&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Lora:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
{style}
<style>{extra_css}</style>
</head>
<body>

{header}

<!-- TOPIC HERO -->
<header class="topic-hero">
  <div class="topic-hero-inner">
    <div>
      <div class="divider"></div>
      <p class="kicker">{cfg['kicker']}</p>
      <h1>{cfg['h1']}</h1>
      <p class="sub">{cfg['intro']}</p>
      <p class="hero-disclaimer">*This list does not include books published in 2026, which are currently under review as part of our 2026 awards program.</p>
    </div>
    <div class="hero-stamp">
      <img src="{cfg['badge']}" alt="The Non-Obvious Book Award seal">
    </div>
  </div>
</header>

{wave(YEL, WHT)}

<!-- ROUNDUP -->
<section style="background:#fff">
  <div class="roundup">
{chr(10).join(rows)}
  </div>
</section>

{wave(WHT, CRM)}

<!-- CROSS CTA -->
<section style="background:var(--cream);text-align:center">
  <div class="wrap" style="display:flex;flex-direction:column;align-items:center;">
    <div class="divider"></div>
    <p class="kicker">Keep Exploring</p>
    <h2>See every winner, every year.</h2>
    <p class="lede" style="text-align:center">Browse the full archive of winners, shortlists and 100-book longlists from every year of the Non-Obvious Book Awards.</p>
    <a class="btn btn-dark" style="margin-top:30px" href="index.html#archive">Explore The Archive &#8594;</a>
  </div>
</section>

{wave(CRM, '#005E8C')}

{footer}

</body>
</html>
'''
    out = os.path.join(SITE, cfg['slug'])
    open(out, 'w').write(page)
    print('wrote', cfg['slug'], len(page) // 1024, 'KB,', len(entries), 'books')


if __name__ == '__main__':
    for key in (sys.argv[1:] or ['useful']):
        build(key)

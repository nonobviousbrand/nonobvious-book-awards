"""Shared SEO/GEO helpers: canonical + OG/Twitter head block and JSON-LD builders."""
import json

DOMAIN = 'https://www.nonobviousbookawards.com'
SITE_NAME = 'The Non-Obvious Book Awards'
DEFAULT_OG = DOMAIN + '/assets/longlist-mosaic.jpg'

SAME_AS = [
    'https://nonobvious.com',
    'https://www.youtube.com/@rohitbhargava',
    'https://www.linkedin.com/in/rohitbhargava/',
    'https://www.instagram.com/rohitbb/',
    'https://www.tiktok.com/@rohitbhargavadc',
]


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def head_block(path, title, desc, og_image=None, og_type='website'):
    """canonical + Open Graph + Twitter card tags. path='' for homepage."""
    url = f'{DOMAIN}/{path}' if path else DOMAIN + '/'
    img = og_image or DEFAULT_OG
    t, d = esc(title), esc(desc)
    return f'''<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">'''


def ld(*objs):
    """Wrap schema.org dicts in a single JSON-LD script tag (@graph)."""
    graph = {'@context': 'https://schema.org', '@graph': list(objs)}
    return ('<script type="application/ld+json">'
            + json.dumps(graph, ensure_ascii=False, separators=(',', ':'))
            + '</script>')


def organization():
    return {
        '@type': 'Organization',
        '@id': DOMAIN + '/#organization',
        'name': SITE_NAME,
        'alternateName': ['Non-Obvious Book Awards', 'NOBA'],
        'url': DOMAIN + '/',
        'logo': DOMAIN + '/assets/badges/web/seal-black.png',
        'description': ('An annual book awards program that curates the best non-fiction books of the year. '
                        'No categories, no entry fees. Winners are chosen across five themes: most important, '
                        'most original, most entertaining, most useful and most shareable.'),
        'foundingDate': '2014',
        'founder': person(),
        'parentOrganization': {
            '@type': 'Organization',
            'name': 'The Non-Obvious Company',
            'url': 'https://nonobvious.com',
        },
        'sameAs': SAME_AS,
    }


def person():
    return {
        '@type': 'Person',
        '@id': DOMAIN + '/#rohit',
        'name': 'Rohit Bhargava',
        'jobTitle': 'Founder, The Non-Obvious Company',
        'description': ('3-time Wall Street Journal bestselling author of ten books on trends, innovation and '
                        'marketing, founder of the Non-Obvious Company and Ideapress Publishing, and curator of '
                        'the annual Non-Obvious Book Awards.'),
        'url': 'https://rohitbhargava.com',
        'sameAs': SAME_AS,
    }


def website():
    return {
        '@type': 'WebSite',
        '@id': DOMAIN + '/#website',
        'url': DOMAIN + '/',
        'name': SITE_NAME,
        'description': 'The best non-fiction books of the year, every year since 2014 — winners, shortlists and 100-book longlists.',
        'publisher': {'@id': DOMAIN + '/#organization'},
    }


def breadcrumbs(*items):
    """items: (name, path-or-None-for-current) tuples."""
    els = []
    for i, (name, path) in enumerate(items, 1):
        el = {'@type': 'ListItem', 'position': i, 'name': name}
        if path is not None:
            el['item'] = f'{DOMAIN}/{path}' if path else DOMAIN + '/'
        els.append(el)
    return {'@type': 'BreadcrumbList', 'itemListElement': els}


def book(title, author, isbn=None, image=None, url=None, award=None):
    authors = [a.strip() for a in author.replace(' and ', '|').replace(' & ', '|').split('|') if a.strip()]
    b = {
        '@type': 'Book',
        'name': title,
        'author': [{'@type': 'Person', 'name': a} for a in authors] if len(authors) > 1
                  else {'@type': 'Person', 'name': authors[0] if authors else author},
    }
    if isbn:
        b['isbn'] = isbn
    if image:
        b['image'] = image
    if url:
        b['url'] = url
    if award:
        b['award'] = award
    return b


def item_list(name, description, books, list_url):
    return {
        '@type': 'ItemList',
        'name': name,
        'description': description,
        'url': list_url,
        'numberOfItems': len(books),
        'itemListOrder': 'https://schema.org/ItemListOrderAscending',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'item': bk}
            for i, bk in enumerate(books, 1)
        ],
    }


# ---------------- Bookshop.org affiliate links ----------------
BOOKSHOP_ID = '8476'
_ISBN13_OVERRIDES = {'B0DRZGQ6FV': '9798892790727'}  # Bag Man (979-prefix, no ISBN-10)


def isbn13(isbn10):
    """Convert ISBN-10 (or override ASIN) to ISBN-13."""
    if not isbn10:
        return None
    if isbn10 in _ISBN13_OVERRIDES:
        return _ISBN13_OVERRIDES[isbn10]
    import re as _re
    if not _re.match(r'^[0-9]{9}[0-9X]$', isbn10):
        return None
    core = '978' + isbn10[:9]
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(core))
    return core + str((10 - total % 10) % 10)


def bookshop_url(isbn10):
    i13 = isbn13(isbn10)
    return f'https://bookshop.org/a/{BOOKSHOP_ID}/{i13}' if i13 else None

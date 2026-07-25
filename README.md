# The Non-Obvious Book Awards — Website

Static site for www.nonobviousbookawards.com. The `site/` folder is the finished website
(what Netlify publishes). The `tools/` folder contains the Python scripts that generate it.

## How the site is built

Every page in `site/` is generated from data + templates in `tools/`:

| Script | Generates |
|---|---|
| `tools/build_year.py <year>` | Year pages (2014, 2016–2025) from `tools/yeardata/y<year>.py` |
| `tools/build_topic.py <key>` | Roundup pages (award categories + topics + South Asian authors) |
| `tools/build_about.py` etc. | About, FAQ, Podcast, How To Enter pages |
| `site/index.html` | The homepage — edited directly, and the source of shared header/footer |

Rebuild everything after any change to `site/index.html` (header/footer/newsletter are
extracted from it by every other builder):

```
cd <repo root>
for y in 2014 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025; do python3 tools/build_year.py $y; done
python3 tools/build_about.py; python3 tools/build_faq.py; python3 tools/build_podcast.py; python3 tools/build_enter.py
python3 tools/build_topic.py useful important original entertaining shareable entrepreneurs ai marketing productivity memoirs southasian
```

Requires Python 3 with Pillow (`pip install Pillow`).

## Common updates

- **Add a new awards year**: create `tools/yeardata/y2026.py` (copy y2025.py as a template:
  winners, shortlist, longlist, trends, video ID, blurbs), add cover images to
  `site/assets/covers/2026/`, ISBNs to `tools/yeardata/isbns.json`, then build.
- **Change a book summary**: edit the year's `WINNER_BLURBS`/`SHORTLIST_BLURBS` (year pages)
  or the topic config blurbs in `tools/build_topic.py` / `tools/topics_curated.py`, rebuild.
- **New podcast guest**: add the name to `tools/podcast_guests.py`, rebuild — every page
  with that author gets a LISTEN TO EPISODE button automatically.
- **Affiliate IDs**: Amazon tag and Bookshop ID live in `tools/build_topic.py` (AFF_TAG)
  and `tools/seo.py` (BOOKSHOP_ID).
- **SEO/schema**: `tools/seo.py` generates canonical/OG tags and JSON-LD for all builders.
  `site/sitemap.xml`, `site/robots.txt` and `site/llms.txt` are maintained by hand — add
  any new page to the sitemap and llms.txt.

## Deployment

Netlify publishes the `site/` folder directly (see `netlify.toml`). Any commit pushed to
the main branch goes live automatically in about a minute.

#!/usr/bin/env python3
"""Inline local assets into a site page as data URIs and write /tmp/preview-<name>.html"""
import base64, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    raw = open(path, 'rb').read()
    if ext in ('.jpg', '.jpeg') and HAS_PIL and len(raw) > 200_000:
        im = Image.open(io.BytesIO(raw)).convert('RGB')
        if max(im.size) > 2200:
            im.thumbnail((2200, 2200))
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=80)
        raw = buf.getvalue()
    mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.gif': 'image/gif', '.svg': 'image/svg+xml', '.webp': 'image/webp'}.get(ext, 'application/octet-stream')
    return f'data:{mime};base64,' + base64.b64encode(raw).decode()


def build(name):
    src = os.path.join(SITE, name)
    html = open(src).read()

    def repl(m):
        rel = m.group(1)
        p = os.path.join(SITE, rel)
        if os.path.exists(p):
            return f'src="{data_uri(p)}"'
        return m.group(0)

    html = re.sub(r'src="(assets/[^"]+)"', repl, html)

    def repl_css(m):
        rel = m.group(1)
        p = os.path.join(SITE, rel)
        if os.path.exists(p):
            return f'url({data_uri(p)})'
        return m.group(0)

    html = re.sub(r'url\((assets/[^)]+)\)', repl_css, html)
    # neutralize internal page links so preview doesn't 404
    html = re.sub(r'href="(?:index\.html|about\.html|enter\.html|faq\.html|podcast\.html|20\d\d\.html)(#[\w-]*)?"',
                  'href="#"', html)
    out = f'/tmp/preview-{os.path.splitext(name)[0]}.html'
    open(out, 'w').write(html)
    print(out, len(html) // 1024, 'KB')
    return out


if __name__ == '__main__':
    for name in sys.argv[1:]:
        build(name)

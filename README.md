# Zimo Liu · Academic portfolio

A static academic website for GitHub Pages. Generated HTML is checked in, so GitHub Pages can serve the repository root directly from the publishing branch. The site needs no backend or deployment build.

## Edit and preview

1. Update the appropriate file in `content/`.
2. Run `python3 scripts/build.py` from the repository root.
3. Run `python3 -m http.server 8000` and open the local site at port 8000.
4. Commit both the content and the generated HTML. Configure GitHub Pages to publish the root of the desired branch.

The build uses the Python standard library. Shared templates live in `scripts/build.py`, and the stylesheet and mobile navigation script live in `assets/css/` and `assets/js/`.

| Area | Edit |
| --- | --- |
| Bio, education, awards, funding, teaching, contact | `content/profile.json` |
| Project text, thumbnails, and figure captions | `content/projects.json` |
| Articles, software, and research outputs | `content/publications.json` |
| WeChat, Douban, and original posts | `content/thoughts.json` |
| CV download | `assets/documents/zimo-liu-cv.pdf` |
| Figures | `assets/images/` |

Project `art` and optional figure `asset` values are lowercase WebP basenames without extensions. Keep figures near 960 × 560 pixels for the existing layout. Supply descriptive `alt` text and a caption identifying what the figure shows. The committed illustrations are schematics. Use `python3 scripts/draw_figures.py` with Pillow if you want to regenerate those four illustrations.

## Thoughts

`content/thoughts.json` is also the public, read-only JSON feed. Add an HTTPS `url` to link to an existing article from WeChat Official Accounts or Douban. To publish on this site, omit `url` and provide a `paragraphs` array. The build adds the local post page and updates the listing. Edit the shared template and stylesheet to customize the presentation. The following examples are for editing reference only.

```json
[
  {
    "slug": "external-example",
    "date": "2026-11-26",
    "source": "WeChat Official Account",
    "title": "Article title",
    "summary": "A short description.",
    "url": "https://mp.weixin.qq.com/example"
  },
  {
    "slug": "local-example",
    "date": "2026-11-26",
    "title": "Research note title",
    "summary": "A short introduction.",
    "paragraphs": ["First paragraph.", "Second paragraph."]
  }
]
```

If you remove or rename a project or local post, remove its previous generated page directory before committing.

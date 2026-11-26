"""Render the static portfolio from the JSON files in content/."""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / f"content/{name}.json").read_text(encoding="utf-8"))


profile = read("profile")
projects = read("projects")
publications = read("publications")
thoughts = read("thoughts")
pages = {
    "Home": "", "Research": "research/", "Publications": "publications/",
    "CV": "cv/", "Thoughts": "thoughts/", "Contact": "contact/",
}
cv_file = "assets/documents/zimo-liu-cv.pdf"


def h(value):
    return escape(value, quote=True)


def slug(value):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError(f"Invalid page slug: {value}")
    return value


def url(value):
    if urlsplit(value).scheme != "https" or not urlsplit(value).hostname:
        raise ValueError(f"Expected an HTTPS URL: {value}")
    return h(value)


def paragraphs(values):
    return "".join(f"<p>{h(value)}</p>" for value in values)


def items(values):
    return "<ul>" + "".join(f"<li>{h(value)}</li>" for value in values) + "</ul>"


def render(path, active, title, description, body):
    relative = "../" * path.count("/") or "./"
    name = h(profile["name"])
    navigation = "".join(
        f'<a href="{relative}{route}"{" aria-current=page" if label == active else ""}>{label}</a>'
        for label, route in pages.items()
    )
    page_title = name if active == title == "Home" else f"{h(title)} | {name}"
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{h(description)}">
  <title>{page_title}</title>
  <link rel="icon" href="{relative}assets/images/favicon.png">
  <link rel="stylesheet" href="{relative}assets/css/site.css">
  <script src="{relative}assets/js/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="shell header-inner">
      <a class="brand" href="{relative}" aria-label="{name} home">{name}</a>
      <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" hidden>Menu</button>
      <nav id="site-nav" aria-label="Main navigation">{navigation}</nav>
    </div>
  </header>
  <main id="main" class="shell" tabindex="-1">{body}</main>
  <footer class="site-footer">
    <div class="shell footer-inner"><span>© {name}</span><div><a href="mailto:{h(profile["email"])}">Email</a><a href="{url(profile["github"])}">GitHub</a></div></div>
  </footer>
</body>
</html>
"""
    output = ROOT / path / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n", encoding="utf-8")


def heading(label, title, description=""):
    lead = f'<p class="lead">{h(description)}</p>' if description else ""
    context = f'<p class="eyebrow">{h(label)}</p>' if label else ""
    return f'<div class="page-heading">{context}<h1>{h(title)}</h1>{lead}</div>'


def image(source, relative, alt="", lazy=False):
    path = f"assets/images/{slug(source)}.webp"
    return f'<img src="{relative}{path}" alt="{h(alt)}" width="960" height="560"{" loading=lazy" if lazy else ""}>'


def project_cards(relative, level="h3"):
    cards = []
    for project in projects:
        path = relative + "research/" + slug(project["slug"]) + "/"
        cards.append(f"""
        <article class="project-card">
          <a href="{path}">
            <div class="card-image">{image(project["art"], relative, lazy=True)}</div>
            <div class="card-copy">
              <p class="eyebrow">{h(project["field"])}</p>
              <{level}>{h(project["title"])}</{level}>
              <p>{h(project["summary"])}</p>
              <span class="card-link">View project</span>
            </div>
         </a>
        </article>""")
    return '<div class="project-grid">' + "".join(cards) + "</div>"


def about():
    education = profile["education"]
    interests = "".join(f"<li>{h(interest)}</li>" for interest in profile["interests"])
    return f"""
    <section class="home-section about-section" aria-labelledby="about-heading">
      <div>
        <h2 id="about-heading">Education</h2>
        <p class="about-degree">{h(education["degree"])} · {h(education["school"])}</p>
        <p>{h(education["details"][0])}</p>
        <p class="small muted">{h(education["dates"])}</p>
      </div>
      <div>
        <h2>Research interests</h2>
        <ul class="interests">{interests}</ul>
      </div>
    </section>"""


render("", "Home", "Home", f"{profile['name']} · {profile['role']} at USTC", f"""
    <section class="hero" aria-labelledby="home-heading">
      <div class="hero-copy">
        <p class="eyebrow hero-label">Materials chemistry &amp; chemical physics</p>
        <h1 id="home-heading">{h(profile["name"])}</h1>
        <p class="hero-role">{h(profile["role"])}</p>
        <p class="hero-institution">{h(profile["institution"])}</p>
        <p class="hero-intro">{h(profile["intro"])}</p>
        <div class="actions">
          <a class="button primary" href="research/">Explore research</a>
          <a class="button" href="cv/">View CV</a>
        </div>
      </div>
      <figure class="hero-figure">
        {image("lattice", "./", "Schematic of stacked atomic sheets with interlayer guests")}
        <figcaption><span>Intercalation in layered materials</span><span>Conceptual schematic</span></figcaption>
      </figure>
    </section>
    <section class="home-section" aria-labelledby="featured-heading">
      <div class="section-heading">
        <h2 id="featured-heading">Selected research</h2>
        <a class="text-link" href="research/">All research</a>
      </div>
      {project_cards("./")}
    </section>
    {about()}
""")

render("research/", "Research", "Research",
       "Research projects in materials chemistry, electrochemistry, microscopy, and photocatalysis.",
       heading("", "Research projects") + project_cards("../", "h2"))

for project in projects:
    project_path = slug(project["slug"])
    figures = "".join(
        f'<figure class="detail-figure">{image(figure.get("asset", project["art"]), "../../", figure["alt"])}'
        f'<figcaption>{h(figure["caption"])}</figcaption></figure>'
        for figure in project["figures"]
    )
    paper = project.get("publication")
    paper_link = (
        f'<p><a class="text-link" href="../../publications/#{slug(paper)}">View related publication</a></p>'
        if paper else ""
    )
    render(f"research/{project_path}/", "Research", project["title"], project["summary"], f"""
    <a class="back-link" href="../">All research</a>
    {heading(project["field"], project["title"], project["summary"])}
    <div class="detail-layout">
      <div class="prose">
        <section><h2>Scientific motivation</h2>{paragraphs([project["motivation"]])}</section>
        <section><h2>My contributions</h2>{paragraphs(project["contributions"])}</section>
        <section><h2>Methods</h2>{items(project["methods"])}</section>
        <section><h2>Selected results &amp; status</h2>{paragraphs(project["results"])}{paper_link}</section>
      </div>
      <aside aria-label="Project details and figures">
        <dl class="project-meta">
          <dt>Institution</dt><dd>{h(project["institution"])}</dd>
          <dt>Advisors</dt><dd>{h(project["advisors"])}</dd>
          <dt>Period</dt><dd>{h(project["dates"])}</dd>
        </dl>
        {figures}
      </aside>
    </div>
    """)

entries = []
for publication in publications:
    authors = f'<p>{h(publication["authors"])}</p>' if publication.get("authors") else ""
    external = f'<a class="text-link" href="{url(publication["url"])}">View output</a>' if publication.get("url") else ""
    entries.append(f"""
    <article class="list-entry" id="{slug(publication["id"])}">
      <p class="eyebrow">{h(publication["type"])}</p>
      <h2>{h(publication["title"])}</h2>
      {authors}<p class="muted">{h(publication["details"])}</p>
      <div class="inline-links"><a class="text-link" href="../research/{slug(publication["project"])}/">Related research</a>{external}</div>
    </article>""")
render("publications/", "Publications", "Publications", "Journal articles, software, and research outputs.",
       heading("", "Publications") + '<div class="entry-list">' + "".join(entries) + "</div>")

education = profile["education"]
awards = "".join(
    f'<li><span class="award-year">{h(year)}</span><span><strong>{h(title)}</strong>'
    + (f'<small>{h(detail)}</small>' if detail else "") + "</span></li>"
    for year, title, detail in profile["awards"]
)
render("cv/", "CV", "Curriculum Vitae", "Download Zimo Liu’s CV and browse education, funding, and honors.", f"""
    {heading("", "Curriculum vitae")}
    <div class="detail-layout">
      <div class="prose">
        <section><h2>Education</h2><p><strong>{h(profile["institution"])}</strong><br>{h(education["degree"])} · {h(education["school"])}<br>{h(education["dates"])}</p>{items(education["details"])}</section>
        <section><h2>Research funding</h2>{paragraphs(profile["funding"])}</section>
        <section><h2>Honors and awards</h2><ul class="award-list">{awards}</ul></section>
        <section><h2>Teaching assistantships</h2>{items(profile["teaching"])}</section>
      </div>
      <aside class="download-panel">
        <h2>Downloadable CV</h2>
        <a class="button primary" href="../{cv_file}" download>Download CV</a>
        <a class="text-link" href="../{cv_file}">Open PDF</a>
      </aside>
    </div>
""")

post_entries = []
for post in sorted(thoughts, key=lambda item: item["date"], reverse=True):
    post_slug = slug(post["slug"])
    source = post.get("source", "On this site")
    if post.get("url"):
        link = url(post["url"])
        label = "Read article"
    else:
        link = f"{post_slug}/"
        label = "Read post"
        render(f"thoughts/{post_slug}/", "Thoughts", post["title"], post["summary"], f"""
        <a class="back-link" href="../">All thoughts</a>
        {heading(post["date"], post["title"], post["summary"])}
        <article class="prose post-body">{paragraphs(post["paragraphs"])}</article>
        """)
    post_entries.append(f"""
    <article class="list-entry">
      <p class="eyebrow">{h(source)} · <time datetime="{h(post["date"])}">{h(post["date"])}</time></p>
      <h2>{h(post["title"])}</h2><p>{h(post["summary"])}</p>
      <a class="text-link" href="{link}">{label}</a>
    </article>""")
thoughts_body = "".join(post_entries) or '<p class="empty-state">No posts have been published yet.</p>'
render("thoughts/", "Thoughts", "Thoughts", "Research notes and selected writing by Zimo Liu.",
       heading("", "Thoughts", "Research notes and selected writing.")
       + '<div class="entry-list">' + thoughts_body + '<p class="feed-link"><a class="text-link" href="../content/thoughts.json">JSON feed</a></p></div>')

render("contact/", "Contact", "Contact", "Academic email and GitHub profile for Zimo Liu.", f"""
    {heading("", "Contact")}
    <div class="contact-grid">
      <article><h2>Academic email</h2><a class="text-link" href="mailto:{h(profile["email"])}">{h(profile["email"])}</a></article>
      <article><h2>GitHub</h2><a class="text-link" href="{url(profile["github"])}">{h(urlsplit(profile["github"]).path.strip("/"))}</a></article>
    </div>
    <p class="contact-affiliation">{h(profile["institution"])} · Hefei, China</p>
""")

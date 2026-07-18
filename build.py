"""Build index.html from template.html.

- Embeds logo-wide.png as a base64 data URI wherever the template says __LOGO_B64__.
- Wraps the template (a <title> line followed by body content) in the full HTML
  skeleton with SEO meta, Open Graph tags, and Organization schema.

Run:  python build.py
Then: git add -A && git commit && git push   (GitHub Pages redeploys zet8.com)
"""
import base64
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="ZET8 makes finished, ready-to-use apps for small businesses — Ponchi workforce management, Deskomigo mobile back office, Zet8 CRM, LocalSave local deals, and OnSMS text-based hiring.">
{title}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23000'/%3E%3Cpath d='M6 8h20L6 24h20' fill='none' stroke='%23F4C82D' stroke-width='4'/%3E%3C/svg%3E">
<!-- Open Graph / Twitter -->
<meta property="og:type" content="website">
<meta property="og:title" content="ZET8 — Tech Solutions for Businesses">
<meta property="og:description" content="Finished, ready-to-use apps for small businesses — workforce management, back office, CRM, local deals, and text-based hiring. Free trials, mobile-first, bilingual.">
<meta property="og:url" content="https://zet8.com">
<meta property="og:image" content="https://zet8.com/logo-wide.png">
<meta property="og:site_name" content="ZET8">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="ZET8 — Tech Solutions for Businesses">
<meta name="twitter:description" content="Finished, ready-to-use apps for small businesses. Free trials, mobile-first, bilingual.">
<meta name="twitter:image" content="https://zet8.com/logo-wide.png">
<link rel="canonical" href="https://zet8.com/">
<!-- Structured data -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ZET8",
  "url": "https://zet8.com",
  "logo": "https://zet8.com/logo.png",
  "description": "ZET8 makes finished, ready-to-use apps for small businesses — Ponchi workforce management, Deskomigo mobile back office, Zet8 CRM, LocalSave local deals, and OnSMS text-based hiring.",
  "email": "hello@zet8.com",
  "address": {{"@type": "PostalAddress","addressLocality": "Houston","addressRegion": "TX","addressCountry": "US"}},
  "parentOrganization": {{"@type": "Organization","name": "Optima Buildsolutions LLC"}},
  "sameAs": ["https://ponchi.app","https://deskomigo.com","https://crm.zet8.com","https://localsave.com","https://onsms.com"]
}}
</script>
</head>
<body>
"""


def main():
    tpl = io.open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    with open(os.path.join(HERE, "logo-wide.png"), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    assert tpl.count("__LOGO_B64__") == 2, "template must reference the logo twice (nav + hero)"
    content = tpl.replace("__LOGO_B64__", b64)
    title_line, rest = content.split("\n", 1)
    out = HEAD.format(title=title_line) + rest + "\n</body>\n</html>\n"
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
    print("built index.html (%d bytes)" % len(out))


if __name__ == "__main__":
    main()

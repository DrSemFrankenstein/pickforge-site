# PickForge: static site (EN / RU / HE)

## Structure

| Path | What it is |
|---|---|
| `index.html`, `ru/index.html`, `he/index.html` | One static page per language (Hebrew is RTL). Every text is in the HTML, so crawlers and AI bots don't need JavaScript. |
| `index.md`, `ru/index.md`, `he/index.md` | Plain Markdown version of each page, linked from the page `<head>`. |
| `llms.txt` | Short site summary for AI assistants ([llmstxt.org](https://llmstxt.org) format). |
| `llms-full.txt` | Full text of all three languages in one file. |
| `robots.txt` | Allows all crawlers, including the main AI crawlers by name, and points to the sitemap and llms.txt. |
| `sitemap.xml` | All three pages with hreflang alternates. |
| `site.webmanifest`, `assets/*.png`, `assets/favicon.svg` | Icons and manifest. |
| `assets/og.jpg` | 1200×630 social preview image (regenerate with `generate_assets.py` if missing). |
| `assets/sprite.webp` | 48-frame sprite sheet (7×7 grid, 405×720 frames). **Commit the real file** — `generate_assets.py` only creates a placeholder if it is missing. |
| `assets/site.css`, `assets/site.js` | Shared styles and the scroll animation. |
| `404.html`, `.nojekyll` | GitHub Pages helpers. |
| `_headers`, `_redirects` | Security headers (Cloudflare Pages / Netlify) and HTTPS/404 rules. |
| `build.py` | Generator (keep in repo; optional to omit from public deploy). |
| `SECURITY.md` | Production checklist and threat notes. |

Each page also carries JSON-LD (Organization, WebSite, WebPage, FAQPage), a canonical URL, hreflang links and Open Graph tags. GEO files (`llms.txt`, etc.) stay at the site root for crawlers — **not** shown in the page UI.

## Before you publish: set the real URL

All absolute URLs currently use the placeholder `https://pickforge.example/`. Once you know your address, run:

```bash
python3 build.py https://YOUR-USER.github.io/YOUR-REPO/
```

This regenerates the HTML, Markdown, llms files, sitemap, robots.txt and JSON-LD with the real URL. (Requires Python 3; `pip install pillow` only for `generate_assets.py`.)

## GitHub Pages

1. Create a **public** GitHub repository (e.g. `pickforge-site`).
2. Push this folder to `main`.
3. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. The workflow `.github/workflows/github-pages.yml` runs on push: it generates assets, runs `build.py` with `https://<user>.github.io/<repo>/`, and deploys.

Site URL:
- **Root home page:** rename the repo to `<username>.github.io` (e.g. `DrSemFrankenstein.github.io`) → `https://<username>.github.io/`
- **Project site:** any other repo name → `https://<username>.github.io/<repo-name>/`

Enable **Enforce HTTPS** under Pages after the first deploy.

## Editing text

Change the `CONTENT` dictionary in `build.py` (one block per language), then rerun the command above.

## Local preview (language links)

Browsers opening `file://` do **not** auto-load `index.html` inside folders. Language links use explicit `index.html` paths. Prefer a local server:

```bash
npx --yes serve .
```

Then open `http://localhost:3000/` and use EN / RU / HE.

## Affiliate programs (any platform)

After deploy, use the live **HTTPS** home URL when a network or retailer asks for your site list. Disclosure is **platform-neutral**; add program-specific wording in `build.py` only if a partner requires it. See `SECURITY.md` before going live.

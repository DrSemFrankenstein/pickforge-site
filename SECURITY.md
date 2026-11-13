# PickForge static site — security notes (production)

This site is **static HTML/CSS/JS** only: no server code, no database, no forms, no auth, no cookies set by PickForge, no API keys in the published folder.

## What we hardened

| Control | Where |
|--------|--------|
| Content-Security-Policy, HSTS, `X-Frame-Options`, `nosniff`, Referrer-Policy, Permissions-Policy | `_headers` (Cloudflare Pages, Netlify) |
| HTTPS redirect | `_redirects` (Netlify); enable **Enforce HTTPS** on GitHub Pages |
| `referrer` meta | Generated HTML + `404.html` (fallback when the host ignores `_headers`) |
| No third-party scripts | Only `assets/site.js` (scroll animation) |
| No user-generated content | All copy from `build.py` at build time |
| `form-action 'none'` in CSP | No forms on site |

CSP allows `'unsafe-inline'` **only** for JSON-LD (`application/ld+json`) in `<head>`. There is no other inline script.

External resources: **Google Fonts** (`fonts.googleapis.com` / `fonts.gstatic.com`). To remove that dependency, self-host font files and tighten CSP to `'self'` only.

## Deploy hygiene

1. Run `python build.py https://YOUR-REAL-ORIGIN/` so canonical URLs, sitemap, and robots are correct.
2. Publish **only** the static artifacts (`index.html`, `ru/`, `he/`, `assets/`, `llms.txt`, `robots.txt`, `sitemap.xml`, `_headers`, `_redirects`, etc.).
3. **Do not** upload `build.py` or `README.md` to the public bucket unless you intend to expose the generator (not required for the live site).
4. No `.env`, secrets, or private keys in this directory.

## GitHub Pages

GitHub Pages does **not** read `_headers`. After enabling HTTPS in repo settings, either:

- Put **Cloudflare** (or similar) in front and apply the same headers there, or  
- Rely on meta referrer + static-only surface (lower hardening than full CSP headers).

## Residual risks (accepted for this project)

- **Clickjacking / XSS via CSP**: mitigated by CSP on hosts that serve `_headers`; affiliate links leave the site to Amazon/retailers (their security models apply).
- **Supply chain**: Google Fonts CDN; mitigate by self-hosting if you need stricter policy.
- **Directory listing**: disabled on proper static hosts; avoid browsing via raw `file://` folders (use `index.html` or `npx serve`).

## Link builder

The store-link tool (`assets/link-generator.js`) runs in the browser. It does not call PickForge, Amazon, or AliExpress. The Associates ID `pickforge-20` is public by design: it is part of every Amazon link. The form does not navigate (`form-action 'none'` in CSP); script handles it. No new host, cookie, or API key.

## If you add features later

Re-review before prod: contact forms, analytics, comments, affiliate redirect endpoints, or any server-side logic introduce new attack surface and need separate hardening. An AliExpress promotion link needs the Portals API on a server. Do not put the Portals secret in this static site.

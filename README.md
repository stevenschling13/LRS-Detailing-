# LRS Service Static Site

## About
This repository contains the production static landing page for **LRS Service**, a mobile car detailing business serving Hennepin County, Minnesota. It is intentionally lightweight and easy to maintain, with all customer-facing content in a single HTML file for fast edits and straightforward deployment.

## Stack
- Single static `index.html` file (plus `404.html`)
- Custom CSS, embedded in the HTML (no framework, no preprocessor)
- Zero build step (no npm, no bundler)
- Google Fonts delivered via CDN
- SVG favicon + minimal web manifest for PWA-style metadata
- JSON-LD `AutoDetailing` schema for local SEO
- Vercel deployment with HTTPS, HSTS, and asset cache headers configured in `vercel.json`

## Repository layout
```
index.html               # Landing page
404.html                 # Branded error page (matches index.html style)
favicon.svg              # SVG favicon (also used as apple-touch-icon)
manifest.webmanifest     # PWA manifest
robots.txt               # Crawler directives + sitemap pointer
sitemap.xml              # Single-page sitemap
vercel.json              # Routing, security, and cache headers
photos/                  # Before/after gallery images (see photos/README.md)
tests/                   # Python stdlib tests for sitemap/robots/404
.github/workflows/       # CI: HTML validate, link check, asset tests, pa11y
```

## Local preview
1. Open a terminal in the repository root.
2. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser.

## Deploy to Vercel
1. Push this repository to GitHub (already done for this project).
2. Go to [https://vercel.com/new](https://vercel.com/new).
3. Click **Import Git Repository** and choose this repo.
4. Accept the default project settings.
5. Click **Deploy**.

After the first deploy, Vercel automatically creates a new deployment on every push to `main`. Pull requests get preview deployments automatically.

## Custom domain
1. In Vercel, open the project and go to **Settings → Domains**.
2. Add your custom domain and follow Vercel's DNS instructions.
3. Update DNS records at your registrar (typically A/ALIAS/CNAME records exactly as shown by Vercel).
4. Wait for DNS propagation and re-check domain status in Vercel.

After your domain is live, update every `lrsservice.com` reference:
- `/sitemap.xml` — `<loc>` entry
- `/robots.txt` — `Sitemap:` line
- `/index.html` — `<link rel="canonical">`, `og:url`, and `"url"` inside the JSON-LD `<script>` block

A repo-wide search for `lrsservice.com` lists every site to update.

## Common edits

| What to update | Where to edit |
| --- | --- |
| Phone number | In `index.html`, update all occurrences of `9522559160` (also in `404.html`) |
| Prices | In `index.html`, search for `From $60`, `From $120`, and `From $200` |
| Service area cities | In `index.html`, edit the `.area-cities` section |
| Tagline | In `index.html`, search for `Cleaner Car` |
| JSON-LD address/region | In `index.html`, edit the `"address"` block inside the `<script type="application/ld+json">` |

## Adding photos
See `/photos/README.md` for naming, sizing, and placeholder replacement instructions.

## Where the contact form goes
The contact CTA currently opens a prefilled SMS using an `sms:` link. This is intentional and does not use a backend form handler.

## CI
On every push and PR, GitHub Actions runs:
- HTML validation (`html5validator`)
- Link checking on Markdown and HTML (`lychee`)
- Python stdlib tests on `sitemap.xml`, `robots.txt`, and `404.html`
- Accessibility (pa11y, WCAG2AA) on `404.html`

CI must be green before merging to `main`. Run the asset tests locally with:
```bash
python3 -m unittest discover -s tests -v
```

## Security & headers
`vercel.json` ships with:
- `Strict-Transport-Security` (2-year HSTS, preload-ready)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` denying geolocation/camera/mic/FLoC
- Per-asset `Cache-Control` for favicon, manifest, sitemap, robots, and photos

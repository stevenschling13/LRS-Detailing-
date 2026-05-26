# LRS Service Static Site

## About
This repository contains the production static landing page for **LRS Service**, a mobile car detailing business serving Hennepin County, Minnesota. It is intentionally lightweight and easy to maintain, with all customer-facing content in a single HTML file for fast edits and straightforward deployment.

## Stack
- Single static `index.html` file
- Custom CSS (no framework)
- Zero build step (no npm, no bundler)
- Google Fonts delivered via CDN

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

After the first deploy, Vercel automatically creates a new deployment on every push to `main`.

## Custom domain
1. In Vercel, open the project and go to **Settings → Domains**.
2. Add your custom domain and follow Vercel's DNS instructions.
3. Update DNS records at your registrar (typically A/ALIAS/CNAME records exactly as shown by Vercel).
4. Wait for DNS propagation and re-check domain status in Vercel.

After your domain is live, update:
- `/sitemap.xml` (`<loc>` entries)
- JSON-LD schema URL in `/index.html`
- `/robots.txt` sitemap line (currently uses placeholder `https://lrsservice.com/sitemap.xml`)

## Common edits

| What to update | Where to edit |
| --- | --- |
| Phone number | In `index.html`, update all 5 occurrences of `9522559160` |
| Prices | In `index.html`, search for `From $60`, `From $120`, and `From $200` |
| Service area cities | In `index.html`, edit the `.area-cities` section |
| Tagline | In `index.html`, search for `Cleaner Car` |

## Adding photos
See `/photos/README.md` for naming, sizing, and placeholder replacement instructions.

## Where the contact form goes
The contact CTA currently opens a prefilled SMS using an `sms:` link. This is intentional and does not use a backend form handler.

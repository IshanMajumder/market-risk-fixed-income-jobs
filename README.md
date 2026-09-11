# Global Market Risk / Fixed Income Analyst Job Site

Searches company career APIs for **Market Risk Analyst** and **Fixed Income
Analyst** roles **anywhere in the world**, keeping postings that either state
a salary of **$60,000 USD-equivalent or more**, or list no salary at all
(postings that explicitly state a salary below $60k are dropped). No
internships.

Two ways to use this:

1. **`main.py`** — an on-demand script you run yourself whenever you want a
   fresh Excel file of matching jobs.
2. **`site/build_site.py`** — powers an always-on website that refreshes
   itself every 4 hours automatically via GitHub Actions + GitHub Pages,
   with no Claude session (and no manual runs) involved once it's set up.

## ⚠️ Run/host this somewhere with normal internet access

This project calls public job-board APIs directly (`boards-api.greenhouse.io`,
`api.lever.co`, `*.myworkdayjobs.com`). Locked-down environments — including
the Claude cloud workspace and Claude's own linked-device sandbox — block
these hosts entirely via a network allowlist (the same issue you hit building
the original USA quant-job-alert pipeline). GitHub Actions' own runners have
normal internet access, so the automated site below is unaffected; `main.py`
just needs to be run from a normal terminal (not inside a Claude session).

---

## Option A: on-demand Excel export (`main.py`)

```bash
pip install -r requirements.txt
python main.py
```

Add `--clear-cache` to re-see jobs you've already been shown. Writes
`jobs_output_<timestamp>.xlsx` (Company, Title, Location, Salary,
Salary_Min_USD_Equiv, Source, Link, Posted) and maintains `seen_jobs.txt` so
each run only shows *new* postings.

## Option B: the auto-refreshing website (recommended for "check it anytime")

### One-time setup (~10 minutes)

1. **Create a new GitHub repo** (public or private — public is required for
   free GitHub Pages on a private-account repo, unless you have GitHub Pro/
   Team/Enterprise which allows Pages on private repos too).
2. **Push everything in this folder** to that repo's default branch:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: market risk / fixed income job site"
   git branch -M main
   git remote add origin https://github.com/<you>/<repo-name>.git
   git push -u origin main
   ```
3. **Enable GitHub Pages**: repo → Settings → Pages → under "Build and
   deployment", set Source to **GitHub Actions** (not "Deploy from a
   branch" — the workflow here uses the official Pages Actions).
4. **Run the workflow once manually** to seed it: repo → Actions →
   "Refresh job site" → Run workflow. After it finishes, your site is live at
   `https://<you>.github.io/<repo-name>/`.
5. From then on, `.github/workflows/refresh-site.yml` reruns automatically
   every 4 hours (cron `0 */4 * * *`, UTC) — scrape, refilter, commit
   `docs/data.json`, redeploy Pages. No further action needed.

### How it works

- `site/build_site.py` does a **full fresh scrape** every run (not just "new
  since last time" — a website should show everything currently open, so
  there's no dedup/hide-old-postings logic here, unlike `main.py`).
- It writes `docs/data.json` (the job list + a `generated_at` timestamp) and,
  on the very first run only, `docs/index.html` (a small static page that
  fetches `data.json` client-side and renders a searchable/sortable/
  filterable table — no server, no build step, no external dependencies).
- The GitHub Actions workflow has two jobs: `build` (scrape + commit the new
  `data.json`) and `deploy` (publish `docs/` to Pages).
- If you want to redesign the page later, edit `docs/index.html` directly
  (it won't be overwritten — `build_site.py` only writes it if it's missing)
  or delete it and let the next run regenerate it from
  `site/index.html.template`.

### Checking it's working

- Actions tab shows each run's log — the same "N sources did not resolve"
  troubleshooting output described below appears there.
- If a run's `data.json` shows 0 jobs and the Actions log lists *every*
  single source as failed with the same connection error, that's a real
  network problem on GitHub's side (rare) — rerun it.

---

## How it decides what's a match

**Role**: title must contain "analyst" plus either "market risk" or "fixed
income" (e.g. "Market Risk Analyst", "Fixed Income Trading Analyst", "Senior
Market Risk Management Analyst"). Internships/co-ops/apprenticeships are
excluded. `test_logic.py` has the exact test cases if you want to tweak the
matching rules — this same logic lives in `sources.py` and is shared by both
`main.py` and `site/build_site.py`.

**Salary**: `salary.py` regex-scans the posting text for pay disclosures like
"$70,000 - $90,000" or "£50,000 - £60,000", converts non-USD currencies using
a fixed approximate FX table (`FX_TO_USD` in `salary.py` — update it
periodically, it's not live), and applies the $60k policy above. Most
postings outside the US won't disclose salary at all — per your instructions
those are kept in, not dropped.

## `companies.py` — the source list, and its limits

Because live network calls are blocked in every sandbox available to build
this, **none of the Greenhouse/Lever/Workday company slugs in `companies.py`
have been verified against the real APIs.** They're best-effort guesses at
which large banks, asset managers, insurers and hedge funds use these three
ATS platforms, in the same style as the source list in your existing
`quant-job-alert` project.

Both `main.py` and `site/build_site.py` degrade safely around bad slugs: any
company that 404s, times out, or returns nothing is silently skipped and
listed under "unresolved sources" in the run's log — a wrong guess never
breaks a run, it just means that company contributes zero jobs.

**Spend 15–20 minutes fixing this list once the site is live and you can see
real results:**

1. Check a run's Actions log (or `main.py`'s console output) for the
   "unresolved sources" list.
2. For each company you care about, open their real careers page, click into
   any job posting, and look at the URL:
   - `boards.greenhouse.io/<slug>/jobs/...` → that's the Greenhouse slug
   - `jobs.lever.co/<slug>/...` → that's the Lever slug
   - `<tenant>.wd#.myworkdayjobs.com/<site>/job/...` → tenant, wd#, and site
     for the `WORKDAY_COMPANIES` entry
3. Fix or remove the wrong ones, add real ones you find, commit + push — the
   next scheduled run (or a manual "Run workflow") picks up the change.
4. Your existing `quant-job-alert` repo already has a validated slug list for
   many of these same companies (JPMorgan, Goldman Sachs, Citi, BlackRock,
   Point72, AQR, Citadel, etc.) — worth cross-checking against that first,
   then adding the additional non-US banks/insurers this project needs for
   global coverage.
5. LinkedIn is intentionally *not* used here (per your existing project's
   notes: it blocks bots and risks account bans) — company-direct APAC/EMEA
   career sites on Greenhouse/Lever/Workday are fair game the same way the
   US ones are.

## Files

- `main.py` — on-demand Excel export tool (with dedup)
- `site/build_site.py` — always-fresh JSON + first-run HTML for the website
- `site/index.html.template` — the static page template `build_site.py`
  seeds `docs/index.html` from
- `sources.py` — shared fetch (Greenhouse/Lever/Workday) + role-matching logic
- `companies.py` — the (unverified) source list described above
- `salary.py` — salary regex extraction + $60k filter logic
- `test_logic.py` — offline unit tests for title/salary matching (no network needed)
- `.github/workflows/refresh-site.yml` — the 4-hourly scrape + Pages deploy
- `docs/` — GitHub Pages root (`data.json` + `index.html`, both regenerated/
  updated by the workflow)
- `requirements.txt` — `requests`, `pandas`, `openpyxl`
# market-risk-fixed-income-jobs
Global Market Risk / Fixed Income Analyst job site, auto-refreshed every 4 hours via GitHub Actions.

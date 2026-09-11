"""
Builds the auto-refreshing job site: scrapes all sources fresh (no dedup --
this always reflects the full set of currently-open matching postings, not
just "new since last run"), applies the role + salary filters, and writes:

    docs/data.json   -- the job list + last-refreshed timestamp
    docs/index.html  -- static page (written once; unchanged normally) that
                         reads data.json at load time

Run by .github/workflows/refresh-site.yml every 4 hours. GitHub Pages should
be configured to serve from the `docs/` folder on the default branch.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))  # so `sources`/`salary`/`companies` import cleanly

from sources import fetch_all, title_matches_role
from salary import extract_salary, passes_salary_filter

MIN_SALARY_USD = 60000
DOCS_DIR = Path(__file__).parent.parent / "docs"


def build():
    unresolved = []
    print("Fetching all sources (Greenhouse, Lever, Workday)...")
    all_jobs = fetch_all(unresolved)
    print(f"Fetched {len(all_jobs)} raw postings.")

    role_matched = [j for j in all_jobs if title_matches_role(j["title"])]
    print(f"{len(role_matched)} match Market Risk / Fixed Income Analyst titles.")

    final = []
    seen_keys = set()
    for j in role_matched:
        key = j["url"] or f"{j['company']}|{j['title']}|{j['location']}"
        if key in seen_keys:
            continue
        seen_keys.add(key)
        salary_info = extract_salary(j["content"])
        if not passes_salary_filter(salary_info, MIN_SALARY_USD):
            continue
        final.append({
            "company": j["company"],
            "title": j["title"],
            "location": j["location"] or "Not specified",
            "salary": salary_info["raw"] if salary_info else None,
            "salary_min_usd": salary_info["min_usd"] if salary_info else None,
            "source": j["source"],
            "url": j["url"],
            "posted": j["posted"],
        })

    final.sort(key=lambda x: (x["company"], x["title"]))

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "min_salary_usd": MIN_SALARY_USD,
        "count": len(final),
        "unresolved_count": len(unresolved),
        "jobs": final,
    }
    (DOCS_DIR / "data.json").write_text(json.dumps(data, indent=2))
    print(f"\nWrote {len(final)} jobs to docs/data.json")

    if unresolved:
        print(f"{len(unresolved)} sources did not resolve. First 10:")
        for src, slug, err in unresolved[:10]:
            print(f"  [{src}] {slug}: {err}")

    if not (DOCS_DIR / "index.html").exists():
        (DOCS_DIR / "index.html").write_text(Path(__file__).with_name("index.html.template").read_text())
        print("Wrote docs/index.html (first run)")


if __name__ == "__main__":
    build()

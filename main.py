"""
Global Market Risk / Fixed Income Analyst job finder -- on-demand personal tool.

Run:
    pip install -r requirements.txt
    python main.py

Produces:
    jobs_output_<timestamp>.xlsx   -- full results table
    seen_jobs.txt                  -- dedup cache (auto-created/updated; delete
                                       it to reset and re-see everything)

For the always-on version of this (a website that refreshes every 4 hours
automatically via GitHub Actions), see site/build_site.py and README.md.

Scope, per Ishan's requirements (2026-09-11):
  - Roles: Market Risk Analyst, Fixed Income Analyst (and close variants)
  - Geography: anywhere in the world (no country filter)
  - Salary: keep jobs with an explicit salary >= $60,000 USD-equivalent, OR
            jobs that list no salary at all. Drop only jobs that explicitly
            state a salary below $60k.
  - No internships.

NOTE ON NETWORK ACCESS: this script must be run somewhere with normal
internet access to boards-api.greenhouse.io / api.lever.co /
*.myworkdayjobs.com. Some sandboxed/locked-down environments (including the
Claude cloud workspace and Claude's own linked-device shell) block these
hosts outright via an egress allowlist -- if you see 403s or connection
errors from *every* source, that's the environment, not your setup. Run it
from a normal terminal (e.g. your Anaconda/PyCharm environment).
"""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from sources import fetch_all, title_matches_role
from salary import extract_salary, passes_salary_filter

MIN_SALARY_USD = 60000
SEEN_FILE = Path(__file__).parent / "seen_jobs.txt"


def load_seen():
    if SEEN_FILE.exists():
        return set(SEEN_FILE.read_text().splitlines())
    return set()


def save_seen(seen):
    SEEN_FILE.write_text("\n".join(sorted(seen)))


def main(clear_cache=False):
    unresolved = []

    print("Fetching all sources (Greenhouse, Lever, Workday)...")
    all_jobs = fetch_all(unresolved)
    print(f"\nFetched {len(all_jobs)} raw postings across all sources.")

    role_matched = [j for j in all_jobs if title_matches_role(j["title"])]
    print(f"{len(role_matched)} match Market Risk / Fixed Income Analyst titles.")

    seen = set() if clear_cache else load_seen()
    final = []
    for j in role_matched:
        key = j["url"] or f"{j['company']}|{j['title']}|{j['location']}"
        if key in seen:
            continue
        salary_info = extract_salary(j["content"])
        if not passes_salary_filter(salary_info, MIN_SALARY_USD):
            continue
        final.append({
            "Company": j["company"],
            "Title": j["title"],
            "Location": j["location"] or "Not specified",
            "Salary": salary_info["raw"] if salary_info else "Not listed",
            "Salary_Min_USD_Equiv": salary_info["min_usd"] if salary_info else None,
            "Source": j["source"],
            "Link": j["url"],
            "Posted": j["posted"],
        })
        seen.add(key)

    save_seen(seen)

    df = pd.DataFrame(final)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(__file__).parent / f"jobs_output_{ts}.xlsx"
    if not df.empty:
        df.to_excel(out_path, index=False)
        print(f"\n{len(df)} new jobs after salary/dedup filters -> {out_path}")
    else:
        print("\nNo new jobs after salary/dedup filters this run.")

    if unresolved:
        print(f"\n{len(unresolved)} sources did not resolve (bad slug, blocked network, or no live jobs).")
        print("First 15 for troubleshooting:")
        for src, slug, err in unresolved[:15]:
            print(f"  [{src}] {slug}: {err}")
        print("If EVERY source failed with the same connection error, you're likely running "
              "in a network-restricted sandbox -- try again from a normal terminal.")

    return df


if __name__ == "__main__":
    clear = "--clear-cache" in sys.argv
    main(clear_cache=clear)

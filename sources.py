"""
Shared fetch + role-matching logic used by both main.py (on-demand personal
xlsx tool) and site/build_site.py (the auto-refreshing GitHub Pages site).
"""
import re

import requests

REQUEST_TIMEOUT = 15
HEADERS = {"User-Agent": "Mozilla/5.0 (job-search-script; contact: ishanmajumder88@gmail.com)"}

ROLE_KEYWORDS = ["market risk", "fixed income"]
EXCLUDE_KEYWORDS = ["intern", "internship", "co-op", "coop", "apprentice", "working student"]


def title_matches_role(title):
    t = title.lower()
    if any(x in t for x in EXCLUDE_KEYWORDS):
        return False
    if "analyst" not in t:
        return False
    return any(k in t for k in ROLE_KEYWORDS)


def strip_html(html):
    if not html:
        return ""
    return re.sub(r"<[^>]+>", " ", html)


def fetch_greenhouse(slug, unresolved):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            unresolved.append(("greenhouse", slug, f"HTTP {r.status_code}"))
            return []
        jobs = r.json().get("jobs", [])
        out = []
        for j in jobs:
            out.append({
                "source": "Greenhouse",
                "company": j.get("company_name") or slug,
                "title": j.get("title", ""),
                "location": (j.get("location") or {}).get("name", ""),
                "url": j.get("absolute_url", ""),
                "content": strip_html(j.get("content", "")),
                "posted": j.get("updated_at", ""),
            })
        return out
    except requests.RequestException as e:
        unresolved.append(("greenhouse", slug, str(e)))
        return []


def fetch_lever(slug, unresolved):
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            unresolved.append(("lever", slug, f"HTTP {r.status_code}"))
            return []
        jobs = r.json()
        out = []
        for j in jobs:
            categories = j.get("categories", {}) or {}
            out.append({
                "source": "Lever",
                "company": slug,
                "title": j.get("text", ""),
                "location": categories.get("location", ""),
                "url": j.get("hostedUrl", ""),
                "content": strip_html(j.get("descriptionPlain") or j.get("description", "")),
                "posted": j.get("createdAt", ""),
            })
        return out
    except requests.RequestException as e:
        unresolved.append(("lever", slug, str(e)))
        return []


def fetch_workday(entry, unresolved):
    tenant, site, wd = entry["tenant"], entry["site"], entry["wd"]
    url = f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    payload = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "analyst"}
    try:
        r = requests.post(url, headers={**HEADERS, "Content-Type": "application/json"},
                           json=payload, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            unresolved.append(("workday", entry["company"], f"HTTP {r.status_code}"))
            return []
        data = r.json()
        postings = data.get("jobPostings", [])
        out = []
        for j in postings:
            out.append({
                "source": "Workday",
                "company": entry["company"],
                "title": j.get("title", ""),
                "location": j.get("locationsText", ""),
                "url": f"https://{tenant}.{wd}.myworkdayjobs.com{j.get('externalPath', '')}",
                "content": "",
                "posted": j.get("postedOn", ""),
            })
        return out
    except requests.RequestException as e:
        unresolved.append(("workday", entry["company"], str(e)))
        return []


def fetch_all(unresolved):
    from companies import GREENHOUSE_COMPANIES, LEVER_COMPANIES, WORKDAY_COMPANIES
    all_jobs = []
    for slug in GREENHOUSE_COMPANIES:
        all_jobs.extend(fetch_greenhouse(slug, unresolved))
    for slug in LEVER_COMPANIES:
        all_jobs.extend(fetch_lever(slug, unresolved))
    for entry in WORKDAY_COMPANIES:
        all_jobs.extend(fetch_workday(entry, unresolved))
    return all_jobs

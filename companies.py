"""
Company source list for the global Market Risk / Fixed Income Analyst job finder.

Each ATS type is queried via its public job-board API (no login needed):
  - Greenhouse: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
  - Lever:      https://api.lever.co/v0/postings/{slug}?mode=json
  - Workday:    POST https://{tenant}.wd{n}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs

STATUS (updated after live verification via a real browser session):
  - GREENHOUSE_COMPANIES and LEVER_COMPANIES below were verified live on
    2026-09-13 by hitting the real APIs -- every slug in these two lists
    returned a real board (200) at verification time. Company career sites
    can still change ATS/slugs later, so treat this as "verified once," not
    "guaranteed forever."
  - WORKDAY_COMPANIES could NOT be verified in the same session: every
    myworkdayjobs.com job-board tenant tested returned Workday's own
    "Workday is currently unavailable / experiencing a service interruption"
    page, while workday.com's marketing site loaded fine -- i.e. a real
    outage of Workday's job-board hosting at verification time, not a bad
    slug. These entries are still best-effort guesses and need re-checking
    once Workday's job-board service is back up (open the company's real
    careers page, click a job, and read tenant/site/wd# off the URL:
    <tenant>.wd#.myworkdayjobs.com/<site>/job/...).

Both main.py and site/build_site.py degrade safely around bad slugs: any
company that 404s, times out, or returns nothing is silently skipped and
listed under "unresolved sources" in the run's log -- a wrong guess never
breaks a run, it just means that company contributes zero jobs.
"""

# Greenhouse: boards-api.greenhouse.io/v1/boards/{slug}/jobs
# Verified live (200 OK) on 2026-09-13.
GREENHOUSE_COMPANIES = [
    "aqr",                    # AQR Capital Management
    "point72",                # Point72 Asset Management
    "marshallwace",           # Marshall Wace
    "apollo",                 # Apollo Global Management
    "akunacapital",           # Akuna Capital
    "imc",                    # IMC Trading
    "jumptrading",            # Jump Trading
    "flowtraders",            # Flow Traders
    "vikingglobalinvestors",  # Viking Global Investors
    "exoduspoint",            # ExodusPoint Capital Management
    "schonfeld",              # Schonfeld Strategic Advisors
    "virtu",                  # Virtu Financial
    "janestreet",             # Jane Street
    "towerresearchcapital",   # Tower Research Capital
    "gsacapital",             # GSA Capital
    "transmarketgroup",       # TransMarket Group
    "walleyecapital",         # Walleye Capital
    "pdtpartners",            # PDT Partners
    "dvtrading",              # DV Trading
]

# Lever: api.lever.co/v0/postings/{slug}?mode=json
# Verified live (200 OK) on 2026-09-13.
LEVER_COMPANIES = [
    "fortress",  # Fortress Investment Group
    "gmo",       # GMO (Grantham, Mayo, & van Otterloo)
]

# Workday: {tenant}.wd{n}.myworkdayjobs.com -- (tenant, site, wd_number)
# NOT independently verified this round -- myworkdayjobs.com itself was down
# for every tenant tested during the 2026-09-13 verification pass (Workday's
# own outage page, not a 404), so these remain best-effort guesses at large
# banks/insurers known to use Workday. wd_number varies by company (wd1, wd3,
# wd5, etc.) and sometimes changes; if a tenant stops resolving once Workday's
# service is back, check the company's live careers page URL for the current
# wd# and site name.
WORKDAY_COMPANIES = [
    {"company": "Goldman Sachs", "tenant": "gs", "site": "GS", "wd": "wd1"},
    {"company": "JPMorgan Chase", "tenant": "jpmc", "site": "CI_External", "wd": "wd5"},
    {"company": "Citi", "tenant": "citi", "site": "CitiCareers", "wd": "wd1"},
    {"company": "BlackRock", "tenant": "blackrock", "site": "Blackrock_Careers", "wd": "wd1"},
    {"company": "PIMCO", "tenant": "pimco", "site": "PIMCO", "wd": "wd1"},
    {"company": "Wells Fargo", "tenant": "wf", "site": "External", "wd": "wd1"},
    {"company": "State Street", "tenant": "statestreet", "site": "Global_Careers", "wd": "wd1"},
    {"company": "BNY Mellon", "tenant": "bnymellon", "site": "BNYMellon", "wd": "wd1"},
    {"company": "Northern Trust", "tenant": "northerntrust", "site": "Northern_Trust_Careers", "wd": "wd1"},
    {"company": "HSBC", "tenant": "hsbc", "site": "External_Career_Site", "wd": "wd3"},
    {"company": "Standard Chartered", "tenant": "standardchartered", "site": "Standard_Chartered_Careers", "wd": "wd3"},
    {"company": "UBS", "tenant": "ubs", "site": "UBSCareers", "wd": "wd3"},
    {"company": "Nomura", "tenant": "nomura", "site": "NomuraCareers", "wd": "wd3"},
    {"company": "AIG", "tenant": "aig", "site": "AIG_Careers", "wd": "wd1"},
    {"company": "Prudential Financial", "tenant": "prudential", "site": "PrudentialCareers", "wd": "wd1"},
    {"company": "MetLife", "tenant": "metlife", "site": "MetLifeCareers", "wd": "wd1"},
    {"company": "Zurich Insurance", "tenant": "zurich", "site": "ZurichCareers", "wd": "wd3"},
    {"company": "Swiss Re", "tenant": "swissre", "site": "SwissReCareers", "wd": "wd3"},
    {"company": "Allianz", "tenant": "allianz", "site": "AllianzCareers", "wd": "wd3"},
    {"company": "AXA", "tenant": "axa", "site": "AXACareers", "wd": "wd3"},
    {"company": "RBC", "tenant": "rbc", "site": "RBCCareers", "wd": "wd3"},
    {"company": "TD Bank", "tenant": "td", "site": "TDBank_Careers", "wd": "wd3"},
    {"company": "Scotiabank", "tenant": "scotiabank", "site": "ScotiabankCareers", "wd": "wd3"},
    {"company": "DBS Bank", "tenant": "dbs", "site": "DBS_Careers", "wd": "wd3"},
]

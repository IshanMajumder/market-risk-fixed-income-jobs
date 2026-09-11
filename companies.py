"""
Company source list for the global Market Risk / Fixed Income Analyst job finder.

Each ATS type is queried via its public job-board API (no login needed):
  - Greenhouse: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
  - Lever:      https://api.lever.co/v0/postings/{slug}?mode=json
  - Workday:    POST https://{tenant}.wd{n}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs

IMPORTANT: these slugs are best-effort guesses at large banks / asset managers /
insurers / hedge funds that are known to use these three ATS platforms. Company
career sites change their ATS and slugs over time, and a wrong slug simply
returns a 404/empty result (main.py skips it silently and logs it under
"unresolved sources" at the end of a run) -- it will NOT break the run.

You should treat this file as a living config: run main.py, check the
"unresolved sources" section it prints, and fix/remove/add slugs as you learn
the real ones (open the company's careers page, click a job, and look at the
URL -- boards.greenhouse.io/<slug>/jobs/..., jobs.lever.co/<slug>/...,  or
<tenant>.wd#.myworkdayjobs.com/<site>/job/...).
"""

# Greenhouse: boards-api.greenhouse.io/v1/boards/{slug}/jobs
GREENHOUSE_COMPANIES = [
    "twosigma",
    "pointc72",
    "aqr",
    "citadel",
    "deshaw",
    "balyasny",
    "manaus",
    "brevanhoward",
    "marshallwace",
    "coatue",
    "vikingglobal",
    "pershingsquare",
    "elliottmanagement",
    "farallon",
    "wellington",
    "gsam",
    "pgim",
    "neubergerberman",
    "lazard",
    "invesco",
    "franklintempleton",
    "oaktreecapitalmanagement",
    "apollo",
    "aresmanagement",
    "kkr",
    "carlyle",
    "blackstone",
    "warburgpincus",
    "akunacapital",
    "imc",
    "optiver",
    "susquehanna",
    "jumptrading",
    "drw",
    "hudsonrivertrading",
    "flowtraders",
    "xtxmarkets",
    "wolverinetrading",
    "robeco",
    "ninetyone",
]

# Lever: api.lever.co/v0/postings/{slug}?mode=json
LEVER_COMPANIES = [
    "brevanhoward",
    "squarepoint",
    "cerebras",  # placeholder examples pruned by the 404-skip logic; replace with real finance Lever slugs as found
    "graham",
    "hbk",
    "man",
]

# Workday: {tenant}.wd{n}.myworkdayjobs.com -- (tenant, site, wd_number)
# wd_number varies by company (wd1, wd3, wd5, etc.) and sometimes changes; if a
# tenant stops resolving, check the company's live careers page URL for the
# current wd# and site name.
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

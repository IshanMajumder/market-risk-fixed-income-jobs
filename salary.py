"""
Best-effort salary extraction + USD normalization from free-text job
descriptions (most ATS APIs don't expose a structured salary field, so this
regexes the posting body/content for pay-transparency-style disclosures).
"""
import re

# Approximate USD conversion rates (update periodically -- these are fixed,
# not live, so this is meant to be "roughly right", not exact).
FX_TO_USD = {
    "$": 1.0, "USD": 1.0, "US$": 1.0,
    "£": 1.27, "GBP": 1.27,
    "€": 1.09, "EUR": 1.09,
    "CHF": 1.13,
    "SGD": 0.75,
    "HKD": 0.128,
    "JPY": 0.0067,
    "CAD": 0.73,
    "AUD": 0.66,
    "INR": 0.012,
    "CNY": 0.14,
    "AED": 0.27,
}

# Matches things like: "$60,000 - $80,000", "£45,000 to £60,000",
# "USD 60,000-80,000", "$60k - $80k", "60,000 EUR"
_RANGE_RE = re.compile(
    r"""
    (?P<cur1>US\$|USD|GBP|EUR|CHF|SGD|HKD|JPY|CAD|AUD|INR|CNY|AED|[$£€])?\s*
    (?P<num1>\d{2,3}(?:[,.]\d{3})*(?:\.\d+)?)\s*(?P<k1>k)?\s*
    (?:-|–|to|—)\s*
    (?P<cur2>US\$|USD|GBP|EUR|CHF|SGD|HKD|JPY|CAD|AUD|INR|CNY|AED|[$£€])?\s*
    (?P<num2>\d{2,3}(?:[,.]\d{3})*(?:\.\d+)?)\s*(?P<k2>k)?\s*
    (?P<cur3>US\$|USD|GBP|EUR|CHF|SGD|HKD|JPY|CAD|AUD|INR|CNY|AED)?
    """,
    re.VERBOSE | re.IGNORECASE,
)

_SINGLE_RE = re.compile(
    r"""
    (?P<cur1>US\$|USD|GBP|EUR|CHF|SGD|HKD|JPY|CAD|AUD|INR|CNY|AED|[$£€])\s*
    (?P<num1>\d{2,3}(?:[,.]\d{3})*(?:\.\d+)?)\s*(?P<k1>k)?
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _to_float(num_str, is_k):
    val = float(num_str.replace(",", ""))
    if is_k:
        val *= 1000
    return val


def _rate_for(cur):
    if not cur:
        return None
    return FX_TO_USD.get(cur.upper()) or FX_TO_USD.get(cur)


def extract_salary(text):
    """
    Returns a dict {"raw": "<matched text>", "min_usd": float} for the first
    plausible salary disclosure found, or None if no salary is mentioned.
    Only treats a number as a salary if it's >= 10,000 (annualized) to avoid
    false positives on phone numbers, years, bonus %, etc.
    """
    if not text:
        return None

    m = _RANGE_RE.search(text)
    if m and m.group("num1") and m.group("num2"):
        cur = m.group("cur1") or m.group("cur2") or m.group("cur3") or "$"
        rate = _rate_for(cur)
        if rate is None:
            rate = 1.0  # unknown currency symbol; assume USD-ish rather than drop it
        min_val = _to_float(m.group("num1"), bool(m.group("k1")))
        min_usd = min_val * rate
        if min_usd >= 10000:
            return {"raw": m.group(0).strip(), "min_usd": round(min_usd)}

    m = _SINGLE_RE.search(text)
    if m:
        cur = m.group("cur1")
        rate = _rate_for(cur) or 1.0
        val = _to_float(m.group("num1"), bool(m.group("k1")))
        val_usd = val * rate
        if val_usd >= 10000:
            return {"raw": m.group(0).strip(), "min_usd": round(val_usd)}

    return None


def passes_salary_filter(salary_info, minimum_usd=60000):
    """
    Per the chosen policy: keep jobs with no listed salary (can't verify, but
    don't want to miss them) AND jobs with an explicit salary >= minimum_usd.
    Only drop jobs that explicitly state a salary below minimum_usd.
    """
    if salary_info is None:
        return True
    return salary_info["min_usd"] >= minimum_usd

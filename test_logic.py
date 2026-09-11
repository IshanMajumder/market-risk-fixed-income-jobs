from main import title_matches_role
from salary import extract_salary, passes_salary_filter

title_cases = [
    ("Market Risk Analyst", True),
    ("Fixed Income Analyst", True),
    ("Senior Fixed Income Trading Analyst", True),
    ("Market Risk Management Analyst II", True),
    ("Market Risk Analyst Intern", False),  # excluded: internship
    ("Fixed Income Portfolio Manager", False),  # no "analyst"
    ("Credit Risk Analyst", False),  # not market risk or fixed income
    ("Operations Analyst", False),
    ("Fixed Income Sales Analyst", True),
]

print("=== Title matching ===")
all_pass = True
for title, expected in title_cases:
    got = title_matches_role(title)
    ok = got == expected
    all_pass &= ok
    print(f"{'OK ' if ok else 'FAIL'} '{title}' -> {got} (expected {expected})")

salary_cases = [
    ("Base salary range: $70,000 - $90,000 per year.", True, 70000),
    ("Compensation: $50,000 - $55,000 annually.", False, 50000),
    ("Salary: £45,000 - £55,000", False, None),  # ~£45k*1.27=57150 < 60k -> excluded
    ("Salary: £50,000 - £60,000", True, None),   # ~£50k*1.27=63500 >= 60k -> included
    ("We are looking for a driven analyst to join our team.", True, None),  # no salary -> included
    ("This role pays $65k to $85k depending on experience.", True, 65000),
]

print("\n=== Salary filter ===")
for text, expect_pass, expect_min in salary_cases:
    info = extract_salary(text)
    result = passes_salary_filter(info)
    ok = result == expect_pass
    all_pass &= ok
    min_usd = info["min_usd"] if info else None
    print(f"{'OK ' if ok else 'FAIL'} passes={result} (expected {expect_pass}) min_usd={min_usd} | '{text}'")

print("\nALL PASS" if all_pass else "\nSOME FAILED")

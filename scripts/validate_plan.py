from pathlib import Path
import csv

root = Path(__file__).resolve().parents[1]

with (root / "data" / "mixture.csv").open() as f:
    rows = list(csv.DictReader(f))
assert abs(sum(float(r["share_percent"]) for r in rows) - 100.0) < 1e-9

with (root / "data" / "indic_allocation.csv").open() as f:
    rows = list(csv.DictReader(f))
assert abs(sum(float(r["target_B_tokens"]) for r in rows) - 18.0) < 1e-9

tiers = {}
for r in rows:
    tiers[r["tier"]] = tiers.get(r["tier"], 0.0) + float(r["target_B_tokens"])
expected = {"Verified": 8.1, "Unverified": 4.5, "Translated": 3.6, "Synthetic": 1.8}
for k, v in expected.items():
    assert abs(tiers[k] - v) < 1e-9

over = [r for r in rows if float(r["sampling_factor"]) > 1.0]
assert len(over) == 1
assert over[0]["language"] == "Telugu" and over[0]["tier"] == "Unverified"
assert float(over[0]["sampling_factor"]) <= 1.25

print("PASS: mixture, Indic tiers and replay caps are internally consistent.")

from pathlib import Path
import pandas as pd
DATA_DIR = Path("E20_folder")
FILES = [
    ("4-WHEELERS", "All Fuel Types (only active 4 wheelers).csv"),
    ("3-WHEELERS", "All fuel types (3 wheelers only).csv"),
    ("2-WHEELERS", "All Fuel Vehicles(two wheelers only).csv"),
]
PERIODS = [
    ("PRE-ROADMAP (2018-2021)", 2018, 2021),
    ("POST-ROADMAP (2022-2025)", 2022, 2025),
]
def load(filename):
    df = pd.read_csv(DATA_DIR / filename, index_col=0)
    df.index = pd.to_numeric(df.index.astype(str).str.strip(), errors="coerce")
    return df
def is_total(col):
    return col.strip().lower() == "total"
def classify(fuel):
    f = fuel.upper()
    if "ETHANOL" in f:
        return "Ethanol E100"
    if "ELECTRIC" in f or "PURE EV" in f or "PLUG-IN" in f or "STRONG HYBRID" in f:
        return "EV (BOV/pure/plug-in/strong hybrid)"
    if "DIESEL" in f:
        return "Diesel (incl. dual diesel)"
    if f.startswith("PETROL") and "CNG" in f:
        return "Petrol + CNG (bi-fuel)"
    if f.startswith("PETROL") and "LPG" in f:
        return "Petrol + LPG"
    if f.startswith("PETROL") and "HYBRID" in f:
        return "Petrol hybrid"
    if f == "PETROL":
        return "Petrol (exact)"
    if f.startswith("PETROL"):
        return "Petrol variant (E20/other)"
    if "CNG" in f or "LPG" in f or "LNG" in f or "HCNG" in f:
        return "CNG / gas only"
    return "Other"
def period_totals(df, start, end):
    mask = (df.index >= start) & (df.index <= end)
    cols = [c for c in df.columns if not is_total(c)]
    return df.loc[mask, cols].apply(pd.to_numeric, errors="coerce").fillna(0).sum()
def print_block(category, filename):
    df = load(filename)
    total_cols = [c for c in df.columns if is_total(c)]
    print(f"\n{'=' * 60}\n{category}\n{'=' * 60}")
    for period_name, start, end in PERIODS:
        totals = period_totals(df, start, end)
        fleet_total = totals.sum()
        print(f"\n{period_name}")
        print("-" * 60)
        print("RAW COUNTS BY FUEL TYPE")
        for fuel, count in totals.items():
            if count:
                print(f"  {fuel}: {count:,.0f}")
        if total_cols:
            mask = (df.index >= start) & (df.index <= end)
            file_total = pd.to_numeric(
                df.loc[mask, total_cols[0]], errors="coerce"
            ).fillna(0).sum()
            status = "OK" if abs(file_total - fleet_total) < 1 else "MISMATCH"
            print(f"\nCheck: fleet total {fleet_total:,.0f} vs. file Total {file_total:,.0f} -> {status}")
        buckets = {}
        for fuel, count in totals.items():
            key = classify(fuel)
            buckets[key] = buckets.get(key, 0) + count
        print(f"\nTOTAL FLEET: {fleet_total:,.0f}")
        print("MUTUALLY EXCLUSIVE SHARES (sum = 100%)")
        for bucket, count in sorted(buckets.items(), key=lambda x: -x[1]):
            share = count / fleet_total * 100 if fleet_total else 0
            print(f"  {bucket}: {count:,.0f} ({share:.2f}%)")
        if fleet_total:
            print(f"  Sum check: {sum(buckets.values()) / fleet_total * 100:.2f}%")
        e20_count = sum(c for f, c in totals.items() if "E20" in f.upper())
        e20_share = e20_count / fleet_total * 100 if fleet_total else 0
        print(f"\nE20 FLAG (any E20 variant, overlaps buckets): {e20_count:,.0f} ({e20_share:.2f}%)")
for category, filename in FILES:
    print_block(category, filename)
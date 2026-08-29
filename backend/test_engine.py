from app.services.smart_engine import analyze_number

tests = [
    "+919876543210",  # reported scam (digital arrest)
    "+919999999999",  # verified safe
    "+918888777555",  # normal valid number -> lowish
    "+917777777777",  # reported scam + repeated digits
    "+916555555555",  # repeated 5s -> flagged
    "+911234567890",  # reported loan fraud
    "+918886666444",  # valid, should be low
]
for n in tests:
    r = analyze_number(n)
    print("{:16s} score={:3d} / {:11s} scam={}  reasons={}".format(
        n, r["risk_score"], r["risk_level"], r["is_scam"], r["details"]["reasons"]))

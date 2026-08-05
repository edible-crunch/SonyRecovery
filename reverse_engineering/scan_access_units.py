from recovery.access_unit_scanner import scan_candidates

mp4 = input("Recovered MP4:\n").strip('"')

print()
print("Scanning...")
print()

results = scan_candidates(
    mp4,
    step=16,
    max_candidates=50
)

print(f"Candidates Found: {len(results)}")
print()

for i, c in enumerate(results, 1):

    print("=" * 60)
    print(f"Candidate {i}")
    print("=" * 60)

    print(f"Offset     : {c.offset:,}")
    print(f"NAL Length : {c.nal_length:,}")

    h = c.header

    print(f"Type       : {h['nal_name']}")
    print(f"Layer      : {h['layer_id']}")
    print(f"Temporal   : {h['temporal_id']}")
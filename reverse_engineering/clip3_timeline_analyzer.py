from parsers.video_tables import get_video_tables

RECOVERED_MOV = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mov\MOV_01m54s_000003.MOV"
)

CHUNK_STARTS = "chunk_starts.txt"

# ----------------------------------------------------------
# Load recovered MOV STCO
# ----------------------------------------------------------

tables = get_video_tables(RECOVERED_MOV)

mov_offsets = tables["stco"].offsets

# ----------------------------------------------------------
# Load detected chunk starts
# ----------------------------------------------------------

detected = []

with open(CHUNK_STARTS) as f:

    for line in f:

        line = line.strip()

        if line:

            detected.append(int(line))

# ----------------------------------------------------------

print()
print("=" * 95)
print("CLIP 3 TIMELINE ANALYZER")
print("=" * 95)

print()

print(f"MOV STCO entries        : {len(mov_offsets)}")
print(f"Detected chunk starts   : {len(detected)}")

print()

print("=" * 95)
print(
    f"{'Idx':>4}  "
    f"{'MOV STCO':>14}  "
    f"{'Detected':>14}  "
    f"{'Difference':>14}  "
    f"Status"
)
print("=" * 95)

count = max(len(mov_offsets), len(detected))

for i in range(count):

    mov = mov_offsets[i] if i < len(mov_offsets) else None
    det = detected[i] if i < len(detected) else None

    if mov is None:

        status = "Missing in MOV"

        diff = ""

    elif det is None:

        status = "Missing in detector"

        diff = ""

    else:

        diff = det - mov

        if diff == 0:

            status = "MATCH"

        else:

            status = "OFFSET"

    mov_text = "-" if mov is None else f"{mov:,}"
    det_text = "-" if det is None else f"{det:,}"
    diff_text = "" if diff == "" else f"{diff:+,}"

    print(
        f"{i+1:4d}  "
        f"{mov_text:>14}  "
        f"{det_text:>14}  "
        f"{diff_text:>14}  "
        f"{status}"
    )

print()
print("=" * 95)

extra = len(detected) - len(mov_offsets)

print(f"Extra detected chunk starts : {extra}")

print("=" * 95)
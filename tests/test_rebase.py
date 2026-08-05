from parsers.stco_reader import read_stco
from repair.stco_rebase import rebase_offsets

VIDEO_STCO_OFFSET = 83355

OLD_PAYLOAD = 131072
NEW_PAYLOAD = 86338

delta = NEW_PAYLOAD - OLD_PAYLOAD

stco = read_stco(
    "moov.bin",
    VIDEO_STCO_OFFSET
)

new_offsets = rebase_offsets(
    stco.offsets,
    delta
)

print()
print("Delta:", delta)

print()

print("Original -> Rebased")

for i in range(10):

    print(
        f"{stco.offsets[i]:>12,}"
        f" -> "
        f"{new_offsets[i]:>12,}"
    )
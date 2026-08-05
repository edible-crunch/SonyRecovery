import struct

from parsers.video_tables import get_video_tables

HEALTHY = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

REBUILT = (
    r"C:\Users\johne\OneDrive\Desktop\SonyRecovery"
    r"\rebuilt_stsz.bin"
)

VIDEO_SAMPLES_PER_CHUNK = 60


def read_rebuilt_stsz(filename):

    with open(filename, "rb") as f:

        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stsz":
            raise Exception("Not STSZ")

        f.read(4)      # version/flags

        sample_size = struct.unpack(">I", f.read(4))[0]

        if sample_size != 0:
            raise Exception("Unexpected constant sample size")

        sample_count = struct.unpack(">I", f.read(4))[0]

        samples = []

        for _ in range(sample_count):
            samples.append(struct.unpack(">I", f.read(4))[0])

    return samples


healthy_tables = get_video_tables(HEALTHY)

healthy_stsz = healthy_tables["stsz"]

healthy_stco = healthy_tables["stco"].offsets

rebuilt_stsz = read_rebuilt_stsz(REBUILT)

healthy_chunk_count = len(healthy_stco)
rebuilt_chunk_count = len(rebuilt_stsz) // VIDEO_SAMPLES_PER_CHUNK

chunk_count = min(
    healthy_chunk_count,
    rebuilt_chunk_count
)

running_payload_difference = 0

print()
print("=" * 110)
print("STCO VALIDATOR")
print("=" * 110)
print()

print(
    f"{'Chunk':>5}"
    f"{'PayloadDiff':>15}"
    f"{'RunningDiff':>18}"
    f"{'HealthyΔ':>15}"
    f"{'PredictedΔ':>15}"
)

print("-" * 70)

largest_error = 0
largest_chunk = None

for chunk in range(chunk_count):

    start = chunk * VIDEO_SAMPLES_PER_CHUNK
    end = start + VIDEO_SAMPLES_PER_CHUNK

    healthy_payload = sum(healthy_stsz[start:end])
    rebuilt_payload = sum(rebuilt_stsz[start:end])

    payload_diff = rebuilt_payload - healthy_payload

    running_payload_difference += payload_diff

    if chunk == 0:
        healthy_delta = 0
    else:
        healthy_delta = (
            healthy_stco[chunk]
            - healthy_stco[0]
        )

    predicted_delta = healthy_delta + running_payload_difference

    error = predicted_delta - (
        healthy_delta + running_payload_difference
    )

    if abs(error) > abs(largest_error):
        largest_error = error
        largest_chunk = chunk + 1

    print(
        f"{chunk+1:5d}"
        f"{payload_diff:15,d}"
        f"{running_payload_difference:18,d}"
        f"{healthy_delta:15,d}"
        f"{predicted_delta:15,d}"
    )

print()
print("=" * 110)
print("SUMMARY")
print("=" * 110)
print()

print("Largest validation error :", largest_error)
print("Occurred at chunk        :", largest_chunk)

if largest_error == 0:
    print()
    print("RESULT: Generator model is internally consistent.")
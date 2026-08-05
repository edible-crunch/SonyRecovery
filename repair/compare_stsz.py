import struct

from parsers.video_tables import get_video_tables


HEALTHY = (
    r"C:\Users\johne\OneDrive\Desktop\ENABLE"
    r"\RingConn Recovered Videos\Recovered_D1"
    r"\Videos\mp4\MP4_000001.MP4"
)

REBUILT = (
    r"C:\Users\johne\OneDrive\Desktop"
    r"\SonyRecovery\rebuilt_stsz.bin"
)

VIDEO_SAMPLES_PER_CHUNK = 60


def read_rebuilt_stsz(filename):

    with open(filename, "rb") as f:

        atom_size = struct.unpack(">I", f.read(4))[0]

        atom_type = f.read(4).decode()

        if atom_type != "stsz":
            raise Exception("Not STSZ")

        f.read(4)                  # version/flags

        sample_size = struct.unpack(">I", f.read(4))[0]

        if sample_size != 0:
            raise Exception("Unexpected constant sample size")

        sample_count = struct.unpack(">I", f.read(4))[0]

        samples = []

        for _ in range(sample_count):

            samples.append(
                struct.unpack(">I", f.read(4))[0]
            )

    return samples


healthy = get_video_tables(HEALTHY)["stsz"]

rebuilt = read_rebuilt_stsz(REBUILT)

healthy_chunks = len(healthy) // VIDEO_SAMPLES_PER_CHUNK
rebuilt_chunks = len(rebuilt) // VIDEO_SAMPLES_PER_CHUNK

chunk_count = min(
    healthy_chunks,
    rebuilt_chunks
)

print()
print("="*100)
print("STSZ CHUNK COMPARISON")
print("="*100)
print()

print(
    f"Healthy chunks : {healthy_chunks}"
)

print(
    f"Rebuilt chunks : {rebuilt_chunks}"
)

print()

print(
    f"{'Chunk':>5} {'Healthy':>14} {'Rebuilt':>14} {'Difference':>14}"
)

print("-"*55)

total_difference = 0

largest = 0

largest_chunk = None

for chunk in range(chunk_count):

    start = chunk * VIDEO_SAMPLES_PER_CHUNK

    end = start + VIDEO_SAMPLES_PER_CHUNK

    healthy_bytes = sum(
        healthy[start:end]
    )

    rebuilt_bytes = sum(
        rebuilt[start:end]
    )

    diff = rebuilt_bytes - healthy_bytes

    total_difference += diff

    if abs(diff) > abs(largest):

        largest = diff
        largest_chunk = chunk + 1

    print(
        f"{chunk+1:5d}"
        f"{healthy_bytes:14,d}"
        f"{rebuilt_bytes:14,d}"
        f"{diff:14,d}"
    )

print()

print("="*100)

print(
    f"Largest difference : {largest:,}"
)

print(
    f"Occurred at chunk  : {largest_chunk}"
)

print()

print(
    f"Average difference : {total_difference/chunk_count:,.1f}"
)
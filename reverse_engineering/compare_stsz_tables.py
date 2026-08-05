HEALTHY = "healthy_stsz.txt"
REBUILT = "rebuilt_stsz.txt"


def load(path):
    with open(path, "r") as f:
        return [int(x.strip()) for x in f if x.strip()]


healthy = load(HEALTHY)
rebuilt = load(REBUILT)

print("=" * 70)
print("STSZ COMPARISON")
print("=" * 70)
print()

print(f"Healthy frames : {len(healthy)}")
print(f"Rebuilt frames : {len(rebuilt)}")
print()

count = min(len(healthy), len(rebuilt))

different = 0
total_diff = 0
largest = 0
largest_frame = 0

print("First 50 differences:")
print()

shown = 0

for i in range(count):

    if healthy[i] != rebuilt[i]:

        diff = rebuilt[i] - healthy[i]

        different += 1
        total_diff += abs(diff)

        if abs(diff) > largest:
            largest = abs(diff)
            largest_frame = i + 1

        if shown < 50:

            print(
                f"Frame {i+1:4d} | "
                f"Healthy {healthy[i]:9,d} | "
                f"Recovered {rebuilt[i]:9,d} | "
                f"Diff {diff:+9,d}"
            )

            shown += 1

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Compared frames : {count}")
print(f"Different       : {different}")
print(f"Same            : {count-different}")
print(f"Average diff    : {total_diff/max(different,1):,.1f}")
print(f"Largest diff    : {largest:,}")
print(f"Largest frame   : {largest_frame}")
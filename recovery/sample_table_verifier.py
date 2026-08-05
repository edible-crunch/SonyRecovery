class SampleTableVerifier:

    def __init__(self, sample_sizes):

        self.sample_sizes = sample_sizes

    def build_virtual_offsets(self):

        offsets = []

        current = 0

        for index, size in enumerate(self.sample_sizes):

            offsets.append({
                "sample": index + 1,
                "offset": current,
                "size": size
            })

            current += size

        return offsets

    def summary(self):

        offsets = self.build_virtual_offsets()

        print()
        print("=" * 60)
        print("VIRTUAL SAMPLE TABLE")
        print("=" * 60)

        print()

        print(f"Samples : {len(offsets)}")

        print(
            f"Total Bytes : "
            f"{offsets[-1]['offset'] + offsets[-1]['size']:,}"
        )

        print()

        print("First 10 Samples")

        for s in offsets[:10]:

            print(
                f"{s['sample']:5}  "
                f"Offset={s['offset']:10,}  "
                f"Size={s['size']:8,}"
            )

        return offsets
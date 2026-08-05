from recovery.sample import Sample


class SampleTable:

    def __init__(self, sample_sizes):

        self.samples = []

        offset = 0

        for i, size in enumerate(sample_sizes):

            s = Sample()

            s.index = i + 1

            s.size = size

            s.expected_offset = offset

            self.samples.append(s)

            offset += size

    def __len__(self):

        return len(self.samples)

    def __getitem__(self, index):

        return self.samples[index]

    def total_size(self):

        if not self.samples:

            return 0

        last = self.samples[-1]

        return last.expected_offset + last.size

    def summary(self):

        print()
        print("=" * 60)
        print("SAMPLE TABLE")
        print("=" * 60)

        print()

        print("Samples :", len(self.samples))

        print("Virtual Size :", f"{self.total_size():,}")

        print()

        print("First 10")

        for sample in self.samples[:10]:

            print(sample)
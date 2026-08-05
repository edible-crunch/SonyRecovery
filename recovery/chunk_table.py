class Chunk:

    def __init__(self):

        self.index = 0

        self.first_sample = 0

        self.last_sample = 0

        self.sample_count = 0

        self.video_bytes = 0

        self.actual_offset = None

    def __repr__(self):

        actual = (
            "?"
            if self.actual_offset is None
            else f"{self.actual_offset:,}"
        )

        return (
            f"<Chunk "
            f"#{self.index} "
            f"samples={self.first_sample}-{self.last_sample} "
            f"bytes={self.video_bytes:,} "
            f"offset={actual}>"
        )


class ChunkTable:

    def __init__(self, sample_sizes, samples_per_chunk):

        self.chunks = []

        chunk_index = 1

        sample = 1

        while sample <= len(sample_sizes):

            c = Chunk()

            c.index = chunk_index

            c.first_sample = sample

            c.last_sample = min(
                sample + samples_per_chunk - 1,
                len(sample_sizes)
            )

            c.sample_count = (
                c.last_sample
                - c.first_sample
                + 1
            )

            c.video_bytes = sum(
                sample_sizes[
                    c.first_sample - 1 :
                    c.last_sample
                ]
            )

            self.chunks.append(c)

            sample += samples_per_chunk

            chunk_index += 1

    def __len__(self):

        return len(self.chunks)

    def __getitem__(self, index):

        return self.chunks[index]

    def summary(self):

        print()
        print("=" * 60)
        print("CHUNK TABLE")
        print("=" * 60)

        print()

        print(
            f"Chunks : {len(self.chunks)}"
        )

        print()

        print("First 10")

        for chunk in self.chunks[:10]:

            print(chunk)
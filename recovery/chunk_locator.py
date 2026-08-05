class ChunkLocator:

    def __init__(self, chunk_table):

        self.chunk_table = chunk_table

        self.video_anchor = None

    def set_video_anchor(
        self,
        mdat_payload_offset,
        relative_video_offset
    ):

        self.video_anchor = (
            mdat_payload_offset +
            relative_video_offset
        )

        return self.video_anchor

    def first_chunk(self):

        return self.chunk_table[0]

    def summary(self):

        print()
        print("=" * 60)
        print("CHUNK LOCATOR")
        print("=" * 60)
        print()

        if self.video_anchor is None:

            print("Video anchor not set.")
            return

        print(
            f"Video Anchor : {self.video_anchor:,}"
        )

        print()

        print(self.first_chunk())
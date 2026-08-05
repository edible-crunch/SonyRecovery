class Sample:

    def __init__(self):

        self.index = 0

        self.size = 0

        self.expected_offset = 0

        self.actual_offset = None

        self.chunk = None

        self.valid = False

    def __repr__(self):

        actual = (
            "?"
            if self.actual_offset is None
            else f"{self.actual_offset:,}"
        )

        return (
            f"<Sample "
            f"#{self.index} "
            f"size={self.size} "
            f"expected={self.expected_offset:,} "
            f"actual={actual}>"
        )
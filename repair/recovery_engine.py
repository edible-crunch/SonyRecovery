from parsers.video_tables import get_video_tables
from recovery.frame_mapper import build_frame_map
from repair.hvcc import parse_hvcc
from repair.hevc import parse_header
from parsers.mdat_reader import locate_mdat

class RecoveryEngine:

    def __init__(self):

        self.mov = None
        self.mp4 = None
        self.mdat = None
        self.hvcc = None
        self.tables = None
        self.frame_map = None

    # -------------------------------------------------

    def load_mov(self, mov_path):

        self.mov = mov_path

        self.tables = get_video_tables(mov_path)

        self.frame_map = build_frame_map(
            self.tables["stco"].offsets,
            self.tables["stsc"],
            self.tables["stsz"]
        )

        print("[OK] MOV loaded")

    # -------------------------------------------------

    def load_mp4(self, mp4_path):

        self.mp4 = mp4_path

        self.mdat = locate_mdat(mp4_path)

        print("[OK] MP4 loaded")

        print(
            f"[OK] mdat @ {self.mdat.offset:,}"
        )

        print(
            f"[OK] mdat payload @ {self.mdat.data_offset:,}"
        )

        print(
            f"[OK] mdat size = {self.mdat.size:,} bytes"
        )

    # -------------------------------------------------

    def load_hvcc(self, hvcc_path):

        self.hvcc = parse_hvcc(hvcc_path)

        print("[OK] HVCC parsed")

    # -------------------------------------------------

    def summary(self):

        print()
        print("=" * 60)
        print("RECOVERY ENGINE")
        print("=" * 60)

        print()

        print("Recovered MOV")
        print(self.mov)

        print()

        print("Recovered MP4")
        print(self.mp4)

        print()

        print("Profile :", self.hvcc.profile_idc)
        print("Tier    :", self.hvcc.tier_flag)
        print("Level   :", self.hvcc.level_idc)
        print("NAL Size:", self.hvcc.nalu_length_size)

        print()

        print("Parameter Sets")

        for array in self.hvcc.arrays:

            print(
                f"Type {array['type']} : "
                f"{len(array['nalus'])} NAL(s)"
            )

        print()

        print("Frames :", len(self.frame_map))

    # -------------------------------------------------

    def analyze_sample(self, frame_number):

        if frame_number < 1:
            return

        if frame_number > len(self.frame_map):
            return

        frame = self.frame_map[frame_number - 1]

        print()
        print("=" * 60)
        print(f"FRAME {frame_number}")
        print("=" * 60)

        print("Chunk :", frame["chunk"])
        print("Offset:", frame["offset"])
        print("Size  :", frame["size"])

        with open(self.mp4, "rb") as f:

            f.seek(frame["offset"])

            sample = f.read(min(frame["size"], 128))

        print()

        print("First 64 Bytes")
        print("-" * 60)

        for i in range(0, min(64, len(sample)), 16):

            chunk = sample[i:i+16]

            hexs = " ".join(
                f"{b:02X}" for b in chunk
            )

            text = "".join(
                chr(b) if 32 <= b < 127 else "."
                for b in chunk
            )

            print(
                f"{i:04X}  "
                f"{hexs:<47} "
                f"{text}"
            )

        print()

        if len(sample) >= 6:

            nal_length = int.from_bytes(
                sample[0:4],
                "big"
            )

            print("First NAL Length :", nal_length)

            header = parse_header(sample[4:6])

            print("Parsed Header")

            for k, v in header.items():

                print(f"  {k:<16} {v}")

        print()

        print("Searching for Annex-B start codes...")

        count = 0

        for i in range(len(sample) - 4):

            if sample[i:i+4] == b"\x00\x00\x00\x01":

                print(
                    f"00000001 at {i}"
                )

                count += 1

            elif sample[i:i+3] == b"\x00\x00\x01":

                print(
                    f"000001 at {i}"
                )

                count += 1

        print()

        print("Start Codes Found :", count)
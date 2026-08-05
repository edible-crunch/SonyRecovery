from locators.stco_locator import find_stco_atoms
from parsers.stco_reader import read_stco
from parsers.mdat_reader import locate_mdat

# ----------------------------------------------------
# FILES
# ----------------------------------------------------

MOOV = "moov.bin"

MP4 = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"

# ----------------------------------------------------

NAL_NAMES = {
    0: "TRAIL_N",
    1: "TRAIL_R",
    19: "IDR_W_RADL",
    20: "IDR_N_LP",
    21: "CRA",
    32: "VPS",
    33: "SPS",
    34: "PPS",
    35: "AUD",
    39: "SEI"
}


def nal_name(t):
    return NAL_NAMES.get(t, f"TYPE_{t}")


def main():

    atoms = find_stco_atoms(MOOV)

    video = read_stco(
        MOOV,
        atoms[0],      # Track 1 = Video
        1
    )

    mdat = locate_mdat(MP4)

    print()
    print("=" * 72)
    print("VIDEO CHUNK PROBE")
    print("=" * 72)
    print()

    with open(MP4, "rb") as f:

        for i, offset in enumerate(video.offsets[:10], start=1):

            print(f"Chunk {i}")
            print("-" * 40)

            print("MOV Chunk Offset :", f"{offset:,}")

            if offset < mdat.data_offset:

                print("Offset occurs before recovered mdat")
                print()
                continue

            f.seek(offset)

            data = f.read(32)

            print("Hex:")
            print(data.hex(" "))

            if len(data) >= 5:

                nal = (data[4] >> 1) & 0x3F

                print("NAL:", nal_name(nal))

            print()


if __name__ == "__main__":
    main()
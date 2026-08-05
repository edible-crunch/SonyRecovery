import struct


META_PAYLOAD = 1_167_360
AUDIO_PAYLOAD = 192_192

VIDEO_SAMPLES_PER_CHUNK = 60


def read_rebuilt_stsz(filename):

    with open(filename, "rb") as f:

        atom_size = struct.unpack(">I", f.read(4))[0]
        atom_type = f.read(4).decode()

        if atom_type != "stsz":
            raise Exception(
                f"Expected stsz, found {atom_type}"
            )

        # version + flags
        f.read(4)

        sample_size = struct.unpack(">I", f.read(4))[0]

        if sample_size != 0:
            raise Exception(
                "Constant-size STSZ not supported."
            )

        sample_count = struct.unpack(">I", f.read(4))[0]

        sizes = []

        for _ in range(sample_count):

            sizes.append(
                struct.unpack(">I", f.read(4))[0]
            )

    return sizes

def generate_offsets(
    rebuilt_stsz_file,
    base_offset,
):
    """
    Generates synchronized
    Meta / Video / Audio STCO tables.

    Parameters
    ----------
    rebuilt_stsz_file : str

    base_offset : int
        Beginning of first META chunk.

    Returns
    -------
    meta_offsets
    video_offsets
    audio_offsets
    """

    stsz = read_rebuilt_stsz(
        rebuilt_stsz_file
    )

    meta_offsets = []
    video_offsets = []
    audio_offsets = []

    meta = base_offset

    sample = 0

    while sample < len(stsz):

        video_payload = sum(
            stsz[
                sample:
                sample + VIDEO_SAMPLES_PER_CHUNK
            ]
        )

        video = meta + META_PAYLOAD

        audio = video + video_payload

        meta_offsets.append(meta)
        video_offsets.append(video)
        audio_offsets.append(audio)

        meta = audio + AUDIO_PAYLOAD

        sample += VIDEO_SAMPLES_PER_CHUNK

    return (
        meta_offsets,
        video_offsets,
        audio_offsets,
    )


if __name__ == "__main__":

    STSZ = (
        r"C:\Users\johne\OneDrive\Desktop"
        r"\SonyRecovery\rebuilt_stsz.bin"
    )

    BASE = 131072

    meta, video, audio = generate_offsets(
        STSZ,
        BASE,
    )

    print()
    print("=" * 80)
    print("STCO GENERATOR")
    print("=" * 80)

    print()

    print("Chunks :", len(video))

    print()

    print("First 10")

    for i in range(min(10, len(video))):

        print()

        print(
            f"{i+1:03d}"
        )

        print(
            f"Meta  : {meta[i]:,}"
        )

        print(
            f"Video : {video[i]:,}"
        )

        print(
            f"Audio : {audio[i]:,}"
        )
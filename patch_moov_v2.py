from pathlib import Path

from parsers.track_locator import get_tracks

from repair.moov_editor import MoovEditor
from repair.stco_generator import generate_offsets
from repair.build_stco_atom import build_stco_atom


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parent

ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"

MOOV = ASSETS / "moov.bin"
STSZ = ASSETS / "rebuilt_stsz.bin"

PATCHED_MOOV = OUTPUT / "patched_moov.bin"


# ------------------------------------------------------------
# Sony constants
# ------------------------------------------------------------

BASE_OFFSET = 131072
def identify_tracks(filename):
    """
    Temporary helper.

    At the moment we assume Sony track order:

        Track 1 -> Video
        Track 2 -> Audio
        Track 3 -> Metadata

    This will later be replaced by automatic HDLR detection.
    """

    tracks = get_tracks(filename)

    if len(tracks) != 3:
        raise RuntimeError(
            f"Expected 3 tracks, found {len(tracks)}."
        )

    return {
        "vide": tracks[0],
        "soun": tracks[1],
        "meta": tracks[2],
    }
def main():

    print("=" * 80)
    print("PATCH MOOV V2")
    print("=" * 80)

    print()
    print("Loading tracks...")

    tracks = identify_tracks(MOOV)

    print("Video track found")
    print("Audio track found")
    print("Metadata track found")

    print()
    print("Generating offsets...")

    meta_offsets, video_offsets, audio_offsets = generate_offsets(
        STSZ,
        BASE_OFFSET,
    )

    print(f"Video chunks : {len(video_offsets)}")
    print(f"Audio chunks : {len(audio_offsets)}")
    print(f"Meta chunks  : {len(meta_offsets)}")

    print()
    print("Building STCO atoms...")

    video_stco = build_stco_atom(video_offsets)
    audio_stco = build_stco_atom(audio_offsets)
    meta_stco = build_stco_atom(meta_offsets)

    print("Done.")

    print()
    print("Opening MOOV editor...")

    editor = MoovEditor(MOOV)

    print("Ready.")

    print()
    print("Replacing Video STSZ...")

    video_track = tracks["vide"]
    video_stsz_offset = video_track["stsz"].offset

    with open(STSZ, "rb") as f:
        rebuilt_stsz = f.read()

    delta = editor.replace_atom(
        video_stsz_offset,
        rebuilt_stsz,
    )

    print(f"Video STSZ delta : {delta:+,}")

    print()
    print("Saving patched MOOV...")

    editor.save(PATCHED_MOOV)

    print()
    print("Finished.")
if __name__ == "__main__":
    main()
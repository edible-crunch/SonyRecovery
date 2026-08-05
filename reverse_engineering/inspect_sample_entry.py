from parsers.video_track import get_video_atoms
from parsers.stsd_reader import read_stsd
from analysis.sample_entry_walker import walk_sample_entry

mp4 = input("Healthy MP4:\n").strip('"')

video = get_video_atoms(mp4)

sample_offset, sample_size = read_stsd(
    mp4,
    video["stsd"].offset
)

walk_sample_entry(
    mp4,
    sample_offset,
    sample_size
)
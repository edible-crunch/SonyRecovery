from parsers.video_track import get_video_atoms
from parsers.stsz_reader import read_stsz

from recovery.sample_table import SampleTable

mp4 = input("Recovered MOV:\n").strip('"')

video = get_video_atoms(mp4)

sizes = read_stsz(
    mp4,
    video["stsz"].offset
)

table = SampleTable(sizes)

table.summary()
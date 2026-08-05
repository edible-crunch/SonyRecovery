from parsers.video_track import get_video_atoms

from parsers.stsz_reader import read_stsz
from parsers.stsc_reader import read_stsc

from recovery.chunk_table import ChunkTable


mov = input("Recovered MOV:\n").strip('"')

video = get_video_atoms(mov)

sizes = read_stsz(
    mov,
    video["stsz"].offset
)

stsc = read_stsc(
    mov,
    video["stsc"].offset
)

samples_per_chunk = stsc[0][1]

table = ChunkTable(
    sizes,
    samples_per_chunk
)

table.summary()
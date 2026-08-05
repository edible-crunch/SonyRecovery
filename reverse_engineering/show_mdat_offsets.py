from parsers.mdat_reader import locate_mdat

files = [
    ("Recovered",
     r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000003.MP4"),
    ("Candidate", "candidate_clip3.mp4"),
]

for name, path in files:
    m = locate_mdat(path)

    print("=" * 60)
    print(name)
    print("=" * 60)
    print("mdat offset      :", m.offset)
    print("mdat data_offset :", m.data_offset)
    print("mdat size        :", m.size)
    print()
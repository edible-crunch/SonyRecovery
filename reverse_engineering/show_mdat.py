from parsers.mdat_reader import locate_mdat

mp4 = input("MP4:\n").strip('"')

mdat = locate_mdat(mp4)

print()
print("=" * 60)
print("MDAT INFORMATION")
print("=" * 60)

print(f"Atom Offset : {mdat.offset:,}")
print(f"Data Offset : {mdat.data_offset:,}")
print(f"Atom Size   : {mdat.size:,}")

print()
print(f"Payload Size: {mdat.size - (mdat.data_offset - mdat.offset):,}")
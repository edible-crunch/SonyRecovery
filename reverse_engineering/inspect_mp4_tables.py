from parsers.video_tables import get_video_tables

FILE = r"C:\Users\johne\OneDrive\Desktop\ENABLE\RingConn Recovered Videos\Recovered_D1\Videos\mp4\MP4_000001.MP4"

tables = get_video_tables(FILE)

stco = tables["stco"]
stsc = tables["stsc"]
stsz = tables["stsz"]

print("=" * 70)
print("MP4 TABLE INSPECTION")
print("=" * 70)

print()

print("STCO")
print("----------------------------")
print("Entries :", len(stco.offsets))
print("First 10:")
for x in stco.offsets[:10]:
    print(x)

print()

print("STSC")
print("----------------------------")

print(type(stsc))

print("Entries :", len(stsc))

print()

print("STSZ")
print("----------------------------")

print(type(stsz))

if isinstance(stsz, list):

    print("Frames :", len(stsz))

    print()

    print("First 20 sizes:")

    for s in stsz[:20]:
        print(s)

    print()

    print("Average:",
          sum(stsz)/len(stsz))

else:

    print(dir(stsz))
print()

print("Average frame size:",
      sum(stsz.sizes)/len(stsz.sizes))
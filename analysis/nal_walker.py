def walk_nals(filename):

    with open(filename, "rb") as f:

        data = f.read()

    pos = 0
    index = 1

    print()
    print("NAL WALK")
    print("-" * 70)
    print(f"{'NAL':>4} {'Offset':>10} {'Length':>10} {'Type':>8}")

    while pos + 4 <= len(data):

        length = int.from_bytes(data[pos:pos+4], "big")

        if length == 0:
            print("\nReached zero-length NAL.")
            break

        if pos + 4 + length > len(data):
            print("\nNAL extends beyond end of sample.")
            print("Offset :", pos)
            print("Length :", length)
            break

        header = data[pos + 4]

        nal_type = (header >> 1) & 0x3F

        print(f"{index:4} {pos:10} {length:10} {nal_type:8}")

        pos += 4 + length
        index += 1

    print()
    print("Bytes consumed :", pos)
    print("Sample size    :", len(data))
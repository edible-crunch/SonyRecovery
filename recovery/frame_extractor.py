def extract_frame(mp4_file, offset, size, output_file):

    with open(mp4_file, "rb") as src:

        src.seek(offset)

        data = src.read(size)

    with open(output_file, "wb") as dst:

        dst.write(data)

    print()
    print("Frame extracted successfully!")
    print("Output :", output_file)
    print("Bytes  :", len(data))
def extract_hvcc(filename, offset, size, output):

    with open(filename, "rb") as f:

        f.seek(offset)

        data = f.read(size)

    with open(output, "wb") as out:

        out.write(data)

    print()
    print("Extracted hvcC successfully!")
    print("Output:", output)
    print("Bytes :", len(data))
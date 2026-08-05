def find_stco_atoms(filename):

    with open(filename, "rb") as f:
        data = f.read()

    offsets = []

    pos = 0

    while True:

        pos = data.find(b"stco", pos)

        if pos == -1:
            break

        # atom begins 4 bytes before the type
        offsets.append(pos - 4)

        pos += 4

    return offsets
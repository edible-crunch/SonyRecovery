def find_all_stco(filename):

    with open(filename, "rb") as f:

        data = f.read()

    pos = 0

    while True:

        pos = data.find(b"stco", pos)

        if pos == -1:
            break

        print(pos - 4)

        pos += 4
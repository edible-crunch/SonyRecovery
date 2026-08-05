def patch_stco(frame_map):

    offsets = []

    current_chunk = None

    for frame in frame_map:

        if frame["chunk"] != current_chunk:

            offsets.append(frame["offset"])

            current_chunk = frame["chunk"]

    return offsets
def build_frame_map(chunk_offsets, stsc_entries, sample_sizes):

    frame_map = []

    sample_index = 0

    for entry_index, entry in enumerate(stsc_entries):

        first_chunk, samples_per_chunk, _ = entry

        if entry_index + 1 < len(stsc_entries):
            last_chunk = stsc_entries[entry_index + 1][0] - 1
        else:
            last_chunk = len(chunk_offsets)

        for chunk in range(first_chunk, last_chunk + 1):

            offset = chunk_offsets[chunk - 1]

            for _ in range(samples_per_chunk):

                if sample_index >= len(sample_sizes):
                    break

                size = sample_sizes[sample_index]

                frame_map.append({
                    "frame": sample_index + 1,
                    "chunk": chunk,
                    "offset": offset,
                    "size": size
                })

                offset += size
                sample_index += 1

    return frame_map

def print_frames(frame_map, start, end):

    print()
    print(f"{'Frame':>6} {'Chunk':>6} {'Offset':>12} {'Size':>10}")

    for item in frame_map[start-1:end]:

        print(
            f"{item['frame']:6}"
            f"{item['chunk']:6}"
            f"{item['offset']:12}"
            f"{item['size']:10}"
        )
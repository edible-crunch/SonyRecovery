NAL_NAMES = {
    35: "AUD",
    39: "SEI",
}


def split_access_units(chunk):

    """
    chunk = output of parse_chunk()

    Returns:

    [
        {
            "offset": ...,
            "size": ...,
            "nals": [...]
        }
    ]
    """

    nals = chunk["nals"]

    access_units = []

    current = []

    for nal in nals:

        #
        # Every AUD starts a NEW frame
        #

        if nal["type"] == 35:

            if current:

                access_units.append(current)

                current = []

        current.append(nal)

    if current:

        access_units.append(current)

    frames = []

    for au in access_units:

        start = au[0]["offset"]

        last = au[-1]

        end = (
            last["offset"]
            + 4
            + last["length"]
        )

        frames.append({

            "offset": start,

            "size": end - start,

            "nals": au

        })

    return frames
def rebase_offsets(offsets, delta):

    """
    Shift every STCO entry by a fixed byte delta.

    delta = new_mdat_payload - old_mdat_payload
    """

    rebased = []

    for offset in offsets:

        rebased.append(offset + delta)

    return rebased
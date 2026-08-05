from recovery.record_parser import parse_record


class RecordStream:

    def __init__(self, data):

        self.data = data

    def walk(self, start_offset, max_records=100):

        offset = start_offset

        records = []

        while len(records) < max_records:

            record = parse_record(self.data, offset)

            if record is None:

                print()
                print(f"[STOP] Invalid record at {offset:,}")
                break

            records.append(record)

            print()
            print("=" * 60)
            print(f"Record {len(records)}")
            print("=" * 60)

            print(f"Offset : {record.offset:,}")
            print(f"Length : {record.length}")
            print(f"Tag    : 0x{record.tag:08X}")
            print(f"NAL    : {record.header['nal_name']}")

            next_offset = offset + 8 + record.length

            if next_offset <= offset:

                print()
                print("[STOP] Offset did not advance.")
                break

            if next_offset >= len(self.data):

                print()
                print("[STOP] End of payload.")
                break

            offset = next_offset

        return records
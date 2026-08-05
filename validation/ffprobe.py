import json
import subprocess


class FFProbe:

    def __init__(self, ffprobe_path):

        self.ffprobe = ffprobe_path

    def packets(self, filename):

        cmd = [
            self.ffprobe,
            "-v", "error",
            "-print_format", "json",
            "-show_packets",
            "-select_streams", "v:0",
            filename
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        print("Return code:", result.returncode)

        if result.stdout:
            print("\nSTDOUT (first 500 chars):")
            print(result.stdout[:500])

        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)

        if result.returncode != 0:
            raise Exception("ffprobe failed.")

        return json.loads(result.stdout)
"""Convert the assignment's -1/0/1 nPrint fields to NetDiffusion colors."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


def convert_nprint_to_png(nprint_dir, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(Path(nprint_dir).glob("*.nprint"))
    if not files:
        raise FileNotFoundError(f"No nPrint files in {nprint_dir}")

    # Array positions 0, 1, 2 correspond to nPrint values -1, 0, 1.
    colors = np.array([[0, 0, 255, 255], [0, 255, 0, 255],
                       [255, 0, 0, 255]], dtype=np.uint8)
    address_fields = ("ipv4_src", "ipv4_dst", "ipv6_src", "ipv6_dst", "src_ip")

    for path in files:
        packets = pd.read_csv(path, nrows=1024)
        # Saved row numbers and IP addresses are not image features.
        packets = packets.loc[:, [c for c in packets.columns
                                  if not c.startswith("Unnamed:")
                                  and not any(s in c for s in address_fields)]]
        values = packets.to_numpy()
        if packets.empty or not np.isin(values, [-1, 0, 1]).all():
            raise ValueError(f"Expected nonempty -1/0/1 packet fields: {path}")

        pixels = np.full((1024, len(packets.columns), 4), colors[0], dtype=np.uint8)
        pixels[:len(packets)] = colors[values.astype(int) + 1]
        # Re-running replaces the same image instead of making duplicate samples.
        Image.fromarray(pixels).save(output_dir / f"{path.stem}.png")

    print(f"Converted {len(files)} nPrint files to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input_dir", required=True)
    parser.add_argument("-o", "--output_dir", required=True)
    args = parser.parse_args()
    convert_nprint_to_png(args.input_dir, args.output_dir)

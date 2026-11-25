"""Convert the NOAA ETOPO 2022 surface GeoTIFF to the globe's 1° grid."""

import argparse
import json
import math
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("geotiff", type=Path)
    args = parser.parse_args()
    # This known global raster is larger than Pillow's default image limit.
    Image.MAX_IMAGE_PIXELS = 21600 * 10800
    with Image.open(args.geotiff) as image:
        dx, dy, _ = image.tag_v2[33550]
        i, j, _, west, north, _ = image.tag_v2[33922]
        if (image.size, image.mode, i, j, west, north) != (
            (21600, 10800), "F", 0, 0, -180, 90
        ) or not (math.isclose(dx, 1 / 60) and math.isclose(dy, 1 / 60)):
            raise ValueError("Expected the global ETOPO 2022 60s surface GeoTIFF")
        pixels = image.load()
        nodata = float(image.tag_v2[42113])

        def sample(latitude, longitude):
            x = math.floor((longitude - west) / dx) % image.width
            y = min(image.height - 1, max(0, math.floor((north - latitude) / dy)))
            value = pixels[x, y]
            if not math.isfinite(value) or value == nodata:
                raise ValueError(f"Missing elevation at {latitude}, {longitude}")
            return value

        # At each pole collapse the 360 longitude samples into a single value.
        def pole(latitude):
            return round(sum(sample(latitude, lon) for lon in range(-180, 180)) / 360)

        heights = [pole(90)]
        heights.extend(
            round(sample(lat, lon))
            for lat in range(89, -90, -1)
            for lon in range(-180, 180)
        )
        heights.append(pole(-90))
        print(f"{len(heights)} samples, {min(heights)} to {max(heights)} m")
        for latitude, longitude in [(28, 87), (0, -140)]:
            print(latitude, longitude, round(sample(latitude, longitude)))

    output = Path(__file__).with_name("elevation.js")
    output.write_text(
        "const elevationMeters = " + json.dumps(heights, indent=2) + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

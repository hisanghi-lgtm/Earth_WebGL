"""NOAA ETOPO 2022에서 1도 간격으로 고도를 읽어 elevation.js를 만든다."""

import argparse
import json
import math
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("geotiff", type=Path)
    args = parser.parse_args()

    # 전 세계 GeoTIFF의 크기에 맞춰 Pillow의 픽셀 수 제한을 설정한다.
    Image.MAX_IMAGE_PIXELS = 21600 * 10800

    with Image.open(args.geotiff) as image:
        # GeoTIFF에서 픽셀 간격과 왼쪽 위 기준 좌표를 읽는다.
        dx, dy, _ = image.tag_v2[33550]
        i, j, _, west, north, _ = image.tag_v2[33922]

        if (image.size, image.mode, i, j, west, north) != (
            (21600, 10800), "F", 0, 0, -180, 90
        ) or not (math.isclose(dx, 1 / 60) and math.isclose(dy, 1 / 60)):
            raise ValueError("Expected the global ETOPO 2022 60s surface GeoTIFF")

        pixels = image.load()
        nodata = float(image.tag_v2[42113])

        def sample(latitude, longitude):
            # 경도는 열 번호로, 위도는 행 번호로 바꾼다.
            # 경도는 날짜변경선에서 이어지고, 위도는 극점에서 행 범위를 벗어나지 않게 한다.
            x = math.floor((longitude - west) / dx) % image.width
            y = min(
                image.height - 1,
                max(0, math.floor((north - latitude) / dy)),
            )

            value = pixels[x, y]
            if not math.isfinite(value) or value == nodata:
                raise ValueError(f"Missing elevation at {latitude}, {longitude}")

            return value

        def pole(latitude):
            # 극점에는 정점이 하나이므로 경도별 고도 360개의 평균을 사용한다.
            return round(sum(sample(latitude, lon) for lon in range(-180, 180)) / 360)

        # 지구 정점의 순서에 맞춰 북극부터 남극까지 고도를 저장한다.
        heights = [pole(90)]
        heights.extend(
            round(sample(lat, lon))
            for lat in range(89, -90, -1)
            for lon in range(-180, 180)
        )
        heights.append(pole(-90))

        # 추출한 값의 개수, 범위, 확인용 좌표 두 곳의 고도를 출력한다.
        print(f"{len(heights)} samples, {min(heights)} to {max(heights)} m")
        for latitude, longitude in [(28, 87), (0, -140)]:
            print(latitude, longitude, round(sample(latitude, longitude)))

    # index.html에서 읽을 수 있도록 고도 배열을 JavaScript 파일로 저장한다.
    output = Path(__file__).with_name("elevation.js")
    heights_json = json.dumps(heights, separators=(",", ":"))
    output.write_text(
        "const elevationMeters = " + heights_json + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
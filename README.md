# 3D 지구 지형

압축을 풀고 `index.html`을 Chrome 또는 Edge에서 연다. `elevation.js`는 같은 폴더에 둔다. 지구를 드래그해 시점을 바꾸고, 자전을 일시정지한 뒤 **지형 높이 적용**을 켜고 끄면 같은 각도에서 비교할 수 있다. 비교할 때 고도에 따른 표면색은 양쪽에 동일하게 표시된다.

## 고도 자료와 전처리

- 제공 기관은 NOAA National Centers for Environmental Information(NCEI)이다. [공식 배포 페이지](https://www.ncei.noaa.gov/products/etopo-global-relief-model) · [데이터 DOI](https://doi.org/10.25921/fd45-gt74)
- 원본은 ETOPO 2022 v1, 60″, Ice Surface GeoTIFF인 `ETOPO_2022_v1_60s_N90W180_surface.tif`이다. [공식 원본 파일](https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/data/60s/60s_surface_elev_gtif/ETOPO_2022_v1_60s_N90W180_surface.tif)
- 원본의 좌상단 좌표와 픽셀 크기로 위도·경도 1° 격자점이 속하는 픽셀을 찾아 미터 정수로 반올림했다. 각 극점은 가장자리 행에서 경도별로 추출한 360개 값의 평균을 사용했다. 날짜변경선의 양쪽은 같은 메시로 연결했다.
- 64,442개 정점에 `1 + 35 × 고도(m) / 6,371,000`을 반지름으로 적용했다. 35배는 시각화용 과장 배율이다. 1° 간격으로 추출했으므로 좁은 지형이나 실제 최고점은 표본에서 빠질 수 있다. 고도 부호를 기준으로 육지와 해저에 다른 색을 적용했으므로 실제 해안선과 일부 차이가 날 수 있다.
- 면을 변형한 뒤 인접 삼각형의 외적을 합해 정점 법선을 구하고, 방향광과 법선의 내적으로 밝기를 계산했다.

고도 파일을 다시 생성하려면 Pillow가 설치된 Python 환경에서 아래 명령을 실행한다. 브라우저에서 실행할 때는 이미 생성된 `elevation.js`를 사용한다.

```sh
python prepare_elevation.py ETOPO_2022_v1_60s_N90W180_surface.tif
```

## 수업 예제 참고

4장 `cube`의 회전각 갱신, `trackball`의 드래그 시작·이동·종료 처리, 6장 `shadedSphere1`의 방향광과 법선을 이용한 확산 반사 계산을 참고했다.

# WebGL을 이용한 3D 지구 지형 표현

## 실행 방법

1. `index.html`과 `elevation.js`를 같은 폴더에 둔다.
2. `index.html`을 Chrome 또는 Edge에서 연다.
3. 지구를 마우스로 드래그하면 보는 방향을 바꿀 수 있다.
4. 자전을 일시정지한 뒤 **지형 높이 적용**을 켜고 끄면 같은 각도에서 표면 모양을 비교할 수 있다. 고도에 따른 표면색은 두 경우에 동일하게 표시된다.


## 고도 자료와 처리 방법

NOAA NCEI에서 공개한 ETOPO 2022 v1 자료를 사용하였다. 원본 파일은 60초각 해상도의 Ice Surface GeoTIFF인 `ETOPO_2022_v1_60s_N90W180_surface.tif`이다.

- [NOAA 공식 배포 페이지](https://www.ncei.noaa.gov/products/etopo-global-relief-model)
- [원본 GeoTIFF 다운로드](https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/data/60s/60s_surface_elev_gtif/ETOPO_2022_v1_60s_N90W180_surface.tif)
- [데이터 DOI](https://doi.org/10.25921/fd45-gt74)

`prepare_elevation.py`에서 원본의 왼쪽 위 기준 좌표와 픽셀 간격을 읽고, 위도와 경도 1도 간격으로 해당하는 픽셀의 고도를 추출하였다. 양쪽 극점에는 각각 정점이 하나 있으므로, 위아래 끝 행에서 경도별로 읽은 360개 고도의 평균을 사용하였다. 추출한 고도 값 64,442개는 미터 단위의 정수로 반올림하여 `elevation.js`에 저장하였다.

WebGL에서는 각 정점의 반지름을 `1 + 35 × 고도(m) / 6,371,000`으로 계산하였다. 지형 차이가 화면에서 잘 보이도록 높이 차이를 35배로 강조하였다. 1도 간격으로 값을 추출했기 때문에 폭이 좁은 지형이나 실제 최고점은 화면에 반영되지 않을 수 있다. 지형을 적용한 뒤에는 인접한 삼각형의 외적을 더해 정점 법선을 구하고, 법선과 광원 방향의 내적으로 밝기를 계산하였다.

## 고도 파일 다시 만들기

브라우저에서 실행할 때는 저장소에 포함된 `elevation.js`를 사용한다. 원본에서 고도 파일을 다시 만들려면 Pillow가 설치된 Python 환경에서 아래 명령을 실행한다. 실행하면 `prepare_elevation.py`와 같은 폴더의 `elevation.js`가 새로 생성된다.

```sh
python prepare_elevation.py ETOPO_2022_v1_60s_N90W180_surface.tif
```

## 인공지능 사용 내역

NOAA ETOPO 2022 원본에서 위도와 경도에 해당하는 픽셀을 찾고, 추출한 고도를 3D 지구에 적용하는 코드를 작성하는 데 ChatGPT를 사용하였다. `prepare_elevation.py`에서는 위도와 경도 1도 간격으로 고도를 읽어 `elevation.js`에 저장하도록 하였고, `index.html`에서는 그 값에 따라 각 정점의 반지름을 조절하도록 하였다. 프로그램에 사용한 고도 값은 NOAA 원본 자료에서 추출하였다.


## 참고한 수업 예제

-**4장 `cube.js`, `cube.html`** — 회전각을 갱신하고 셰이더에 전달하는 방식을 자동 자전에 적용하였다.
-**4장 `trackball.js`** — 마우스 드래그의 시작, 이동, 종료를 처리하는 방식을 참고하였다.
-**6장 `shadedSphere1.html`** — 표면 법선과 광원 방향의 내적을 이용한 확산 반사 계산을 참고하였다.

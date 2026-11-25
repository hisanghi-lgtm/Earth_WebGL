# WebGL을 이용한 3D 지구 모델

## 실행 방법
1. `earth.html`과 `elevation.js`를 같은 폴더에 둔다.
2. `earth.html`을 Chrome이나 Edge에서 연다.
3. 지구 위에서 마우스 왼쪽 버튼을 누른 채 움직이면 보는 방향을 바꿀 수 있다.
4. **자전 일시정지**를 누르고 **지형 높이 적용 (40배)**을 켜거나 끄면 같은 각도에서 표면을 비교할 수 있다. 이때 고도에 따른 색은 그대로 표시된다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `earth.html` | WebGL로 지구를 그리고 자전, 마우스 드래그, 조명을 처리한다. |
| `elevation.js` | 위도·경도 1도 간격으로 추출한 고도 값 64,442개를 저장한다. |
| `prepare_elevation.py` | NOAA 원본에서 고도를 읽어 `elevation.js`를 만든다. |

## 고도 자료

NOAA 국립환경정보센터(NCEI)의 **ETOPO 2022 v1 Ice Surface** 자료를 사용하였다. 원본 파일은 60초각 해상도의 GeoTIFF인 `ETOPO_2022_v1_60s_N90W180_surface.tif`이다. [NOAA 공식 배포 페이지](https://www.ncei.noaa.gov/products/etopo-global-relief-model) · [데이터 DOI](https://doi.org/10.25921/fd45-gt74)

원본에서 위도와 경도 1도 간격으로 고도를 읽어 미터 단위의 정수로 저장하였다. 북극과 남극에는 정점이 하나씩 있으므로, 원본의 위쪽과 아래쪽 끝 행에서 경도별로 읽은 값 360개의 평균을 각각 사용하였다. 지구 전체를 한 화면에 표시했을 때 굴곡이 잘 보이도록 높이 차이를 40배로 강조하였다.

저장소에 포함된 `elevation.js`로 바로 실행할 수 있다. 고도 파일을 다시 만들려면 Pillow가 설치된 Python 환경에서 아래 명령을 실행한다. 실행하면 `prepare_elevation.py`와 같은 폴더의 `elevation.js`가 새로 저장된다.

```sh
python prepare_elevation.py ETOPO_2022_v1_60s_N90W180_surface.tif
```

GeoTIFF에서 위도와 경도에 해당하는 고도를 읽고, 그 값을 WebGL의 정점에 적용하는 코드를 작성하는 데 **ChatGPT**를 사용하였다. prepare_elevation.py에서는 위도와 경도를 픽셀의 행과 열로 변환하고, NOAA 원본에서 읽은 고도를 구의 정점 순서에 맞춰 elevation.js에 저장하였다. earth.html에서는 이 값을 이용해 각 정점의 반지름을 계산하였다. 

## 참고한 수업 예제

- **4장 `cube.html`, `cube.js`** — 회전 변환과 프레임마다 회전각을 갱신하는 방식을 참고하였다.
- **4장 `trackball.js`** — 마우스 드래그의 시작, 이동, 종료를 나누어 처리하는 방식을 참고하였다.
- **6장 `shadedSphere1.html`** — 표면 법선과 광원 방향의 내적으로 확산 반사를 계산하는 방식을 참고하였다. 
-> 자세한 내용은 보고서 참고